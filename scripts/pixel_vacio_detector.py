
# pixel_vacio_detector.py - detecta mxwinx.mx / downxbetsmxwinx.mx con respuesta vacia migrando a mxwinx.blog
import requests
DOMS_PREVIOS = ["https://mxwinx.mx", "https://downxbetsmxwinx.mx", "https://mxwinx.blog/?t=1&d=q0sDfJTb"]
for d in DOMS_PREVIOS:
    try:
        r = requests.get(d, timeout=8, headers={"User-Agent":"Mozilla/5.0"})
        vacio = len(r.text)<1000
        print(f"{d} -> {r.status_code} len={len(r.text)} vacio={vacio} server={r.headers.get('Server')} cf={r.headers.get('CF-Ray')}")
        if vacio:
            print(f"[!] INFRAESTRUCTURA INACTIVA / PIXEL VACIO - TRANSICION FORZADA detectada")
    except Exception as e:
        print(f"{d} -> ERROR {e} (posible NXDOMAIN / bloqueo UDP 53 Telcel/AT&T)")
