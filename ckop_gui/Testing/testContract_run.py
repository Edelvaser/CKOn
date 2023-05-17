import unittest
from web3 import Web3
from web3.middleware import geth_poa_middleware
from testDataSet import *
import json

def read_abi(name_file, path = "./Contract/abi_address/"):
    with open (path + name_file) as fp:
        abi = json.load(fp)
    return abi

def read_address(name_file, path = "./Contract/abi_address/"):
    with open (path + name_file) as fp:
        address = json.load(fp)
    return address

def miner_geth(bool):
    if bool:
        w3.geth.miner.start()
    else:
        w3.geth.miner.stop()

# def constructData():
#     labs_befor = cont_struct_0.functions.getLaboratories().call({"from":w3.eth.accounts[0]})
#     schSubj_befor = cont_struct_0.functions.getSchSubjects().call({"from":w3.eth.accounts[0]})
#     if labs_befor !=list(range(100, 107)) and schSubj_befor !=list(range(7)):
#         tx_hash = cont_teacher_0.functions.constructData().transact({"from":w3.eth.accounts[0]})
#         tx_res = w3.eth.wait_for_transaction_receipt(tx_hash)

def unlockUser(w3):
    for user in w3.eth.accounts:
        w3.geth.personal.unlock_account(user, "1", 1000000)

def construct_contracts():
    addr_struct_0 = read_address("MakeStruct0_address")
    addr_struct_1 = read_address("MakeStruct1_address")
    addr_teacher_0 = read_address("Teacher_address_0")
    addr_teacher_1 = read_address("Teacher_address_1")
    addr_student = read_address("Student_address")

    abi_struct_0 = read_abi("MakeStruct0_abi")
    abi_struct_1 = read_abi("MakeStruct1_abi")
    abi_teacher_0 = read_abi("Teacher_abi_0")
    abi_teacher_1 = read_abi("Teacher_abi_1")
    abi_student = read_abi("Student_abi")

    w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    cont_struct_0 = w3.eth.contract(address=addr_struct_0, abi=abi_struct_0)
    cont_struct_1 = w3.eth.contract(address=addr_struct_1, abi=abi_struct_1)
    cont_teacher_0 = w3.eth.contract(address=addr_teacher_0, abi=abi_teacher_0)
    cont_teacher_1 = w3.eth.contract(address=addr_teacher_1, abi=abi_teacher_1)
    cont_student = w3.eth.contract(address=addr_student, abi=abi_student)
    print("Contracts created")
    w3.geth.miner.set_gas_price('0x0')
    unlockUser(w3)
    return w3, cont_struct_0, cont_struct_1, cont_teacher_0, cont_teacher_1, cont_student

# w3, cont_struct_0, cont_struct_1, cont_teacher_0, cont_teacher_1, cont_student = construct_contracts()

# constructData()
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
# w3.middleware_onion.inject(geth_poa_middleware, layer=0)
# cont_struct_0 = w3.eth.contract(address=addr_struct_0, abi=abi_struct_0)
# cont_struct_1 = w3.eth.contract(address=addr_struct_1, abi=abi_struct_1)
# cont_teacher_0 = w3.eth.contract(address=addr_teacher_0, abi=abi_teacher_0)
# cont_teacher_1 = w3.eth.contract(address=addr_teacher_1, abi=abi_teacher_1)
# cont_student = w3.eth.contract(address=addr_student, abi=abi_student)
# print("Contracts created")
# w3.geth.miner.set_gas_price('0x0')
unlockUser(w3)

# if __name__ == "__main__":
#     try:
#         miner_geth(True)
#         # unittest.main()
#     except BaseException as e:
#         print(e)
#     finally:
#         miner_geth(False)
