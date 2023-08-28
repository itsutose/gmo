import json
import pytz
import websocket
from pprint import pprint
from datetime import datetime, timedelta
import threading
import signal
import sys
import os
from board_info import save_to_database

# base_path = 'C:/Users/yamaguchi/MyDocument/gmo_data/board_websocket'
# jst = pytz.timezone('Asia/Tokyo')
# datetime_now = datetime.now(jst)

# yesterday = datetime_now.strftime("%Y-%m-%d")

def start_websocket(drive_letter):

    base_path = 'C:/Users/yamaguchi/MyDocument/gmo_data/board_websocket'
    jst = pytz.timezone('Asia/Tokyo')
    datetime_now = datetime.now(jst)

    yesterday = datetime_now.strftime("%Y-%m-%d")

    def on_open(self):
        message = {
            "command": "subscribe",
            "channel": "orderbooks",
            "symbol": "BTC"
        }
        ws.send(json.dumps(message))

    def on_message(self, message):
        # pprint(json.loads(message))

        print("==================  board websocket ===")
        
        # 日にちを取得
        jst = pytz.timezone('Asia/Tokyo')
        datetime_now = datetime.now(jst)

        date = datetime_now.strftime("%Y-%m-%d")
        if date != yesterday:
            # if datetime_now 
            directory_path = os.path.join(base_path, str(date))

            # ディレクトリが存在しない場合、ディレクトリを生成
            if not os.path.exists(directory_path):
                os.makedirs(directory_path)

        yesterday = date
        hour = datetime_now.hour
        minute = datetime_now.minute
        sec = datetime_now.second


        # 累計用
        board_info_path = f'sqlite:////workspace/gmo_data/board_info/board_info.db'
        # 日にち用
        board_info_date_path = f'sqlite:////workspace/gmo_data/board_info/'+date+'_board_info.db'
        board_info_date_path = f'sqlite:///{base_path}/{date}/{date}-{hour}_board_info.db'

        file_path = board_info_date_path
        
        content = json.loads(message)
        # print(content)
        timestamp_str = content['timestamp']
        timestamp = datetime.fromisoformat(timestamp_str[:-1])
        new_timestamp = timestamp + datetime.timedelta(hours=9)
        content['timestamp'] = new_timestamp

        # print(content)
        # print(file_path)
    
        save_to_database(content, file_path)
        print(f'{content["timestamp"]}')

    # ws.on_open = on_open
    # ws.on_message = on_message

    # ws.run_forever()
    
    def on_close(ws):
        print("WebSocket connection closed : websocket board info")


    websocket.enableTrace(True)
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
