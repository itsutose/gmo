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
from datetime import datetime, timedelta
import time
import pytz

if __name__ == '__main__':

    base_path = "C:/Users/yamaguchi/MyDocument/gmo_data/board"
    yesterday = None

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

        if sec % 0 == 0:
            print(datetime_now)

        # Create an SQLite database and add the data into it
        # engine = create_engine(f'sqlite:////workspace/gmo_data/board/{date}_board.db')
        engine = create_engine(f'sqlite:///{base_path}/{date}/{date}-{hour}_board.db')
        Base.metadata.create_all(engine)

        board_status,b,c = orderbooks()
        
        if board_status == -1:
            time.sleep(30)
            continue

        if board_status == 5:
            # その日の11時のdatetimeオブジェクトを作成
            datetime_11am = datetime_now.replace(hour=11, minute=0, second=0, microsecond=0)

            # 現在の時間が11時より前である場合
            if datetime_now < datetime_11am:
                # 11時までの待機時間を計算
                sleep_seconds = (datetime_11am - datetime_now).total_seconds()
                # その時間だけプログラムを一時停止
                time.sleep(sleep_seconds)
                continue    

        c = datetime.fromisoformat(c.replace("Z", ""))
        jst_c = c + timedelta(hours = 9)

        save_to_database(b,board_status,jst_c)

        # 10秒待つ
        time.sleep(1)

        # https://chat.openai.com/c/db64838f-baa7-4b3e-bd0a-69c16a6e6323

