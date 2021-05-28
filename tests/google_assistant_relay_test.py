#!/usr/bin/env python3

import argparse
import sys

from assistant_relay_client import AssistantRelayClient

def main(argv):
    usage = ("{FILE} "
            "--url http://192.168.1.199:3000/assistant "
            "--user charlie").format(FILE=__file__)

    description = 'Test Google Assistant Relay'

    parser = argparse.ArgumentParser(usage=usage, description=description)

    parser.add_argument("-u", "--url",  help="Assistant Relay URL",  required=True)
    parser.add_argument("-n", "--user", help="Assistant Relay User", required=True)

    args = parser.parse_args()

    google_home_client = AssistantRelayClient(url=args.url, user=args.user)
    google_home_client.broadcast_to_all_devices("This is a test")

if __name__ == '__main__':
    main(sys.argv)