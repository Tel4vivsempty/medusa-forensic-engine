
# Parser defensivo - resource fork 68k + smishing + cabeceras
import hashlib, pathlib
AUTHOR="T31425a9"

def audit_resource_fork(path):
    data=pathlib.Path(path).read_bytes() if pathlib.Path(path).exists() else b""
    # Detecta patron MacBinary / APPL / RESOURCE de Basilisk
    flags=[]
    if b"RESOURCE" in data or b"mMOR" in data: flags.append("68k_resource_fork")
    if b"N3" in data: flags.append("N3_marker")
    return flags

def parse_sample(path):
    sha=hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest() if pathlib.Path(path).exists() else "no_file"
    return {"path":str(path),"sha256":sha,"flags":audit_resource_fork(path)}
