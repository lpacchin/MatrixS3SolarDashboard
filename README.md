# MatrixS3SolarDashboard

Firmware CircuitPython per MatrixPortal S3 con pannello LED HUB75 64x32 - Dashboard produzione impianto fotovoltaico.

## Descrizione

Dashboard dedicata alla produzione dell'impianto fotovoltaico su un singolo pannello LED RGB 64x32. Legge i dati in tempo reale da Home Assistant (SolarEdge) e li visualizza in pagine che si alternano automaticamente. Il display mostra produzione totale, potenza attuale, produzione giornaliera, export e import.

## Funzionalita

- **Produzione totale lifetime** (sensore SolarEdge) su pagina principale
- **Potenza attuale** in tempo reale
- **Produzione giornaliera** (oggi)
- **Export e Import** verso/dalla rete
- **Pagine multiple** con alternanza automatica:
  - Pagina 1: Produzione totale (font grande)
  - Pagina 2: Attuale, Oggi, Export, Import (font piccolo)
  - Pagina 3: Dati aggiuntivi
- **Font differenziati**: FiraSans-Bold-14 per valori principali, 5x8 per dettagli
- **Gestione Wi-Fi** robusta con riconnessione automatica

## Stack Tecnologico

- **Microcontrollore**: Adafruit MatrixPortal S3 (ESP32-S3)
- **Display**: Pannello LED RGB HUB75 64x32 (bit_depth 6)
- **Linguaggio**: CircuitPython
- **Librerie**: adafruit_matrixportal, adafruit_requests, adafruit_bitmap_font
- **API dati**: Home Assistant REST API (sensori SolarEdge)

## Configurazione

Credenziali Wi-Fi e token Home Assistant nel file `settings.toml`.

## Struttura File

| File/Cartella | Descrizione |
|---------------|-------------|
| `code.py` | Firmware principale: pagine display, fetch dati da HA |
| `fonts/` | Font BDF (FiraSans-Bold-14, 5x8) |
| `sd/` | File su SD card |
| `settings.toml` | Configurazione Wi-Fi, URL e token Home Assistant |
| `boot_out.txt` | Output boot CircuitPython |
