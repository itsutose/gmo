import datetime
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
    # print("====================")
    # print("test_sql RatestRateTable()")
    for key, column in RATEST_RATE_COLUMNS.items():
        print(key,column)
        locals()[key] = column

# 説明用
# class RatestRateTable(Base):
#     __tablename__ = 'ratest_rate'
    
#     id = Column(Integer, primary_key=True, autoincrement=True)  # id: 主キー、整数型 (Integer)
#     timestamp = Column(String(64))  # timestamp: 時刻、文字列型 (String(64))
#     channel = Column(String(64))  # channel: ticker、文字列型 (String(64))
#     ask = Column(Integer)  # ask: 現在の売注文の最良気配値、整数型 (Integer)
#     bid = Column(Integer)  # bid: 現在の買注文の最良気配値、整数型 (Integer)
#     high = Column(Integer)  # high: 当日の最高値(最終取引価格)、整数型 (Integer)
#     last = Column(Integer)  # last: 最終取引価格、整数型 (Integer)
#     low = Column(Integer)  # low: 当日の最安値(最終取引価格)、整数型 (Integer)
#     symbol = Column(String(64))  # symbol: 銘柄名、文字列型 (String(64))
#     volume = Column(Float)  # volume: 24時間の取引量、浮動小数点型 (Float)

#### SqliteデーターベースにPUSH配信されたデーターを格納する ####
def RatestRate_Save2SQL(content, file_path):


    engine = create_engine(file_path, echo=False)
    Base.metadata.create_all(engine)
    ####### ＜＜sqlalchemy＞＞でデーターを書き込む ######
    # 必要なライブラリー
    # from sqlalchemy.orm import sessionmaker
    Session = sessionmaker(bind=engine)
    #### セッションオブジェクトを作る ####
    session = Session()

    ratest_rate_table = RatestRateTable()

    print("test_sql RatestRate_Save2SQL()")
    # 設定ファイルに従ってデータを登録
    for key, value in content.items():
        print(key,value)
        # if REGISTERED_DATA.get(key, False):
        setattr(ratest_rate_table, key, value)
 
    # ######　セッションにａｄｄする ######
    # session.add(candle_data1)
    session.add(ratest_rate_table)
 
    ##### コミットして初めて永続化決定 ########
    session.commit()
    print('save to ',file_path)
    print('DBに保存しました。')


# if __name__ == '__main__':
#     RatestRate_Save2SQL()