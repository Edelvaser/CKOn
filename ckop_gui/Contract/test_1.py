from web3 import Web3
from web3.middleware import geth_poa_middleware
import json

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
w3.geth.miner.set_gas_price('0x0')

w3.ens.address()