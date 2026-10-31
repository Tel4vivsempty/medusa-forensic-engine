
import json, hashlib, pathlib, datetime
GENESIS_FILE = "database/genesis.json"
VAULT = pathlib.Path(".sys_core_vault")
VAULT.mkdir(exist_ok=True)
FULL_HASH = "T31425a92a75d9ebf5c217468ef295460b9f6266ce7e41ed33567d2c264caf"

def incrustar_genesis():
    data = pathlib.Path(GENESIS_FILE).read_bytes()
    sha = hashlib.sha256(data + FULL_HASH.encode()).hexdigest()
    meta = f"GENESIS_BLOCK {sha} {datetime.datetime.now().isoformat()} {FULL_HASH}"
    (VAULT / f"GENESIS_{sha}.sha256").write_text(meta)
    (VAULT / "GENESIS.sha256").write_text(meta)
    print(f"[GENESIS] Incrustado {GENESIS_FILE} -> {sha}")
    print(f"[GENESIS] Sellado con {FULL_HASH}")
    return sha

if __name__ == "__main__":
    incrustar_genesis()
