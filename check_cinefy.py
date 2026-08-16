import os
import json
import requests
from bs4 import BeautifulSoup

CINEFY_URL = "https://cinefy.gg/juanzone"
STATE_FILE = "last_vod.json"

DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(CINEFY_URL, headers=headers, timeout=30)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

# Procura links que parecem levar para conteúdos/VODs
links = []

for a in soup.find_all("a", href=True):
    href = a.get("href", "").strip()
    text = a.get_text(" ", strip=True)

    if not href:
        continue

    # Ignora links genéricos
    if href in ["/", "/juanzone", "https://cinefy.gg/juanzone"]:
        continue

    if href.startswith("/"):
        full_url = "https://cinefy.gg" + href
    else:
        full_url = href

    if "cinefy.gg" in full_url:
        links.append({
            "title": text or "Novo VOD",
            "url": full_url
        })

# Remove links duplicados
unique = []
seen = set()

for item in links:
    if item["url"] not in seen:
        seen.add(item["url"])
        unique.append(item)

print("Links encontrados:", len(unique))

for item in unique[:10]:
    print("-", item["title"], "=>", item["url"])

if not unique:
    print("❌ Nenhum possível VOD encontrado.")
    raise SystemExit(0)

latest = unique[0]

print("Possível VOD mais recente:")
print(latest["title"])
print(latest["url"])

# Primeira execução: apenas salva o estado sem mandar alerta
if not os.path.exists(STATE_FILE):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(latest, f, ensure_ascii=False, indent=2)

    print("✅ Primeiro VOD salvo como referência.")
    print("Nenhum alerta foi enviado.")
    raise SystemExit(0)

with open(STATE_FILE, "r", encoding="utf-8") as f:
    previous = json.load(f)

if previous.get("url") == latest["url"]:
    print("✅ Nenhum VOD novo.")
    raise SystemExit(0)

print("🎬 Novo VOD detectado!")

message = {
    "content": (
        "@everyone 🎬 **VOD NOVO NO JUANZONE!** 💜\n\n"
        "Um novo conteúdo acabou de ser publicado no Cinefy! 🍿\n\n"
        f"🎥 **{latest['title']}**\n"
        f"🔗 {latest['url']}"
    ),
    "allowed_mentions": {
        "parse": ["everyone"]
    }
}

if not DISCORD_WEBHOOK:
    raise RuntimeError("DISCORD_WEBHOOK não está configurado.")

discord_response = requests.post(
    DISCORD_WEBHOOK,
    json=message,
    timeout=30
)

discord_response.raise_for_status()

print("✅ Alerta enviado para o Discord!")

with open(STATE_FILE, "w", encoding="utf-8") as f:
    json.dump(latest, f, ensure_ascii=False, indent=2)
