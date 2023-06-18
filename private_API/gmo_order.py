import requests
import json
import hmac
import hashlib
import time
from datetime import datetime, timedelta

import subsettings


# 注文
# https://api.coin.z.com/docs/#order

apiKey    = subsettings.apiKey
secretKey = subsettings.secretKey

print(datetime.now())
# 現在の時刻を取得
current_time = datetime.now()

# # 9時間引くためのtimedeltaオブジェクトを作成
# delta = datetime.timedelta(hours=9)
# delta = datetime.timedelta(seconds=32374, microseconds=49414)

# # 現在の時刻から9時間引いた時刻を計算
# new_time = current_time - delta
# print(new_time)

timestamp = '{0}000'.format(int(time.mktime(datetime.now().timetuple())))
method    = 'POST'
endPoint  = 'https://api.coin.z.com/private'
path      = '/v1/order'
reqBody = {
    "symbol": "BTC_JPY",
    "side": "BUY",
    "executionType": "LIMIT",
    "timeInForce": "FAS",
    "price": "00",
    "losscutPrice": "30012",
    "size": "0.0001"
}

text = timestamp + method + path + json.dumps(reqBody)
sign = hmac.new(bytes(secretKey.encode('ascii')), bytes(text.encode('ascii')), hashlib.sha256).hexdigest()

headers = {
    "API-KEY": apiKey,
    "API-TIMESTAMP": timestamp,
    "API-SIGN": sign
}

res = requests.post(endPoint + path, headers=headers, data=json.dumps(reqBody))
# print (json.dumps(res.json(), indent=2))

# res = requests.get(endPoint + path, headers=headers, params=parameters)
# # print (json.dumps(res.json(), indent=2))
# # print(type(res.json()),type(res))


##### apiのresponse時間が9時間遅いので，修正

_data = res.json()

# # "timestamp"の修正
# for item in _data["messages"]:
#     timestamp = datetime.fromisoformat(item["timestamp"].rstrip("Z"))
#     corrected_timestamp = timestamp + timedelta(hours=9)
#     item["timestamp"] = corrected_timestamp.strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"

# "responsetime"の修正
responsetime = datetime.fromisoformat(_data["responsetime"].rstrip("Z"))
corrected_responsetime = responsetime + timedelta(hours=9)
_data["responsetime"] = corrected_responsetime.strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"

# 修正結果を出力
print(json.dumps(_data, indent=2))