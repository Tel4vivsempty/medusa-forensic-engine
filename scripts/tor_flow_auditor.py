
# Auditor de flujos Tor que vamos a emitir - defensivo, no generador de trafico anonimo
# Lee tor log o pcap y audita
import re, pathlib

def audit_tor_flow(log_path):
    if not pathlib.Path(log_path).exists():
        return ["LOG_NO_EXISTE"]
    txt=pathlib.Path(log_path).read_text(errors="ignore")
    findings=[]
    circuits=re.findall(r"CIRC.*\d+",txt)
    findings.append(f"CIRCUITS_FOUND: {len(circuits)}")
    if "N3" in txt or "directed" in txt.lower():
        findings.append("N3_MARKER_IN_TOR_LOG")
    # Verifica que el flujo tenga cabecera de custodia forense
    if "T31425a9" not in txt:
        findings.append("MISSING_AUTHORSHIP_HASH_IN_FLOW - no trazable")
    return findings
