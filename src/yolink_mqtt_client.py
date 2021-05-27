import hashlib
import json
import os
import sys

import paho.mqtt.client as mqtt
from logger import getLogger
log = getLogger(__name__)

"""
Object representation for YoLink MQTT Client
"""
class YoLinkMQTTClient(object):

    def __init__(self, csid, csseckey, topic, mqtt_url, mqtt_port, device_hash,
                 google_home_client, client_id=os.getpid()): 
        self.csid = csid
        self.csseckey = csseckey
        self.topic = topic
        self.mqtt_url = mqtt_url
        self.mqtt_port = int(mqtt_port)
        self.device_hash = device_hash
        self.google_home_client = google_home_client

        self.client = mqtt.Client(client_id=str(__name__ + str(client_id)),
                clean_session=True, userdata=None,
                protocol=mqtt.MQTTv311, transport="tcp")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        #self.client.tls_set()

    def connect_to_broker(self):
        """
        Connect to MQTT broker
        """
        log.info("Connecting to broker...")

        log.debug(hashlib.md5(self.csseckey.encode('utf-8')).hexdigest())
        self.client.username_pw_set(username=self.csid,
                password=hashlib.md5(self.csseckey.encode('utf-8')).hexdigest())

        self.client.connect(self.mqtt_url, self.mqtt_port, 10)
        self.client.loop_forever()

    def on_message(self, client, userdata, msg):
        """
        Callback for broker published events
        """
        log.debug(msg.topic, msg.payload)

        try:
            payload = json.loads(msg.payload.decode("utf-8"))
            log.debug(payload)

            event = payload['event']
            deviceId = payload['deviceId']
            state = payload['data']['state']
            device = self.device_hash[deviceId]

            log.info("Event:{0} Device:{1} State:{2}".format(event,
                device.get_name(), state))

            if ('open' in state and not device.get_ignore()):
                self.google_home_client.send_message_to_device(device_name="Kitchen display",
                    message=device.get_google_home_message())
        except:
            error = sys.exc_info()[0]
            log.info("Error reading payload: %s" % error)

    def on_connect(self, client, userdata, flags, rc):
        """
        Callback for connection to broker
        """
        log.info("Connected with result code %s" % rc)

        if (rc == 0):
            log.info("Successfully connected to broker %s" % self.mqtt_url)
        else:
            log.info("Connection with result code %s" % rc);
            sys.exit(2)
    
        self.client.subscribe(self.topic)
