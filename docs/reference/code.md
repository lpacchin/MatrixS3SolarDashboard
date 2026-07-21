# Reference: code

> SHA: `d54489d` · Copertura LLM: 4/4  
> Fotografia generata da `funcref.generate` — overview ACTIVE-only, storico completo nel corpo.

## Module Overview

Il modulo `code` possiede **4** funzioni ACTIVE, di cui **0** endpoint HTTP.  
Dipende da (chiamate uscenti cross-module): nessun modulo interno.  
È usato da (chiamate entranti cross-module): nessun modulo interno.

| Funzione | Firma | Route | Scopo |
|---|---|---|---|
| [`code.clear_indices`](#code.clear_indices) | `clear_indices(idx_map)` | `—` | Azzera il testo su due indici per ogni entry della mappa. |
| [`code.connect_wifi`](#code.connect_wifi) | `connect_wifi()` | `—` | Tenta di connettersi alla rete WiFi specificata, ritentando per un massimo di 20 secondi. Stampa stato su stdout. |
| [`code.read_sensor`](#code.read_sensor) | `read_sensor(eid, wh=False, pct=False, one_decimal=False)` | `—` | Interroga l'API Home Assistant per leggere lo stato di un sensore e restituisce valore formattato e unità di misura (KW o %) in base ai flag. |
| [`code.reset_wifi`](#code.reset_wifi) | `reset_wifi()` | `—` | Disabilita e riabilita la radio Wi-Fi (ciclo off/on) per forzarne il reset, quindi riconnette tramite connect_wifi. |

---

<!-- fn:code.clear_indices -->
## `code.clear_indices` <a name="code.clear_indices"></a>

**Stato**: `[ACTIVE]`  
**Firma**: `clear_indices(idx_map)`  
**Async**: no  
**Posizione**: `code.py:140`  
**Route**: —  
**Env**: —  
**Side-effects**: —  
**Chiama**: —  
**Chiamata da**: —  

**Scopo**: Azzera il testo su due indici per ogni entry della mappa.

**Input**: idx_map: dict o mapping con valori iterabili contenenti esattamente due elementi (l, v).

**Output**: None. Può sollevare ValueError se i valori non hanno due elementi.

**Gotcha**: —

<!-- fn:code.connect_wifi -->
## `code.connect_wifi` <a name="code.connect_wifi"></a>

**Stato**: `[ACTIVE]`  
**Firma**: `connect_wifi()`  
**Async**: no  
**Posizione**: `code.py:28`  
**Route**: —  
**Env**: —  
**Side-effects**: —  
**Chiama**: —  
**Chiamata da**: [`code.reset_wifi`](#code.reset_wifi)  

**Scopo**: Tenta di connettersi alla rete WiFi specificata, ritentando per un massimo di 20 secondi. Stampa stato su stdout.

**Input**: Nessun parametro.

**Output**: True se la connessione riesce entro il timeout; False in caso di timeout o errori persistenti.

**Gotcha**: Dipende da variabili globali WIFI_SSID e WIFI_PASSWORD; blocca l’esecuzione fino a 20 s; assume l’esistenza dell’oggetto wifi.radio e che possa essere abilitato.

<!-- fn:code.read_sensor -->
## `code.read_sensor` <a name="code.read_sensor"></a>

**Stato**: `[ACTIVE]`  
**Firma**: `read_sensor(eid, wh=False, pct=False, one_decimal=False)`  
**Async**: no  
**Posizione**: `code.py:176`  
**Route**: —  
**Env**: —  
**Side-effects**: `network`  
**Chiama**: [`code.reset_wifi`](#code.reset_wifi)  
**Chiamata da**: —  

**Scopo**: Interroga l'API Home Assistant per leggere lo stato di un sensore e restituisce valore formattato e unità di misura (KW o %) in base ai flag.

**Input**: eid: stringa identificativa del sensore (obbligatoria). wh: booleano, se True divide per 1000. pct: booleano, se True indica percentuale. one_decimal: booleano, se True forza una cifra decimale. Dipende da variabili globali HA_URL e HA_TOKEN.

**Output**: Tupla (disp, suf): disp è stringa del valore formattato, suf è 'KW' o '%'. In caso di errore HTTP o eccezione restituisce ('?', ''). Scrive anche su stdout tramite print.

**Gotcha**: Utilizza variabili globali HA_URL e HA_TOKEN non validate; in caso di qualsiasi eccezione richiama reset_wifi() (effetto collaterale non tracciato nei segnali); la divisione per 1000 con wh=True può perdere precisione; non gestisce la mancanza delle variabili globali.

<!-- fn:code.reset_wifi -->
## `code.reset_wifi` <a name="code.reset_wifi"></a>

**Stato**: `[ACTIVE]`  
**Firma**: `reset_wifi()`  
**Async**: no  
**Posizione**: `code.py:45`  
**Route**: —  
**Env**: —  
**Side-effects**: —  
**Chiama**: [`code.connect_wifi`](#code.connect_wifi)  
**Chiamata da**: [`code.read_sensor`](#code.read_sensor)  

**Scopo**: Disabilita e riabilita la radio Wi-Fi (ciclo off/on) per forzarne il reset, quindi riconnette tramite connect_wifi.

**Input**: Nessun parametro.

**Output**: Ritorna il valore restituito da connect_wifi (tipicamente lo stato della connessione, es. booleano o stringa). Nessuna eccezione documentata.

**Gotcha**: Richiede che l'oggetto wifi.radio sia accessibile e time.sleep importato; eventuali eccezioni di connect_wifi non sono gestite.
