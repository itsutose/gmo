import json
import websocket
import ratest_rate
from datetime import datetime, timedelta

file_path = 'sqlite:///I:/マイドライブ/pytest/virtual_currency/gmo/gmo_data/ratest_rate/ratest_rate.db'

websocket.enableTrace(True)
ws = websocket.WebSocketApp('wss://api.coin.z.com/ws/public/v1')


def on_open(self):
    message = {
        "command": "subscribe",
        "channel": "ticker",
        "symbol": "BTC"
    }
    ws.send(json.dumps(message))

def on_message(self, message):
    print("==================")
    content = json.loads(message)
    timestamp_str = content['timestamp']
    timestamp = datetime.fromisoformat(timestamp_str[:-1])
    new_timestamp = timestamp + timedelta(hours=9)
    content['timestamp'] = new_timestamp

    print(content) 
    print(file_path)
    ratest_rate.RatestRate_Save2SQL(content, file_path)

def run_ws(path):
    global file_path
    file_path = path
    ws.on_open = on_open
    ws.on_message = on_message

    ws.run_forever()

if __name__ == '__main__':

    date = datetime.now().strftime("%Y-%m-%d")

    ratest_rate_date = 'sqlite:///I:/マイドライブ/pytest/virtual_currency/gmo/gmo_data/ratest_rate/'+date+'_ratest_rate.db'

    run_ws(ratest_rate_date)