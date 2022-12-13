import base64
import execjs
import pytest
import rsa
import csv
import random
from time import sleep
from urllib import parse



# 要写入的文件名
filename = 'follow_data.csv'
# 随机数据的行数
num_rows = 20000000
# 随机数据的列数
num_cols = 4
# 使用 with 语句打开文件，并创建一个 CSV 写入器
with open(filename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # 循环 num_rows 次，每次生成一行随机数据，并使用写入器写入到文件中
    for i in range(num_rows):
        row = [(random.randint(1, 10000000))] + [random.randint(1, 100) for _ in range(num_cols - 1)]
        writer.writerow(row)
# # base 加密方法
# auth_info = '["{}","{}"]'.format("root","nebula").encode() # Explorer要求 转为数组
# print(auth_info)
# auth_info = base64.b64encode(auth_info)  # 对数组进行加密
# auth = "Bearer "+ auth_info.decode('UTF-8')



# # 公钥rsa 加密方法
# public_key = """-----BEGIN RSA PUBLIC KEY-----
# MIGJAoGBANxHSR4gyaZX7uet7fGzCwqhUcvTYTQpakPDihLkW+e4Ib4kBCd84Ldb
# dI7cziiOk1e6NjMEqnsjs6hOZ0tTPXrE7eKHMR9vwIJW08O0pyGw275DSQLVbP5k
# mlWs0W/pGfnO+sh3apaeLHF86qzkFmS6Q6pjYGTw3jCQy6bOP0F3AgMBAAE=
# -----END RSA PUBLIC KEY-----
# """
# password = 'nebula'
# bp = bytes(public_key, encoding='utf8') # 公钥转为数组
# pk = rsa.PublicKey.load_pkcs1(bp) # 公钥加密
# bh = bytes(password, encoding='utf8')
# m = rsa.encrypt(bh, pk)
# code = base64.b64encode(m).decode('utf-8')
# print(code)

