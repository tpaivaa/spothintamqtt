import random
import time
import os
import asyncio
import syslog as l
import requests
from paho.mqtt import client as mqtt_client
from dotenv import load_dotenv
load_dotenv()

broker = os.getenv("MQTT")
port = os.getenv("MQTT_PORT")
topic = os.getenv("MQTT_TOPIC_NOW")
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 99999)}'
mqtt_username = os.getenv("MQTT_USER")
mqtt_password = os.getenv("MQTT_PASSWORD")

def on_disconnect(client, userdata, rc):
   l.syslog(f"MQTT client disconnected ok, rc: `{rc}`")

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            l.syslog("Connected to MQTT Broker!")
        else:
            l.syslog("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(mqtt_username, mqtt_password)
    client.on_connect = on_connect
    client.connect(broker, int(port))
    return client


def publish(client, message):
    result = client.publish(topic, message)
    status = result[0]
    if status == 0:
        l.syslog(f"Send `{message}` to topic `{topic}`")
    else:
        l.syslog(f"Failed to send `{message}` to topic `{topic}`")
    msg_count += 1

async def getspotdata(service):
  URL = f"https://api.spot-hinta.fi/{service}"
  l.syslog(f"Querying API `{URL}`")
  r = requests.get(URL)
  l.syslog(f"`{r.json()}`")
  return r.json()

async def run():
    l.syslog('Started')
    client = connect_mqtt()
    client.on_disconnect = on_disconnect
    spothintaJustNow = await getspotdata('JustNow')
    publish(client, spothintaJustNow)
    l.syslog('Stopping')
    client.disconnect()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())