#!/usr/bin/env python3
import ssl, socket, pathlib, json, datetime
from cryptography import x509
from cryptography.hazmat.backends import default_backend

TARGETS = ["mxwinx.mx", "betmexico.mx"]
print("[*] Iniciando sondeo criptografico de infraestructura cruzada...")

resultados = []
for host in TARGETS:
    print(f"[*] [MEDUSA-SSL] Extrayendo certificado TLS/SSL para: {host}")
    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=host) as s:
            s.settimeout(5)
            s.connect((host, 443))
            cert_bin = s.getpeercert(binary_form=True)
            cert = x509.load_der_x509_certificate(cert_bin, default_backend())
            issuer = cert.issuer.rfc4514_string()
            subject = cert.subject.rfc4514_string()
            san = [x.value for x in cert.extensions.get_extension_for_class(x509.SubjectAlternativeName).value] if cert.extensions else []
            print(f"  -> Emisor (Issuer): {issuer}")
            print(f"  -> Sujeto (Subject): {subject}")
            print(f"  -> Dominios SAN: {san}")
            resultados.append({"host":host, "issuer":issuer, "subject":subject, "san":san, "timestamp":datetime.datetime.now().isoformat()})
            print(f"[+] Certificado de '{host}' cifrado y almacenado en la base de datos de Medusa.")
    except Exception as e:
        print(f"[-] Error {host}: {e}")
        resultados.append({"host":host, "error":str(e)})

pathlib.Path("database/ssl_audit.json").write_text(json.dumps(resultados, indent=2))
print("-"*60)
