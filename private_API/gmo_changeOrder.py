import requests
import json
import hmac
import hashlib
import time
from datetime import datetime
import subsettings

# 注文変更
# https://api.coin.z.com/docs/#change-order

def change_order(orderID, price, losscutPrice):
    apiKey    = subsettings.apiKey
    secretKey = subsettings.secretKey

    timestamp = '{0}000'.format(int(time.mktime(datetime.now().timetuple())))
    method    = 'POST'
    endPoint  = 'https://api.coin.z.com/private'
    path      = '/v1/changeOrder'

    if losscutPrice == '0':
        reqBody = {
            "orderId": orderID,
            "price": price
        }
    else:
        reqBody = {
            "orderId": orderID,
            "price": price,
            "losscutPrice": losscutPrice
        }

    text = timestamp + method + path + json.dumps(reqBody)
    sign = hmac.new(bytes(secretKey.encode('ascii')), bytes(text.encode('ascii')), hashlib.sha256).hexdigest()

    headers = {
        "API-KEY": apiKey,
        "API-TIMESTAMP": timestamp,
        "API-SIGN": sign
    }

    res = requests.post(endPoint + path, headers=headers, data=json.dumps(reqBody))
    return res

from gmo_activeOrders_info import get_action_orders
from pprint import pprint

if __name__ == '__main__':
    orders_data = get_action_orders()
    orders_list = orders_data['data']['list']
    order0 = orders_list[0]
    
    pprint(order0)
    orderId = order0['orderId']
    side = order0['side']
    if side == 'BUY':
        price = str(int(order0['price']) - 10)
    else:
        price = str(int(order0['price']) + 10)

    # losscutPrice = str(int(order0['price']) - 50000)
    losscutPrice = order0['losscutPrice']
    res = change_order(orderId, price, losscutPrice)
    print(type(res))
    print (json.dumps(res.json(), indent=2))