
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Connect to the SQLite database
conn = sqlite3.connect(r'H:\マイドライブ\pytest\virtual_currency\gmo\gmo_data\board\2023-08-15_board2.db')

# Query the data
board_data_df = pd.read_sql_query("SELECT * FROM board_data", conn)
asks_data_df = pd.read_sql('SELECT * FROM asks', conn)
bids_data_df = pd.read_sql('SELECT * FROM bids', conn)

# Convert time data from string to datetime
asks_data_df['responsetime'] = pd.to_datetime(asks_data_df['board_data_responsetime'])
bids_data_df['responsetime'] = pd.to_datetime(bids_data_df['board_data_responsetime'])

# Extracting only the hour and minute from the datetime for plotting purposes
asks_data_df['time'] = asks_data_df['responsetime'].dt.strftime('%H:%M')
bids_data_df['time'] = bids_data_df['responsetime'].dt.strftime('%H:%M')

# Convert the time strings to a float representation
asks_data_df['time_float'] = asks_data_df['time'].str.split(':').apply(lambda x: float(x[0]) + float(x[1])/60)
bids_data_df['time_float'] = bids_data_df['time'].str.split(':').apply(lambda x: float(x[0]) + float(x[1])/60)

# Adjusting the x-axis ticks to show hours in HH:MM format
fig, ax = plt.subplots(figsize=(16, 10))

# Plotting the asks using scatter plot (with Blues color map)
sc1 = ax.scatter(asks_data_df['time_float'], asks_data_df['price'], c=asks_data_df['size'], cmap='Blues', s=10, label='Asks', alpha=0.)

# Plotting the bids using scatter plot (with Reds color map)
sc2 = ax.scatter(bids_data_df['time_float'], bids_data_df['price'], c=bids_data_df['size'], cmap='Reds', s=10, label='Bids', alpha=0.6)

cb = plt.colorbar(sc1, ax=ax)
cb.set_label('Total Order Size')

ax.set_title('Distribution of Ask and Bid Orders Over Time')
ax.set_xlabel('Time (HH:MM)')
ax.set_ylabel('Price')

# Setting the ticks to show hours and minutes
ax.set_xticks(np.arange(min(asks_data_df['time_float']), max(asks_data_df['time_float']) + 1, 0.25))
ax.set_xticklabels([f"{int(tick)}:{int((tick%1)*60):02d}" for tick in ax.get_xticks()])

ax.grid(True)
ax.legend()

# Display the plot
plt.show()
