import json
import websocket
import trading_history
from datetime import datetime, timedelta

websocket.enableTrace(True)
ws = websocket.WebSocketApp('wss://api.coin.z.com/ws/public/v1')

def on_open(self):
    message = {
        "command": "subscribe",
        "channel": "trades",
        "symbol": "BTC"
    }
    ws.send(json.dumps(message))

id_num = 1

def on_message(self, message):
    global id_num
    
    if id_num % 2 != 0:
        print("===============")
        content = json.loads(message)
        timestamp_str = content['timestamp']
        timestamp = datetime.fromisoformat(timestamp_str[:-1])
        new_timestamp = timestamp + timedelta(hours=9)
        content['timestamp'] = new_timestamp

        print(content)
        trading_history.TradingHist_Save2SQL(content)

    id_num += 1

ws.on_open = on_open
ws.on_message = on_message

ws.run_forever()