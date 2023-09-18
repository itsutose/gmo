# 確認用

import gym

env = gym.make('CartPole-v1', render_mode = 'human')

o = env.reset()

for _ in range(100):
    o, r, d, i, _ = env.step(env.action_space.sample())
    env.render()
    if d:
        env.reset()

# env.close()
# env.display()