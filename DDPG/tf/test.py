import tensorflow as tf

# GPUが利用可能か確認
if tf.config.list_physical_devices('GPU'):
    print("GPU is available.")
else:
    print("GPU is not available.")
