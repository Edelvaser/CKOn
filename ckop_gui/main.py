from app import create_flask_app
from web3 import Web3
# env passs
from modules.secret_key import passs

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

if __name__ == "__main__":
    try:
        w3.geth.personal.unlock_account("0xff42Fc7fdB5928b63da0bF2340880369fE335bf0", 
           passs)
        w3.geth.miner.start()
        print("Start server")
        create_flask_app().run(host="0.0.0.0", debug=True)
    finally:
        print("Stop server")
        w3.geth.miner.stop()