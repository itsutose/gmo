import torch

# import gym
import math
import random
import numpy as np
# import matplotlib
# import matplotlib.pyplot as plt
from collections import namedtuple
from itertools import count
from PIL import Image
import os

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torchvision.transforms as T

# env = gym.make('CartPole-v0').unwrapped

# matplotlibの設定
# is_ipython = 'inline' in matplotlib.get_backend()
# if is_ipython:
#   from IPython import display

# plt.ion()

# gpuが使用される場合の設定
device = torch.device("cuda" if torch.cuda.is_available() else "cpu" )

print("CUDA available:" , torch.cuda.is_available())
print("Number of GPUs:", torch.cuda.device_count())
if torch.cuda.is_available():
    print("Current GPU:", torch.cuda.current_device())
    print("GPU name:", torch.cuda.get_device_name(torch.cuda.current_device()))

# googleドライブが A‐Zドライブの頭文字を取得
current_path = os.path.abspath(__file__)
drive_letter = os.path.splitdrive(current_path)[0]

print(drive_letter)
print(os.getcwd())