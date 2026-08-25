const messages = document.querySelector("#messages");
const statusLine = document.querySelector("#status");
const template = document.querySelector("#message-template");

function status(text, error = false) {
  statusLine.textContent = text;
  statusLine.classList.toggle("error", error);
}

async function api(path, options = {}) {
  const response = await fetch(path, {
    ...options,
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
  });
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || `Erreur HTTP ${response.status}`);
  return data;
}

async function refresh() {
  status("Chargement…");
  try {
    const data = await api("api/messages");
    messages.replaceChildren();
    if (!data.messages.length) {
      messages.textContent = "Aucun SMS.";
    }
    for (const item of data.messages) {
      const row = template.content.cloneNode(true);
      const article = row.querySelector("article");
      article.classList.toggle("sent", item.box === "sent");
      article.classList.toggle("unread", item.unread);
      row.querySelector("strong").textContent = item.phone || "Numéro inconnu";
      row.querySelector("time").textContent = item.date;
      row.querySelector("p").textContent = item.content;
      row.querySelector(".delete").addEventListener("click", async () => {
        if (!confirm("Supprimer ce SMS ?")) return;
        try {
          await api(`api/messages/${encodeURIComponent(item.id)}`, { method: "DELETE" });
          await refresh();
        } catch (error) {
          status(error.message, true);
        }
      });
      messages.append(row);
    }
    status(`${data.messages.length} message(s)`);
  } catch (error) {
    status(error.message, true);
  }
}

document.querySelector("#send-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const phone = document.querySelector("#phone");
  const content = document.querySelector("#content");
  status("Envoi…");
  try {
    await api("api/messages", {
      method: "POST",
      body: JSON.stringify({ phone: phone.value, content: content.value }),
    });
    content.value = "";
    status("SMS envoyé.");
    await refresh();
  } catch (error) {
    status(error.message, true);
  }
});

document.querySelector("#refresh").addEventListener("click", refresh);
refresh();
setInterval(refresh, 30000);

