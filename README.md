[Deprecated] Use YoLink API V2: https://github.com/Tonio101/YoLinkAPI_V2

# YoLinkHome

Simple script that will send a broadcast message to your Google device(s)<br/>
whenever a door opens (or mailbox).

If you are only interested in integrating with YoLink products via the <br/>
MQTT protocol, you can skip the setup for Assistant Relay and go to <br/>
[YoLink Integration](#yolink-integration) steps.

## Parts Needed
 - Raspberry Pi (any model should sufficie)
 - [YoLink Hub + Door Sensors](https://www.amazon.com/gp/product/B084X9D9HY/ref=ppx_yo_dt_b_asin_title_o04_s00?ie=UTF8&psc=1)
 - [YoLink Garage Door Sensor](https://www.amazon.com/gp/product/B07Z7QQV8K/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1)

## Prereqs

Follow the steps [here](https://assistantrelay.com/docs/getting-started/installation) to install and configure Assistant Relay.<br/>
This will essentially configure the Raspberry Pi as anther Google device in<br/>
order to broadcast messages to other Google devices in your network.

[YoLink API Documentation](http://www.yosmart.com/doc/lorahomeapi/#/YLAS/?id=quickstart)

As mentioned in the API documentation wiki, contact Chi Yao (yaochi@yosmart.com)<br/>
to request your YoLink account API keys.

KEEP YOUR YOLINK ACCOUNT API KEYS SECURED!

Ensure you have the following information:
Required YoLink Account API Keys:
 - CSID 
 - CSName
 - CSSecKey
 - SVR_URL

Using a QR Code Scanner, gather all the IoT device(s) serial number (32 char code).<br/>
List them somewhere as they will be required to enable the API for each device.

## Testing Google Assistant Relay

I'm assuming that at this point you have carefully followed the steps mentioned<br/>
above to configure Assistant Relay on the Raspberry Pi.

On your Raspberry Pi run the `google_assistant_relay_test.py` script to ensure<br/>
that Assistant Relay is working.

```bash
/usr/bin/python3 tests/google_assistant_relay_test.py --url http://192.168.1.199:3000/assistant --user bob
```

## YoLink Integration

[YoLink API Documentation](http://www.yosmart.com/doc/lorahomeapi/#/YLAS/?id=quickstart)<br/>
YoLink supports both HTTP callback API (webhook) or MQTT report topic.

This script will go over subscribing to the YoLink MQTT broker topic to receive<br/>
sensor events such as open/close. It will broadcast a message to your Google<br/>
devices whenever a door is opened

Install python required modules:
```bash
/usr/bin/python3 -m pip install -r requirements.txt
```

Add the IoT device(s) serial number to `yolink_data.yml`.

Execute the python script providing your YoLink account API keys:

```bash
* Note: For mqtt_url arg, discard the "https://" in {SVR_URL}

/usr/bin/python3 src/yolink.py --url {SVR_URL}/openApi \
                               --mqtt_url {SVR_URL} \
                               --mqtt_port 8003 \
                               --csid {CSID} \
                               --csseckey {CSSecKey} \
                               --topic {CSName}/report \
                               --file src/yolink_data.yml
```

Populate the yolink credentials in `start_yolinkhome.sh`.<br/>
Then simply execute the script.

## YoLink Cron Job

Add a cron job to start the process on startup.<br/>
Use `start_yolinkhome.sh` for the cron job entry.
Or even better, create a systemd service.

## YoLink Systemd Service

[systemd service documentation](https://www.raspberrypi.org/documentation/linux/usage/systemd.md)

Modify the `yolinkhome.service` file.<br/>

Copy this file into `/etc/systemd/system` as root.<br/>

```bash
sudo cp yolinkhome.service /etc/systemd/system/yolinkhome.service
```

Inform `systemd` about the new service.<br/>

```bash
sudo systemctl daemon-reload
```

Start the service.<br/>

```bash
sudo systemctl start yolinkhome.service
```

When you are happy with the results, enable the service.<br/>
It should now start automatically at startup.

```bash
sudo systemctl enable
```
