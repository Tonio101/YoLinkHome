import sys
import yaml

from assistant_relay_client import AssistantRelayClient
from logger import getLogger
log = getLogger(__name__)

def test_assistant_relay_client():
    url = 'http://192.168.1.199:3000/assistant'
    assistant_relay_client = AssistantRelayClient(url, user='Blah')
    print(assistant_relay_client.send_message_to_device("Kitchen display", "Test"))

def test_yolink_data_file():
    list_of_devices = []
    with open('../src/yolink_data.yml', 'r') as fp:
        data = yaml.safe_load(fp)
        list_of_devices = data['device_parameters']

    for device in list_of_devices:
        print(device)

def main(argv):
    test_assistant_relay_client()
    test_yolink_data_file()

if __name__ == '__main__':
    main(sys.argv)