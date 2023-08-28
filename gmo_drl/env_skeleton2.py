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


if __name__ == '__main__':
    # Create an instance for testing
    env = BTCenv("/workspace/gmo_drl/BTC_sample.csv")
    env

    for i in range(50):
        shots, done = env.step()
        shot = shots[0]
        print(shot.symbol, shot.side, shot.size, shot.price, shot.timestamp, done)
        # print(len(shots))