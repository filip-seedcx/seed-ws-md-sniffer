#!/usr/bin/env python3
import json
import logging
import websocket
import requests

log = logging.getLogger('ws')
log.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s|%(levelname)s|%(message)s')
ch.setFormatter(formatter)
log.addHandler(ch)


def get_instruments(url):
    r = requests.get(url)
    j = r.json()

    instruments = []
    for o in j['message']:
        instruments.append(o["code"])

    return instruments


instruments_to_subscribe = get_instruments("https://api.seedcx.com/instruments")


def on_message(ws, message):
    log.info(message)


def on_error(ws, error):
    log.error(error)


def on_close(ws):
    log.warning("closed")


def on_pong(ws):
    log.info('pong')


def on_open(ws):
    for code in instruments_to_subscribe:
        req = {"messageType": "marketDataRequest", "payload": code}
        payload = json.dumps(req)
        log.info('sending: ' + payload)
        ws.send(payload)


def main():
    ws = websocket.WebSocketApp("wss://api.seedcx.com",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close,
                                on_pong=on_pong)
    ws.on_open = on_open
    ws.run_forever()


if __name__ == '__main__':
    main()
