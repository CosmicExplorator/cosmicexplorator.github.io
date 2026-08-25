class HuaweiSmsCard extends HTMLElement {
  setConfig(config) {
    if (!config.entity) throw new Error("La propriété entity est obligatoire");
    this.config = config;
  }

  set hass(hass) {
    this._hass = hass;
    this.render();
  }

  getCardSize() {
    return 8;
  }

  element(tag, options = {}) {
    const node = document.createElement(tag);
    if (options.className) node.className = options.className;
    if (options.text !== undefined) node.textContent = options.text;
    if (options.type) node.type = options.type;
    if (options.placeholder) node.placeholder = options.placeholder;
    if (options.value !== undefined) node.value = options.value;
    return node;
  }

  async call(service, data = {}) {
    try {
      await this._hass.callService("huawei_sms", service, data);
    } catch (error) {
      alert(`Erreur Huawei : ${error.message || error}`);
    }
  }

  render() {
    if (!this._hass || !this.config) return;
    const state = this._hass.states[this.config.entity];
    if (!state) {
      this.replaceChildren(this.element("ha-card", { text: "Entité Huawei introuvable" }));
      return;
    }

    const card = this.element("ha-card");
    const title = this.element("h1", {
      className: "card-header",
      text: this.config.title || "SMS et contacts SIM",
    });
    const content = this.element("div", { className: "card-content" });
    const messages = Array.isArray(state.attributes.messages)
      ? state.attributes.messages
      : [];
    const contacts = Array.isArray(state.attributes.contacts)
      ? state.attributes.contacts
      : [];

    content.append(
      this.sectionTitle(`Messages (${messages.length})`),
      this.sendForm(),
      this.messageList(messages),
      this.deleteAllButton(messages.length),
      this.sectionTitle(`Contacts SIM (${contacts.length})`),
      this.contactForm(),
      this.contactList(contacts),
    );
    card.append(title, content, this.styles());
    this.replaceChildren(card);
  }

  sectionTitle(text) {
    return this.element("h2", { text });
  }

  sendForm() {
    const form = this.element("form", { className: "form" });
    const phone = this.element("input", {
      type: "tel",
      placeholder: "+33612345678",
    });
    phone.required = true;
    const message = this.element("textarea", { placeholder: "Message" });
    message.required = true;
    const submit = this.element("button", { type: "submit", text: "Envoyer" });
    form.append(phone, message, submit);
    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      await this.call("send", {
        phone_number: phone.value,
        message: message.value,
      });
      message.value = "";
    });
    return form;
  }

  contactForm() {
    const form = this.element("form", { className: "form contact-form" });
    const name = this.element("input", { placeholder: "Nom" });
    name.required = true;
    const phone = this.element("input", {
      type: "tel",
      placeholder: "+33612345678",
    });
    phone.required = true;
    const submit = this.element("button", { type: "submit", text: "Ajouter" });
    form.append(name, phone, submit);
    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      await this.call("add_contact", {
        name: name.value,
        phone_number: phone.value,
      });
      name.value = "";
      phone.value = "";
    });
    return form;
  }

  messageList(messages) {
    const list = this.element("div", { className: "list" });
    if (!messages.length) {
      list.append(this.element("p", { className: "empty", text: "Aucun SMS" }));
      return list;
    }
    for (const message of messages) {
      const row = this.element("article", {
        className: `row${message.unread ? " unread" : ""}`,
      });
      const body = this.element("div", { className: "body" });
      const sender = message.contact_name
        ? `${message.contact_name} — ${message.from}`
        : message.from || "Numéro inconnu";
      body.append(
        this.element("strong", { text: sender }),
        this.element("small", { text: message.date || "" }),
        this.element("p", { text: message.content || "" }),
      );
      const remove = this.element("button", { type: "button", text: "Supprimer" });
      remove.className = "danger";
      remove.addEventListener("click", () =>
        this.call("delete", { message_id: Number(message.id) }),
      );
      row.append(body, remove);
      list.append(row);
    }
    return list;
  }

  contactList(contacts) {
    const list = this.element("div", { className: "list" });
    if (!contacts.length) {
      list.append(
        this.element("p", { className: "empty", text: "Aucun contact SIM" }),
      );
      return list;
    }
    for (const contact of contacts) {
      const row = this.element("article", { className: "row" });
      const body = this.element("div", { className: "body" });
      body.append(
        this.element("strong", { text: contact.name || "Sans nom" }),
        this.element("small", { text: contact.phone_number || "" }),
      );
      const remove = this.element("button", { type: "button", text: "Supprimer" });
      remove.className = "danger";
      remove.addEventListener("click", () => {
        if (confirm(`Supprimer le contact « ${contact.name || "Sans nom"} » ?`)) {
          this.call("delete_contact", { contact_id: Number(contact.id) });
        }
      });
      row.append(body, remove);
      list.append(row);
    }
    return list;
  }

  deleteAllButton(count) {
    const button = this.element("button", {
      type: "button",
      text: "Vider la boîte de réception",
    });
    button.className = "danger delete-all";
    button.disabled = count === 0;
    button.addEventListener("click", () => {
      if (confirm("Supprimer définitivement tous les SMS ?")) {
        this.call("delete_all");
      }
    });
    return button;
  }

  styles() {
    const style = this.element("style");
    style.textContent = `
      .card-content { padding-top: 0; }
      h2 { margin: 24px 0 12px; font-size: 1.1rem; }
      .form { display: grid; grid-template-columns: minmax(150px, 1fr) 2fr auto; gap: 8px; }
      .contact-form { grid-template-columns: 1fr 1fr auto; }
      input, textarea, button { box-sizing: border-box; font: inherit; }
      input, textarea { padding: 10px; color: var(--primary-text-color); background: var(--card-background-color); border: 1px solid var(--divider-color); border-radius: 6px; }
      textarea { min-height: 42px; resize: vertical; }
      button { padding: 8px 12px; cursor: pointer; color: var(--text-primary-color); background: var(--primary-color); border: 0; border-radius: 6px; }
      button:disabled { cursor: default; opacity: .45; }
      .list { display: grid; gap: 8px; margin-top: 12px; }
      .row { display: flex; align-items: center; justify-content: space-between; gap: 12px; padding: 12px; border: 1px solid var(--divider-color); border-radius: 8px; }
      .row.unread { border-left: 4px solid var(--primary-color); }
      .body { min-width: 0; display: grid; gap: 3px; }
      .body p { margin: 6px 0 0; white-space: pre-wrap; overflow-wrap: anywhere; }
      .body small, .empty { color: var(--secondary-text-color); }
      .danger { background: var(--error-color, #db4437); }
      .delete-all { margin-top: 12px; }
      @media (max-width: 650px) {
        .form, .contact-form { grid-template-columns: 1fr; }
        .row { align-items: flex-start; flex-direction: column; }
      }
    `;
    return style;
  }
}

customElements.define("huawei-sms-card", HuaweiSmsCard);

window.customCards = window.customCards || [];
window.customCards.push({
  type: "huawei-sms-card",
  name: "Huawei SMS et contacts SIM",
  description: "Boîte SMS et carnet de contacts d'un modem Huawei HiLink",
});
