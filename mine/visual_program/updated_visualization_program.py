
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Connect to the SQLite database
conn = sqlite3.connect(r'C:\Users\yamaguchi\MyDocument\gmo_data\board\2023-09-15\2023-09-15-0_board.db')
# conn = sqlite3.connect(r'C:\Users\yamaguchi\MyDocument\pytest\virtual_currency\gmo\mine\visual_program\sample.db')


# Query the data
board_data_df = pd.read_sql_query("SELECT * FROM board_data", conn)
asks_data_df = pd.read_sql('SELECT * FROM asks', conn)
bids_data_df = pd.read_sql('SELECT * FROM bids', conn)

# Apply log transformation to the 'size' column
asks_data_df['log_size'] = np.log(asks_data_df['size'] + 1)
bids_data_df['log_size'] = np.log(bids_data_df['size'] + 1)


# この部分を修正する必要がある
# Extract time information and generate time in float format
# asks_data_df['time'] = asks_data_df['board_data_responsetime'].str.split(' ').str[1].str.split(':').str[:2].str.join(':')
# bids_data_df['time'] = bids_data_df['board_data_responsetime'].str.split(' ').str[1].str.split(':').str[:2].str.join(':')
# asks_data_df['time_float'] = asks_data_df['time'].str.split(':').apply(lambda x: float(x[0]) + float(x[1])/60)
# bids_data_df['time_float'] = bids_data_df['time'].str.split(':').apply(lambda x: float(x[0]) + float(x[1])/60)

# # Plotting the data with enhanced color mapping using log transformed 'size' values
# fig, ax = plt.subplots(figsize=(16, 10))
# sc1 = ax.scatter(asks_data_df['time_float'], asks_data_df['price'], c=asks_data_df['log_size'], cmap='Blues', s=1, label='Asks', alpha=0.6)
# sc2 = ax.scatter(bids_data_df['time_float'], bids_data_df['price'], c=bids_data_df['log_size'], cmap='Reds', s=1, label='Bids', alpha=0.6)
# cb = plt.colorbar(sc1, ax=ax)
# cb.set_label('Log Transformed Total Order Size')
# ax.set_title('Distribution of Ask and Bid Orders Over Time with Enhanced Color Mapping')
# ax.set_xlabel('Time (HH:MM)')
# ax.set_ylabel('Price')
# ax.set_xticks(np.arange(min(asks_data_df['time_float']), max(asks_data_df['time_float']) + 1, 0.25))
# ax.set_xticklabels([f"{int(tick)}:{int((tick%1)*60):02d}" for tick in ax.get_xticks()])
# ax.grid(True)
# ax.legend()
# plt.show()

# 新しく追加
# Convert 'board_data_responsetime' in asks and bids to datetime format
board_data_df['responsetime'] = pd.to_datetime(board_data_df['responsetime'])
asks_data_df['board_data_responsetime'] = pd.to_datetime(asks_data_df['board_data_responsetime'])
bids_data_df['board_data_responsetime'] = pd.to_datetime(bids_data_df['board_data_responsetime'])

# Plotting the data with enhanced color mapping using log transformed 'size' values
fig, ax = plt.subplots(figsize=(16, 10))
sc1 = ax.scatter(asks_data_df['board_data_responsetime'], asks_data_df['price'], c=asks_data_df['log_size'], cmap='Blues', s=1, label='Asks', alpha=0.6)
sc2 = ax.scatter(bids_data_df['board_data_responsetime'], bids_data_df['price'], c=bids_data_df['log_size'], cmap='Reds', s=1, label='Bids', alpha=0.6)

# Adding a colorbar
cb = plt.colorbar(sc1, ax=ax)
cb.set_label('Log Transformed Total Order Size')

# Adding titles and labels
ax.set_title('Distribution of Ask and Bid Orders Over Time with Enhanced Color Mapping')
ax.set_xlabel('Time')
ax.set_ylabel('Price')

# Formatting x-axis to show time in HH:MM format
ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%H:%M'))

# Adding grid and legend
ax.grid(True)
ax.legend()

# Show the plot
plt.show()