from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import os

from gmo_public_orderbooks import orderbooks


Base = declarative_base()


class BoardData(Base):
    __tablename__ = 'board_data'
    
    id = Column(Integer, primary_key=True)
    status = Column(Integer)
    symbol = Column(String)
    responsetime = Column(DateTime)
    
    asks = relationship("Ask", back_populates="board_data")
    bids = relationship("Bid", back_populates="board_data")

class Ask(Base):
    __tablename__ = 'asks'
    
    id = Column(Integer, primary_key=True)
    price = Column(Float)
    size = Column(Float)
    board_data_responsetime = Column(Integer, ForeignKey('board_data.responsetime'))
    
    board_data = relationship("BoardData", back_populates="asks")

class Bid(Base):
    __tablename__ = 'bids'
    
    id = Column(Integer, primary_key=True)
    price = Column(Float)
    size = Column(Float)
    # board_data_id = Column(Integer, ForeignKey('board_data.id'))
    board_data_responsetime = Column(Integer, ForeignKey('board_data.responsetime'))
    
    board_data = relationship("BoardData", back_populates="bids")

def save_to_database(board_data, board_status, board_responsetime):
    Session = sessionmaker(bind=engine)
    session = Session()
    
    board = BoardData(status=board_status, symbol=board_data['symbol'], responsetime=board_responsetime)
    session.add(board)
    session.commit()  # Commit to get the board_id
    
    for ask in board_data['asks']:
        new_ask = Ask(price=float(ask['price']), size=float(ask['size']), board_data_responsetime=board.responsetime)
        session.add(new_ask)
        
    for bid in board_data['bids']:
        new_bid = Bid(price=float(bid['price']), size=float(bid['size']), board_data_responsetime=board.responsetime)
        session.add(new_bid)
    
    session.commit()
    session.close()

from board_data_model import model
from datetime import datetime, timedelta, time as dtime
import time
import pytz

if __name__ == '__main__':

    base_path = "C:/Users/yamaguchi/MyDocument/gmo_data/board_test"
    yesterday = None
    error_count = 0
    error_type = ['ConnectionError', "Timeout", "RequestException", "Exception", "JSONDecodeError"]

    while True:

        # googleドライブが A‐Zドライブの頭文字を取得
        current_path = os.path.abspath(__file__)
        drive_letter = os.path.splitdrive(current_path)[0]

        # 日にちを取得
        jst = pytz.timezone('Asia/Tokyo')
        datetime_now = datetime.now(jst)

        date = datetime_now.strftime("%Y-%m-%d")
        if date != yesterday:
            # if datetime_now 
            directory_path = os.path.join(base_path, str(date))

            # ディレクトリが存在しない場合、ディレクトリを生成
            if not os.path.exists(directory_path):
                os.makedirs(directory_path)

        yesterday = date
        hour = datetime_now.hour
        minute = datetime_now.minute
        sec = datetime_now.second

        if sec % 10 == 0:
            print(datetime_now)

        # Create an SQLite database and add the data into it
        # engine = create_engine(f'sqlite:////workspace/gmo_data/board/{date}_board.db')
        engine = create_engine(f'sqlite:///{base_path}/{date}/{date}-{hour}_board.db')
        Base.metadata.create_all(engine)

        board_status,b,c = orderbooks()
        
        # for exception perturns
        # 今のところは時間を置いて再度実行すると直ると予想，修正がいるかも
        if board_status in error_type:
            time.sleep(3)
            error_count += 1
            if error_count >= 5:
                error_count = 0
                time.sleep(15)
            continue

        # for mentainance am 9 ~ am 11 in saturday
        if board_status == 5:
            datetime_11am = datetime_now.replace(hour=11, minute=0, second=0, microsecond=0)

            if datetime_now.strftime('%Y-%m-%d') == '2023-09-02':
                datetime_11am = datetime_now.replace(hour=16, minute=0, second=0, microsecond=0)

            if datetime_now < datetime_11am:
                # 11時までの待機時間を計算
                sleep_seconds = (datetime_11am - datetime_now).total_seconds()

                # 時間、分、秒に変換
                hours = int(sleep_seconds // 3600)
                minutes = int((sleep_seconds % 3600) // 60)
                seconds = int(sleep_seconds % 60)

                # print(f'now : {datetime.now(jst)}, sleep_seconds : {sleep_seconds}')
                print(f'now: {datetime.now(jst)}, sleep_seconds: {sleep_seconds}')
                print(f'Time to sleep: {hours} : {minutes} : {seconds}')
                
                # その時間だけプログラムを一時停止
                time.sleep(sleep_seconds)
                continue    

        # おそらく通ることはないと思うが一応
        if c == 'MAINTENANCE. Please wait for a while':
            continue

        c = datetime.fromisoformat(c.replace("Z", ""))
        jst_c = c + timedelta(hours = 9)

        save_to_database(b,board_status,jst_c)

        # 10秒待つ
        time.sleep(1)

        # https://chat.openai.com/c/db64838f-baa7-4b3e-bd0a-69c16a6e6323

