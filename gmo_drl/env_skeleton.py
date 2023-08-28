import numpy as np

class SimpleBTCTradingEnvironment:
    def __init__(self, initial_price=10000, price_history_length=10):
        self.initial_price = initial_price
        self.price_history_length = price_history_length
        self.reset()

    def reset(self):
        self.current_price = self.initial_price
        self.price_history = [self.initial_price] * self.price_history_length
        return self.price_history

    def step(self, action):
        # 0: Buy, 1: Sell, 2: Hold
        reward = 0
        
        last_price = self.current_price
        # For simplicity, we simulate price as a random walk
        self.current_price += np.random.randint(-500, 500)

        # Update price history
        self.price_history.pop(0)
        self.price_history.append(self.current_price)

        # Simple reward calculation based on action
        if action == 0:  # Buy
            reward = last_price - self.current_price
        elif action == 1:  # Sell
            reward = self.current_price - last_price

        return self.price_history, reward, False

    def render(self):
        # For visualization purposes, if needed later.
        pass

