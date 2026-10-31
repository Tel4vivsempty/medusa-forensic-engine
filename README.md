# Medusa Forensic Engine
Pipeline local automatizado en Debian-PRoot (Termux) para la interceptación, auditoría forense, resolución HTTP de IoCs de smishing y registro inalterable mediante hashes SHA-256.

## Componentes
- **Core C++ (.03):** Interceptación de sockets y análisis de alto rendimiento.
- **Python Scripts:** Resolución activa de URLs, control de telemetría e inyección a broker MQTT (localhost:1883).
- **Vault de Evidencias:** Resguardo criptográfico con verificación de integridad SHA-256.
