import requests
from requests.exceptions import ConnectionError, Timeout, RequestException, JSONDecodeError
import json
import datetime
from pprint import pprint


def write_log(message):
    with open("error_log.txt", "a") as f:
        f.write(f"{message}\n")


# プログラムの開始時間を記録
start_time = datetime.datetime.now()
write_log("============================================")
write_log(f"Program started at {start_time}")

endPoint = 'https://api.coin.z.com/public'
path     = '/v1/orderbooks?symbol=BTC'

def orderbooks():
    
    try:
        response = requests.get(endPoint + path, timeout=10)  # timeoutを10秒に設定
        response.raise_for_status()  # HTTPエラー（4xx, 5xx）が発生した場合に例外を発生させる
        # 正常な処理
        # print(response.json())

    # ネットワーク接続に関連するエラー（例えば、DNS解決の失敗、接続拒否など）を検出
    except (ConnectionError, Timeout, RequestException, Exception) as e:
        error_time = datetime.datetime.now()
        error_type = type(e).__name__
        error_message = (
                            f"Network Error\n"
                            f"error type       : {error_type}\n"
                            f"time             : {error_time}\n"
                            f"{e}\n"
                        )
        # action_taken = "No action taken yet"  # ここに後で行った対応を記述する

        # ログにエラー情報を書き出す
        write_log(error_message)
        print("======================= error message =========================")
        print("error type : ", error_type)
        print(error_message)

        return error_type, None, None


    try:
        response_data = response.json()
    except JSONDecodeError as e:
        error_time = datetime.datetime.now()
        error_type = "JSONDecodeError"  # 例外の型（クラス）名

        # error_message = f"A {error_type} occurred at {error_time}:"  # 例外の詳細を含む
        error_message = (
                            f"JSON Decode Error\n"
                            f"error type       : {error_type}\n"
                            f"time             : {error_time}\n"
                            f"HTTP Status Code : {response.status_code}\n"
                            f"{response.text}"
                        )
        
        # action_taken = "No action taken yet"  # ここに後で行った対応を記述する

        # ログにエラー情報と追加情報を書き出す
        write_log(error_message)

        print("======================= error message =========================")
        print(error_message)

        return "JSONDecodeError", None, None
    
    if response_data['status'] == 5:
        board_status = response_data['status']
        board_message_code = response_data['messages'][0]['message_code']
        board_message_string = response_data['messages'][0]['message_string']
        return board_status, board_message_code, board_message_string

    elif response_data['status'] == 0:
        board_status = response_data['status']
        board_data = response_data['data']
        board_responsetime = response_data['responsetime']
        return board_status, board_data, board_responsetime 
    
    else :
        board_status = response_data['status']
        unknown_status = (
                    f"Unknown json status\n"
                    f"status : {board_status}\n"
                    f"{response_data}"
                )
        
        write_log(unknown_status)
        print(unknown_status)
        
        return board_status, None, None

if __name__ == '__main__':
    response = requests.get(endPoint + path)
    board_status, b, c = orderbooks()

    print(board_status)
    print(b)
    print(c)


'''
板情報
Request example:
指定した銘柄の板情報(snapshot)を取得します。
'''
"""
{
  "status": 5,
  "messages": [
    {
      "message_code": "ERR-5201",
      "message_string": "MAINTENANCE. Please wait for a while"
    }
  ]
}
"""

"""
{
  "status": 0,
  "data": {
    "status": "OPEN"
  },
  "responsetime": "2019-03-19T02:15:06.001Z"
}
"""