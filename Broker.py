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


  def correctDate(self, text):
    splitDate = text.split('/')
    result = '2020-'
    print(splitDate[0])
    if int(splitDate[0]) < 10:
      result += str('0' + splitDate[0] + '-')
    else:
      result += str(splitDate[0] + '-')
    if int(splitDate[1]) < 10:
      result += str('0' + splitDate[1])
    else:
      result += str(splitDate[1])
    return result


  def parserBuyOption(self, messageList):
    #buy SQ 162.50 calls 10/2 @2.50
    option = {}
    splitTemp = messageList
    option['symbol'] = splitTemp[1]
    if splitTemp[3] == 'calls':
      option['optionType'] = 'call'
    elif splitTemp[3] == 'puts':
      option['optionType'] = 'put'
    else:
      option['optionType'] = splitTemp[3]
    option['strike'] = float(splitTemp[2])
    option['expirationDate'] = self.correctDate(splitTemp[4])
    option['price'] = float(splitTemp[5][1:])
    option['amount'] = float(splitTemp[6])
    option['quantity'] = int(round(option['amount']/(option['price']*100), 0))
    print(option)
    return option


  def buyOption(self, messageList):
    option = self.parserBuyOption(messageList)
    try:
      
      # robin_stocks.orders.order_buy_option_limit(4.20, 'MSFT', 1, 2020-03-13, 185.00, optionType='call', timeInForce='gfd')
      #buyOption NFLX 500 calls 10/2 @5.20
      #Buy 5 $150 May 1st, 2020 SPY puts if the price per contract is $1.00. Good until cancelled.
      #robin_stocks.order_buy_option_limit('open','debit',1.00,'SPY',5,'2020-05-01',150,'put','gtc')
      print(option)
      result = r.orders.order_buy_option_limit('open', 'debit', option['price'], option['symbol'], option['quantity'], option['expirationDate'], option['strike'], option['optionType'], timeInForce='gtc')
    except Exception as e:
      print('Error 5: ', e)
      return e

    print('Result 5: ', result)
    return result


  def parserSellOption(self, symb):
    option = {}
    option['symbol'] = symb
    try:
      myoptions = self.getAllOptionOrders()
      position = None
      for pos in myoptions:
        print('debug',pos)
        if pos['Symbol'] == symb:
          position = pos
      option['quantity'] = position['Quantity']
      option['Expire'] = position['Expire']
      price = r.find_options_by_expiration(symb, position['Expire'] ,position['Type'])
      
      for item in price:
        a = float(item['strike_price'])
        b = float(position['Strike'])
        if a == b:
          tempLimPrice = round(float(item['mark_price']),3)
          if tempLimPrice <= 0.01:
            option['limitPrice'] = 0.01
            option['stopPrice'] = 0.01
          else:
            option['limitPrice'] = tempLimPrice
            temp = float(item['mark_price']) - float(item['mark_price']) * .03
            option['stopPrice'] = round(temp,3)
          option['strike'] = item['strike_price']
    except Exception as e:
      print ('Error 7: ', e)
      return e
    return option


  def sellOption(self, messageList):
    option = self.parserSellOption(messageList)
    try:
      print('option:', option)
      result = r.order_sell_option_stop_limit(positionEffect = 'close',creditOrDebit = 'credit',expirationDate = option['Expire'], symbol=option['symbol'],strike = option['strike'],  quantity = option['quantity'],limitPrice = option['limitPrice'],stopPrice =  option['stopPrice'], optionType = 'call' )
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
      result = r.get_open_option_positions()
      my_options = []
      for item in result:
        # gets expiry date using the option_id from returned result
        option_expiry = r.get_option_instrument_data_by_id(item['option_id'], info='expiration_date') 
        strike_price = r.get_option_instrument_data_by_id(item['option_id'], info='strike_price')
        option_type = r.get_option_instrument_data_by_id(item['option_id'], info='type') 
        print()
        # Dict style response
        res2 = {'Symbol': item['chain_symbol'], 
                'Quantity': item['quantity'],
                'Price': item['average_price'],
                'Expire': option_expiry,
                'Strike': strike_price,
                'Type': option_type
                }
        my_options.append(res2)
    except Exception as e:
      print('Error 1: ', e)
      return e 
    return my_options