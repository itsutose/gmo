from sqlalchemy import create_engine, MetaData, Table, inspect
import pandas as pd

def dbpd(file_path):
    # Create a connection to the SQLite database
    engine = create_engine(f'sqlite:///{file_path}')
    # engine = create_engine('sqlite://///workspace/gmo_data/ratest_rate/2023-08-20_ratest_rate.db')

    inspector = inspect(engine)
    table_names = inspector.get_table_names()[0]

    # Reflect the trading_history table
    metadata = MetaData()
    trading_history = Table(table_names, metadata, autoload=True, autoload_with=engine)

    # Query all rows of the table
    results = engine.execute(trading_history.select()).fetchall()

    # Convert results to a list of dictionaries for easy viewing
    rows = [dict(row) for row in results]


    # Convert the list of dictionaries to a pandas DataFrame
    df_trading_history = pd.DataFrame(rows).drop('id',axis=1)
    df_trading_history['timestamp'] = pd.to_datetime(df_trading_history['timestamp'])

    return df_trading_history

# db2pd('/workspace/gmo_data/trading_hist/2023-08-19_trading_hist.db')
# db2pd('/workspace/gmo_data/ratest_rate/2023-08-20_ratest_rate.db')

#==================================================================================================

# https://chat.openai.com/c/c66579d0-b358-431a-bd97-e390b24edb96

# trading_hist.dbのtimestampを最小にする

# from funcs import dbpd 
# import pandas as pd
# db_path = r"C:\Users\yamaguchi\MyDocument\gmo_data\trading_hist\2023-08-21_trading_hist.db"

def min_trading_history(db_path):
    tmp = dbpd(db_path)
    tmp['id'] = tmp.index + 1
    tmp

    g = tmp.groupby('timestamp')

    # List to store the final results
    results_list = []

    for key, group in g:
        if len(group) == 1:
            results_list.append(group.iloc[0])
            continue
        
        group_min = group['price'].min()
        group_max = group['price'].max()
        
        if group_max - group_min >= 3000:
            min_row = group[group['price'] == group_min].iloc[0]
            max_row = group[group['price'] == group_max].iloc[0]
            results_list.extend([min_row, max_row])
        else:
            avg_price = group['price'].mean().astype(int)
            sum_size = group['size'].sum()
            
            new_row = group.iloc[0].copy()
            new_row['price'] = avg_price
            new_row['size'] = sum_size
            
            results_list.append(new_row)

    # Combine results from the list into a DataFrame
    result_df = pd.DataFrame(results_list)

    # Resetting the index of the result DataFrame
    result_df.reset_index(drop=True, inplace=True)
    sorted_result = result_df.sort_values(by='id').reset_index(drop=True)
    sorted_result['timestamp'] = pd.to_datetime(sorted_result['timestamp'])

    return sorted_result

# 改善前のやつ
def min_trading_history2(db_path):
    df_trading_history = dbpd(db_path)
    g = df_trading_history.groupby('timestamp')
    # Creating an empty DataFrame for storing the final results
    result_df = pd.DataFrame(columns=df_trading_history.columns)

    for key in g.groups.keys():
        group = g.get_group(key)
        if len(group) == 1:
            result_df = pd.concat([result_df, group])
            continue
        
        group_min = group['price'].min()
        group_min_index = group[group['price'] == group_min].index[0]
        group_max = group['price'].max()
        group_max_index = group[group['price'] == group_max].index[0]
        
        if group_max - group_min >= 3000:
            min_row = df_trading_history.loc[group_min_index]
            max_row = df_trading_history.loc[group_max_index]
            result_df = pd.concat([result_df, pd.DataFrame([min_row, max_row])])
        else:
            avg_price = group['price'].mean().astype(int)
            sum_size = group['size'].sum()
            
            new_row = group.iloc[0].copy()
            new_row['price'] = avg_price
            new_row['size'] = sum_size
            
            result_df = pd.concat([result_df, pd.DataFrame([new_row])])

    # Resetting the index of the result DataFrame
    result_df.reset_index(drop=True, inplace=True)
    sorted_result = result_df.sort_values(by='id').reset_index(drop=True)
    sorted_result['timestamp'] = pd.to_datetime(sorted_result['timestamp'])
    sorted_result.head(20)
    sorted_result

#==================================================================================================

# timestampとpriceがあるものに対して移動平均線の描画

import matplotlib.pyplot as plt

def show_ma(dataframe, *args, ma=True, color=False, df=False):
    import matplotlib.colors as mcolors
    # Convert the 'timestamp' column to datetime format
    dataframe['timestamp'] = pd.to_datetime(dataframe['timestamp'])

    # Sort by date
    dataframe = dataframe.sort_values(by='timestamp')

    # Plotting
    plt.figure(figsize=(15, 7))
    
    # Iterate over each window value provided in args
    for window in args:
        # Calculate moving averages
        dataframe[f'ma{window}'] = dataframe['price'].rolling(window=window, center=True).mean()
        
        # Determine which data to plot based on the ma argument
        if ma:  # Plot moving averages
            # Calculate the slope for coloring
            dataframe[f'slope_ma{window}'] = dataframe[f'ma{window}'].diff()
            
            if color:
                colors = ['red' if x > 0 else 'blue' for x in dataframe[f'slope_ma{window}']]
                plt.scatter(dataframe['timestamp'], dataframe[f'ma{window}'], c=colors, s=1, label=f'{window}-period MA')
            else:
                plt.plot(dataframe['timestamp'], dataframe[f'ma{window}'], label=f'{window}-period MA')
        else:  # Plot the slope of the moving averages
            dataframe[f'slope_ma{window}'] = dataframe[f'ma{window}'].diff()
            plt.plot(dataframe['timestamp'], dataframe[f'slope_ma{window}'], label=f'Slope of {window}-period MA')
        

    if ma:
        plt.title('Moving Averages with Slope Color' if color else 'Moving Averages')
        plt.ylabel('Moving Average')
    else:
        plt.title('Slope of Moving Averages')
        plt.ylabel('Slope')
        
    plt.xlabel('Date and Time')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.xticks(rotation=45)
    plt.show()

    if df == True:
        return dataframe
    

#==================================================================================================

def filter_time(df, start_time, end_time):
    """
    Filter the DataFrame based on a specified time range.
    
    Parameters:
    - df: DataFrame containing the data
    - start_time: The start of the time range (string in the format 'YYYY-MM-DD HH:MM:SS.ssssss')
    - end_time: The end of the time range (string in the format 'YYYY-MM-DD HH:MM:SS.ssssss')
    
    Returns:
    - DataFrame containing the filtered data
    """
    # Convert the strings to datetime format
    start_time = pd.to_datetime(start_time)
    end_time = pd.to_datetime(end_time)
    
    # Filter the DataFrame
    return df[(df['timestamp'] >= start_time) & (df['timestamp'] <= end_time)]

"""    # Example of using the function
    example_start_time = '2023-08-21 00:00:17.000000'
    example_end_time = '2023-08-21 12:01:50.500000'
    tmp = dbpd(r"C:\Users\yamaguchi\MyDocument\gmo_data\trading_hist\2023-08-21_trading_hist.db")
    filtered_data = filter_time(tmp, example_start_time, example_end_time)
    filtered_data
"""