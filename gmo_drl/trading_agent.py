
from dezero import Model, optimizers
import dezero.functions as F
import dezero.layers as L

class TradingAgentWithUpdate(Model):
    def __init__(self, gamma=0.99):
        super().__init__()
        self.l1 = L.Linear(256)  # hidden layer 1
        self.l2 = L.Linear(128)  # hidden layer 2
        self.l3 = L.Linear(64)   # hidden layer 3
        self.out_buy = L.Linear(1)  # output node for buy action amount
        self.out_sell = L.Linear(1) # output node for sell action amount
        self.out_hold = L.Linear(1) # output node for hold probability
        self.gamma = gamma

    def forward(self, x):
        x = F.relu(self.l1(x))
        x = F.relu(self.l2(x))
        x = F.relu(self.l3(x))
        buy_amount = F.sigmoid(self.out_buy(x))
        sell_amount = F.sigmoid(self.out_sell(x))
        hold_prob = F.sigmoid(self.out_hold(x))
        return buy_amount, sell_amount, hold_prob

    def update(self, state, action, reward, next_state, done):
        buy_q, sell_q, hold_q = self(state)
        next_buy_q, next_sell_q, next_hold_q = self(next_state)
        if action[0] == 0:  # Buy action
            target_q = reward + (1 - done) * self.gamma * next_buy_q
            loss = F.mean_squared_error(buy_q, target_q)
        elif action[0] == 1:  # Sell action
            target_q = reward + (1 - done) * self.gamma * next_sell_q
            loss = F.mean_squared_error(sell_q, target_q)
        else:  # Hold action
            target_q = reward + (1 - done) * self.gamma * next_hold_q
            loss = F.mean_squared_error(hold_q, target_q)
        self.cleargrads()
        loss.backward()
        optimizer.update()
