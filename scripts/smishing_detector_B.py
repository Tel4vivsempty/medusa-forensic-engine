
import re, hashlib, datetime, pathlib

AUTHOR = "T31425a9"
FULL_HASH = "T31425a92a75d9ebf5c217468ef295460b9f6266ce7e41ed33567d2c264caf"
import json, pathlib
FICHA_PATH = pathlib.Path("../knowledge/ficha_conocimiento_pila.json")
try:
    FICHA = json.loads(FICHA_PATH.read_text())
except:
    FICHA = {"pila_datos":{"personas_morales_oficiales":[]}}

# Links que no tienen http/https - tipicos de smishing
LINK_PATTERNS = [
    r'https?://[^\s]+',
    r'hxxps?://[^\s]+',
    r'www\.[^\s]+',
    r'(?:bit\.ly|tinyurl\.com|t\.me|goo\.gl|is\.gd|ow\.ly)/[^\s]+',
    r'[a-zA-Z0-9.-]+\.(?:com|mx|net|io|info|online|site|top|xyz|link|bank|secure)[^\s]*/[^\s]*',
    r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(?::\d+)?/[^\s]*',
    r'[a-zA-Z0-9-]+\.(?:com|mx|net|io)/[a-zA-Z0-9/_-]+'
]

URGENCY_KEYWORDS = ["bloqueado","verifica","urgente","suspendida","actualiza","clic","click","ingresa","inmediato","banco","BBVA","Santander","Banamex","HSBC"]

def extract_links(text):
    links=[]
    for pat in LINK_PATTERNS:
        for m in re.findall(pat, text, re.I):
            # limpia puntuacion final
            m = m.rstrip('.,);!\'"')
            if len(m)>4:
                links.append(m)
    # deduplica manteniendo orden
    seen=set()
    uniq=[]
    for l in links:
        if l.lower() not in seen:
            seen.add(l.lower())
            uniq.append(l)
    return uniq

def has_http(link):
    return link.lower().startswith(('http://','https://','hxxp://','hxxps://'))

def audit_sms(sender, content):
    links = extract_links(content)
    findings=[]
    risk_score=0

    # 0. Correlacion con ficha de conocimiento pila
    ficha_match = None
    for pm in FICHA.get("pila_datos",{}).get("personas_morales_oficiales",[]):
        if pm["nombre"].lower() in sender.lower() or sender.lower() in [s.lower() for s in pm.get("senders_oficiales",[])]:
            ficha_match = pm
            break
    if ficha_match:
        findings.append(f"CORRELACION_FICHA: Sender coincide con persona moral oficial {ficha_match['nombre']} - dominios oficiales {ficha_match.get('dominios_oficiales',[])}")
        # verifica si links usan dominio no oficial
        for link in links:
            if not any(dom in link.lower() for dom in ficha_match.get("dominios_oficiales",[])):
                if "." in link:
                    findings.append(f"TYPO_POSIBLE: Link {link} no usa dominio oficial de {ficha_match['nombre']}")
                    risk_score+=2
    
    # 1. Sender
    if sender:
        if re.match(r'^\+?\d{7,15}$', sender.replace(' ','')):
            findings.append(f"SENDER_NUMERICO: {sender} - posible spoof de persona moral")
            risk_score+=1
        if len(sender)<=6 and sender.isdigit():
            findings.append(f"SENDER_CORTO: {sender} - tipico de SMS corto smishing")
            risk_score+=2

    # 2. Links
    for link in links:
        if not has_http(link):
            findings.append(f"LINK_SIN_HTTP_HTTPS: {link} - alto riesgo smishing, no tiene esquema")
            risk_score+=3
        if re.search(r'bit\.ly|tinyurl|is\.gd|ow\.ly', link, re.I):
            findings.append(f"LINK_ACORTADO: {link} - oculta destino real")
            risk_score+=3
        if re.match(r'^\d+\.\d+\.\d+\.\d+', link):
            findings.append(f"LINK_IP: {link} - smishing usa IP directa")
            risk_score+=4

    # 3. Urgencia
    for kw in URGENCY_KEYWORDS:
        if kw.lower() in content.lower():
            findings.append(f"KEYWORD_URGENCIA: {kw}")
            risk_score+=1

    # Veredicto
    if risk_score>=6:
        veredicto="SMISHING_PROBABLE - NO RESPONDER"
        recomendacion="No abras links, verifica directo con la persona moral por app oficial o telefono oficial. Sella este evento."
    elif risk_score>=3:
        veredicto="SOSPECHOSO - VERIFICAR"
        recomendacion="No respondas aun. Llama al numero oficial de la persona moral, no al del SMS."
    else:
        veredicto="PROBABLEMENTE_LEGITIMO - VERIFICAR_DE_TODOS_MODOS"
        recomendacion="Aun asi verifica en canal oficial antes de dar datos."

    # Sellado Vault con hash autoritario
    vault_dir = pathlib.Path("../.sys_core_vault")
    vault_dir.mkdir(exist_ok=True)
    payload = f"{sender}|{content}|{risk_score}|{datetime.datetime.now().isoformat()}|{FULL_HASH}"
    sha = hashlib.sha256(payload.encode()).hexdigest()
    (vault_dir / f"{sha}.sha256").write_text(f"{sha} {sender} {risk_score} {veredicto} {FULL_HASH}")

    return {
        "sender": sender,
        "links_detectados": links,
        "findings": findings,
        "risk_score": risk_score,
        "veredicto": veredicto,
        "recomendacion": recomendacion,
        "vault_hash": sha,
        "author_hash": AUTHOR,
        "full_hash": FULL_HASH,
        "sellado": True
    }
