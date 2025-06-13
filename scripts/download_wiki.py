

"""
Pobiera czysty tekst (bez HTML) wybranych haseł z polskiej Wikipedii
przez endpoint action=query&prop=extracts.
Licencja artykułów: CC BY-SA 3.0.
"""

import os, re, requests, json

os.makedirs("../literatura2", exist_ok=True)

PAGES = {
    "wiki_maria_sklodowska_curie": "Maria Skłodowska-Curie",
    "wiki_adam_malysz":            "Adam Małysz",
    "wiki_wislawa_szymborska":     "Wisława Szymborska",
    "wiki_robert_lewandowski":     "Robert Lewandowski",
    "wiki_olga_tokarczuk":         "Olga Tokarczuk",
    "wiki_lech_walesa":            "Lech Wałęsa",
    "wiki_krzysztof_penderecki":   "Krzysztof Penderecki",
    "wiki_jozef_pilsudski":        "Józef Piłsudski",
}

API = "https://pl.wikipedia.org/w/api.php"
HEADERS = {"User-Agent": "TextMiningBot/0.2 (kontakt: twoj@mail.pl)"}


def fetch_extract(title: str) -> str:
    """Zwraca plaintext artykułu (bez sekcji przypisów)."""
    params = {
        "action": "query",
        "prop": "extracts",
        "titles": title,
        "format": "json",
        "explaintext": 1,
        "exsectionformat": "plain",
    }
    r = requests.get(API, params=params, headers=HEADERS, timeout=20)
    r.raise_for_status()
    data = r.json()

    page = next(iter(data["query"]["pages"].values()))
    if "extract" not in page:
        raise ValueError(page.get("title", "???") + " – brak extract")

    text = page["extract"]

    
    blacklist = ("Przypisy", "Bibliografia", "Linki zewnętrzne", "Zobacz też")
    for blk in blacklist:
        idx = text.lower().find("\n" + blk.lower())
        if idx != -1:
            text = text[:idx].strip()
   
    text = re.sub(r"\[\d+]", "", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    return text.strip()


for fname, title in PAGES.items():
    try:
        txt = fetch_extract(title)
        path = f"../literatura2/{fname}.txt"
        with open(path, "w", encoding="utf-8") as f:
            f.write(txt)
        print(f"✓ zapisano {fname}.txt ({len(txt)//1024} kB)")
    except Exception as e:
        print(f"✗ błąd przy {fname}: {e}")