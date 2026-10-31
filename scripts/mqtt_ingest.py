
# MQTT ingest 1883 -> Vault
import paho.mqtt.client as mqtt, hashlib, pathlib, datetime
AUTHOR="T31425a9"

def on_message(client, userdata, msg):
    payload=msg.payload.decode(errors="ignore")
    sha=hashlib.sha256(payload.encode()).hexdigest()
    print(f"[MQTT {msg.topic}] {payload[:100]} -> {sha}")
    pathlib.Path("../.sys_core_vault").mkdir(exist_ok=True)
    open(f"../.sys_core_vault/{sha}.sha256","w").write(f"{sha} {msg.topic} {datetime.datetime.now().isoformat()}")
    # guarda en evidence
    pathlib.Path("../evidence").mkdir(exist_ok=True)
    open(f"../evidence/{sha}.json","w").write(payload)

client=mqtt.Client()
client.on_message=on_message
if __name__=="__main__":
    print("Conectando a localhost:1883")
    try:
        client.connect("localhost",1883,60)
        client.subscribe("medusa/#")
        client.loop_forever()
    except Exception as e:
        print(f"MQTT fallo (esperado en PRoot si no hay broker): {e}")
