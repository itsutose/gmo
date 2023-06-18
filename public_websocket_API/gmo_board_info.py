import json
import websocket

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
    print(message)

ws.on_open = on_open
ws.on_message = on_message

ws.run_forever()

