import requests
import base64
from PIL import Image
import io

def SpotyData(nomeCanzone, autore):
    clientID = "dcb58526464d467a949a1c1b6f37dd25"
    clientSecret = "6deeda307cb1460f9408d7fb9c03537f"

    # Codifica credenziali in base64
    clientCreds = f"{clientID}:{clientSecret}"
    clientCredsB64 = base64.b64encode(clientCreds.encode()).decode()

    # Richiesta token
    tokenURL = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": f"Basic {clientCredsB64}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    response = requests.post(tokenURL, headers=headers, data=data)
    response_json = response.json()
    access_token = response_json.get("access_token")

    # 🔍 Ricerca canzone + autore
    query = f"{nomeCanzone} {autore}"
    search_url = f"https://api.spotify.com/v1/search?q={requests.utils.quote(query)}&type=track&limit=1"
    headers_search = {
        "Authorization": f"Bearer {access_token}"
    }

    response_search = requests.get(search_url, headers=headers_search)
    tracks = response_search.json()

    if not tracks["tracks"]["items"]:
        raise ValueError("Canzone non trovata")

    # Estrai dati
    prima_canzone = tracks["tracks"]["items"][0]
    copertina_url = prima_canzone["album"]["images"][0]["url"]
    nome_album = prima_canzone["album"]["name"]
    nome_artista = prima_canzone["artists"][0]["name"]
    titolo_canzone = prima_canzone["name"]

    # Scarica la copertina
    response = requests.get(copertina_url)
    image_bytes = io.BytesIO(response.content)
    copertina = Image.open(image_bytes).convert("RGBA")

    return copertina, nome_artista, titolo_canzone


