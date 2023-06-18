import requests
import json
import hmac
import hashlib
import time
from datetime import datetime, timedelta
import subsettings

# 注文情報取得
# https://api.coin.z.com/docs/#orders

apiKey    = subsettings.apiKey
secretKey = subsettings.secretKey

timestamp = '{0}000'.format(int(time.mktime(datetime.now().timetuple())))
method    = 'GET'
endPoint  = 'https://api.coin.z.com/private'
path      = '/v1/orders'

text = timestamp + method + path
sign = hmac.new(bytes(secretKey.encode('ascii')), bytes(text.encode('ascii')), hashlib.sha256).hexdigest()
parameters = { "orderId": "123456789,223456789" }

headers = {
    "API-KEY": apiKey,
    "API-TIMESTAMP": timestamp,
    "API-SIGN": sign
}

res = requests.get(endPoint + path, headers=headers, params=parameters)
# print (json.dumps(res.json(), indent=2))

##### apiのresponse時間が9時間遅いので，修正

_data = res.json()

# "timestamp"の修正
for item in _data["data"]:
    timestamp = datetime.fromisoformat(item["timestamp"].rstrip("Z"))
    corrected_timestamp = timestamp + timedelta(hours=9)
    item["timestamp"] = corrected_timestamp.strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"

# "responsetime"の修正
responsetime = datetime.fromisoformat(_data["responsetime"].rstrip("Z"))
corrected_responsetime = responsetime + timedelta(hours=9)
_data["responsetime"] = corrected_responsetime.strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"

# 修正結果を出力
print(json.dumps(_data, indent=2))

'''
Request
GET /private/v1/orders

Parameters
Parameter type: query
+-----------+-------+----------+-------------------------------------------------------------+
| Parameter | Type  | Required | Available Values                                            
+-----------+-------+----------+-------------------------------------------------------------+
| orderId   |string | Required | カンマ区切りで最大10件まで指定可能。 
+-----------+-------+----------+-------------------------------------------------------------+


Response
+----------------+---------+-------------------------------------------------------------+
| Property Name  | Value   | Description                                                 |
+----------------+---------+-------------------------------------------------------------+
| rootOrderId    | number  | 親注文ID                                                     
| orderId        | number  | 注文ID                                                       
| symbol         | string  | 取扱銘柄はこちら                                             
| side           | string  | 売買区分: BUY SELL                                           
| orderType      | string  | 取引区分: NORMAL LOSSCUT                                     
| executionType  | string  | 注文タイプ: MARKET LIMIT STOP                                
| settleType     | string  | 決済区分: OPEN CLOSE                                         
| size           | string  | 発注数量                                                     
| executedSize   | string  | 約定数量                                                     
| price          | string  | 注文価格 (MARKET注文の場合は"0")                             
| losscutPrice   | string  | ロスカットレート (現物取引や未設定の場合は"0")                
| status         | string  | 注文ステータス: WAITING ORDERED MODIFYING CANCELLING CANCELED EXECUTED EXPIRED  
|                |         |    ※逆指値注文の場合はWAITINGが有効                          
| cancelType     | string  | 取消区分: USER POSITION_LOSSCUT INSUFFICIENT_BALANCE         
|                |         | INSUFFICIENT_MARGIN ACCOUNT_LOSSCUT MARGIN_CALL              
|                |         | MARGIN_CALL_LOSSCUT EXPIRED_FAK EXPIRED_FOK EXPIRED_SOK       
|                |         |    ※statusがCANCELLING、CANCELEDまたはEXPIREDの場合のみ返ってきます。
| timeInForce    | string  | 執行数量条件: FAK FAS FOK (Post-onlyの場合はSOK)              
| timestamp      | string  | 注文日時                                                    
+----------------+---------+-------------------------------------------------------------+

'''