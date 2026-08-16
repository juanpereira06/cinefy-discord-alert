import requests
import re

URL = "https://cinefy.gg/juanzone"

headers = {
    "User-Agent": "Mozilla/5.0"
}

r = requests.get(URL, headers=headers, timeout=30)
r.raise_for_status()

html = r.text

print("Status:", r.status_code)
print("Tamanho:", len(html))

termos = [
    "watch/",
    "__NEXT_DATA__",
    "api",
    "graphql",
    "juanzone"
]

for termo in termos:
    quantidade = html.lower().count(termo.lower())
    print(f"{termo}: {quantidade}")

print("\n--- URLs encontradas ---")

urls = re.findall(r'https?://[^"\'\s<>]+', html)

for url in urls:
    if "cinefy" in url.lower():
        print(url[:500])
