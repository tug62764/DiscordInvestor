import robin_stocks as r
# import json
# import Protect as PT
import Broker as BK
from unittest import unittest, patch

from datetime import date, datetime


class TestFunctions(unittest.TestCase):
  
  def __init__(self):
    self.BRService = BK.Broker(userName = 'natan132', password = 'Moneymakingmachine1!')
    response = self.BRService.login()
    print('\n', response, '\n')
  
  def test_login_check_stocks(self):
    response = self.BRService.getAllStockOrders()
    self.assertEquals(response, {})


  def test_buy_parser(self):
    input = '.buy AMZN 3200.00 calls 11/6 @1.25 10'
    option = self.BRService.parserBuyOption(input)
    test_option = {}
    test_option['price'] = 1.25
    test_option['symbol'] = 'AMZN'
    test_option['percent'] = 10
    buyingPower = self.getBuyingPower()
    test_option['amount'] = buyingPower * (option['percent']/100.0)
    test_option['quantity'] = int(round(option['amount']/(option['price']*100.0), 0))
    test_option['Expire'] = '2020-11-06'
    test_option['Strike'] = 3200.00
    test_option['Type'] = 'call'


  def test_correct_date(self):
    test_date = '11/6'
    test_result_date = self.BRService.correctDate(test_date)
    expected_result = '2020-11-06'
    self.assertEquals(expected_result, test_result_date)

  @patch('parserBuyOption')
  def test_buy_option(self, PRS):
    self.test_option = {}
    weeks = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

    self.test_option['symbol'] = 'NOK'
    self.test_option['Type'] = 'call'
    self.test_option['quantity'] = 1

    #Expire
    today = date.today()
    while weeks[today.weekday()] !='Fri':
      today = datetime.today() + datetime.timedelta(days=1)
    self.test_option['Expire'] = str(today.month) + '/' + str(today.day)
    
    #Price
    price_flag = False
    strikes = [4.00, 4.5, 3.5]
    for strike in strikes:
      self.test_option['Strike'] = strike
      items = r.find_options_by_expiration_and_strike(inputSymbols=self.test_option['symbol'], expirationDate=self.test_option['Expire'], optionType=self.test_option['Type'])
      for item in items:
        a = float(item['strike_price']) * 100
        if a <= 6 :
          self.test_option['price'] = round(float(item['mark_price']),3)
          price_flag = True
    self.assertEquals(price_flag, True)
  
    #execute option and validate
    PRS.return_value = self.test_option
    test_result = self.BRService.buyOption('test')
  
    bool_result = self.BRService.validateOptionResponse(test_result)
    self.assertEquals(bool_result, True)

  def test_sell_parser(self):    
    test_result = self.BRService.parserSellOption(self.test_option['symbol'])
    item = self.BRService.getOptionPrice(self.test_option['symbol'], self.self.test_option)
    tempLimPrice = round(float(item['mark_price']),3)
    self.test_option['limitPrice'] = tempLimPrice
    self.assertEquals(test_result, self.test_option)

  @patch('parserSellOption')
  def test_sell_option(self, PSO):
    PSO.return_value = self.test_option
    test_result = self.BRService.sellOption('test')
    bool_result = self.BRService.validateOptionResponse(test_result)
    self.assertEquals(bool_result, True)


    

    

if __name__ == '__main__': 
    unittest.main() 