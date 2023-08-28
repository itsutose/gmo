
import numpy as np
from dezero import as_variable
from bitcoin_trading_env import BitcoinTradingEnv
from trading_agent import TradingAgentWithUpdate

from dezero import Model, optimizers


# Define epsilon-greedy strategy
def select_action(state, epsilon):
    state_tensor = as_variable(np.array([state], dtype=np.float32))
    
    if np.random.rand() < epsilon:
        action_type = np.random.choice([0, 1, 2]) # 0: Buy, 1: Sell, 2: Hold
        action_amount = np.random.rand() # Random amount between 0 and 1
    else:
        buy_q, sell_q, hold_q = agent(state_tensor)
        action_type = np.argmax([buy_q.data[0], sell_q.data[0], hold_q.data[0]])
        if action_type == 0:
            action_amount = buy_q.data[0, 0]
        elif action_type == 1:
            action_amount = sell_q.data[0, 0]
        else:
            action_amount = 0 # Hold action
    return (action_type, action_amount)

# Training parameters
num_episodes = 10
epsilon = 0.9

# Initialize environment and agent
env = BitcoinTradingEnv(data)  # 'data' should be loaded in the main script
agent = TradingAgentWithUpdate()
optimizer = optimizers.Adam().setup(agent)

# Training loop
rewards = []

for episode in range(num_episodes):
    state = env.reset()
    total_reward = 0
    done = False
    
    while not done:
        action = select_action(state, epsilon)
        next_state, reward, done = env.step(action)
        state_tensor = as_variable(np.array([state], dtype=np.float32))
        next_state_tensor = as_variable(np.array([next_state], dtype=np.float32))
        agent.update(state_tensor, action, reward, next_state_tensor, done)
        total_reward += reward
        state = next_state

    rewards.append(total_reward)

print(rewards)
