import requests
import json

endPoint = 'https://api.coin.z.com/public'
path     = '/v1/status'

response = requests.get(endPoint + path)
print(response.json())

'''
取引所のステータス
取引所の稼働状態を取得します．
'''