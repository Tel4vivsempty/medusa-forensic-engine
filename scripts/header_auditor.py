
# Auditor de cabeceras HTTP - presenta punto de como se auditan
import re

SUSPICIOUS_HEADERS=["X-N3","X-Forwarded-For: 127.0.0.1","Server: BasiliskII", "X-Medusa-Bypass"]

def audit_headers(raw_headers: str):
    findings=[]
    lines=raw_headers.split("\n")
    for line in lines:
        for sig in SUSPICIOUS_HEADERS:
            if sig.lower() in line.lower():
                findings.append(f"N3_SUSPICIOUS_HEADER: {line.strip()}")
        # Detecta Tor intentando ocultar origen
        if re.search(r"via:.*tor",line,re.I):
            findings.append(f"TOR_VIA_DETECTED: {line.strip()}")
        # Detecta inconsistencia de tierra/materiales en User-Agent geo
        if "User-Agent" in line and "68k" in line:
            findings.append(f"68K_UA_ANOMALY: {line.strip()}")
    return findings

if __name__=="__main__":
    sample="GET / HTTP/1.1\nHost: example.com\nX-N3: directed\nVia: Tor 0.4.8"
    print(audit_headers(sample))
