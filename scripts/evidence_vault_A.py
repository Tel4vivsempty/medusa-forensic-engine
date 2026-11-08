
import hashlib, pathlib, datetime
VAULT=pathlib.Path("../.sys_core_vault")
VAULT.mkdir(exist_ok=True)

def seal_evidence(file_path, geo_tag="ciencias_tierra: Pachuca Hgo, material: silicon"):
    data=pathlib.Path(file_path).read_bytes()
    sha=hashlib.sha256(data).hexdigest()
    meta=f"{sha} {file_path} {geo_tag} {datetime.datetime.now().isoformat()} T31425a9"
    (VAULT / f"{sha}.sha256").write_text(meta)
    print(f"[Vault] Sellado {file_path} -> {sha}")
    return sha
