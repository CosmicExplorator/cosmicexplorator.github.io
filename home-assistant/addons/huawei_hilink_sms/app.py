"""Small Ingress web application for Huawei HiLink SMS."""

from __future__ import annotations

import atexit
import json
import os
from pathlib import Path
from threading import Lock
from typing import Any

from flask import Flask, jsonify, render_template, request
from huawei_lte_api.Client import Client
from huawei_lte_api.Connection import Connection
from huawei_lte_api.enums.sms import BoxTypeEnum


OPTIONS_FILE = Path(os.getenv("OPTIONS_FILE", "/data/options.json"))
APP_DIR = Path(__file__).resolve().parent


def load_options() -> dict[str, Any]:
    """Load Supervisor options, with development-friendly defaults."""
    defaults: dict[str, Any] = {
        "modem_url": "http://192.168.8.1/",
        "username": "",
        "password": "",
        "max_messages": 50,
    }
    if OPTIONS_FILE.exists():
        defaults.update(json.loads(OPTIONS_FILE.read_text(encoding="utf-8")))
    return defaults


options = load_options()
connection = Connection(
    str(options["modem_url"]),
    username=options.get("username") or None,
    password=options.get("password") or None,
    timeout=15,
)
client = Client(connection)
modem_lock = Lock()
app = Flask(
    __name__,
    static_folder=str(APP_DIR / "static"),
    template_folder=str(APP_DIR / "templates"),
)


def message_list(box: BoxTypeEnum) -> list[dict[str, Any]]:
    """Return a normalized list for one modem SMS box."""
    response = client.sms.get_sms_list(
        box_type=box,
        read_count=int(options["max_messages"]),
        ascending=False,
    )
    messages = response.get("Messages", {}).get("Message", [])
    if isinstance(messages, dict):
        messages = [messages]
    return [
        {
            "id": str(item.get("Index", "")),
            "phone": str(item.get("Phone", "")),
            "date": str(item.get("Date", "")),
            "content": str(item.get("Content", "")),
            "unread": str(item.get("Smstat", "1")) == "0",
            "box": "inbox" if box == BoxTypeEnum.LOCAL_INBOX else "sent",
        }
        for item in messages
    ]


@app.get("/")
def index() -> str:
    return render_template("index.html")


@app.get("/health")
def health() -> tuple[str, int]:
    return "ok", 200


@app.get("/api/messages")
def messages() -> Any:
    try:
        with modem_lock:
            result = message_list(BoxTypeEnum.LOCAL_INBOX)
            try:
                result += message_list(BoxTypeEnum.LOCAL_SENT)
            except Exception:
                # Some HiLink firmwares do not expose the sent box.
                pass
        result.sort(key=lambda item: item["date"], reverse=True)
        return jsonify({"messages": result})
    except Exception as err:
        app.logger.exception("Could not read SMS")
        return jsonify({"error": str(err)}), 502


@app.post("/api/messages")
def send_message() -> Any:
    payload = request.get_json(silent=True) or {}
    phone = str(payload.get("phone", "")).strip()
    content = str(payload.get("content", "")).strip()
    if not phone or not content:
        return jsonify({"error": "Le numéro et le message sont obligatoires."}), 400
    if len(phone) > 32 or len(content) > 1600:
        return jsonify({"error": "Numéro ou message trop long."}), 400
    try:
        with modem_lock:
            client.sms.send_sms([phone], content)
        return jsonify({"ok": True}), 201
    except Exception as err:
        app.logger.exception("Could not send SMS")
        return jsonify({"error": str(err)}), 502


@app.delete("/api/messages/<int:message_id>")
def delete_message(message_id: int) -> Any:
    try:
        with modem_lock:
            client.sms.delete_sms(message_id)
        return jsonify({"ok": True})
    except Exception as err:
        app.logger.exception("Could not delete SMS")
        return jsonify({"error": str(err)}), 502


@atexit.register
def close_connection() -> None:
    connection.close()

