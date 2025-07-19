from difflib import SequenceMatcher

def sim(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def correggi_testo_utente(testo_utente, testo_originale, soglia=0.75, soglia_rifiuto=0.5, tolleranza_errori=0.3):
    parole_originale = testo_originale.replace("\n", " ").split()
    parole_utente = testo_utente.strip().split()

    # 🔍 Controllo iniziale: almeno un blocco deve essere simile
    lunghezza = len(parole_utente)
    ha_blocco_valido = False
    for i in range(len(parole_originale) - lunghezza + 1):
        blocco = " ".join(parole_originale[i:i+lunghezza])
        if sim(testo_utente, blocco) >= soglia_rifiuto:
            ha_blocco_valido = True
            break
    if not ha_blocco_valido:
        return "Testo non riconosciuto come parte della canzone"

    risultato = []
    i = 0
    parole_riconosciute = 0

    while i < len(parole_utente):
        best_match = None
        best_score = 0
        best_chunk = None
        lunghezza_massima = min(6, len(parole_utente) - i)

        for lunghezza in range(lunghezza_massima, 2, -1):
            blocco = parole_utente[i:i+lunghezza]
            frase = " ".join(blocco)

            for j in range(0, len(parole_originale) - lunghezza + 1):
                frase_originale = " ".join(parole_originale[j:j+lunghezza])
                score = sim(frase, frase_originale)

                if score > best_score:
                    best_score = score
                    best_match = frase_originale
                    best_chunk = lunghezza

        if best_score >= soglia:
            risultato.append(best_match)
            parole_riconosciute += best_chunk
            i += best_chunk
        else:
            i += 1  # Salta parola errata (non la includiamo)

    # 📉 Calcolo parole corrette / totali
    accuratezza = parole_riconosciute / len(parole_utente)
    if accuratezza < (1 - tolleranza_errori):
        return "Testo non riconosciuto come parte della canzone"

    return " ".join(risultato)



