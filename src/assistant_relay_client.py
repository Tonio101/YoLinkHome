import json
import requests

from logger import getLogger
log = getLogger(__name__)

"""
Object representatiaon for Google Assistant Relay Client
"""
class AssistantRelayClient(object):

    def __init__(self, url, user='YoLink'):
        self.url = url
        self.user = user

        self.header = {'Content-Type': 'application/json'}
        self.data = {'user': user,
                     'broadcast': False,
                     'command': ''}

    def send_message(self, message, broadcast=False):
        """
        Send a message to a particular device.
        """
        self.data['user'] = self.user
        self.data['broadcast'] = broadcast
        self.data['command'] = message

        log.info(self.data)
        response = requests.post(self.url, headers=self.header,
            data=json.dumps(self.data))
        log.info(response)

    def send_message_to_device(self, device_name, message):
        """
        Send a message to a particular device (check your Google Home app for the device name).
        """
        message = 'Hey Google, broadcast message to {device}, {msg}'.format(device=device_name, msg=message)
        self.send_message(message)

    def broadcast_to_all_devices(self, message):
        """
        Send a message to all devices.
        """
        message = 'Hey Google, broadcast message, {msg}'.format(msg=message)
        self.send_message(message, broadcast=True)