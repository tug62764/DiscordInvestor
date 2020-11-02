import unittest
import threadMain as TM

class TestStringMethods(unittest.TestCase):
  def test_verifyEmail(self, email):
    emailTest = 'example@gmail.com'
    result = TM.verifyEmail(emailTest)
    self.assertEqual(result,True)

  if __name__ == '__main__':
    print('testinggg')
    unittest.main()