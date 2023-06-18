import requests
import json
import hmac
import hashlib
import time
from datetime import datetime, timedelta
import subsettings

# 取引高情報を取得
# https://api.coin.z.com/docs/#tradingVolume

apiKey    = subsettings.apiKey
secretKey = subsettings.secretKey

timestamp = '{0}000'.format(int(time.mktime(datetime.now().timetuple())))
method    = 'GET'
endPoint  = 'https://api.coin.z.com/private'
path      = '/v1/account/tradingVolume'

text = timestamp + method + path
sign = hmac.new(bytes(secretKey.encode('ascii')), bytes(text.encode('ascii')), hashlib.sha256).hexdigest()

headers = {
    "API-KEY": apiKey,
    "API-TIMESTAMP": timestamp,
    "API-SIGN": sign
}

res = requests.get(endPoint + path, headers=headers)
# print (json.dumps(res.json(), indent=2))

##### apiのresponse時間が9時間遅いので，修正

_data = res.json()

# "responsetime"の修正
responsetime = datetime.fromisoformat(_data["responsetime"].rstrip("Z"))
corrected_responsetime = responsetime + timedelta(hours=9)
_data["responsetime"] = corrected_responsetime.strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"

# 修正結果を出力
print(json.dumps(_data, indent=2))

'''
Request
GET /private/v1/account/tradingVolume

Parameters
無し

Response
+------------------------+---------+--------------------------------------------------------+
| Property Name          | Value   | Description                                            |
+------------------------+---------+--------------------------------------------------------+
| jpyVolume              | string  | 今週の取引高(日本円)                                   |
| tierLevel              | number  | 現在の取引高レベル: 1 2                                |
| limit.symbol           | string  | 取扱銘柄はこちら                                       |
| limit.todayLimitOpenSize | string | 1日の最大取引数量の残量(新規)※レバレッジ銘柄の場合のみ |
| limit.todayLimitBuySize  | string | 1日の最大取引数量の残量(購入)※現物銘柄の場合のみ        |
| limit.todayLimitSellSize | string | 1日の最大取引数量の残量(売却)※現物銘柄の場合のみ        |
+------------------------+---------+--------------------------------------------------------+


+-------+-------------------------+----------+------------------------------------------------------------------+
| レベル | 取引高                    | 呼び出し上限 | 説明                                                             |
+-------+-------------------------+----------+------------------------------------------------------------------+
| Tier 1 | 先週の取引高 < 1,000,000,000円 | 6req/s   | 同一アカウントからGETのAPI呼び出しは、1秒あたり6回が上限です。
                                                        同一アカウントからPOSTのAPI呼び出しは、1秒あたり6回が上限です。 |
| Tier 2 | 先週の取引高 >= 1,000,000,000円 | 10req/s  | 同一アカウントからGETのAPI呼び出しは、1秒あたり10回が上限です。
                                                        同一アカウントからPOSTのAPI呼び出しは、1秒あたり10回が上限です。 |
+-------+-------------------------+----------+------------------------------------------------------------------+

'''