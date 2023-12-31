import requests
import json
import hmac
import hashlib
import time
from datetime import datetime, timedelta
import subsettings

# 有効注文一覧
# https://api.coin.z.com/docs/#active-orders
def get_action_orders():
    apiKey    = subsettings.apiKey
    secretKey = subsettings.secretKey

    timestamp = '{0}000'.format(int(time.mktime(datetime.now().timetuple())))
    method    = 'GET'
    endPoint  = 'https://api.coin.z.com/private'
    path      = '/v1/activeOrders'

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

    ##### apiのresponse時間が9時間遅いので，修正

    _data = res.json()

    # "timestamp"の修正
    for item in _data["data"]["list"]:
        timestamp = datetime.fromisoformat(item["timestamp"].rstrip("Z"))
        corrected_timestamp = timestamp + timedelta(hours=9)
        item["timestamp"] = corrected_timestamp.strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"

    # "responsetime"の修正
    responsetime = datetime.fromisoformat(_data["responsetime"].rstrip("Z"))
    corrected_responsetime = responsetime + timedelta(hours=9)
    _data["responsetime"] = corrected_responsetime.strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"

    return json.loads(json.dumps(_data, indent=2))

import pprint

if __name__ == '__main__':
    _data = get_action_orders()
    pprint.pprint(_data)