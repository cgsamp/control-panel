import network
import json
import time
from common import helps

def connect():
    config = helps.get_config('wifi')

    
    preferred_ssid = config["networks"][0]["ssid"]
    preferred_ssid_passwd = config["networks"][0]["passwd"]

    helps.log(helps.LOG_DEBUG,f'ssid={preferred_ssid} password_length={len(preferred_ssid_passwd)}')
                                                    
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    networks = wlan.scan()

    found_ssid = False
    for network_config in networks:
        ssid = network_config[0].decode()
        if ssid == preferred_ssid:
            found_ssid = True

    helps.log(helps.LOG_DEBUG,f'Found network {preferred_ssid}: {found_ssid}')

    wlan.connect(preferred_ssid,preferred_ssid_passwd)

    connection_timeout = 10
    while connection_timeout > 0:
        if wlan.status() >= 3:
            break
        connection_timeout -= 1
        helps.log(helps.LOG_DEBUG,'Waiting for Wi-Fi connection...')
        time.sleep(1)
        

    if wlan.status() != 3:
        raise RuntimeError('Failed to establish a network connection')
    else:
        helps.log(helps.LOG_DEBUG,'Connection successful!')
        network_info = wlan.ifconfig()
        helps.log(helps.LOG_DEBUG,f'IP address: {network_info[0]}')

    

