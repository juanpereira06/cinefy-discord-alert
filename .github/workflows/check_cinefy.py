import requests

CINEFY_URL = "https://cinefy.gg/juanzone"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(CINEFY_URL, headers=headers, timeout=30)

print("Status:", response.status_code)
print("URL final:", response.url)
print("Tamanho da página:", len(response.text))

with open("cinefy_debug.html", "w", encoding="utf-8") as arquivo:
    arquivo.write(response.text)

if response.status_code == 200:
    print("✅ Página do Cinefy acessada com sucesso!")
else:
    print("❌ Não foi possível acessar o Cinefy.")
