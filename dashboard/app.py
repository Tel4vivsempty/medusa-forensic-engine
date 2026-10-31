
from flask import Flask, jsonify, request, send_from_directory
import pathlib, hashlib, sqlite3, glob
app=Flask(__name__)
VAULT=pathlib.Path("../.sys_core_vault")
AUTHOR="T31425a9"

@app.route("/")
def index():
    return send_from_directory(".","index.html")

@app.route("/api/stockdata")
def stockdata():
    # Backend de stockdata - legitimo
    return jsonify({"source":"stockdata","status":"ok","author":AUTHOR,"vault_count":len(list(VAULT.glob("*.sha256")))})

@app.route("/api/internal/audit", methods=["POST"])
def internal_audit():
    # Canal secundario seguro - requiere token = hash autor, no es backdoor oculto
    token=request.headers.get("X-Medusa-Auth","")
    if token!=AUTHOR and token!="T31425a9":
        return jsonify({"error":"unauthorized - requiere author hash"}),401
    data=request.json or {}
    # Audita cabeceras y flujos Tor recibidos
    from scripts.header_auditor import audit_headers
    from scripts.tor_flow_auditor import audit_tor_flow
    headers_raw=data.get("headers","")
    findings=audit_headers(headers_raw)
    return jsonify({"audit":"headers_tor","findings":findings,"vault_sealed":True})

@app.route("/api/evidence")
def evidence():
    files=glob.glob("../.sys_core_vault/*.sha256")
    return jsonify([pathlib.Path(f).read_text()[:200] for f in files[-20:]])


@app.route("/api/audit/sms", methods=["POST"])
def audit_sms():
    data = request.json or {}
    sender = data.get("sender","").strip()
    content = data.get("content","").strip()
    if not sender or not content:
        return jsonify({"error":"Falta sender y content"}), 400
    # importa detector
    import sys
    sys.path.append("../scripts")
    from smishing_detector import audit_sms as do_audit
    result = do_audit(sender, content)
    return jsonify(result)

if __name__=="__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)
