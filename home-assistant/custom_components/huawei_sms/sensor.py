"""SMS inbox and SIM phone book for Huawei HiLink modems."""

from __future__ import annotations

import asyncio
from datetime import timedelta
import logging
import re
from typing import Any

import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA, SensorEntity
from homeassistant.const import CONF_NAME, CONF_PASSWORD, CONF_USERNAME, CONF_URL
from homeassistant.core import HomeAssistant, ServiceCall
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from huawei_lte_api.Client import Client
from huawei_lte_api.Connection import Connection
from huawei_lte_api.enums.sms import BoxTypeEnum

from . import DOMAIN

_LOGGER = logging.getLogger(__name__)

CONF_MAX_MESSAGES = "max_messages"
CONF_COUNTRY_CODE = "country_code"
CONF_PHONE_NUMBER = "phone_number"
CONF_MESSAGE = "message"
CONF_MESSAGE_ID = "message_id"
CONF_CONTACT_ID = "contact_id"

DEFAULT_NAME = "SMS Huawei E3372"
DEFAULT_COUNTRY_CODE = "+33"
SCAN_INTERVAL = timedelta(seconds=60)
SIM_SAVE_TYPE = 1

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_URL): cv.url,
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
        vol.Optional(CONF_USERNAME): cv.string,
        vol.Optional(CONF_PASSWORD): cv.string,
        vol.Optional(CONF_MAX_MESSAGES, default=20): vol.All(
            vol.Coerce(int), vol.Range(min=1, max=50)
        ),
        vol.Optional(CONF_COUNTRY_CODE, default=DEFAULT_COUNTRY_CODE): vol.Match(
            r"^\+\d{1,3}$"
        ),
    }
)


async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the Huawei SMS sensor and its services."""
    entity = HuaweiSmsSensor(
        config[CONF_URL],
        config.get(CONF_USERNAME),
        config.get(CONF_PASSWORD),
        config[CONF_NAME],
        config[CONF_MAX_MESSAGES],
        config[CONF_COUNTRY_CODE],
    )
    async_add_entities([entity], True)

    async def send(call: ServiceCall) -> None:
        await entity.async_send(call.data[CONF_PHONE_NUMBER], call.data[CONF_MESSAGE])

    async def delete(call: ServiceCall) -> None:
        await entity.async_delete_message(call.data[CONF_MESSAGE_ID])

    async def delete_all(_: ServiceCall) -> None:
        await entity.async_delete_all_messages()

    async def add_contact(call: ServiceCall) -> None:
        await entity.async_add_contact(
            call.data[CONF_NAME], call.data[CONF_PHONE_NUMBER]
        )

    async def delete_contact(call: ServiceCall) -> None:
        await entity.async_delete_contact(call.data[CONF_CONTACT_ID])

    services = (
        (
            "send",
            send,
            vol.Schema(
                {
                    vol.Required(CONF_PHONE_NUMBER): cv.string,
                    vol.Required(CONF_MESSAGE): cv.string,
                }
            ),
        ),
        (
            "delete",
            delete,
            vol.Schema({vol.Required(CONF_MESSAGE_ID): vol.Coerce(int)}),
        ),
        ("delete_all", delete_all, vol.Schema({})),
        (
            "add_contact",
            add_contact,
            vol.Schema(
                {
                    vol.Required(CONF_NAME): cv.string,
                    vol.Required(CONF_PHONE_NUMBER): cv.string,
                }
            ),
        ),
        (
            "delete_contact",
            delete_contact,
            vol.Schema({vol.Required(CONF_CONTACT_ID): vol.Coerce(int)}),
        ),
    )
    for service_name, handler, schema in services:
        if not hass.services.has_service(DOMAIN, service_name):
            hass.services.async_register(DOMAIN, service_name, handler, schema=schema)


class HuaweiSmsSensor(SensorEntity):
    """Represent a Huawei SMS inbox and SIM phone book."""

    _attr_icon = "mdi:message-text"
    _attr_should_poll = True

    def __init__(
        self,
        url: str,
        username: str | None,
        password: str | None,
        name: str,
        max_messages: int,
        country_code: str,
    ) -> None:
        self._attr_name = name
        self._attr_unique_id = "huawei_e3372_sms"
        self._connection = Connection(
            url, username=username, password=password, timeout=15
        )
        self._client = Client(self._connection)
        self._max_messages = max_messages
        self._country_code = country_code
        self._messages: list[dict[str, Any]] = []
        self._contacts: list[dict[str, str]] = []
        self._lock = asyncio.Lock()

    @property
    def native_value(self) -> int:
        """Return the number of messages."""
        return len(self._messages)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Expose messages and contacts."""
        return {"messages": self._messages, "contacts": self._contacts}

    async def async_update(self) -> None:
        """Refresh messages and contacts without blocking Home Assistant."""
        async with self._lock:
            try:
                messages, contacts = await self.hass.async_add_executor_job(
                    self._fetch_data
                )
            except Exception:
                self._attr_available = False
                _LOGGER.exception("Unable to read Huawei SMS or SIM contacts")
                return
            self._messages = messages
            self._contacts = contacts
            self._attr_available = True

    async def async_will_remove_from_hass(self) -> None:
        """Close the HiLink session."""
        await self.hass.async_add_executor_job(self._connection.close)

    def _fetch_data(self) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
        contacts = self._normalize_contacts(
            self._client.pb.get_pb_list(read_count=50, save_type=SIM_SAVE_TYPE)
        )
        names = {
            item["normalized_number"]: item["name"]
            for item in contacts
            if item["normalized_number"]
        }
        response = self._client.sms.get_sms_list(
            box_type=BoxTypeEnum.LOCAL_INBOX,
            read_count=self._max_messages,
            ascending=False,
        )
        raw_messages = response.get("Messages", {}).get("Message", [])
        if isinstance(raw_messages, dict):
            raw_messages = [raw_messages]
        messages = []
        for item in raw_messages:
            phone = str(item.get("Phone", ""))
            messages.append(
                {
                    "id": str(item.get("Index", "")),
                    "from": phone,
                    "contact_name": names.get(self._normalize_number(phone), ""),
                    "date": str(item.get("Date", "")),
                    "content": str(item.get("Content", "")),
                    "unread": str(item.get("Smstat", "1")) == "0",
                }
            )
        return messages, contacts

    def _normalize_contacts(self, payload: dict[str, Any]) -> list[dict[str, str]]:
        phonebook = payload.get("PhoneBook", payload)
        pb_list = phonebook.get("PbList", {}) if isinstance(phonebook, dict) else {}
        entries = pb_list.get("PbItem", []) if isinstance(pb_list, dict) else []
        if isinstance(entries, dict):
            entries = [entries]
        contacts = []
        for entry in entries:
            fields = entry.get("Field", [])
            if isinstance(fields, dict):
                fields = [fields]
            values = {
                str(field.get("Name", "")): str(field.get("Value", ""))
                for field in fields
                if isinstance(field, dict)
            }
            phone = values.get("MobilePhone", "")
            contacts.append(
                {
                    "id": str(entry.get("Index", "")),
                    "name": values.get("FormattedName", ""),
                    "phone_number": phone,
                    "normalized_number": self._normalize_number(phone),
                }
            )
        return contacts

    def _normalize_number(self, value: str) -> str:
        value = value.strip()
        digits = re.sub(r"\D", "", value)
        if value.startswith("+"):
            return f"+{digits}"
        if digits.startswith("00"):
            return f"+{digits[2:]}"
        if digits.startswith("0"):
            return f"{self._country_code}{digits[1:]}"
        return f"+{digits}" if digits else ""

    async def _run_and_refresh(self, function: Any, *args: Any) -> None:
        async with self._lock:
            await self.hass.async_add_executor_job(function, *args)
        await self.async_update()
        self.async_write_ha_state()

    async def async_send(self, phone_number: str, message: str) -> None:
        await self._run_and_refresh(
            self._client.sms.send_sms, [phone_number.strip()], message
        )

    async def async_delete_message(self, message_id: int) -> None:
        await self._run_and_refresh(self._client.sms.delete_sms, message_id)

    async def async_delete_all_messages(self) -> None:
        async with self._lock:
            response = await self.hass.async_add_executor_job(
                self._client.sms.get_sms_list,
                1,
                BoxTypeEnum.LOCAL_INBOX,
                50,
            )
            raw_messages = response.get("Messages", {}).get("Message", [])
            if isinstance(raw_messages, dict):
                raw_messages = [raw_messages]
            for item in raw_messages:
                await self.hass.async_add_executor_job(
                    self._client.sms.delete_sms, int(item["Index"])
                )
        await self.async_update()
        self.async_write_ha_state()

    async def async_add_contact(self, name: str, phone_number: str) -> None:
        if not name.strip() or not phone_number.strip():
            raise ValueError("Contact name and phone number must not be empty")
        await self._run_and_refresh(
            self._client.pb.pb_new,
            0,
            SIM_SAVE_TYPE,
            name.strip(),
            phone_number.strip(),
        )

    async def async_delete_contact(self, contact_id: int) -> None:
        await self._run_and_refresh(self._client.pb.pb_delete, contact_id)
