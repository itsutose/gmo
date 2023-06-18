import requests
import json
import hmac
import hashlib
import time
from datetime import datetime, timedelta
import subsettings

# 余力情報を取得
# https://api.coin.z.com/docs/#margin

apiKey    = subsettings.apiKey
secretKey = subsettings.secretKey

timestamp = '{0}000'.format(int(time.mktime(datetime.now().timetuple())))
method    = 'GET'
endPoint  = 'https://api.coin.z.com/private'
path      = '/v1/account/margin'

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

# 修正結果を出力
print(json.dumps(_data, indent=2))

'''
Request
GET /private/v1/account/margin

Parameters
無し

Response
+-------------------+-------------+------------------------------------------------+
| Property Name     | Value       | Description                                    |
+-------------------+-------------+------------------------------------------------+
| actualProfitLoss  | string      | 時価評価総額                                    |
| availableAmount   | string      | 取引余力                                        |
| margin            | string      | 拘束証拠金                                      |
| marginCallStatus  | string      | 追証ステータス: NORMAL MARGIN_CALL LOSSCUT      |
| marginRatio       | string      | 証拠金維持率                                    |
| profitLoss        | string      | 評価損益                                        |
+-------------------+-------------+------------------------------------------------+

'''