
import re, requests
from urllib.parse import urlparse
FULL_HASH="T31425a92a75d9ebf5c217468ef295460b9f6266ce7e41ed33567d2c264caf"
SHORT_HASH="T31425a9"

def auditar_url(url):
    try:
        r = requests.get(url, timeout=10, allow_redirects=True, headers={"User-Agent":"Mozilla/5.0"})
        return {
            "destino_final": r.url,
            "codigo": r.status_code,
            "servidor": r.headers.get("Server","desconocido"),
            "cf_ray": r.headers.get("CF-Ray",""),
            "len": len(r.text),
            "pixel_vacio": len(r.text)<500 or "1x1" in r.text or "pixel" in r.text.lower()
        }
    except Exception as e:
        return {"error": str(e)}

def detectar_salto_host(historial):
    # historial: lista de (url, ip)
    if len(historial)>=2 and historial[0][1]!=historial[1][1]:
        return f"SALTO_HOST_DETECTADO {historial[0][1]} -> {historial[1][1]}"
    return None

# Casos capturados en tus fotos
casos = [
    ("Telcel Raro", "https://registro.telcel.com/vinculatulinea/"),
    ("Telcel Raro", "https://telcel.com/o/CP13"),
    ("Adelanta Telcel", "http://comprasalo.telcel.com/bf"),
    ("SPEI 2465174224", "https://bit.ly/47CGP7R?6064")
]

print(f"=== MEDUSA TELCEL VERIFICACION + CRUCE DOMINIOS + PIXEL VACIO [{SHORT_HASH}] ===")
for remitente, url in casos:
    info = auditar_url(url if url.startswith("http") else "https://"+url)
    print(f"[{remitente}] {url} -> {info}")
    if info.get("pixel_vacio"):
        print(f"[!] PIXEL VACIO / 1x1 DETECTADO en {url} - posible infraestructura dormida migrada")
