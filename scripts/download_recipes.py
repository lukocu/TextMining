# scripts/download_recipes.py
import requests, os, re
from bs4 import BeautifulSoup

t
script_dir = os.path.dirname(os.path.abspath(__file__))

base_dir = os.path.dirname(script_dir)

output_dir = os.path.join(base_dir, 'literatura2')
os.makedirs(output_dir, exist_ok=True)


RECIPES = {

    "kuchnia_pierogi_ruskie":  "https://www.mojegotowanie.pl/przepis/pierogi-ruskie",
    "kuchnia_zurek":           "https://www.mojegotowanie.pl/przepis/zurek-domowy",
    "kuchnia_sernik_krakowski":"https://www.kwestiasmaku.com/przepis/sernik-krakowski",
  
}

def scrape_recipe(url):
    """Zwraca tekst (składniki + wykonanie) z podanej strony przepisu."""
    html = requests.get(url, timeout=15).text
    soup = BeautifulSoup(html, "html.parser")
    

    ingr_blocks = soup.select("div.ingredients, ul.ingredients, div.recipe-ingredients")
    ingredients = "\n".join(
        li.get_text(" ", strip=True) for block in ingr_blocks for li in block.select("li")
    )
    

    steps_blocks = soup.select("div.directions, ol.directions, div.preparation, div.recipe-preparation")
    steps = "\n".join(
        re.sub(r"\s+", " ", p.get_text(" ", strip=True))
        for block in steps_blocks for p in block.select("li, p")
    )
  
    if not steps:
        steps = "\n".join(p.get_text(" ", strip=True) for p in soup.select("p")[:20])
    
    return "SKŁADNIKI:\n" + ingredients.strip() + "\n\nPRZYGOTOWANIE:\n" + steps.strip()

for fname, url in RECIPES.items():
    try:
        text = scrape_recipe(url)
        open(f"../literatura2/{fname}.txt", "w", encoding="utf-8").write(text)
        print(f"✓ zapisano {fname}.txt")
    except Exception as e:
        print(f"✗ błąd {fname}: {e}")