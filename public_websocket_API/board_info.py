from datetime import datetime, timedelta
import json
import pytz
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import os

# from gmo_public_orderbooks import orderbooks


Base = declarative_base()
engine = create_engine(f'sqlite:///C:/Users/yamaguchi/MyDocument/gmo_data/board_websocket/2023-08-28/2023-08-28-14_board_info.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


class BoardData(Base):
    __tablename__ = 'board_data'
    
    id = Column(Integer, primary_key=True)
    grouping = Column(Integer)
    symbol = Column(String)
    responsetime = Column(DateTime)
    
    asks = relationship("Ask", back_populates="board_data")
    bids = relationship("Bid", back_populates="board_data")

class Ask(Base):
    __tablename__ = 'asks'
    
    id = Column(Integer, primary_key=True)
    price = Column(Float)
    size = Column(Float)
    board_data_responsetime = Column(DateTime, ForeignKey('board_data.responsetime'))
    
    board_data = relationship("BoardData", back_populates="asks")

class Bid(Base):
    __tablename__ = 'bids'
    
    id = Column(Integer, primary_key=True)
    price = Column(Float)
    size = Column(Float)
    # board_data_id = Column(Integer, ForeignKey('board_data.id'))
    board_data_responsetime = Column(DateTime, ForeignKey('board_data.responsetime'))
    
    board_data = relationship("BoardData", back_populates="bids")



def save_to_database(content_list, file_path):

    # if engine == None:
    #     engine = create_engine(f'sqlite:///{file_path}')
    #     Base.metadata.create_all(engine)
    #     Session = sessionmaker(bind=engine)

    
    # session = Session()

    # for content in content_list:
    #     if type(content) != dict:
    #         content = json.loads(content)

    #     asks = content['asks']
    #     bids = content['bids']
    #     grouping = content['grouping']
    #     symbol = content['symbol']


    #     timestamp = content['timestamp']
    #     # print(type(timestamp))
    #     if type(timestamp) != datetime:
    #         timestamp = datetime.fromisoformat(timestamp[:-1])
    #         # new_timestamp = timestamp + timedelta(hours=9)    
    #         # content['timestamp'] = timestamp

        
    #     board = BoardData(grouping=grouping, symbol=symbol, responsetime=timestamp)
    #     session.add(board)
    #     # session.commit()  # Commit to get the board_id
        

    #     for ask in asks:
    #         new_ask = Ask(price=float(ask['price']), size=float(ask['size']), board_data_responsetime=board.responsetime)
    #         session.add(new_ask)
            
    #     for bid in bids:
    #         new_bid = Bid(price=float(bid['price']), size=float(bid['size']), board_data_responsetime=board.responsetime)
    #         session.add(new_bid)
        
    # session.commit()
    # session.close()

    session = Session()

    board_data_list = []
    ask_list = []
    bid_list = []

    for content in content_list:

        if type(content) != dict:
            content = json.loads(content)

        asks = content['asks']
        bids = content['bids']
        grouping = content['grouping']
        symbol = content['symbol']
        timestamp = content['timestamp']
        if type(timestamp) != datetime:
            timestamp = datetime.fromisoformat(timestamp[:-1])

        # Your existing logic to populate board, ask, and bid objects
        board = BoardData(grouping=grouping, symbol=symbol, responsetime=timestamp)
        board_data_list.append(board)
        
        for ask in asks:
            new_ask = Ask(price=float(ask['price']), size=float(ask['size']), board_data_responsetime=board.responsetime)
            ask_list.append(new_ask)
            
        for bid in bids:
            new_bid = Bid(price=float(bid['price']), size=float(bid['size']), board_data_responsetime=board.responsetime)
            bid_list.append(new_bid)

    # Bulk insert
    session.bulk_save_objects(board_data_list)
    session.bulk_save_objects(ask_list)
    session.bulk_save_objects(bid_list)
    
    session.commit()
    session.close()

# def session_close()
    

def getDriveLetter():
    current_path = os.path.abspath(__file__)
    return os.path.splitdrive(current_path)[0].upper()


from board_data_model import model

if __name__ == '__main__':
    # 日にちを取得
    # date = datetime.now().strftime("%Y-%m-%d")

    drive_letter = getDriveLetter()

    jst = pytz.timezone('Asia/Tokyo')
    datetime_now = datetime.now(jst)

    date = datetime_now.strftime("%Y-%m-%d")

    # date = datetime_now.strftime("%Y-%m-%d")


    # if date != yesterday:
    #     # if datetime_now 
    #     directory_path = os.path.join(base_path, str(date))

    #     # ディレクトリが存在しない場合、ディレクトリを生成
    #     if not os.path.exists(directory_path):
    #         os.makedirs(directory_path)

    # 累計用
    board_info_path = f'{getDriveLetter()}/マイドライブ/pytest/virtual_currency/gmo/gmo_data/board_info/board_info.db'
    # 日にち用
    board_info_date_path = f'{getDriveLetter()}/マイドライブ/pytest/virtual_currency/gmo/gmo_data/board_info/'+date+'_board_info.db'
    board_info_date_path = f'C:/Users/yamaguchi/MyDocument/gmo_data/board_websocket/{date}/{date}_board_info.db'
    # board_info_date_path = f'C:/Users/yamaguchi/MyDocument/gmo_data/board_websocket/2023-08-28/2023-08-29_board_info.db'
    
    content = model

    print(board_info_date_path)
    # board_info_date_path = "sqlite:///J:/マイドライブ/pytest/virtual_currency/gmo/gmo_data/board_info/2023-08-04-board_info.db"
    
    save_to_database(content, board_info_date_path)
