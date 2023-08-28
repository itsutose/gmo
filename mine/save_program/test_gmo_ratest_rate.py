import json
import websocket
import ratest_rate
from datetime import datetime, timedelta
import threading
import signal
import sys
import os

def start_websocket(drive_letter):

    # print(drive_letter)
    
    def on_open(self):
        message = {
            "command": "subscribe",
            "channel": "ticker",
            "symbol": "BTC"
        }
        ws.send(json.dumps(message))

    def on_message(self, message):

        print("==================  ratest rate ===")
        
        # 日にちを取得
        date = datetime.now().strftime("%Y-%m-%d")

        # 累計用
        ratest_rate_path = f'sqlite:////workspace/gmo_data/ratest_rate/ratest_rate.db'
        # 日にち用
        ratest_rate_date_path = f'sqlite:////workspace/gmo_data/ratest_rate/'+date+'_ratest_rate.db'
        ratest_rate_date_path = f'sqlite:///C:/Users/yamaguchi/MyDocument/gmo_data/ratest_rate/'+date+'_ratest_rate.db'

        file_path = ratest_rate_date_path
        
        content = json.loads(message)
        # print(content)
        timestamp_str = content['timestamp']
        timestamp = datetime.fromisoformat(timestamp_str[:-1])
        new_timestamp = timestamp + timedelta(hours=9)
        content['timestamp'] = new_timestamp

        print(content)
        # print(file_path)
    
        ratest_rate.RatestRate_Save2SQL(content, file_path)

    def on_close(ws):
        print("WebSocket connection closed : Ratest Rate")

    # websocket.enableTrace(True)
    ws = websocket.WebSocketApp('wss://api.coin.z.com/ws/public/v1',
                                on_open = on_open,
                                on_message = on_message,
                                on_close=on_close
                                )

    def run_websocket():
        ws.run_forever()

    thread = threading.Thread(target=ws.run_forever)
    thread.start()

    return ws, thread

def handle_signal(signal, frame):
    print("Interrupt received, closing WebSocket connection...")
    ws.close()
    sys.exit(0)


if __name__ == '__main__':
    
    # googleドライブが A‐Zドライブの頭文字を取得
    current_path = os.path.abspath(__file__)
    drive_letter = os.path.splitdrive(current_path)[0]

    ws, ws_thread = start_websocket(drive_letter)

    # Ctrl+Cシグナルをハンドルする
    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    while True:
        # メインスレッドをブロックしないために無限ループで待機
        pass

