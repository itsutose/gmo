import requests
import json
from pprint import pprint

endPoint = 'https://api.coin.z.com/public'
path     = '/v1/orderbooks?symbol=BTC'


def orderbooks():
    response = requests.get(endPoint + path)
    
    # Check the HTTP status code
    # print(f"HTTP Status Code: {response.status_code}")
    
    # Check the response text
    # print(f"Response Text: {response.text[:500]}")  # first 500 characters
    
    try:
        response_data = response.json()
    except requests.exceptions.JSONDecodeError:
        print("Failed to decode JSON.")

        # Check the HTTP status code
        print(f"HTTP Status Code: {response.status_code}")
        
        # Check the response text
        print(f"Response Text: {response.text[:500]}")  # first 500 characters

        return -1, None, None
    
    if response_data.get('status') == 5:
        board_status = response_data['status']
        board_message = response_data['message']
        return board_status, board_message, None


    elif response.json()['status'] == 0:
        board_status = response.json()['status']
        board_data = response.json()['data']
        board_responsetime = response.json()['responsetime']
        return board_status, board_data, board_responsetime 
    
    else :
        board_status = response.json()['status']
        return board_status, None, None

if __name__ == '__main__':
    response = requests.get(endPoint + path)
    # print(json.dumps(response.json(), indent=2))
    # print(type(json.dumps(response.json(), indent=2)))
    # print(type(response.json()),response.json().keys())
    # pprint(response.json())
    # # print(len(asklist))
    # board_status = response.json()['status']
    # board_data = response.json()['data']
    # board_responsetime = response.json()['responsetime']
    # print(len(board_data['asks']))
    # print(len(board_data['bids']))
    # print(board_responsetime)
    orderbooks()


'''
板情報
Request example:
指定した銘柄の板情報(snapshot)を取得します。
'''
"""
{
  "status": 5,
  "messages": [
    {
      "message_code": "ERR-5201",
      "message_string": "MAINTENANCE. Please wait for a while"
    }
  ]
}"""