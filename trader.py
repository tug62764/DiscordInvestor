import robin_stocks as r
import pandas as pd
from datetime import datetime
# from config import *
import numpy as np

e = 'df'
p = 'adsf
'
def login(email, password):
  r.login(email, password)


login(e, p)

data = r.options.find_tradable_options_for_stock('MSFT', optionType='call')
pd.DataFrame(data)

price = 4.50
strike = 183.70
symbol = 'MSFT'
quantity = 1
expirationDate =  '2020-03-13'
optionTY = 'call'
tmf = 'gtd'

r.orders.order_buy_option_limit(price, symbol, quantity, expirationDate, strike, optionType=optionTY, timeInForce=tmf)

