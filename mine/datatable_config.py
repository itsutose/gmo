# config.py
from sqlalchemy import Column, String, Integer, Float, Date

RATEST_RATE_COLUMNS = {
    "id" : Column(Integer, primary_key=True, autoincrement=True), # 主キー
    "timestamp" :Column(String(64)),  # 時刻 
    "channel" : Column(String(64)),  # ticker
    'ask': Column(Integer), # 現在の売注文の最良気配値
    'bid': Column(Integer), # 現在の買注文の最良気配値
    'high': Column(Integer),  # 当日の最高値(最終取引価格)
    'last': Column(Integer),  # 最終取引価格
    'low': Column(Integer),  # 当日の最安値(最終取引価格)
    'symbol': Column(String(64)),  # 銘柄名
    'volume': Column(Float)  # 24時間の取引量

}

TRADING_HISTORY_COLUMNS = {
    "id" : Column(Integer, primary_key=True, autoincrement=True), # 主キー
    "timestamp" :Column(String(64)),  # 時刻 
    "price" : Column(Integer), # 約定価格
    "channel" : Column(String(64)),  # ticker
    'size': Column(Float),  # 約定数量
    'side': Column(String(64)),  # 売買区分，BUY or SELL
    'symbol': Column(String(64))  # 銘柄名
}


