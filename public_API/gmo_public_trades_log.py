import requests
from datetime import datetime, timedelta
import json

endPoint = 'https://api.coin.z.com/public'
path     = '/v1/trades?symbol=BTC&page=1&count=100'

response = requests.get(endPoint + path)
# print(json.dumps(response.json(), indent=2))


##### apiのresponse時間が9時間遅いので，修正

_data = response.json()

# "timestamp"の修正
for item in _data["data"]["list"]:
    timestamp = datetime.fromisoformat(item["timestamp"].rstrip("Z"))
    corrected_timestamp = timestamp + timedelta(hours=9)
    item["timestamp"] = corrected_timestamp.strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"

# "responsetime"の修正
responsetime = datetime.fromisoformat(_data["responsetime"].rstrip("Z"))
corrected_responsetime = responsetime + timedelta(hours=9)
_data["responsetime"] = corrected_responsetime.strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"

# 修正結果を出力
print(json.dumps(_data, indent=2))


dictdata = response.json()
print(dictdata.keys())
print(dictdata['data'].keys())
print(len(dictdata['data']['list']))
print(len(dictdata['data']['pagination']))

'''
+----------+-------+----------+-------------------------------------------------------------+
| Parameter | Type  | Required | Available Values                                            |
+----------+-------+----------+-------------------------------------------------------------+
| symbol   | string | Required | 取扱銘柄はこちら                                            |
| page     | number | Optional | 取得対象ページ: 指定しない場合は1を指定したとして動作する。 |
| count    | number | Optional | 1ページ当りの取得件数: 指定しない場合は100(最大値)を指定したとして動作する。 |
+----------+-------+----------+-------------------------------------------------------------+
'''