import json
import websocket

websocket.enableTrace(True)
ws = websocket.WebSocketApp('wss://api.coin.z.com/ws/private/v1/ljWrsReEunBn_NBMI9wq8NJvPhIgPNBBB8P9_X4JhF38Y4LmpXMNVfXovJbo')

def on_open(self):
    message = {
        "command": "subscribe",
        "channel": "executionEvents"
    }
    ws.send(json.dumps(message))

def on_message(self, message):
    print(message)

ws.on_open = on_open
ws.on_message = on_message

ws.run_forever()