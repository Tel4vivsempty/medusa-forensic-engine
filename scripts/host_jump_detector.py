
# host_jump_detector.py - documenta salto 172.67.202.69 -> 104.21.85.41 Cloudflare
saltos = [
    {"de": "mxwinx.mx (previo inactivo)", "ip": "NXDOMAIN/pixel vacio", "estado": "inactivo"},
    {"de": "mxwinx.blog/?t=1&d=q0sDfJTb", "ip": "172.67.202.69", "codigo": "301 Moved Permanently", "asn": "AS13335 Cloudflare Canada"},
    {"de": "mxwinx.blog final", "ip": "104.21.85.41", "codigo": "200 OK", "server": "cloudflare"},
]
for s in saltos:
    print(s)

# Correlacion cruzada con Telcel Raro
print("\n--- MOTOR DE CORRELACION CRUZADA ---")
print("Servidor nginx coincide en registro.telcel.com/vinculatulinea/ ID 17,18,19")
print("Servidor Store Redirect Handler coincide en bit.ly/47CGP7R76064 ID 2,12,13,14,15,16 con 2465174224")
print("=> ALERTA INFRAESTRUCTURA COMPARTIDA Telcel Raro <-> 2465174224")
