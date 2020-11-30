
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