from web3 import Web3
import time

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

t = 0
while w3.isConnected() and t < 20:
    time.sleep(1)
    t += 1
if t>=20 and w3.isConnected():
    print("Error")
else:
    w3.geth.personal.unlock_account(w3.eth.accounts[0], "1")
    print("User unlocked")
input()