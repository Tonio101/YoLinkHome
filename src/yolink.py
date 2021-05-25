#!/usr/bin/env python3

import argparse
import sys
import yaml

from assistant_relay_client import AssistantRelayClient
from logger import getLogger
from yolink_devices import YoLinkDevice
from yolink_mqtt_client import YoLinkMQTTClient
log = getLogger(__name__)

ASSISTANT_RELAY_URL = 'http://192.168.1.199:3000/assistant'

def main(argv):

    usage = ("{FILE} "
            "--url <API_URL> "
            "--csid <ID> "
            "--csseckey <SECKEY> "
            "--mqtt_url <MQTT_URL> "
            "--mqtt_port <MQTT_PORT> "
            "--topic <MQTT_TOPIC> "
            "--file <DATA_FILE>").format(FILE=__file__)

    description = 'Enable Sensor APIs and subscribe to MQTT broker'

    parser = argparse.ArgumentParser(usage=usage, description=description)

    parser.add_argument("-u", "--url",       help="Device API URL",    required=True)
    parser.add_argument("-i", "--csid",      help="Unique Identifier", required=True)
    parser.add_argument("-k", "--csseckey",  help="Security Key",      required=True)
    parser.add_argument("-m", "--mqtt_url",  help="MQTT Server URL",   required=True)
    parser.add_argument("-p", "--mqtt_port", help="MQTT Server Port",  required=True)
    parser.add_argument("-t", "--topic",     help="Broker Topic",      required=True)
    parser.add_argument("-f", "--file",      help="Data file",         required=True)

    args = parser.parse_args()
    log.debug("{0}\n".format(args))

    device_hash = {}
    list_of_devices = []

    with open(args.file, 'r') as fp:
        data = yaml.safe_load(fp)
        list_of_devices = data['device_parameters']

    for device in list_of_devices:
        yolink_device = YoLinkDevice(args.url, args.csid, args.csseckey,
                                     device['serial_number'])
        yolink_device.build_device_api_request_data()
        yolink_device.enable_device_api()
        yolink_device.set_type(device['type'])
        yolink_device.set_friendly_name(device['name'])

        if ('ignore' in device):
            yolink_device.set_ignore(ignore=device['ignore'])

        device_hash[yolink_device.get_id()] = yolink_device

    log.debug(device_hash)

    # Use the user name for Assistant Relay
    google_home_client = AssistantRelayClient(url=ASSISTANT_RELAY_URL)

    yolink_client = YoLinkMQTTClient(args.csid, args.csseckey,
            args.topic, args.mqtt_url, args.mqtt_port, device_hash,
            google_home_client)
    yolink_client.connect_to_broker()

if __name__ == '__main__':
    main(sys.argv)