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


# 最初にやるやつらしい．よくわからん．
Base = declarative_base()

# datatableの型を定義
class RatestRateTable(Base):
    __tablename__ = 'ratest_rate'
    # print("====================")
    # print("test_sql RatestRateTable()")
    for key, column in RATEST_RATE_COLUMNS.items():
        # print(key,column)
        locals()[key] = column
        # setattr(self, key, column)

# # カラム定義を辞書に追加
# class_attrs = {key: column for key, column in RATEST_RATE_COLUMNS.items()}
# class_attrs['__tablename__'] = 'ratest_rate'

# # 動的にクラスを生成
# RatestRateTable = type('RatestRateTable', (Base,), class_attrs)


'''
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
'''



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

    drive_letter = getDriveLetter()

    # 累計用
    ratest_rate_path = f'sqlite:///{getDriveLetter()}/マイドライブ/pytest/virtual_currency/gmo/gmo_data/ratest_rate/ratest_rate.db'
    # 日にち用
    ratest_rate_date_path = f'sqlite:///{getDriveLetter()}/マイドライブ/pytest/virtual_currency/gmo/gmo_data/ratest_rate/'+date+'_ratest_rate.db'
    
    content = {'channel': 'ticker', 'ask': '4179187', 'bid': '4177779', 'high': '4193000', 'last': '4179187', 'low': '4166834', 'symbol': 'BTC', 'timestamp': datetime.datetime(2023, 8, 4, 15, 4, 15, 516000), 'volume': '86.6484'}
    
    print(ratest_rate_date_path)
    # ratest_rate_date_path = "sqlite:///J:/マイドライブ/pytest/virtual_currency/gmo/gmo_data/ratest_rate/2023-08-04-ratest_rate.db"
    
    RatestRate_Save2SQL(content, ratest_rate_date_path)
