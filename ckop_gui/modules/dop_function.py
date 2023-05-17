import json
from web3 import Web3, middleware, parity, exceptions
from web3.middleware import geth_poa_middleware
import re 
import os

isMiner = False
if os.name == "nt":
    path_default = "D:/Work/MegaProject/MegaProject/ckop_gui/Contract/abi_address/"
else:
    path_default = "/home/ckop_admin/MegaProject/MegaProject/ckop_gui/Contract/abi_address/"


def read_abi(name_file, path = "./abi_address/"):
    with open (path + name_file) as fp:
        abi = json.load(fp)
    return abi

def read_address(name_file, path = "./abi_address/"):
    with open (path + name_file) as fp:
        address = json.load(fp)
    return address

def construct_contracts(path = path_default):
    # path = "D:/Work/MegaProject/MegaProject/Contract/abi_address/"
    addr_struct_0 = read_address("MakeStruct0_address", path)
    addr_struct_1 = read_address("MakeStruct1_address",path)
    addr_teacher_0 = read_address("Teacher_address_0",path)
    addr_teacher_1 = read_address("Teacher_address_1",path)
    addr_student = read_address("Student_address",path)

    abi_struct_0 = read_abi("MakeStruct0_abi",path)
    abi_struct_1 = read_abi("MakeStruct1_abi",path)
    abi_teacher_0 = read_abi("Teacher_abi_0",path)
    abi_teacher_1 = read_abi("Teacher_abi_1",path)
    abi_student = read_abi("Student_abi",path)

    w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    cont_struct_0 = w3.eth.contract(address=addr_struct_0, abi=abi_struct_0)
    cont_struct_1 = w3.eth.contract(address=addr_struct_1, abi=abi_struct_1)
    cont_teacher_0 = w3.eth.contract(address=addr_teacher_0, abi=abi_teacher_0)
    cont_teacher_1 = w3.eth.contract(address=addr_teacher_1, abi=abi_teacher_1)
    cont_student = w3.eth.contract(address=addr_student, abi=abi_student)
    print("Contracts created")
    # w3.geth.miner.set_gas_price('0x0')
    return w3, cont_struct_0, cont_struct_1, cont_teacher_0, cont_teacher_1, cont_student

def miner_geth(w3, bool_mining):
    if not w3.eth.mining and bool_mining:
        w3.geth.miner.start()
    elif not bool_mining:
        w3.geth.miner.stop()
    
    return w3.eth.mining

# def check_email_re(email):
#     # "test_123@test.test"
#     template = '[A-Za-z0-9_]+@[A-Za-z]+[.][A-Za-z]+'

#     if re.fullmatch(template, email) is not None:
#         return True
#     else:
#         return False

def check_email_re(email):
    # # "test_123@test.test"
    # template = '[A-Za-z0-9_]+@[A-Za-z]+[.][A-Za-z]+'

    # if re.fullmatch(template, email) is not None:
    #     return True
    # else:
    #     return False
    return True


def check_len_str(s):
    if len(s)<2:
        return False, "Слишком короткая строка"
    elif len(s)>15:
        return False, "Слишком длинная строка"
    else:
        return True, "Ok"