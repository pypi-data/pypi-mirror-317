from SajadEnc import hk
import time
import os

file = input('Path File : ')

print('Wait For Encryption ')
time.sleep(3)

with open(file, 'r') as file:
    code = file.read()

enco = hk(code)
os.system('clear')
input(enco + '\n')