from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import requests
from bs4 import BeautifulSoup
import time
import re

GENIUS_TOKEN = "g-_b79QqK6cI_ecEqEIJ2HlRYyvwiKnCBzCkLSWju92gP47uWIV96yLit69LRVuP"

def get_lyrics(artista, titolo):
    # === 1. Cerca il link della canzone tramite API Genius ===
    headers_api = {
        "Authorization": f"Bearer {GENIUS_TOKEN}"
    }
    query = f"{titolo} {artista}"
    search_url = "https://api.genius.com/search"
    params = {"q": query}
    response = requests.get(search_url, headers=headers_api, params=params)
    data = response.json()

    try:
        url = data["response"]["hits"][0]["result"]["url"]
    except (IndexError, KeyError):
        return "Testo non trovato (errore nella ricerca)."

    # === 2. Apri il link con Selenium (browser headless) ===
    options = Options()
    options.headless = True  # Nasconde il browser
    driver = webdriver.Firefox(options=options)
    driver.get(url)
    time.sleep(2)  # Tempo per caricare la pagina completamente

    html = driver.page_source
    driver.quit()

    # === 3. Estrai il testo dei <div> con BeautifulSoup ===
    soup = BeautifulSoup(html, "html.parser")
    lyrics_divs = soup.find_all("div", class_=lambda c: c and "Lyrics__Container" in c)

    if lyrics_divs:
        testo = "\n".join(div.get_text(separator="\n").strip() for div in lyrics_divs)
        return pulisci_testo(testo)

    return "Testo non trovato (contenuto non rilevato)."

def pulisci_testo(testo):
    # 1. Rimuovi tutto tra parentesi quadre []
    testo = re.sub(r"\[.*?\]", "", testo)
    
    # 2. Rimuovi tutto tra parentesi tonde ()
    testo = re.sub(r"\(.*?\)", "", testo)

    # 4. Rimuovi righe vuote multiple
    testo = re.sub(r"\n{2,}", "\n", testo)

    return testo.strip()


