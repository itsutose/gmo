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


class start_websocket:
    def __init__(self, base_path = 'C:/Users/yamaguchi/MyDocument/gmo_data/board_websocket', drive_letter = None):
        self.ws = None
        self.thread = None
        self.base_path = base_path
        self.datetime_now = datetime.now(pytz.timezone('Asia/Tokyo'))
        self.yesterday = self.datetime_now.strftime("%Y-%m-%d")
        # self.hour = self.datetime_now.hour
        self.content_list = []

    def on_open(self, ws):
        message = {
            "command": "subscribe",
            "channel": "orderbooks",
            "symbol": "BTC"
        }
        self.ws.send(json.dumps(message))

    def on_message(self, ws, message):
        # pprint(json.loads(message))

        print("==================  board websocket ===")
        
        # 日にちを取得
        jst = pytz.timezone('Asia/Tokyo')
        datetime_now = datetime.now(jst)

        date = datetime_now.strftime("%Y-%m-%d")
        if date != self.yesterday:
            # if datetime_now 
            directory_path = os.path.join(self.base_path, str(date))

            # ディレクトリが存在しない場合、ディレクトリを生成
            if not os.path.exists(directory_path):
                os.makedirs(directory_path)

        self.yesterday = date
        hour = datetime_now.hour
        
        # # 日にち用
        # board_info_date_path = f'sqlite:////workspace/gmo_data/board_info/'+date+'_board_info.db'
        board_info_date_path = f'{self.base_path}/{date}/{date}-{hour}_board_info.db'

        # print(board_info_date_path)

        file_path = board_info_date_path
        
        content = json.loads(message)
        # print(content)
        timestamp_str = content['timestamp']
        timestamp = datetime.fromisoformat(timestamp_str[:-1])
        new_timestamp = timestamp + timedelta(hours=9)
        content['timestamp'] = new_timestamp

        self.content_list.append(content)
        if len(self.content_list) >= 100:
            save_to_database(self.content_list, file_path)
            print('save 20 items ')
            self.content_list = []
        print(f'{content["timestamp"]}')
    
    def on_close(self, ws):
        print("WebSocket connection closed : websocket board info")


    def set_ws(self):
        websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp('wss://api.coin.z.com/ws/public/v1',
                                on_open = lambda ws: self.on_open(ws),
                                on_message = lambda ws, msg: self.on_message(ws, msg),
                                on_close = lambda ws: self.on_close(ws)
                                    )
        self.thread = threading.Thread(target=self.ws.run_forever)
        self.thread.start()

    def run_websocket(self):
        self.ws.run_forever()


    def handle_signal(self, signal, frame):
        print("Interrupt received, closing WebSocket connection...")
        self.ws.close()
        sys.exit(0)

    def get_ws_thread(self):

        if self.ws is None or self.thread is None:
            raise Exception("WebSocket and thread are not initialized. Call set_ws() first.")
        return self.ws, self.thread

if __name__ == '__main__':

    base_path = 'C:/Users/yamaguchi/MyDocument/gmo_data/board_websocket'

    # googleドライブが A‐Zドライブの頭文字を取得
    current_path = os.path.abspath(__file__)
    drive_letter = os.path.splitdrive(current_path)[0]

    # ws, ws_thread = start_websocket(drive_letter)
    sws = start_websocket(base_path, drive_letter)
    sws.set_ws()
    ws, ws_thread = sws.get_ws_thread()

    # Ctrl+Cシグナルをハンドルする
    signal.signal(signal.SIGINT, sws.handle_signal)
    signal.signal(signal.SIGTERM, sws.handle_signal)

    while True:
        # メインスレッドをブロックしないために無限ループで待機
        pass
