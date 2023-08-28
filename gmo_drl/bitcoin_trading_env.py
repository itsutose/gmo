
import numpy as np

class BitcoinTradingEnv:
    def __init__(self, data, initial_balance=1_000_000, window_size=10):
        self.data = data
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.btc_held = 0
        self.window_size = window_size
        self.current_step = 0

    @property
    def state(self):
        window_data = self.data[self.current_step:self.current_step+self.window_size]
        price = window_data['price'].values
        volume = window_data['size'].values
        moving_avg = np.mean(price)
        return [price[-1], moving_avg, volume[-1], self.balance, self.btc_held]

    def step(self, action):
        action_type, action_amount = action
        current_price = self.data.loc[self.current_step, 'price']
        if action_type == 0:  # Buy
            btc_bought = (self.balance * action_amount) / current_price
            self.balance -= btc_bought * current_price
            self.btc_held += btc_bought
        elif action_type == 1:  # Sell
            btc_sold = self.btc_held * action_amount
            self.balance += btc_sold * current_price
            self.btc_held -= btc_sold
        self.current_step += 1
        next_state = self.state
        total_asset_now = self.balance + self.btc_held * current_price
        reward = total_asset_now - self.initial_balance
        done = self.current_step >= len(self.data) - 1
        return next_state, reward, done

    def reset(self):
        self.balance = self.initial_balance
        self.btc_held = 0
        self.current_step = 0
        return self.state
