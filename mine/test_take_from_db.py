import sys
import os

def getDriveLetter():
    current_path = os.path.abspath(__file__)
    return os.path.splitdrive(current_path)[0].upper()

# current_dir = os.path.dirname(os.path.abspath(__file__))
save_program_dir = f'{getDriveLetter()}/マイドライブ/pytest/virtual_currency/gmo/mine/save_program'
# print(save_program_dir)
sys.path.append(save_program_dir)
import re
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from ratest_rate import RatestRateTable
from trading_history import TradingHistTable

# db_path = r'I:\マイドライブ\pytest\virtual_currency\gmo\gmo_data\ratest_rate\2023-06-18_ratest_rate.db'

def take_from_db(database_path):
    # SQLite データベースファイルのパス
    # database_path = r'I:/マイドライブ/pytest/virtual_currency/gmo/gmo_data/ratest_rate/2023-06-22_ratest_rate.db'

    # SQLite データベースに接続
    engine = create_engine(f"sqlite:///{database_path}", echo=False)
    print(engine)
    Session = sessionmaker(bind=engine)

    def get_table_type(database_path):

        # パターンに一致する部分文字列を抽出します
        match = re.search(r"gmo_data/([^/]+)", database_path)

        if match:
            extracted_string = match.group(1)
            # print(extracted_string)
            return extracted_string
        else:
            # print("一致する部分文字列が見つかりませんでした")
            return -1

    # RatestRateTableの最後に追加されたデータを取得する関数
    def RatestRateTable_get_last_added_data():
        # セッションを作成
        session = Session()
        # 直近に追加されたデータを取得
        last_added_data = session.query(RatestRateTable).order_by(RatestRateTable.id.desc()).first()
        # セッションをクローズ
        session.close()

        return last_added_data
    
    # TradingHistTableの最後に追加されたデータを取得する関数
    def TradingHistTable_get_last_added_data():
        # セッションを作成
        session = Session()
        # 直近に追加されたデータを取得
        last_added_data = session.query(TradingHistTable).order_by(TradingHistTable.id.desc()).first()
        # セッションをクローズ
        session.close()

        return last_added_data
    
    table_type = get_table_type(database_path)
    print(table_type)

    if table_type == 'ratest_rate':
        last_added_data = RatestRateTable_get_last_added_data()
        if last_added_data:
            print('ここから')
            print(last_added_data.timestamp, last_added_data.channel, last_added_data.ask, last_added_data.bid, last_added_data.high, last_added_data.last, last_added_data.low, last_added_data.symbol, last_added_data.volume)
        else:
            print("No added data.")
    elif table_type == 'trading_hist':
        last_added_data = TradingHistTable_get_last_added_data()
        if last_added_data:
            print('ここから')
            print(last_added_data.timestamp, last_added_data.channel, last_added_data.ask, last_added_data.bid, last_added_data.high, last_added_data.last, last_added_data.low, last_added_data.symbol, last_added_data.volume)
        else:
            print("No added data.")


    # 最後に追加されたデータを取得
    
    if table_type == -1:
        # print(last_added_data)
        pass

if __name__ == '__main__':

    date = datetime.now().strftime("%Y-%m-%d")
    # print(sys.argv)
    if len(sys.argv) == 2:
        take_from_db(sys.argv[1])
    else:
        # 累計用
        ratest_rate_path = 'sqlite:///J:/マイドライブ/pytest/virtual_currency/gmo/gmo_data/ratest_rate/ratest_rate.db'
        # 日にち用
        ratest_rate_date_path = r'J:/マイドライブ/pytest/virtual_currency/gmo/gmo_data/ratest_rate/'+date+r'_ratest_rate.db'
        take_from_db(ratest_rate_date_path)