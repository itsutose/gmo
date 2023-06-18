import requests
import json

endPoint = 'https://api.coin.z.com/public'
path     = '/v1/orderbooks?symbol=BTC'

response = requests.get(endPoint + path)
# print(json.dumps(response.json(), indent=2))
print(type(json.dumps(response.json(), indent=2)))
print(type(response.json()),response.json().keys())
# print(response.json())
# print(len(asklist))
board_status = response.json()['status']
board_data = response.json()['data']
board_responsetime = response.json()['responsetime']
print(len(board_data['asks']))
print(len(board_data['bids']))
print(board_responsetime)

'''
板情報
Request example:
指定した銘柄の板情報(snapshot)を取得します。
'''