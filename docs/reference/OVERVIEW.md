# Function Reference — OVERVIEW (cosa fa il progetto, per aree)

> Data: `2026-07-21` · SHA: `d54489d`  
> Generato da `funcref.overview` — sintesi grounded, ACTIVE-only. Le aree sono una sintesi tematica ancorata a moduli reali dell'inventario; i moduli citati esistono tutti (gate anti-allucinazione).

## Cosa fa

Il progetto fornisce utilità per la gestione della connettività WiFi (connessione con retry e reset hardware/software), la lettura di sensori da Home Assistant con formattazione del valore e unità, e l'azzeramento di indici testuali in una mappa dati.

## Aree / capability

### Connettività WiFi

Funzioni per tentare la connessione a una rete WiFi specifica con timeout e per forzare il ripristino della radio Wi-Fi tramite ciclo off/on e riconnessione.

Moduli: [`code`](code.md)

### Interrogazione Sensori

Interroga l'API di Home Assistant per leggere lo stato di un sensore, restituendo valore e unità di misura (KW o %) in base a flag.

Moduli: [`code`](code.md)

### Cancellazione Indici

Azzera il contenuto testuale di due indici per ogni entry di una mappa dati.

Moduli: [`code`](code.md)

## Flussi chiave

_(nessun flusso seed definito)_
