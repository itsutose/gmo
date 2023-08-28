import requests
import json
import hmac
import hashlib
import time
from datetime import datetime, timedelta
import subsettings

# 最新の約定一覧
# https://api.coin.z.com/docs/#latest-executions
# 最新約定一覧を取得します。
# 対象: 現物取引、レバレッジ取引
# 直近1日分の約定情報を返します。

def get_exe_hist():
    apiKey    = subsettings.apiKey
    secretKey = subsettings.secretKey

    timestamp = '{0}000'.format(int(time.mktime(datetime.now().timetuple())))
    method    = 'GET'
    endPoint  = 'https://api.coin.z.com/private'
    path      = '/v1/latestExecutions'

    text = timestamp + method + path
    sign = hmac.new(bytes(secretKey.encode('ascii')), bytes(text.encode('ascii')), hashlib.sha256).hexdigest()
    parameters = {
        "symbol": "BTC",
        "page": 1,
        "count": 100
    }

    headers = {
        "API-KEY": apiKey,
        "API-TIMESTAMP": timestamp,
        "API-SIGN": sign
    }

    res = requests.get(endPoint + path, headers=headers, params=parameters)
    # print (json.dumps(res.json(), indent=2))

    ##### apiのresponse時間が9時間遅いので，修正

    _data = res.json()
    # print(json.dumps(_data, indent=2))

    # "timestamp"の修正
    for item in _data["data"]["list"]:
        timestamp = datetime.fromisoformat(item["timestamp"].rstrip("Z"))
        corrected_timestamp = timestamp + timedelta(hours=9)
        item["timestamp"] = corrected_timestamp.strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"

    # "responsetime"の修正
    responsetime = datetime.fromisoformat(_data["responsetime"].rstrip("Z"))
    corrected_responsetime = responsetime + timedelta(hours=9)
    _data["responsetime"] = corrected_responsetime.strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"
    # print(json.dumps(_data, indent=2))
    # print(1)
    return json.loads(json.dumps(_data, indent=2))
    # return _data

if __name__ == '__main__':
    res = get_exe_hist()
    # res = json.loads(res)
    print(type(res))
    print(json.dumps(res, indent=2))
    # print(res['data']['list'])
    print(len(res['data']['list']))
    # print(res)