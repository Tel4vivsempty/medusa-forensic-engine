
import pathlib, hashlib, datetime, json
FULL_HASH = "T31425a92a75d9ebf5c217468ef295460b9f6266ce7e41ed33567d2c264caf"
VAULT = pathlib.Path(".sys_core_vault")
VAULT.mkdir(exist_ok=True)
data = pathlib.Path("database/genesis.json").read_bytes()
sha = hashlib.sha256(data + FULL_HASH.encode()).hexdigest()
meta = f"GENESIS_BLOCK {sha} {datetime.datetime.now().isoformat()} {FULL_HASH} - SPEI 2465174224 bit.ly->mxwinx.blog"
(VAULT / f"GENESIS_{sha}.sha256").write_text(meta)
(VAULT / "GENESIS.sha256").write_text(meta)
print(f"[GENESIS] Caso SPEI $329 MXN incrustado -> {sha}")
print(f"[GENESIS] Sender 2465174224 -> mxwinx.blog 104.21.85.41 Cloudflare")
