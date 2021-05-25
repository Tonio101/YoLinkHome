import hashlib
import time
import json
import requests
import sys

from logger import getLogger
log = getLogger(__name__)

"""
Object representatiaon for YoLink Device
"""
class YoLinkDevice(object):

    def __init__(self, url, csid, csseckey, serial_number):
        self.url = url
        self.csid = csid
        self.csseckey = csseckey
        self.serial_number = serial_number
        self.friendly_name = 'Unknown'
        self.ignore = False

        self.data = {}
        self.header = {}

        self.device_data = {}

    def set_friendly_name(self, name):
        self.friendly_name = name

    def get_friendly_name(self):
        return str(self.friendly_name)

    def set_type(self, type):
        self.type = type

    def get_type(self):
        return str(self.type)

    def set_ignore(self, ignore=True):
        self.ignore = ignore

    def get_ignore(self):
        return self.ignore

    def get_google_home_message(self):
        if ('mailbox_sensor' in self.type):
            return 'You\'ve got mail!'
        
        return '{0} open'.format(self.friendly_name)

    def get_name(self):
        return str(self.device_data['name'])

    def get_sensor_type(self):
        return str(self.device_data['type'])

    def get_id(self):
        return str(self.device_data['deviceId'])

    def get_uuid(self):
        return str(self.device_data['deviceUDID'])

    def get_token(self):
        return str(self.device_data['token'])

    def build_device_api_request_data(self):
        """
        Build header + payload to enable sensor API
        """
        self.data["method"] = 'Manage.addYoLinkDevice'
        self.data["time"] = str(int(time.time()))
        self.data["params"] = {'sn': self.serial_number}

        self.header['Content-type'] = 'application/json'
        self.header['ktt-ys-brand'] = 'yolink'
        self.header['YS-CSID'] = self.csid

        # MD5(data + csseckey)
        self.header['ys-sec'] = str(hashlib.md5((json.dumps(self.data) +
            self.csseckey).encode('utf-8')).hexdigest())

        log.debug("Header:{0} Data:{1}\n".format(self.header, self.data))

    def enable_device_api(self):
        """
        Send request to enable the device API
        """
        response = requests.post(self.url, data=json.dumps(self.data), headers=self.header)
        log.debug(response.status_code)

        response = json.loads(response.text)
        log.debug(response)

        self.device_data = response['data']

        if (response['code'] == '000000'):
            log.info("Successfully enabled device API")

            log.info("Name:{0} DeviceId:{1}".format(
                self.device_data['name'],
                self.device_data['deviceId']))
            
        else:
            log.info("Failed to enable API response!")
            log.info(response)
            log.info(self.data)
            sys.exit(2)
