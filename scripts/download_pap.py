

import requests, os, re
from bs4 import BeautifulSoup

PAP_ARTICLES = {
    "pap_wulkan_etyopia": "https://naukawpolsce.pl/aktualnosci/news%2C108259%2Cwroclaw-naukowcy-opracowali-etykiety-na-produkty-spozywcze-reagujace-na",
    "pap_radiofarmaceutyki": "https://naukawpolsce.pl/aktualnosci/news%2C108242%2Cwroclawska-uczelnia-i-stawy-milickie-beda-przeciwdzialac-zmianom",
}

os.makedirs("../literatura2", exist_ok=True)
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; TextMiningBot/0.1)"}


def scrape_pap(url: str) -> str:
    html = requests.get(url, headers=HEADERS, timeout=20).text
    soup = BeautifulSoup(html, "html.parser")


    body = soup.select_one("div.article-body") or soup.select_one("div.field-item")
    if not body:
        body = soup  # fallback

 
    title = soup.select_one("h1").get_text(" ", strip=True) if soup.select_one("h1") else ""
    lead = soup.select_one("div.lead") or soup.select_one("p.lead")
    lead = lead.get_text(" ", strip=True) if lead else ""

    paragraphs = [p.get_text(" ", strip=True) for p in body.select("p")]

 
    paragraphs = [re.sub(r"^Czytaj także.*", "", p, flags=re.I) for p in paragraphs]
    paragraphs = [p for p in paragraphs if len(p) > 30]

    text = title + "\n\n" + lead + "\n\n" + "\n".join(paragraphs)
    return text.strip()


for fname, url in PAP_ARTICLES.items():
    try:
        txt = scrape_pap(url)
        open(f"../literatura2/{fname}.txt", "w", encoding="utf-8").write(txt)
        print(f"✓ zapisano {fname}.txt ({len(txt)//1024} kB)")
    except Exception as e:
        print(f"✗ błąd przy {fname}: {e}")