import time
import wifi
import board
import socketpool
import ssl
import adafruit_requests
from adafruit_matrixportal.matrixportal import MatrixPortal
import terminalio
import microcontroller  # Per resettare il dispositivo in caso estremo

# -----------------------------
# Fonts e display settings
# -----------------------------
WIDTH = 64
HEIGHT = 32
FONT_P1    = "/fonts/FiraSans-Bold-14.bdf"  # Pagina 1
SMALL_FONT = "/fonts/5x8.bdf"              # Pagine 2 e 3

# -----------------------------
# WiFi credentials
# -----------------------------
WIFI_SSID     = "***"
WIFI_PASSWORD = "***."

# -----------------------------
# Funzioni WiFi con log
# -----------------------------
def connect_wifi():
    print("[WIFI] Abilitazione radio WiFi e tentativo di connessione")
    wifi.radio.enabled = True
    start = time.monotonic()
    while time.monotonic() - start < 20:
        try:
            wifi.radio.connect(WIFI_SSID, WIFI_PASSWORD)
            ip = wifi.radio.ipv4_address
            print(f"[WIFI] Connesso a '{WIFI_SSID}', IP assegnato: {ip}")
            return True
        except Exception as e:
            print(f"[WIFI] Errore connessione: {e}, ritento...")
            time.sleep(1)
    print("[WIFI] Timeout connessione WiFi")
    return False


def reset_wifi():
    print("[WIFI] Resetting WiFi radio...")
    wifi.radio.enabled = False
    time.sleep(1)
    wifi.radio.enabled = True
    status = connect_wifi()
    print(f"[WIFI] Reset completato, stato connessione: {status}")
    return status

# -----------------------------
# Inizializzazione display
# -----------------------------
matrixportal = MatrixPortal(width=WIDTH, height=HEIGHT, bit_depth=6, debug=False)

# -----------------------------
# Pagine setup
# -----------------------------
# Pagina 1: Totale produzione su due righe
sensor_total = "sensor.solaredge_lifetime_energy"  # Wh
idx_p1_label = matrixportal.add_text(
    text_font=FONT_P1,
    text_position=(WIDTH//2, 0),
    text_anchor_point=(0.5, 0.5),
    scrolling=False,
    text_scale=1
)
idx_p1_value = matrixportal.add_text(
    text_font=FONT_P1,
    text_position=(WIDTH//2, 10),
    text_anchor_point=(0.5, 0.5),
    scrolling=False,
    text_scale=1
)

# Pagina 2: ATTUALE, OGGI, EXPORT, IMPORT
LABEL_X = 0
VALUE_X = 63
Y_POS    = [4, 12, 20, 28]
labels2  = ["ATTUALE", "OGGI", "EXPORT", "IMPORT"]
sensors2 = [
    "sensor.porlezza_solar_power",
    "sensor.porlezza_solar_generated",
    "sensor.porlezza_grid_exported",
    "sensor.porlezza_grid_imported"
]
indices2 = {}
for i, lbl in enumerate(labels2):
    l = matrixportal.add_text(
        text_font=SMALL_FONT,
        text_position=(LABEL_X, Y_POS[i]),
        text_anchor_point=(0.0, 0.5),
        scrolling=False,
        text_scale=1
    )
    v = matrixportal.add_text(
        text_font=SMALL_FONT,
        text_position=(VALUE_X, Y_POS[i]),
        text_anchor_point=(1.0, 0.5),
        scrolling=False,
        text_scale=1
    )
    indices2[lbl] = (l, v)
    matrixportal.set_text("", index=l)
    matrixportal.set_text("", index=v)

# Pagina 3: CONSUMO, CHARGE, RESIDUA, WALLCONN
labels3  = ["CONSUMO", "CHARGE", "RESIDUA", "WALLCONN"]
sensors3 = [
    "sensor.porlezza_load_power",
    "sensor.porlezza_percentage_charged",
    "sensor.powerwall_energia_residua_kw",
    "sensor.wall_connector_power_6"
]
indices3 = {}
for i, lbl in enumerate(labels3):
    l = matrixportal.add_text(
        text_font=SMALL_FONT,
        text_position=(LABEL_X, Y_POS[i]),
        text_anchor_point=(0.0, 0.5),
        scrolling=False,
        text_scale=1
    )
    v = matrixportal.add_text(
        text_font=SMALL_FONT,
        text_position=(VALUE_X, Y_POS[i]),
        text_anchor_point=(1.0, 0.5),
        scrolling=False,
        text_scale=1
    )
    indices3[lbl] = (l, v)
    matrixportal.set_text("", index=l)
    matrixportal.set_text("", index=v)

# Utility clear per pagine

def clear_indices(idx_map):
    for l, v in idx_map.values():
        matrixportal.set_text("", index=l)
        matrixportal.set_text("", index=v)

# -----------------------------
# Costanti loop e colori
# -----------------------------
UPDATE_I = 60  # sec tra aggiornamenti
SWITCH_I = 40  # sec per cambio pagina iniziale
colors = [0x404000, 0x004040, 0x004000, 0x400000]

# -----------------------------
# Connessione WiFi e HTTP
# -----------------------------
if not connect_wifi():
    matrixportal.set_text("WiFi Error", index=idx_p1_label)
    matrixportal.set_text_color(0x7F7F00, index=idx_p1_label)
    while True:
        time.sleep(1)

print("[HTTP] Configurazione SocketPool e SSL")
pool        = socketpool.SocketPool(wifi.radio)
ssl_context = ssl.create_default_context()
requests    = adafruit_requests.Session(pool, ssl_context)
print("[HTTP] Sessione HTTP pronta")

HA_URL = "https://e7h76qr4jx9zoycwmpa4klm9l00h2xs8.ui.nabu.casa/api/states"
HA_TOKEN = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
    "eyJpc3MiOiIwZDkzZGE2ODA1ZmI0Y2RlYTFiNDdkMGRhM2RlMzQyZiIsImlhdCI6MTc1MjIyNjIwNCwiZXhwIjoyMDY3NTg2MjA0fQ."
    "KY9ADeH9S3scuR8KPGXy0ruCtvJJgjRC6rkVUikvc9w"
)

# Lettura sensori con log

def read_sensor(eid, wh=False, pct=False, one_decimal=False):
    url     = f"{HA_URL}/{eid}"
    headers = {"Authorization": f"Bearer {HA_TOKEN}"}
    try:
        r = requests.get(url, headers=headers, timeout=5)
        if r.status_code == 200:
            s = float(r.json().get("state", 0))
            if wh:
                s /= 1000
            disp = f"{s:.1f}" if one_decimal else str(int(s))
            suf  = '%' if pct else 'KW'
            print(f"[SENSOR] {eid} -> {disp}{suf}")
            return disp, suf
        else:
            print(f"[SENSOR] Stato HTTP {r.status_code} per {eid}")
    except Exception as e:
        print(f"[SENSOR] Errore lettura {eid}: {e}, reset WiFi")
        reset_wifi()
    return "?", ''

# -----------------------------
# Main loop con 3 pagine e log
# -----------------------------
print("[MAIN] Avvio loop principale")
# Disegna subito pagina 1
total, suf = read_sensor(sensor_total, wh=True)
matrixportal.set_text("Totale", index=idx_p1_label)
matrixportal.set_text_color(colors[0], index=idx_p1_label)
matrixportal.set_text(f"{total}{suf}", index=idx_p1_value)
matrixportal.set_text_color(colors[0], index=idx_p1_value)

last_up = time.monotonic()
last_sw = last_up
page    = 1

while True:
    now = time.monotonic()
    # Aggiornamento dati
    if now - last_up >= UPDATE_I:
        print(f"[MAIN] Update pagina {page}")
        if page == 1:
            matrixportal.set_text("", index=idx_p1_label)
            matrixportal.set_text("", index=idx_p1_value)
            total, suf = read_sensor(sensor_total, wh=True)
            matrixportal.set_text("Totale", index=idx_p1_label)
            matrixportal.set_text_color(colors[0], index=idx_p1_label)
            matrixportal.set_text(f"{total}{suf}", index=idx_p1_value)
            matrixportal.set_text_color(colors[0], index=idx_p1_value)
        elif page == 2:
            clear_indices(indices2)
            for i, lbl in enumerate(labels2):
                val, suf = read_sensor(sensors2[i], one_decimal=(i==0))
                l, v = indices2[lbl]
                matrixportal.set_text(lbl, index=l)
                matrixportal.set_text_color(colors[i], index=l)
                matrixportal.set_text(f"{val}{suf}", index=v)
                matrixportal.set_text_color(colors[i], index=v)
        else:
            clear_indices(indices3)
            for i, lbl in enumerate(labels3):
                val, suf = read_sensor(sensors3[i], one_decimal=(i==0), pct=(i==1))
                l, v = indices3[lbl]
                matrixportal.set_text(lbl, index=l)
                matrixportal.set_text_color(colors[i], index=l)
                matrixportal.set_text(f"{val}{suf}", index=v)
                matrixportal.set_text_color(colors[i], index=v)
        last_up = now
    # Cambio pagina
    if now - last_sw >= SWITCH_I:
        # Pulisce schermo
        matrixportal.set_text("", index=idx_p1_label)
        matrixportal.set_text("", index=idx_p1_value)
        clear_indices(indices2)
        clear_indices(indices3)
        page = page % 3 + 1
        print(f"[MAIN] Switch a pagina {page}")
        if SWITCH_I > 20:
            SWITCH_I = 20
        last_sw = now
        last_up  = 0
    time.sleep(0.1)
