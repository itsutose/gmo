import datetime
import subprocess
import os
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy.types import Float
from sqlalchemy.types import Integer
from sqlalchemy.types import String
from sqlalchemy.orm import sessionmaker
from datatable_config import RATEST_RATE_COLUMNS
from collections import OrderedDict
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


# 最初にやるやつらしい．よくわからん．
Base = declarative_base()

# datatableの型を定義
class RatestRateTable(Base):
    __tablename__ = 'ratest_rate'
    
    id = Column(Integer, primary_key=True, autoincrement=True) # 主キー
    timestamp =Column(String(64))  # 時刻 
    channel = Column(String(64))  # ticker
    ask = Column(Integer) # 現在の売注文の最良気配値
    bid = Column(Integer) # 現在の買注文の最良気配値
    high = Column(Integer)  # 当日の最高値(最終取引価格)
    last = Column(Integer)  # 最終取引価格
    low = Column(Integer)  # 当日の最安値(最終取引価格)
    symbol = Column(String(64))  # 銘柄名
    volume = Column(Float)  # 24時間の取引量


#### SqliteデーターベースにPUSH配信されたデーターを格納する ####
def RatestRate_Save2SQL(content, file_path):

    engine = create_engine(file_path, echo=False)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    ratest_rate_table = RatestRateTable()

    # 設定ファイルに従ってデータを登録
    for key, value in content.items():
        print(key,value)
        setattr(ratest_rate_table, key, value)
 
    session.add(ratest_rate_table)
    session.commit()

    print(f'Save to DB : {file_path}')
    # execute_test_take_from_db(file_path)

def getDriveLetter():
    current_path = os.path.abspath(__file__)
    return os.path.splitdrive(current_path)[0].upper()

def execute_test_take_from_db(file_path):
    test_take_from_db_path = f"{getDriveLetter()}/マイドライブ/pytest/virtual_currency/gmo/mine/test_take_from_db.py"
    
    # test_take_from_db.pyを実行
    subprocess.run(["python", test_take_from_db_path])
    
    
if __name__ == '__main__':
    # 日にちを取得
    date = datetime.datetime.now().strftime("%Y-%m-%d")

    file_path = 'sqlite:///C:/Users/yamaguchi/MyDocument/pytest/virtual_currency/gmo/public_websocket_API/test_ratest_rate.db'
    
    content = {'channel': 'ticker', 'ask': '4179187', 'bid': '4177779', 'high': '4193000', 'last': '4179187', 'low': '4166834', 'symbol': 'BTC', 'timestamp': datetime.datetime(2023, 8, 4, 15, 4, 15, 516000), 'volume': '86.6484'}
    
    RatestRate_Save2SQL(content, file_path)


# WebSocket connection closed : Trading History
# Interrupt received, closing WebSocket connection...