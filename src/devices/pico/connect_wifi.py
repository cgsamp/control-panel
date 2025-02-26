import network
import json
import time

with open("config_connections_private.json") as f:
    config = json.load(f)["wifi"]

preferred_ssid = config["networks"][0]["ssid"]
preferred_ssid_passwd = config["networks"][0]["passwd"]

print(f'ssid={preferred_ssid} password_length={len(preferred_ssid_passwd)}')
                                                
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
networks = wlan.scan()

found_ssid = False
for network_config in networks:
    ssid = network_config[0].decode()
    print(f'{ssid}')
    if ssid == preferred_ssid:
        found_ssid = True

print(f'Found network {preferred_ssid}: {found_ssid}')

wlan.connect(preferred_ssid,preferred_ssid_passwd)

connection_timeout = 10
while connection_timeout > 0:
    if wlan.status() >= 3:
        break
    connection_timeout -= 1
    print('Waiting for Wi-Fi connection...')
    time.sleep(1)
    

if wlan.status() != 3:
    raise RuntimeError('Failed to establish a network connection')
else:
    print('Connection successful!')
    network_info = wlan.ifconfig()
    print('IP address:', network_info[0])

    
