import paho.mqtt.client as mqtt
import json
import time
import requests
import sys
import yaml

def configure(params):
    for param, name, device_class, unit_of_measurement, extra in params:
        data = {
            'availability': [{'topic': f'{topic}/bridge/state'}],
            'device': {
                'identifiers': [f'{topic}_{did}'],
                'manufacturer': "ZEVER",
                'model': 'COM',
                'name': 'ZEVER COM'
            },
            'entity_category': 'diagnostic',
            'icon': 'mdi:solar-power-variant',
            'json_attributes_topic': f'{topic}/{did}',
            'name': f'ZEVERCOM {name}',
            'state_topic': f'{topic}/{did}',
            'unique_id': f'{topic}_{did}_{param}',
            'value_template': f"{{{{ value_json['update']['{param}'] }}}}"
        }
        if device_class:
            data['device_class'] = device_class
        if unit_of_measurement:
            data['unit_of_measurement'] = unit_of_measurement
        if extra:
            data.update(extra)
        payload = json.dumps(data)
        print(f"homeassistant/sensor/{did}/{param}/config", payload)
        mqttc.publish(f"homeassistant/sensor/{did}/{param}/config", payload)

def get_data(ip):
    data = {}
    try:
        response = requests.get(f"http://{ip}/home.cgi")
        lines = response.text.split('\n')
        inv_count = int(lines[8])
        data['status'] = 'available' if (int(lines[7]) == 0) else 'unavailable'
        plus = 8
        if inv_count:
            data['inv_pac'] = lines[8+2].strip()
            data['e_today'] = lines[8+3].strip()
            plus = plus + 4 * inv_count
        else:
            data['inv_pac'] = 0
        data['line_pac'] = lines[plus+2].strip()
        data['line_e_in'] = lines[plus+3].strip()
        data['line_e_out'] = lines[plus+4].strip()

        return data

    except Exception as e:
        return {'status': 'unavailable', 'error': str(e)}


def set_state(state):
    print(f"{topic}/bridge/state", state)
    mqttc.publish(f"{topic}/bridge/state", state)

###

conf = None
with open("/etc/zevercom.conf", 'r') as f:
    conf = yaml.safe_load(f)

topic = conf.get('topic', 'zevercom')
did = conf.get('device_id', '0xdeadbeef00000001')
zevercom_ip = conf.get('zevercom_ip', '172.17.0.192')

mqttc = mqtt.Client()
mqttc.connect(conf.get('mqtt_server', 'mqtt'))

configure([
    ['status', 'Status', None, None, None],
    ['inv_pac', 'Inverter PAC', 'power', 'W', None],
    ['e_today', 'Energy (Today)', 'energy', 'kWh', {'state_class': 'total_increasing'}],
    ['line_pac', 'Line PAC', 'power', 'W', None],
    ['line_e_in', 'Line Energy Imported', 'energy', 'kWh', {'state_class': 'total_increasing'}],
    ['line_e_out', 'Line Energy Exported', 'energy', 'kWh', {'state_class': 'total_increasing'}],
])
time.sleep(2)

set_state('online')

while True:
    try:
        data = get_data(zevercom_ip)
        payload = json.dumps({'update': data})
        print(f"{topic}/{did}", payload)
        mqttc.publish(f"{topic}/{did}", payload)
        time.sleep(59)
    except Exception as e:
        set_state('offline')
        break

set_state('offline')
