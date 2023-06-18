import requests
import json
import hmac
import hashlib
import time
from datetime import datetime, timedelta
import subsettings

# 約定情報取得
# https://api.coin.z.com/docs/#executions

apiKey    = subsettings.apiKey
secretKey = subsettings.secretKey

timestamp = '{0}000'.format(int(time.mktime(datetime.now().timetuple())))
method    = 'GET'
endPoint  = 'https://api.coin.z.com/private'
path      = '/v1/executions'

text = timestamp + method + path
sign = hmac.new(bytes(secretKey.encode('ascii')), bytes(text.encode('ascii')), hashlib.sha256).hexdigest()
parameters = {
    "executionId": "72123911,92123912"
}

headers = {
    "API-KEY": apiKey,
    "API-TIMESTAMP": timestamp,
    "API-SIGN": sign
}

res = requests.get(endPoint + path, headers=headers, params=parameters)
_data = res.json()

# "responsetime"の修正
responsetime = datetime.fromisoformat(_data["responsetime"].rstrip("Z"))
corrected_responsetime = responsetime + timedelta(hours=9)
_data["responsetime"] = corrected_responsetime.strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"

# 修正結果を出力
print(json.dumps(_data, indent=2))