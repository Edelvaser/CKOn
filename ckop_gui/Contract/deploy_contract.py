from web3 import Web3
from web3.middleware import geth_poa_middleware
from solcx import compile_files
from solcx import install_solc
import json

install_solc(version='latest')

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
w3.geth.miner.set_gas_price('0x0')

addr_owner = w3.eth.accounts[0]
w3.geth.personal.unlock_account("0xff42Fc7fdB5928b63da0bF2340880369fE335bf0", "1")
def compile_source_file(file_path):
    return compile_files(file_path, output_values=['abi', 'bin'], optimize=True) #, optimize_runs=100

contract_source_path = './'

def miner_geth(bool):
    if bool:
        w3.geth.miner.start()
    else:
        w3.geth.miner.stop()

def write_abi(name_file, abi, path = "./abi_address/"):
    with open (path + name_file, "w") as fp:
        json.dump(abi, fp)

def read_abi(name_file, path = "./abi_address/"):
    with open (path + name_file) as fp:
        abi = json.load(fp)
    return abi

def write_address(name_file, address, path = "./abi_address/"):
    with open (path + name_file, "w") as fp:
        json.dump(address, fp)

def read_address(name_file, path = "./abi_address/"):
    with open (path + name_file) as fp:
        address = json.load(fp)
    return address

def deploy_GlobalStorage():
    compiled_sol = compile_source_file(contract_source_path + 'GlobalStorage.sol')
    # contract_id, contract_interface = compiled_sol.popitem()
    contract_interface_abi = compiled_sol["GlobalStorage.sol:GlobalStorage"]["abi"]
    contract_interface_bytecode = compiled_sol["GlobalStorage.sol:GlobalStorage"]["bin"]
    write_abi("GlobalStorage_abi", contract_interface_abi)
    GlobalStorage = w3.eth.contract(abi=contract_interface_abi, bytecode=contract_interface_bytecode)
    tx_hash = GlobalStorage.constructor().transact()
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    addr_storage = tx_receipt.contractAddress
    write_address("GlobalStorage_address", str(addr_storage))
    globalStorage = w3.eth.contract(address=addr_storage,abi=contract_interface_abi)
    print(f'Deployed GlobalStorage to: {addr_storage}\n')
    return addr_storage, globalStorage

def deploy_Makestruct0(addr_storage):
    w3.eth.default_account = w3.eth.accounts[0]
    miner_geth(True)
    compiled_sol = compile_source_file(contract_source_path + 'MakeStruct0.sol')
    # contract_id, contract_interface = compiled_sol.popitem()
    contract_interface_abi = compiled_sol["MakeStruct0.sol:MakeStruct0"]["abi"]
    contract_interface_bytecode = compiled_sol["MakeStruct0.sol:MakeStruct0"]["bin"]
    write_abi("MakeStruct0_abi", contract_interface_abi)
    MakeStruct0 = w3.eth.contract(abi=contract_interface_abi, bytecode=contract_interface_bytecode)
    tx_hash = MakeStruct0.constructor(addr_storage).transact()
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    addr_struct_0 = tx_receipt.contractAddress
    write_address("MakeStruct0_address", str(addr_struct_0))
    makeStruct_0 = w3.eth.contract(address=addr_struct_0,abi=contract_interface_abi)
    print(f'Deployed MakeStruct0 to: {addr_struct_0}\n')

    globalStorage = w3.eth.contract(address=addr_storage,abi=read_abi("GlobalStorage_abi"))

    print("Start add address contract to GlobalStorage")
    tx_hash = globalStorage.functions.setAddressContract(addr_struct_0).transact({'from':addr_owner})
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print("End add address contract to GlobalStorage")

    miner_geth(False)
    return addr_struct_0, makeStruct_0

def deploy_Makestruct1(addr_storage):
    w3.eth.default_account = w3.eth.accounts[0]
    miner_geth(True)
    compiled_sol = compile_source_file(contract_source_path + 'MakeStruct1.sol')
    # contract_id, contract_interface = compiled_sol.popitem()
    contract_interface_abi = compiled_sol["MakeStruct1.sol:MakeStruct1"]["abi"]
    contract_interface_bytecode = compiled_sol["MakeStruct1.sol:MakeStruct1"]["bin"]
    write_abi("MakeStruct1_abi", contract_interface_abi)
    MakeStruct1 = w3.eth.contract(abi=contract_interface_abi, bytecode=contract_interface_bytecode)
    tx_hash = MakeStruct1.constructor(addr_storage).transact()
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    addr_struct_1 = tx_receipt.contractAddress
    write_address("MakeStruct1_address", str(addr_struct_1))
    makeStruct_1 = w3.eth.contract(address=addr_struct_1,abi=contract_interface_abi)
    print(f'Deployed MakeStruct1 to: {addr_struct_1}\n')

    globalStorage = w3.eth.contract(address=addr_storage, abi=read_abi("GlobalStorage_abi"))

    print("Start add address contract to GlobalStorage")
    tx_hash = globalStorage.functions.setAddressContract(addr_struct_1).transact({'from':addr_owner})
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print("End add address contract to GlobalStorage")
    miner_geth(False)
    return addr_struct_1, makeStruct_1

def deploy_Student(addr_storage, addr_struct_0, addr_struct_1):
    w3.eth.default_account = w3.eth.accounts[0]
    miner_geth(True)
    compiled_sol = compile_source_file(contract_source_path + 'Student.sol')
    # contract_id, contract_interface = compiled_sol.popitem()
    contract_interface_abi = compiled_sol["Student.sol:Student"]["abi"]
    contract_interface_bytecode = compiled_sol["Student.sol:Student"]["bin"]
    write_abi("Student_abi", contract_interface_abi)
    Student = w3.eth.contract(abi=contract_interface_abi, bytecode=contract_interface_bytecode)
    tx_hash = Student.constructor(addr_storage, addr_struct_0, addr_struct_1).transact()
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    addr_student = tx_receipt.contractAddress
    write_address("Student_address", str(addr_student))
    student = w3.eth.contract(address=addr_student,abi=contract_interface_abi)
    print(f'Deployed Student to: {addr_student}\n')
    
    makeStruct_0 = w3.eth.contract(address=addr_struct_0, abi=read_abi("MakeStruct0_abi"))
    makeStruct_1 = w3.eth.contract(address=addr_struct_1, abi=read_abi("MakeStruct1_abi"))

    print("Start add address contract to MakeStruct")
    tx_hash = makeStruct_0.functions.setAddressContract(addr_student).transact({'from':addr_owner})
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    tx_hash = makeStruct_1.functions.setAddressContract(addr_student).transact({'from':addr_owner})
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print("End add address contract to MakeStruct")
    
    miner_geth(False)
    return addr_student, student

def deploy_Teacher(addr_storage, addr_struct_0, addr_struct_1):
    w3.eth.default_account = w3.eth.accounts[0]
    miner_geth(True)
    compiled_sol = compile_source_file(contract_source_path + 'Teacher0.sol')
    # contract_id, contract_interface = compiled_sol.popitem()
    contract_interface_abi = compiled_sol["Teacher0.sol:Teacher_0"]["abi"]
    contract_interface_bytecode = compiled_sol["Teacher0.sol:Teacher_0"]["bin"]
    write_abi("Teacher_abi_0", contract_interface_abi)
    Teacher = w3.eth.contract(abi=contract_interface_abi, bytecode=contract_interface_bytecode)
    tx_hash = Teacher.constructor(addr_storage, addr_struct_0, addr_struct_1).transact()
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    addr_teacher_0 = tx_receipt.contractAddress
    write_address("Teacher_address_0", str(addr_teacher_0))
    teacher_0 = w3.eth.contract(address=addr_teacher_0,abi=contract_interface_abi)
    print(f'Deployed Teacher_0 to: {addr_teacher_0}\n')

    compiled_sol = compile_source_file(contract_source_path + 'Teacher1.sol')
    # contract_id, contract_interface = compiled_sol.popitem()
    contract_interface_abi = compiled_sol["Teacher1.sol:Teacher_1"]["abi"]
    contract_interface_bytecode = compiled_sol["Teacher1.sol:Teacher_1"]["bin"]
    write_abi("Teacher_abi_1", contract_interface_abi)
    Teacher = w3.eth.contract(abi=contract_interface_abi, bytecode=contract_interface_bytecode)
    tx_hash = Teacher.constructor(addr_storage, addr_struct_0, addr_struct_1).transact()
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    addr_teacher_1 = tx_receipt.contractAddress
    write_address("Teacher_address_1", str(addr_teacher_1))
    teacher_1 = w3.eth.contract(address=addr_teacher_1,abi=contract_interface_abi)
    print(f'Deployed Teacher_1 to: {addr_teacher_1}\n')

    makeStruct_0 = w3.eth.contract(address=addr_struct_0, abi=read_abi("MakeStruct0_abi"))
    makeStruct_1 = w3.eth.contract(address=addr_struct_1, abi=read_abi("MakeStruct1_abi"))

    print("Start add address contract to MakeStruct")
    tx_hash = makeStruct_0.functions.setAddressContract(addr_teacher_0).transact({'from':addr_owner})
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    tx_hash = makeStruct_1.functions.setAddressContract(addr_teacher_0).transact({'from':addr_owner})
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    tx_hash = makeStruct_0.functions.setAddressContract(addr_teacher_1).transact({'from':addr_owner})
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    tx_hash = makeStruct_1.functions.setAddressContract(addr_teacher_1).transact({'from':addr_owner})
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print("End add address contract to MakeStruct")

    miner_geth(False)
    return addr_teacher_0, addr_teacher_1, teacher_0, teacher_1

def deploy_all(contract_source_path = "./"):
    """
    Деплоит все контракты по очереди: GlobalStorage, MakeStruct0, MakeStruct1, Student, Teacher;
    Записывает все abi в папку по умолчанию abi_address;
    Записывает все адреса контрактов в папку по умолчанию abi_address;
    Прописывает адреса контрактов со структурами в контракте с данными;
    Прописывает адреса контрактов учителя и ученика в контрактах со структурами;
    Заполняет контракт первоначальными данными;
    Возвращает пять объектов контрактов и список адресов всех контрактов
    
    return globalStorage, makeStruct_0, makeStruct_1, student, teacher,\
            [addr_storage, addr_struct_0, addr_struct_1, addr_student, addr_teacher]
    """
    w3.eth.default_account = w3.eth.accounts[0]
    miner_geth(True)

    addr_storage, globalStorage = deploy_GlobalStorage()
    addr_struct_0, makeStruct_0 = deploy_Makestruct0(addr_storage)
    addr_struct_1, makeStruct_1 = deploy_Makestruct1(addr_storage)
    addr_teacher_0, addr_teacher_1, teacher_0, teacher_1 = deploy_Teacher(
            addr_storage, addr_struct_0, addr_struct_1)
    addr_student, student = deploy_Student(addr_storage, addr_struct_0, addr_struct_1)

    miner_geth(True)
    print("Start add data to contract")
    tx_hash = teacher_0.functions.constructData().transact({'from':addr_owner})
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print("End add data to contract")

    miner_geth(False)

    # with open("Contract_address"):

    return globalStorage, makeStruct_0, makeStruct_1, student, teacher_0, teacher_1,\
            [addr_storage, addr_struct_0, addr_struct_1, addr_student, addr_teacher_0, 
            addr_teacher_1]

if __name__ == "__main__":
    s = input("Выберите контракты для деплоя: \n\
0 - деплоить все (GlobalStorage, MakeStruct_s, Teacher, Student) и загружать данные \n\
1 - деплоить начиная с MakeStruct_s (MakeStruct_s, Teacher, Student) \n\
2 - деплоить контракт Учителя (Teacher) \n\
3 - деплоить контракт Ученика (Student) \n\
>>> ")
    if s == "0" or s == "":
        globalStorage, makeStruct_0, makeStruct_1, student, teacher_0, teacher_1, addr_contr = deploy_all()
    elif s == "1":
        addr_storage = read_address("GlobalStorage_address")
        addr_struct_0, makeStruct_0 = deploy_Makestruct0(addr_storage)
        addr_struct_1, makeStruct_1 = deploy_Makestruct1(addr_storage)
        addr_teacher_0, addr_teacher_1, teacher_0, teacher_1 = deploy_Teacher(
                addr_storage, addr_struct_0, addr_struct_1)
        addr_student, student = deploy_Student(addr_storage, addr_struct_0, addr_struct_1)
    elif s == "2":
        addr_storage = read_address("GlobalStorage_address")
        addr_struct_0 = read_address("MakeStruct0_address")
        addr_struct_1 = read_address("MakeStruct1_address")
        addr_teacher_0, addr_teacher_1, teacher_0, teacher_1 = deploy_Teacher(
                addr_storage, addr_struct_0, addr_struct_1)
    elif s == "3":
        addr_storage = read_address("GlobalStorage_address")
        addr_struct_0 = read_address("MakeStruct0_address")
        addr_struct_1 = read_address("MakeStruct1_address")
        addr_student, student = deploy_Student(addr_storage, addr_struct_0, addr_struct_1)
    else:
        print("Попробуй еще раз")
    # globalStorage, makeStruct_0, makeStruct_1, student, teacher, addr_contr = deploy_all("./UseStorage/")


# with open('./Student.sol') as fp:
#     contr = fp.read()
# compiled_sol = compile_files(["Student.sol"], output_values=['abi', 'bin'], optimize=True)
# contract_id, contract_interface = compiled_sol.popitem()
# print(compiled_sol)
# print(compiled_sol["Student.sol:Student"]["abi"])
# print(contract_interface['abi'])
# compile_source_file(file_path, output_values=['abi', 'bin'], optimize=True)