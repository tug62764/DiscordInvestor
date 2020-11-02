# bot.py
import robin_stocks as r


class Broker():
  def __init__(self, **kwargs):
    self.userName = kwargs['userName']
    self.password = kwargs['password']

  def verifyEmail(email):
    if '@' in email:
      return True
    return False

  def login(self):
    try:
      response =  r.login(self.userName, self.password)
      print('response: ', response)
    except Exception as e:
      print('Exceptionnn: ', e)
      return e
    return 'Login Succesful'

  def logout():
    try:
      response =  r.logout()
      print('response: ', response)
    except Exception as e:
      print('Exceptionnn: ', e)
      return e
    return 'Logout Succesful'

  def buyOption(price, symbol, quantity, expirationDate, strike, optionType='both', timeInForce='gfd'):
    try:
      #Buy 5 $150 May 1st, 2020 SPY puts if the price per contract is $1.00. Good until cancelled.
      #robin_stocks.order_buy_option_limit('open','debit',1.00,'SPY',5,'2020-05-01',150,'put','gtc')
      
      result = r.orders.order_buy_option_limit(price, symbol, quantity, expirationDate, strike, optionType, timeInForce)
    except Exception as e:
      print('Error 5: ', e)
      return e

    print('Result 5: ', result)
    return result

  def sellOptionorder_sell_option_stop_limit(positionEffect, creditOrDebit, limitPrice, stopPrice, symbol, quantity, expirationDate, strike, optionType='both', timeInForce='gtc'):
    try:
      result = r.orders.order_sell_option_stop_limit(positionEffect, creditOrDebit, limitPrice, stopPrice, symbol, quantity, expirationDate, strike, optionType, timeInForce)
    except Exception as e:
      print ('Error 6: ', e)
      return e

    print('Result 6: ', result)
    return result


  def sellStock(sell, symbol, quantity):
    try:
      result = r.order_sell_market(symbol, quantity)
    except Exception as e:
      print('Error 4: ', e)
      return e
    print('Result 4: ', result)
    return result


  def buyStock(self, symbol, quantity):
    try:
      result = r.order_buy_market(symbol, quantity)
    except Exception as e:
      print('Error 3: ', e)
      return e

    print('Result 3: ', result)
    return result

  def getAllStockOrders(self):
    print('test2')
    try:
      #result = r.get_all_open_stock_orders()
      result = []
      my_stocks = r.build_holdings()
      for key,value in my_stocks.items():
        print(key,value)
        res = value['name'] + ' ' + value['quantity'] + ' '+ value['percent_change'] + ' ' + value['equity_change']
        result.append(res)
    except Exception as e:
      print('Error 2: ', e)
      return e

    print('Result 2: ', result)
    return result

  def getAllOptionOrders(self):
    try:
      result = r.get_all_open_option_orders()
    except Exception as e:
      print('Error 1: ', e)
      return e

    print('Result 1: ', result)
    return result