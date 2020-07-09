#author:shangzekai

# class obj():
#
#     USER = '123'
#     PWD = '123qwe'
#
#
# r = obj()
# setattr(obj, 'key', 'val')
#
# print(getattr(r, 'USER'))
# print(getattr(r, ''))

# from concurrent.futures import ThreadPoolExecutor
#
# import time
#
# def test(i):
#     time.sleep(2)
#     print(i)
#
# p = ThreadPoolExecutor(10)
#
# for i in range(100):
#     p.submit(test, i)
import hashlib

import requests

####### a.发送一个静态的令牌 ######

# TOKEN = 'fwbqhfebwqhbfheqwhuehuwqre2121'
# response = requests.get('http://127.0.0.1:8200/api/asset.html/', headers = {'TOKEN':TOKEN})
# print(response.text)

####### b. 发送一个动态的令牌 ######
import time

client_key = '549f8ad22475e79dd7c68c6f0a882f04|1545122656.8889768'

response = requests.get('http://127.0.0.1:8200/api/asset.html/', headers = {'TOKEN':client_key})
print(response.text)
