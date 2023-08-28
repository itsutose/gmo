import json
import websocket
import trading_history
from datetime import datetime, timedelta
import threading
import signal
import sys
import os

def start_websocket(drive_letter):


    def on_open(ws):
        message = {
            "command": "subscribe",
            "channel": "trades",
            "symbol": "BTC"
        }
        ws.send(json.dumps(message))

    id_num = [1]  # mutable object

    def on_message(ws, message):

        # 日にちを取得
        date = datetime.now().strftime("%Y-%m-%d")

        # 累計用
        trading_hist_path = f'sqlite:////workspace/gmo_data/trading_hist/trading_hist.db'
        # 日にち用
        trading_hist_date_path = f'sqlite:////workspace/gmo_data/trading_hist/'+date+'_trading_hist.db'
        trading_hist_date_path = f'sqlite:///C:/Users/yamaguchi/MyDocument/gmo_data/trading_hist/'+date+'_trading_hist.db'

        file_path = trading_hist_date_path

        if id_num[0] % 2 != 0:
            print("===============  trading history ===")
            content = json.loads(message)
            print(content)
            timestamp_str = content['timestamp']
            timestamp = datetime.fromisoformat(timestamp_str[:-1])
            new_timestamp = timestamp + timedelta(hours=9)
            content['timestamp'] = new_timestamp

            trading_history.TradingHist_Save2SQL(content, file_path)

        id_num[0] += 1

    def on_close(ws):
        print("WebSocket connection closed : Trading History")

    # websocket.enableTrace(True)
    ws = websocket.WebSocketApp('wss://api.coin.z.com/ws/public/v1',
                                on_open=on_open,
                                on_message=on_message,
                                on_close=on_close)

    def run_websocket():
        ws.run_forever()

    thread = threading.Thread(target=run_websocket)
    thread.start()

    return ws, thread

def handle_signal(signal, frame):
    print("Interrupt received, closing WebSocket connection...")
    ws.close()
    sys.exit(0)

if __name__ == '__main__':

    current_path = os.path.abspath(__file__)
    drive_letter = os.path.splitdrive(current_path)[0]

    

    ws, ws_thread = start_websocket(drive_letter)

    # Ctrl+Cシグナルをハンドルする
    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    while True:
        # メインスレッドをブロックしないために無限ループで待機
        pass
