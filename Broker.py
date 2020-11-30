# bot.py
import robin_stocks as r
import json
from datetime import date, datetime
# import Protect as PT

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


  def logout(self):
    try:
      response =  r.logout()
      print('response: ', response)
    except Exception as e:
      print('Exceptionnn: ', e)
      return e
    return 'Logout Succesful'


  def buyOption(self, messageList):
    option = self.parserBuyOption(messageList)
    try:
      result = r.orders.order_buy_option_limit('open', 'debit', option['price'], option['symbol'], option['quantity'], option['Expire'], option['Strike'], option['Type'], timeInForce='gtc')
    except Exception as e:
      print('Error 5: ', e)
      return e

    print('Result 5: ', result)
    return result


  def sellOption(self, messageList):
    option = self.parserSellOption(messageList)
    try:
      result = r.order_sell_option_limit(positionEffect = 'close',creditOrDebit = 'credit',expirationDate = option['Expire'], symbol=option['symbol'],strike = option['Strike'],  quantity = option['quantity'],price = option['limitPrice'], optionType = option['Type'] )
    except Exception as e:
      print ('Error 6: ', e)
      return e

    print('Result 6: ', result)
    return result


  def getAllStockOrders(self):
    try:
      result = []
      my_stocks = r.build_holdings()
      for key,value in my_stocks.items():
        res = value['name'] + ' ' + value['quantity'] + ' '+ value['percent_change'] + ' ' + value['equity_change']
        result.append(res)
    except Exception as e:
      print('Error 2: ', e)
      return e
    return result


  def getOpenOptionOrders(self):
    try:
      result = r.robin_stocks.options.get_open_option_positions()
      my_options = []
      for item in result:
        # gets expiry date using the option_id from returned result
        option_expiry = r.get_option_instrument_data_by_id(item['option_id'], info='expiration_date')
        strike_price = r.get_option_instrument_data_by_id(item['option_id'], info='strike_price')
        option_type = r.get_option_instrument_data_by_id(item['option_id'], info='type')
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



  def getAllOptionOrders(self):
    try:
      result = r.get_open_option_positions()
      my_options = []
      for item in result:
        # gets expiry date using the option_id from returned result
        option_expiry = r.get_option_instrument_data_by_id(item['option_id'], info='expiration_date')
        strike_price = r.get_option_instrument_data_by_id(item['option_id'], info='strike_price')
        option_type = r.get_option_instrument_data_by_id(item['option_id'], info='type')
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


  def help(self):
    #buy tgt 157.50 11/6 calls @1.90
    result = []
    # item1 = 'These are the list of commands with appropriate formatting'
    item2 = 'Buy Option: **.buy AMZN 3200.00 calls 11/6 @1.25 4000**'
    item3 = '\nSell Option: **.sell AMZN**'
    item4 = '\nShow Options: **.options**'
    # result = [item2, item3, item4]
    result = item2 +item3+ item4
    return result


  def getBuyingPower(self):
    try:
      buying_power = r.load_account_profile('buying_power')
      buying_power = round(float(buying_power),0)
    except Exception as e:
      print('Error 1: ', e)
      return e
    return buying_power

  def splitBuy(self, messageList):
    # .buy AMZN 3200.00 calls 11/6 @1.25 4000
    option = {}
    splitTemp = messageList
    option['symbol'] = splitTemp[1]
    option['Strike'] = float(splitTemp[2])

    if splitTemp[3] == 'calls' or splitTemp[3] ==  'call':
      option['Type'] = 'call'
    elif splitTemp[3] == 'puts' or splitTemp[3] == 'put':
      option['Type'] = 'put'
    else:
      option['Expire'] = self.correctDate(splitTemp[3])

    if splitTemp[4] == 'calls' or splitTemp[4] ==  'call':
      option['Type'] = 'call'
    elif splitTemp[4] == 'puts' or splitTemp[4] == 'put':
      option['Type'] = 'put'
    else:
      option['Expire'] = self.correctDate(splitTemp[4])

    if splitTemp[5][0] == '@':
      option['price'] = float(splitTemp[5][1:])
      option['percent'] = float(splitTemp[6])
    else:
       option['percent'] = float(splitTemp[5])
       option['price'] = None
    return option

  def parserBuyOption(self, messageList):
    #buy SQ 162.50 calls 10/2 @2.50
    #buy tgt 157.50 11/6 calls @1.90
    option =self.splitBuy(messageList)
    print(option)
    # option['amount'] = float(splitTemp[6])
    # option['quantity'] = int(round(option['amount']/(option['price']*100), 0))
    try:
      item = self.getOptionPrice(option['symbol'], option)
      print('\n debug:', item)
      tempLimPrice = round(float(item['mark_price']),3)
    except Exception as e:
      raise e('Error while getting current option price. Try again')

    if option['price'] == None:
      option['price'] = round(tempLimPrice,2)
    else:
      difference = abs(tempLimPrice - option['price'])
      diffPercent = (difference*100)/option['price']
      if diffPercent < 5:
        option['price'] = round(tempLimPrice,2)
      else:
        # Give an error message to the user with the new price of the option
        raise Exception('Your option is no longer available at that price. ')
    
    buyingPower = self.getBuyingPower()
    print(type(buyingPower), buyingPower, float(buyingPower))
    option['amount'] = buyingPower * (option['percent']/100.0)
    option['quantity'] = int(round(option['amount']/(option['price']*100.0), 0))
    print(option)
    return option


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

  def getOptionPrice(self, symb, position):  

    # print(symb, position['Expire'], position['Type'], position['Strike'])

    item = r.find_options_by_expiration_and_strike(inputSymbols=symb,
                                                    expirationDate=position['Expire'],
                                                    strikePrice=position['Strike'],
                                                    optionType=position['Type'])
    
    return item[0]


  def parserSellOption(self, symb):

    option = {}
    option['symbol'] = symb
    try:
      myoptions = self.getAllOptionOrders()
      position = None
      for pos in myoptions:
        if pos['Symbol'] == symb:
          position = pos
      option['quantity'] = position['Quantity']
      option['Expire'] = position['Expire']
      option['Type'] = position['Type']
      option['Strike'] = position['Strike']
      item = self.getOptionPrice(symb, option)
      tempLimPrice = round(float(item['mark_price']),2)
      if tempLimPrice <= 0.01:
        option['limitPrice'] = 0.01
        option['stopPrice'] = 0.01
      else:
        option['limitPrice'] = tempLimPrice
        temp = float(item['mark_price']) - float(item['mark_price']) * .03
        option['stopPrice'] = round(temp,2)
    except Exception as e:
      print ('Error 7: ', e)
      return e
    return option

  def getDict(self):
    f = open('parse.json', 'r')
    # distros_dict = json.load(f)
    val = f.read()
    val = val.replace('\'', '\"')
    val = val.replace(' ', '')
    val = val.replace('\t','')
    val = val.replace('\n','')
    print(val)
    data = json.loads(val)

    # p = re.compile('(?<!\\\\)\'')
    # str = p.sub('\"', str)
    #
    # s = f.read()
    # s = s.replace('\t','')

  def getDayTradeLimit(self):
    try:
      dayTrade = r.profiles.load_account_profile()
      print(dayTrade)
    except Exception as e:
      print ('Error 7: ', e)
      return e
    return dayTrade

  def validateOptionResponse(self,val):
    val = dict(val)
    if 'cancel_url' in val:
      return True
    return False
