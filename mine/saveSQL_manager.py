import test_gmo_ratest_rate
import test_gmo_trading_hist
import datetime

# 日にちを取得
date = datetime.datetime.now().strftime("%Y-%m-%d")

# 累計用
ratest_rate = 'sqlite:///I:/マイドライブ/pytest/virtual_currency/gmo/gmo_data/ratest_rate/ratest_rate.db'
# 日にち用
ratest_rate_date = 'sqlite:///I:/マイドライブ/pytest/virtual_currency/gmo/gmo_data/ratest_rate/'+date+'_ratest_rate.db'

test_gmo_ratest_rate.run_ws(ratest_rate_date)