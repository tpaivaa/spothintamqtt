# spothintamqtt
Get spot-hinta from API and publish to MQTT

# .env example

MQTT=x.x.x.x
MQTT_PORT=1883
MQTT_TOPIC_NOW=topic/here
MQTT_USER=mqttUser
MQTT_PASSWORD=Password


# How to get started
git clone repo:
git clone git@github.com:tpaivaa/spothintamqtt.git

create virtual environment:
cd ./spothintamqtt
python3 -m venv
source ./venv/bin/activate

install requirements with pip:

pip install -r requirements.txt

set systemd service up and running

