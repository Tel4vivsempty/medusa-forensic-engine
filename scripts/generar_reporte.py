
import datetime, timezone
def generar_reporte_profeco():
    ahora_utc = datetime.datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    reporte_contenido = open("/mnt/data/medusa-forensic-engine/expediente_auditoria_pericial_profeco.txt", "r", encoding="utf-8").read()
    reporte_contenido = reporte_contenido.replace("{{ahora_utc}}", ahora_utc)
    archivo_salida = "expediente_auditoria_pericial_profeco.txt"
    with open(archivo_salida, "w", encoding="utf-8") as f:
        f.write(reporte_contenido)
    print(f"[+] Expediente maestro integrado y generado con exito - T31425a9")

if __name__ == "__main__":
    generar_reporte_profeco()
