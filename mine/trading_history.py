import datetime
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


engine = create_engine('sqlite:///I:/マイドライブ/pytest/virtual_currency/gmo/gmo_data/trading_hist.db', echo=False)

# 最初にやるやつらしい．よくわからん．
Base = declarative_base()

# datatableの型を定義
class TradingHistTable(Base):
    __tablename__ = 'trading_history'
    # print("====================")
    # print("test_sql TradingHistTable()")
    for key, column in TRADING_HISTORY_COLUMNS.items():
        print(key,column)
        locals()[key] = column

Base.metadata.create_all(engine)

#### SqliteデーターベースにPUSH配信されたデーターを格納する ####
def TradingHist_Save2SQL(content):

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
        print(key,value)
        # if REGISTERED_DATA.get(key, False):
        setattr(trading_history_table, key, value)
 
    # ######　セッションにａｄｄする ######
    # session.add(candle_data1)
    session.add(trading_history_table)
 
    ##### コミットして初めて永続化決定 ########
    session.commit()
    print('DBに保存しました。')