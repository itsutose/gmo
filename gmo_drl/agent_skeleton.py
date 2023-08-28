import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import matplotlib.pyplot as plt
from env_skeleton2 import one_shot, BTCenv
import pandas as pd

class one_shot:
    def __init__(self, symbol, side, size, price, timestamp):
        self._symbol = symbol
        self._side = side
        self._size = size
        self._price = price
        self._timestamp = timestamp
    @property
    def symbol(self):
        return self._symbol
    @property
    def side(self):
        return self._side
    @property
    def size(self):
        return self._size
    @property
    def price(self):
        return self._price
    @property
    def timestamp(self):
        return self._timestamp
    

class BTCenv:
    def __init__(self, csv_path, history_length=10):
        self.reset()
        df = pd.read_csv(csv_path)
        for _, row in df.iterrows():
            self.shots.append(one_shot(row['symbol'], row['side'], row['size'], row['price'], row['timestamp']))
        self.history_length = history_length

    def reset(self):
        # Start from the beginning of the data and initialize price history
        self.shots = []
        self.current_step = 0
    
    def step(self):
        done = False
        self.current_step += 1

        if self.current_step < self.history_length:
            return self.shots[:self.current_step], done
        
        elif self.current_step < len(self.shots) - 1:
            return self.shots[self.current_step - self.history_length : self.current_step], done
        
        else:
            done = True
            return self.shots[self.current_step - self.history_length : self.current_step], done

    def render(self):
        # For visualization purposes, if needed later.
        pass


class SimpleNN(nn.Module):
    def __init__(self, input_size, hidden_size=128):
        super(SimpleNN, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, 1)  # Output is a single scalar value (signed value)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x

# Define the neural network with input size of 20 (10 shots * 2 values per shot)
# nn_model = SimpleNN(input_size=20)
# nn_model

class Agent:
    def __init__(self, history_length, initial_balance=1000000, btc=0, lr=0.01, epsilon = 0.1, gamma=0.99):
        # エージェントの初期ステータス
        self.balance = initial_balance  # 初期残高 (日本円)
        self.btc = btc  # 初期BTC保有量

        self.lr = lr
        self.epsilon = epsilon
        self.gamma = gamma
        
        self.net = SimpleNN(input_size = history_length * 2) # 現状は未定義のNN(ニューラルネットワークとしている)
        # self.optimizer 未定 
        # self.criterion 未定

    def get_state(self, state_history):
        """
        状態を取得します。
        :param state_history: 現在から過去の数個を含むリスト
        :return: エージェントの現在の状態
        """
        self.ratest_price = state_history[0].price
        self.timestamp = state_history[0].timestamp
        
        # 合計資産
        self.total_yen = self.balance + self.btc*self.ratest_price
        self.total_btc = self.balance/self.ratest_price + self.btc

    def act(self, state): 
        """
        エージェントが状態をもとに行動を選択します。
        :param state: エージェントの現在の状態
        :return: 選択された行動を整数値で返す (買う:正の値、売る:負の値、何もしない:0)
        """
        self.get_state(state)

        # stateを前処理する．SimpleNNでは簡易的に符号付size，priceのみ
        input_list = []
        for shot in state:
            if shot.side == 'SELL':
                size = shot.size * -1
            else:
                size = shot.size
            input_list.append(size)
            input_list.append(shot.price)
            
        input_tensor = torch.tensor(input_list).float().unsqueeze(0) 

        # ここに行動選択のロジック（例：深層学習モデル）を実装
        if np.random.rand() < self.epsilon:
            return np.random.randn()*self.balance # tensorにする必要あり
        else:
            how_many_buy = self.net(input_tensor)
            return how_many_buy

    def update(self, reward):
        """
        エージェントの状態を更新します。
        :param reward: 取得した報酬
        """
        # ここに状態更新のロジックを実装
        # 今回はプレースホルダーとしてpassを使用
        pass

    def immediate_reward(self, current_price, next_price):
        """
        即時報酬を計算します。
        :param current_price: 現在のBTC価格
        :param next_price: 次のタイムステップのBTC価格
        :return: 計算された即時報酬
        """
        # 購入した場合の損益を計算するロジックを実装
        # 今回はプレースホルダーとしてpassを使用
        

        pass

    def delayed_reward(self, price_history):
        """
        遅延報酬を計算します。
        :param price_history: 一定の期間の価格履歴
        :return: 計算された遅延報酬
        """
        # 一定の期間の損益を計算するロジックを実装
        # 今回はプレースホルダーとしてpassを使用
        pass



if __name__ == '__main__':
    history_length = 1
    # Create an instance for testing
    env = BTCenv("/workspace/gmo_drl/BTC_sample.csv", history_length)
    
    # エージェントのインスタンスを作成
    agent = Agent(history_length)


    for i in range(15): 
        sample_shots, done = env.step()
        sample_shots = sample_shots[::-1] # shotsを逆順，新しいものを前に
        if i < history_length:
            continue
        print(len(sample_shots))

        if done == True:
            pass
        else:
            # shotsの場合のactが取る行動を取得，整数値を取得
            how_many_buy = agent.act(sample_shots)
            print(how_many_buy)


