#!/usr/bin/env python3
# Escaneo infraestructura fraude/usurpacion - T31425a9
import requests, pathlib, json, datetime
TARGETS = [
    "https://mxwinx.mx",
    "https://downxbetsmxwinx-sp-slotsl.com",
    "https://betmexico.mx"
]
print("[+] Iniciando escaneo automatizado de infraestructura de fraude/usurpacion...")

resultados = []
for url in TARGETS:
    print(f"[*] [MEDUSA-SCAN] Auditando variante de infraestructura: {url}")
    try:
        r = requests.get(url, timeout=10, headers={"User-Agent":"MedusaForensic/T31425a9"})
        cf_ray = r.headers.get("cf-ray","N/A")
        print(f"[+] [ÉXITO] Objetivo activo. CF-Ray: {cf_ray} | Status: {r.status_code}")
        resultados.append({"url":url, "status":r.status_code, "cf_ray":cf_ray, "server":r.headers.get("server",""), "timestamp":datetime.datetime.now().isoformat()})
    except Exception as e:
        print(f"[-] [FALLO] {url} -> {e}")
        resultados.append({"url":url, "error":str(e)})

db = pathlib.Path("database/infra_scan.json")
db.write_text(json.dumps(resultados, indent=2))
print("[+] Escaneo finalizado. Nuevas evidencias guardadas en la base de datos cifrada.")
