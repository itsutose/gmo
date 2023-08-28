import test_gmo_trading_hist
import test_gmo_ratest_rate
import datetime
import time
import os


current_path = os.path.abspath(__file__)
drive_letter = os.path.splitdrive(current_path)[0]

# 日にちを取得
date = datetime.datetime.now().strftime("%Y-%m-%d")

# 累計用
ratest_rate = f'sqlite:///{drive_letter.upper()}/マイドライブ/pytest/virtual_currency/gmo/gmo_data/ratest_rate/ratest_rate.db'
# 日にち用
ratest_rate_date = f'sqlite:///{drive_letter.upper()}/マイドライブ/pytest/virtual_currency/gmo/gmo_data/ratest_rate/'+date+'_ratest_rate.db'
# print(ratest_rate_date)

# 累計用
trading_hist = f'sqlite:///{drive_letter.upper()}/マイドライブ/pytest/virtual_currency/gmo/gmo_data/trading_hist/trading_hist.db'
# 日にち用
trading_hist_date = f'sqlite:///{drive_letter.upper()}/マイドライブ/pytest/virtual_currency/gmo/gmo_data/trading_hist/'+date+'_trading_hist.db'
# print(trading_hist_date)

test_gmo_ratest_rate.start_websocket(ratest_rate_date)
print('next func')
time.sleep(1)
test_gmo_trading_hist.start_websocket(trading_hist_date)
print('end')