
# medusa-forensic-engine
Pipeline forense defensivo - MQTT + Vault SHA-256 + Core C++ .03
Author Hash: T31425a92a75d9ebf5c217468ef295460b9f6266ce7e41ed33567d2c264caf

## Pipeline alineado
Ingesta (stockdata) -> Parser (header audit + resource fork 68k) -> Core .03 (intercept + geomat) -> Resolver (IoC + Tor flow audit) -> MQTT 1883 -> Vault SHA-256 -> Dashboard

- Backend: API Flask en dashboard/app.py expone /api/stockdata y /api/evidence
- Canal secundario seguro (antes backdoor): /api/internal/audit con token Vault - para auditoría interna de cabeceras y flujos Tor, no para acceso externo.
- Ciencias de la Tierra/Materiales: evidencia física taggeada con contexto geológico y cadena de custodia.

## Estructura
core/ - C++ .03 intercept
database/ - resolver y schema
scripts/ - parser, header_auditor, tor_flow_auditor, mqtt_ingest, evidence_vault
dashboard/ - UI para auditoría de cabeceras y flujos Tor
.sys_core_vault/ - hashes de autor
evidence/ - pcap, dumps

## Uso PRoot
cd /root/medusa-forensic-engine
cp -r /mnt/data/medusa-forensic-engine/* .
pip install -r scripts/requirements.txt
