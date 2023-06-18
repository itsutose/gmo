import json
import sys
import websocket
import _thread
import pprint

def on_open(self):
    message = {
        "command": "subscribe",
        "channel": "orderbooks",
        "symbol": "BTC"
    }
    ws.send(json.dumps(message))

    def run(*args):
        while(True):
            line = sys.stdin.readline()
            if line != '':
                print('closing...')
                ws.close()
    _thread.start_new_thread(run, ())

def on_message(self, message):
    # print(type(message)) # str
    pprint.pprint(json.loads(message))
    # print(message)


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp('wss://api.coin.z.com/ws/public/v1')
    ws.on_open = on_open
    ws.on_message = on_message
    ws.run_forever()
