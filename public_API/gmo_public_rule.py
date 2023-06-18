import requests
import json

endPoint = 'https://api.coin.z.com/public'
path     = '/v1/symbols'

response = requests.get(endPoint + path)
print(json.dumps(response.json(), indent=2))

"""
symbol	        string	取扱銘柄はこちら
minOrderSize	string	最小注文数量/回
maxOrderSize	string	最大注文数量/回
sizeStep        string	最小注文単位/回
tickSize	    string	注文価格の呼値
takerFee	    string	taker手数料
makerFee	    string	maker手数料
"""