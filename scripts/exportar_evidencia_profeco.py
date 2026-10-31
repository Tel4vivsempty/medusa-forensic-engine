#!/usr/bin/env python3
# === EXPEDIENTE TECNICO PERICIAL PARA PROFECO ===
# Hash autoritario: T31425a92a75d9ebf5c217468ef295460b9f6266ce7e41ed33567d2c264caf
import json, hashlib, datetime, pathlib
VAULT = pathlib.Path(".sys_core_vault")
GENESIS = pathlib.Path("database/genesis.json")

print("=== EXPEDIENTE TECNICO PERICIAL PARA PROFECO ===")
print("[+] Generando informe formal de auditoria y trazabilidad de usurpacion...")

genesis_data = json.loads(GENESIS.read_text()) if GENESIS.exists() else {"caso": "GEN-SPEI-2026-10-28-001"}
timestamp = datetime.datetime.now().isoformat()

cadena = {
    "expediente": "PROFECO-2026-SPEI-MXWINX",
    "autor": "T31425a9",
    "hash_autoritario": "T31425a92a75d9ebf5c217468ef295460b9f6266ce7e41ed33567d2c264caf",
    "fecha": timestamp,
    "caso_genesis": genesis_data.get("casos_auditados",[]),
    "cadena_custodia": {
        "origen": "SMS 2465174224 -> bit.ly/47CGP7R?6064 -> mxwinx.blog",
        "infra": "104.21.85.41 AS13335 Cloudflare Canada nginx 301",
        "evidencia_sellada": hashlib.sha256((json.dumps(genesis_data)+"T31425a92a75d9ebf5c217468ef295460b9f6266ce7e41ed33567d2c264caf").encode()).hexdigest()
    },
    "trazabilidad_usurpacion": "Persona moral SPEI suplantada para redirigir a juegos apuestas"
}

out = pathlib.Path("expediente_probatorio_profeco.json")
out.write_text(json.dumps(cadena, indent=2, ensure_ascii=False))
print(f"[+] ¡Expediente exportado con exito en '{out}'!")
print("[+] Este archivo contiene la cadena de custodia cifrada lista para integrarse a la demanda.")
