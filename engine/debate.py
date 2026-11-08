# MEDUSA - Debate de Verdad / Condicional de Operabilidad
# Cada variante es una hipótesis. Ninguna tiene la razón sola.
# Solo gana la que tiene evidencia + hash.

import hashlib, json, time

def hash_evidencia(data: dict) -> str:
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()

def debatir(variantes: list) -> dict:
    """
    variantes = [
      {"nombre": "A_strict", "veredicto": "smishing", "confianza": 0.92, "evidencia": {...}},
      {"nombre": "B_permissive", "veredicto": "limpio", "confianza": 0.61, "evidencia": {...}},
      {"nombre": "C_offline", "veredicto": "smishing", "confianza": 0.85, "evidencia": {...}},
    ]
    """
    # 1. Cada variante sella su evidencia
    for v in variantes:
        v["hash"] = hash_evidencia(v["evidencia"])
        v["timestamp"] = time.time()

    # 2. Votación por confianza ponderada
    votos = {}
    for v in variantes:
        votos[v["veredicto"]] = votos.get(v["veredicto"], 0) + v["confianza"]

    ganador = max(votos, key=votos.get)
    total = sum(votos.values())
    consenso = votos[ganador] / total if total else 0

    # 3. Condicional de operabilidad
    if consenso >= 0.66:
        estado = "ACEPTADO - 2/3 o más coinciden"
        accion = "ejecutar"
    elif consenso >= 0.50:
        estado = "DUDA - va a Vault para revisión humana"
        accion = "vault + humano"
    else:
        estado = "CONFLICTO TOTAL - no ejecutar, solo registrar"
        accion = "bloquear"

    return {
        "ganador": ganador,
        "consenso": round(consenso, 3),
        "estado": estado,
        "accion": accion,
        "votos": votos,
        "variantes": variantes,
        "aprendizaje": "Cada variante aprende del hash de la otra. La próxima vez ajusta su confianza."
    }

if __name__ == "__main__":
    ejemplo = [
        {"nombre": "A_strict", "veredicto": "smishing", "confianza": 0.92, "evidencia": {"sender": "x", "link_sin_http": True}},
        {"nombre": "B_permissive", "veredicto": "limpio", "confianza": 0.61, "evidencia": {"sender": "x", "link_sin_http": False}},
        {"nombre": "C_offline", "veredicto": "smishing", "confianza": 0.85, "evidencia": {"sender": "x", "link_sin_http": True}},
    ]
    print(json.dumps(debatir(ejemplo), indent=2, ensure_ascii=False))
