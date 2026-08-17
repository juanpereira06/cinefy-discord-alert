import os
import json
import requests

API_URL = (
    "https://api.cinefy.gg/v1/videos"
    "?perPage=20"
    "&page=1"
    "&author=3c7bc2d2-ea73-4052-add6-12177a9677cb"
    "&collapse=false"
    "&sortedOrder=desc"
)

STATE_FILE = "last_vod.json"
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(API_URL, headers=headers, timeout=30)
response.raise_for_status()

payload = response.json()
videos = payload.get("data", [])

if not videos:
    print("❌ Nenhum VOD encontrado.")
    raise SystemExit(0)

latest = videos[0]

vod_id = latest.get("id")
title = latest.get("title") or "Novo VOD"
published = latest.get("published", False)
published_at = latest.get("publishedAt")

vod_url = f"https://cinefy.gg/watch/{vod_id}"

print("VOD mais recente:")
print("Título:", title)
print("ID:", vod_id)
print("Publicado:", published)
print("Publicado em:", published_at)
print("Link:", vod_url)

# Ignora vídeos que ainda não estejam publicados
if not published:
    print("⚠️ O VOD mais recente ainda não está publicado.")
    raise SystemExit(0)

current = {
    "id": vod_id,
    "title": title,
    "url": vod_url,
    "publishedAt": published_at
}

# Primeira execução: só salva referência
if not os.path.exists(STATE_FILE):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(current, f, ensure_ascii=False, indent=2)

    print("✅ Primeiro VOD salvo como referência.")
    print("Nenhum alerta enviado nesta primeira execução.")
    raise SystemExit(0)

with open(STATE_FILE, "r", encoding="utf-8") as f:
    previous = json.load(f)

if previous.get("id") == vod_id:
    print("✅ Nenhum VOD novo.")
    raise SystemExit(0)

if not DISCORD_WEBHOOK:
    raise RuntimeError("DISCORD_WEBHOOK não está configurado.")

message = {
    "content": (
        "@everyone 🎬 **VOD NOVO NO JUANZONE!** 💜\n\n"
        "Perdeu a live ou quer assistir de novo? 👀🍿\n\n"
        f"🎥 **{title}**\n"
        "🔗 Assista no Cinefy: https://cinefy.gg/juanzone"
    ),
    "allowed_mentions": {
        "parse": ["everyone"]
    }
}

discord_response = requests.post(
    DISCORD_WEBHOOK,
    json=message,
    timeout=30
)

discord_response.raise_for_status()

print("✅ Alerta enviado para o Discord!")

with open(STATE_FILE, "w", encoding="utf-8") as f:
    json.dump(current, f, ensure_ascii=False, indent=2)
