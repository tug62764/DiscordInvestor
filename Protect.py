import binascii
from Crypto.Cipher import AES

#random password derivation salt to derive encryption key
passwordSalt = b'\xe2\x0e\xfd`\xba\x1f\xccobH/\n\xa9 )p'
secretKey = "s3cr3t*c0d3pnv3q"

def decryptDice(message):
  message = message.decode('utf-8')
  resultList = message.split(' ')
  nonce = binascii.unhexlify(str.encode(resultList[1]))
  ciphertext = binascii.unhexlify(str.encode(resultList[0]))
  
  cipher = AES.new(secretKey.encode('utf-8'), AES.MODE_EAX, nonce=nonce)
  plaintext = cipher.decrypt(ciphertext)
  plaintext = plaintext.decode('utf-8')

  return plaintext


def encryptDice(data):
  cipher = AES.new(secretKey.encode('utf-8'), AES.MODE_EAX)
  iv = binascii.hexlify(cipher.nonce)
  ciphertext, tag = cipher.encrypt_and_digest(data.encode('utf-8'))
  message = binascii.hexlify(ciphertext) + str.encode(" ") + iv
  return message