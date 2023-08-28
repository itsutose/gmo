import datetime
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



# engine = create_engine('sqlite:///I:/マイドライブ/pytest/virtual_currency/gmo/gmo_data/trading_hist.db', echo=False)

# 最初にやるやつらしい．よくわからん．
Base = declarative_base()

# datatableの型を定義
class TradingHistTable(Base):
    __tablename__ = 'trading_history'
    # print("====================")
    # print("test_sql TradingHistTable()")
    for key, column in TRADING_HISTORY_COLUMNS.items():
        # print(key,column)
        locals()[key] = column



#### SqliteデーターベースにPUSH配信されたデーターを格納する ####
def TradingHist_Save2SQL(content, file_path):

    engine = create_engine(file_path, echo=False)
    Base.metadata.create_all(engine)
    ####### ＜＜sqlalchemy＞＞でデーターを書き込む ######
    # 必要なライブラリー
    # from sqlalchemy.orm import sessionmaker
    Session = sessionmaker(bind=engine)
    #### セッションオブジェクトを作る ####
    session = Session()

    trading_history_table = TradingHistTable()

    print("test_sql TradingHist_Save2SQL()")
    # 設定ファイルに従ってデータを登録
    for key, value in content.items():
        # print(key,value)
        # if REGISTERED_DATA.get(key, False):
        setattr(trading_history_table, key, value)
 
    # ######　セッションにａｄｄする ######
    # session.add(candle_data1)
    session.add(trading_history_table)
 
    ##### コミットして初めて永続化決定 ########
    session.commit()
    print('save to ',file_path)
    print('DBに保存しました。')
    # execute_test_take_from_db(file_path)

def getDriveLetter():
    current_path = os.path.abspath(__file__)
    return os.path.splitdrive(current_path)[0].upper()


def execute_test_take_from_db(file_path):
    # est_take_from_db.pyのパス
    test_take_from_db_path = f"{getDriveLetter()}/マイドライブ/pytest/virtual_currency/gmo/mine/test_take_from_db.py"
    # 引数として渡すデータベースパス
    # database_path = r'I:/マイドライブ/pytest/virtual_currency/gmo/gmo_data/ratest_rate/2023-06-18_ratest_rate.db'

    # test_take_from_db.pyを実行
    subprocess.run(["python", test_take_from_db_path, file_path])
    # pass