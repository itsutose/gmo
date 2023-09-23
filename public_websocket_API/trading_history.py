from datetime import datetime, timedelta

import os
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy.types import Float
from sqlalchemy.types import Integer
from sqlalchemy.types import String
from sqlalchemy.orm import sessionmaker
from datatable_config import TRADING_HISTORY_COLUMNS
from collections import OrderedDict
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import subprocess



# 最初にやるやつらしい．よくわからん．
Base = declarative_base()

# datatableの型を定義
class TradingHistTable(Base):
    __tablename__ = 'trading_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(String(64))
    price = Column(Integer)
    channel = Column(String(64))
    size = Column(Float)
    side = Column(String(64))
    symbol = Column(String(64))

#### SqliteデーターベースにPUSH配信されたデーターを格納する ####
def TradingHist_Save2SQL(content, file_path):

    engine = create_engine(file_path, echo=False)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    trading_history_table = TradingHistTable()

    # 設定ファイルに従ってデータを登録
    for key, value in content.items():
        # print(key,value)
        # if REGISTERED_DATA.get(key, False):
        setattr(trading_history_table, key, value)
 
    session.add(trading_history_table)
    session.commit()

    print(f'Save to DB : {file_path}')
    # execute_test_take_from_db(file_path)

def getDriveLetter():
    current_path = os.path.abspath(__file__)
    return os.path.splitdrive(current_path)[0].upper()


def execute_test_take_from_db(file_path):
    test_take_from_db_path = f"{getDriveLetter()}/マイドライブ/pytest/virtual_currency/gmo/mine/test_take_from_db.py"

    # test_take_from_db.pyを実行
    subprocess.run(["python", test_take_from_db_path, file_path])


if __name__ == '__main__':
    
    content = {'channel': 'trades', 'price': '4053000', 'side': 'BUY', 'size': '0.0012', 'symbol': 'BTC', 'timestamp': '2023-09-19T16:00:24.405Z'}
    timestamp_str = content['timestamp']
    timestamp = datetime.fromisoformat(timestamp_str[:-1])
    new_timestamp = timestamp + timedelta(hours=9)
    content['timestamp'] = new_timestamp

    file_path = 'sqlite:///C:/Users/yamaguchi/MyDocument/pytest/virtual_currency/gmo/public_websocket_API/test_trading_history.db'
    file_path = 'sqlite:///C:/Users/yamaguchi/MyDocument/pytest/virtual_currency/gmo/public_websocket_API/2023-09-20_trading_hist.db'
    TradingHist_Save2SQL(content, file_path)
