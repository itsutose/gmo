import json
import websocket
from pprint import pprint

websocket.enableTrace(True)
ws = websocket.WebSocketApp('wss://api.coin.z.com/ws/public/v1')

def on_open(self):
    message = {
        "command": "subscribe",
        "channel": "orderbooks",
        "symbol": "BTC"
    }
    ws.send(json.dumps(message))

def on_message(self, message):
    pprint(json.loads(message))



ws.on_open = on_open
ws.on_message = on_message

ws.run_forever()

