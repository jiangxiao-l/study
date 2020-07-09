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

token = 'fwbqhfebwqhbfheqwhuehuwqre2121'
ctime = time.time()

tmp = "%s|%s" % (token, ctime)

m = hashlib.md5()
m.update(bytes(tmp, encoding='utf-8'))
client_md5_key = m.hexdigest()



client_key = "%s|%s" % (client_md5_key, ctime)

print(client_key)

response = requests.get('http://127.0.0.1:8200/api/asset.html/', headers = {'TOKEN':client_key})
print(response.text)
