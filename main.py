from PIL import Image, ImageDraw, ImageFont
Image.MAX_IMAGE_PIXELS = None  # Disattiva il limite
import textwrap
from albumReq import SpotyData
from lyrics import get_lyrics
from LyricCorr import correggi_testo_utente


#constanti
MAX_RGIHE=10
LARGHEZZA_RIGHE=25
spazioRighe = 75
DIM_TESTO = 120
DIM_TITOLO = 90
DIM_AUTORE = 60

def creaGrafica(tipoMesh,NC,T,A,C=True):
    TIPO_MESH = tipoMesh
    nomeCanzone = NC
    testo = T
    autore = A


    #cerco i dati della canzone
    album, titolo, autore = SpotyData(nomeCanzone,A)

    #verifico che il testo sia coretto
    if C:
        fullLyrics=get_lyrics(autore, titolo)
        testo = correggi_testo_utente(testo, fullLyrics, soglia=0.4)


    #carichiamo la base
    img = Image.open(TIPO_MESH).convert("RGBA")
    draw = ImageDraw.Draw(img)
    imgW, imgH = img.size

    #carico la foto album
    album = album.resize((270, 270))

    #calcolo posizione copertina
    copW, copH = album.size
    if TIPO_MESH == "hoodie.png":
        xCop=2250
        yCop=2250
    elif TIPO_MESH == "cover.png":
        xCop=2150
        yCop=2250
    elif TIPO_MESH == "tee.png":
        xCop=2150
        yCop=2100

    #posiziono la copertina

    img.paste(album, (xCop,yCop))


    #carichiamo font e definiamo il testo
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", DIM_TESTO) #dimensioni testo
    fontTitolo = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", DIM_TITOLO) #dimensioni testo
    fontAutore = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", DIM_AUTORE) #dimensioni testo

    #divido il testo in base a i \n
    righeRaw = testo.split("\n")

    #definisco i limiti di lunghezza del testo
    righe = []
    for r in righeRaw:
        righe+=textwrap.wrap(r,width=LARGHEZZA_RIGHE)

    #limito il numero di righe
    if len(righe)>MAX_RGIHE:
        righe=righe[:MAX_RGIHE] #slicing taglio le restanti righe

    #misuriamo altezza riga
    bbox = draw.textbbox((0, 0), "A", font=font)
    hRiga = bbox[3] - bbox[1]

    # Calcola partenza verticale e orrizontale
    x = xCop
    xTitolo = xCop + copW + 60
    yTitolo = yCop
    xAutore = xTitolo
    yAutore = yTitolo + 120
    y_base = imgH-3300

    #scrivo riga per riga sull'immagine
    for i, riga in enumerate(righe):
        bbox = draw.textbbox((0,0),riga,font=font)
        w=bbox[2]-bbox[0]
        y=y_base+i*(hRiga + spazioRighe)
        draw.text((x,y), riga, font=font, fill="white")

    #scrivo titolo e autore
        draw.text((xTitolo,yTitolo),titolo, font=fontTitolo, fill="white")
        draw.text((xAutore,yAutore),autore, font=fontAutore, fill="grey")

    return img




