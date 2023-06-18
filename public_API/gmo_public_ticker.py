import requests
import json

endPoint = 'https://api.coin.z.com/public'
path     = '/v1/ticker?symbol=BTC'

response = requests.get(endPoint + path)
print(json.dumps(response.json(), indent=2))

'''
最新レート
全銘柄分の最新レートを取得する場合はsymbolパラメータ指定無しでの実行をおすすめします。
'''