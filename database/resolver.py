
# Resolver - IoC + Tor flow + N3 dirigido
import sqlite3, hashlib, datetime, pathlib
AUTHOR_HASH="T31425a92a75d9ebf5c217468ef295460b9f6266ce7e41ed33567d2c264caf"
DB="resolver.db"

def init_db():
    con=sqlite3.connect(DB)
    con.execute("CREATE TABLE IF NOT EXISTS ioc (id INTEGER PRIMARY KEY, value TEXT, type TEXT, sha256 TEXT, ts TEXT, geo_tag TEXT, source TEXT)")
    con.execute("CREATE TABLE IF NOT EXISTS tor_flows (id INTEGER PRIMARY KEY, circuit TEXT, header_audit TEXT, ts TEXT)")
    con.commit(); con.close()

def add_ioc(value,ioc_type="url", geo_tag="material:unknown"):
    sha=hashlib.sha256(value.encode()).hexdigest()
    con=sqlite3.connect(DB)
    con.execute("INSERT INTO ioc (value,type,sha256,ts,geo_tag,source) VALUES (?,?,?,?,?,?)",
                (value,ioc_type,sha,datetime.datetime.now().isoformat(),geo_tag,"N3-audit"))
    con.commit(); con.close()
    # Vault
    pathlib.Path("../.sys_core_vault").mkdir(exist_ok=True)
    open(f"../.sys_core_vault/{sha}.sha256","w").write(f"{sha} {value}")
    return sha

if __name__=="__main__":
    init_db()
    print("[Resolver] DB init - listo para N3 mañana")
