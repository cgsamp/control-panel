import json
import time
import machine

LOG_DEBUG = 10
LOG_INFO = 5
LOG_FATAL = 0
logConsole = True
logFile = False

def ts_formatted():
    t = time.localtime()
    timestamp = "{:04}-{:02}-{:02};{:02}:{:02}:{:02}.{:06}".format(
        t[0], t[1], t[2], t[3], t[4], t[5], int(time.ticks_ms())
    )
    return timestamp

def ts_micros():
    t = time.time() * 10**6 + int(time.ticks_ms)
    return t

def set_time():
    pass

def get_machine_id():
    return str(machine.unique_id().hex())


def get_config(domain):
    log(LOG_DEBUG,f'Getting config for domain {domain}')
    config = {}
    if domain in ('wifi','mqtt'):
        with open("common/config_connections_private.json") as f:
            config = json.load(f)[domain]

    if domain in ('control_panel'):
        with open("control_panel.json") as f:
            config = json.load(f)

    return config

def log(log_level, message):
    log_line = f'{ts_formatted()} | {log_level} | {get_machine_id()} | {message}'
    if logConsole:
        print(log_line)
    if logFile:
        with open("pico.log","a"):
            f.write(log_line+'\n')
