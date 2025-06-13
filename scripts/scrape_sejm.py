

import requests, os, re
from bs4 import BeautifulSoup


SEJM_SPEECHES = {

    "sejm_kamila_gasiuk_2024-05-09": "https://www.sejm.gov.pl/Sejm10.nsf/wypowiedz.xsp?posiedzenie=7&dzien=1&wyp=8&type=A",
    "sejm_michal_dworczyk_2024-03-14": "https://www.sejm.gov.pl/Sejm10.nsf/wypowiedz.xsp?posiedzenie=3&dzien=2&wyp=45&type=A",
}

os.makedirs("../literatura2", exist_ok=True)
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; TextMiningBot/0.1)"}


def scrape_sejm(url: str) -> str:
    html = requests.get(url, headers=HEADERS, timeout=20).text
    soup = BeautifulSoup(html, "html.parser")

    main = soup.select_one("div#content, div.wypowiedz, div.tresc")
    if not main:
        main = soup  

    paragraphs = [p.get_text(" ", strip=True) for p in main.select("p")]
    text = "\n".join(paragraphs)
    text = re.sub(r"\[\d+ *[A-Z]?\]", "", text)
    text = re.sub(r"\s{2,}", " ", text)
    return text.strip()


for fname, url in SEJM_SPEECHES.items():
    try:
        txt = scrape_sejm(url)
        open(f"../literatura2/{fname}.txt", "w", encoding="utf-8").write(txt)
        print(f"✓ zapisano {fname}.txt ({len(txt)//1024} kB)")
    except Exception as e:
        print(f"✗ błąd przy {fname}: {e}")