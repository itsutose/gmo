import json
import time
import websocket
import ratest_rate
from datetime import datetime, timedelta
import threading
import signal
import sys
import os


def start_websocket(folder_path):

    def on_open(ws):
        message = {
            "command": "subscribe",
            "channel": "ticker",
            "symbol": "BTC"
        }
        ws.send(json.dumps(message))

    def on_message(ws, message):

        print("==================  ratest rate ===")
        
        # 日にちを取得
        date = datetime.now().strftime("%Y-%m-%d")

        file_path = f'sqlite:///{folder_path}/{date}_ratest_rate.db'
        
        content = json.loads(message)
        timestamp_str = content['timestamp']
        timestamp = datetime.fromisoformat(timestamp_str[:-1])
        new_timestamp = timestamp + timedelta(hours=9)
        content['timestamp'] = new_timestamp

        print(content)

        ratest_rate.RatestRate_Save2SQL(content, file_path)

    def on_close(ws):
        print("WebSocket connection closed : Ratest Rate")

    def on_error(ws, error):
        print(f"WebSocket error: {error}")


    # websocket.enableTrace(True)
    ws = websocket.WebSocketApp('wss://api.coin.z.com/ws/public/v1',
                                on_open = on_open,
                                on_message = on_message,
                                on_close=on_close,
                                on_error=on_error
                                )
    

    def run_websocket():
        # ws.run_forever()
        sleep_time = 0
        while True:
            try:
                sleep_time = 0
                ws.run_forever()
            except Exception as e:
                print(f"Exception caught when connecting: {e}")
                sleep_time += 3
                if sleep_time >= 21:
                    print("websocketが複数回接続できなかった．根本的な問題がある．")
                    break

            print("=============================================================")
            print("WebSocket connection closed or failed, retrying...")
            time.sleep(sleep_time)  # wait for 3 seconds before retrying

    thread = threading.Thread(target=run_websocket)
    thread.start()

    return ws, thread

def handle_signal(signal, frame):
    print("Interrupt received, closing WebSocket connection...")
    ws.close()
    sys.exit(0)


if __name__ == '__main__':
    
    folder_path = "C:/Users/yamaguchi/MyDocument/gmo_data/ratest_rate_test"
    folder_path = "C:/Users/yamaguchi/MyDocument/gmo_data/ratest_rate"
    # ディレクトリが存在しない場合、ディレクトリを生成
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


    ws, ws_thread = start_websocket(folder_path)

    # Ctrl+Cシグナルをハンドルする
    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    # while True:
    #     # メインスレッドをブロックしないために無限ループで待機
    #     pass

