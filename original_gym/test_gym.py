import gym
from gym import spaces
import numpy as np

class MyGymEnv(gym.Env):
   # 利用できるrender_modesを指定するようです
   metadata = {"render_modes": ["ansi", "rgb_array"], "render_fps": 4}

   def __init__(self, render_mode: str or None = None):
      self.render_mode = render_mode
      """
      initで以下2つの変数を定義する必要あり
      spaces.Space型については省略します。

      self.action_space      : アクションが取りうる範囲を指定
      self.observation_space : 状態が取りうる範囲を指定
      """

      self.action_space: spaces.Space = spaces.Discrete(2)
      self.observation_space: spaces.Space = spaces.Box(-1, 1, shape=(1,))

   def reset(self, *, seed=None, options=None)-> tuple[np.ndarray, dict]:
      super().reset(seed=seed)
      """ 1エピソードの最初に実行。（初期化処理を実装）
      return 初期状態, 情報
      """
      return np.array([0], dtype=np.float32), {}

   def step(self, action) -> tuple[np.ndarray, float, bool, bool, dict]:
      """ actionを元に1step進める処理を実装
      return (
            1step後の状態,
            即時報酬,
            予定通り終了したらTrue(terminated),
            予想外で終了したらTrue(truncated),
            情報(任意),
      )
      """
      return np.array([0], dtype=np.float32), 0.0, True, False, {}

   def render(self):
      """
      描画処理を書きます。
      """
      pass