import requests
import json
import hmac
import hashlib
import time
from datetime import datetime, timedelta
import subsettings

# 資産残高を取得
# https://api.coin.z.com/docs/#assets
def get_assets():
    apiKey    = subsettings.apiKey
    secretKey = subsettings.secretKey

    timestamp = '{0}000'.format(int(time.mktime(datetime.now().timetuple())))
    method    = 'GET'
    endPoint  = 'https://api.coin.z.com/private'
    path      = '/v1/account/assets'

    text = timestamp + method + path
    sign = hmac.new(bytes(secretKey.encode('ascii')), bytes(text.encode('ascii')), hashlib.sha256).hexdigest()

    headers = {
        "API-KEY": apiKey,
        "API-TIMESTAMP": timestamp,
        "API-SIGN": sign
    }

    res = requests.get(endPoint + path, headers=headers)
    _data = res.json()

    # "responsetime"の修正
    responsetime = datetime.fromisoformat(_data["responsetime"].rstrip("Z"))
    corrected_responsetime = responsetime + timedelta(hours=9)
    _data["responsetime"] = corrected_responsetime.strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"
    
    return _data


'''
Parameters
無し

Response
+-----------------+------------+---------------------------------------------------------------------------------------------------------+
| Property Name   | Value      | Description                                                                                             |
+-----------------+------------+---------------------------------------------------------------------------------------------------------+
| amount          | string     | 残高                                                                                                 
| available       | string     | 利用可能金額（残高 - 出金予定額）                                                                    
| conversionRate  | string     | 円転レート（販売所での売却価格です。※販売所で取り扱いのない銘柄は、取引所現物での最終約定価格です。）
| symbol          | string     | 資産残高銘柄: 取扱銘柄はこちら                                                                       
|                 |            | ※取引所（現物取引）の取扱銘柄のみAPIでご注文いただけます。取扱銘柄はこちら                            
+-----------------+------------+---------------------------------------------------------------------------------------------------------+
'''

# 修正結果を出力
if __name__ == '__main__':
    _data =  get_assets()
    print(json.dumps(_data, indent=2))