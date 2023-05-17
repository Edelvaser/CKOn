from web3 import Web3
from web3.middleware import geth_poa_middleware

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
# cont_struct_0 = w3.eth.contract(address=addr_struct_0, abi=abi_struct_0)
# cont_struct_1 = w3.eth.contract(address=addr_struct_1, abi=abi_struct_1)
# cont_teacher = w3.eth.contract(address=addr_teacher, abi=abi_teacher)
# cont_student = w3.eth.contract(address=addr_student, abi=abi_student)
# print("Contracts created")
# w3.geth.miner.set_gas_price('0x0')

for user in w3.eth.accounts:
    w3.geth.personal.unlock_account(user, "1", 1000000)