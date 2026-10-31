
import hashlib, pathlib, datetime
VAULT=pathlib.Path("../.sys_core_vault")
VAULT.mkdir(exist_ok=True)

def seal_evidence(file_path, geo_tag="HASH_AUTORITARIO_INTELECTUAL: T31425a92a75d9ebf5c217468ef295460b9f6266ce7e41ed33567d2c264caf"):
    data=pathlib.Path(file_path).read_bytes()
    sha=hashlib.sha256(data).hexdigest()
    meta=f"{sha} {file_path} {geo_tag} {datetime.datetime.now().isoformat()} T31425a9"
    (VAULT / f"{sha}.sha256").write_text(meta)
    print(f"[Vault] Sellado {file_path} -> {sha}")
    return sha
