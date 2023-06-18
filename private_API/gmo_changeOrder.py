import requests
import json
import hmac
import hashlib
import time
from datetime import datetime
import subsettings

# 注文変更
# https://api.coin.z.com/docs/#change-order

apiKey    = subsettings.apiKey
secretKey = subsettings.secretKey

timestamp = '{0}000'.format(int(time.mktime(datetime.now().timetuple())))
method    = 'POST'
endPoint  = 'https://api.coin.z.com/private'
path      = '/v1/changeOrder'
reqBody = {
    "orderId": 2,
    "price": "1201",
    "losscutPrice": "1000"
}

text = timestamp + method + path + json.dumps(reqBody)
sign = hmac.new(bytes(secretKey.encode('ascii')), bytes(text.encode('ascii')), hashlib.sha256).hexdigest()

headers = {
    "API-KEY": apiKey,
    "API-TIMESTAMP": timestamp,
    "API-SIGN": sign
}

res = requests.post(endPoint + path, headers=headers, data=json.dumps(reqBody))
print (json.dumps(res.json(), indent=2))