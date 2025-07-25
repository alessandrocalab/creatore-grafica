import re

def correggi_testo_utente(testoUtente, testoOriginale, tolleranza=1):

    chiavePulita = re.sub(r'\[[^\]]*\]', '', testoUtente)  # [ ... ]
    chiavePulita = re.sub(r'\([^)]*\)', '', chiavePulita)
    chiavePulita = ' '.join(chiavePulita.replace('\n', ' ').split())

    TOLen = len(testoOriginale)
    keyLen = len(chiavePulita)

    indiceInizio = 0
    indiceFine = 0
    maxPtg = 0

    for i in range(TOLen-keyLen+1):

        TemPtg = 0

        for j in range(keyLen):
            if chiavePulita[j].lower()==testoOriginale[i+j].lower():
                TemPtg+=1

        if TemPtg > maxPtg:
            maxPtg = TemPtg
            indiceInizio = i
            indiceFine = i+keyLen
    
    print(keyLen)
    print(maxPtg)
    if maxPtg >= (keyLen * tolleranza):

        while indiceInizio > 0 and testoOriginale[indiceInizio] != '\n':
            indiceInizio-=1

        while indiceFine < len(testoOriginale) and testoOriginale[indiceFine] != '\n':
            indiceFine+=1

        return testoOriginale[indiceInizio+1:indiceFine]
    else:
        return "Il testo inserito non fa parte della canzone"
   