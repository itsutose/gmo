
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Connect to the SQLite database
conn = sqlite3.connect(r'H:\マイドライブ\pytest\virtual_currency\gmo\gmo_data\board\2023-08-15_board2.db')

# Query the data
asks_data_df = pd.read_sql('SELECT * FROM asks', conn)
bids_data_df = pd.read_sql('SELECT * FROM bids', conn)

# Apply log transformation to the 'size' column
asks_data_df['log_size'] = np.log(asks_data_df['size'] + 1)
bids_data_df['log_size'] = np.log(bids_data_df['size'] + 1)

# Extract time information and generate time in float format
asks_data_df['time'] = asks_data_df['board_data_responsetime'].str.split(' ').str[1].str.split(':').str[:2].str.join(':')
bids_data_df['time'] = bids_data_df['board_data_responsetime'].str.split(' ').str[1].str.split(':').str[:2].str.join(':')
asks_data_df['time_float'] = asks_data_df['time'].str.split(':').apply(lambda x: float(x[0]) + float(x[1])/60)
bids_data_df['time_float'] = bids_data_df['time'].str.split(':').apply(lambda x: float(x[0]) + float(x[1])/60)

# Plotting the data with enhanced color mapping using log transformed 'size' values
fig, ax = plt.subplots(figsize=(16, 10))
sc1 = ax.scatter(asks_data_df['time_float'], asks_data_df['price'], c=asks_data_df['log_size'], cmap='Blues', s=1, label='Asks', alpha=0.6)
sc2 = ax.scatter(bids_data_df['time_float'], bids_data_df['price'], c=bids_data_df['log_size'], cmap='Reds', s=1, label='Bids', alpha=0.6)
cb = plt.colorbar(sc1, ax=ax)
cb.set_label('Log Transformed Total Order Size')
ax.set_title('Distribution of Ask and Bid Orders Over Time with Enhanced Color Mapping')
ax.set_xlabel('Time (HH:MM)')
ax.set_ylabel('Price')
ax.set_xticks(np.arange(min(asks_data_df['time_float']), max(asks_data_df['time_float']) + 1, 0.25))
ax.set_xticklabels([f"{int(tick)}:{int((tick%1)*60):02d}" for tick in ax.get_xticks()])
ax.grid(True)
ax.legend()
plt.show()
