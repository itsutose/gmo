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
# import keyboard
import pytz

if __name__ == '__main__':

    while True:
    
        # googleドライブが A‐Zドライブの頭文字を取得
        current_path = os.path.abspath(__file__)
        drive_letter = os.path.splitdrive(current_path)[0]

        # 日にちを取得
        jst = pytz.timezone('Asia/Tokyo')
        date = datetime.now(jst).strftime("%Y-%m-%d")
        
        

        # Create an SQLite database and add the data into it
        # engine = create_engine(f'sqlite:////workspace/gmo_data/board/{date}_board.db')
        engine = create_engine(f'sqlite:///C:/Users/yamaguchi/MyDocument/gmo_data/board/2023-08-20_board.db')
        Base.metadata.create_all(engine)

        board_status,b,c = orderbooks()

        if board_status == 5:
            while current_time < datetime.strptime("10:58:45", "%H:%M:%S").time():
                print(f"Waiting for the 2-minute mark. Current time: {current_time.strftime('%H:%M:%S')}")
                time.sleep(60)  # wait for 60 seconds before checking again
                current_time = datetime.now(jst).time()

            # Once it's 2 minutes before 11:00, check every 5 seconds
            while current_time < datetime.strptime("11:00:00", "%H:%M:%S").time():
                print(f"Waiting for 11:00 AM JST. Current time: {current_time.strftime('%H:%M:%S')}")
                time.sleep(5)  # wait for 5 seconds before checking again
                current_time = datetime.now(jst).time()
            

        c = datetime.fromisoformat(c.replace("Z", ""))
        jst_c = c + timedelta(hours = 9)

        # print(model)
        # board_status = model['status']
        # b = model['data']
        # c = model['responsetime']
        # c = datetime.fromisoformat(c.replace("Z", ""))
        print(c, jst_c)
        save_to_database(b,board_status,jst_c)

            # 'q' キーが押されたらループを終了する
        # if keyboard.is_pressed('q'):
        #     print("Exiting the program...")
        #     break

        # 10秒待つ
        time.sleep(10)

        # https://chat.openai.com/c/db64838f-baa7-4b3e-bd0a-69c16a6e6323

