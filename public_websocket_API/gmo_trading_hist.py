import json
import websocket

websocket.enableTrace(True)
ws = websocket.WebSocketApp('wss://api.coin.z.com/ws/public/v1')

def on_open(self):
    message = {
        "command": "subscribe",
        "channel": "trades",
        "symbol": "BTC"
    }
    ws.send(json.dumps(message))

def on_message(self, message):
    print("===============")
    # print(message)
    # print(type(message))

    content = json.loads(message)
    print(content)
    # print("===============")

ws.on_open = on_open
ws.on_message = on_message

ws.run_forever()