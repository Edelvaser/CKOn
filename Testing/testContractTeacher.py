import unittest
from web3 import Web3
from web3.middleware import geth_poa_middleware
# from abi import abi_struct_0, abi_struct_1, abi_teacher, abi_student
# from addresses import addr_struct_0, addr_struct_1, addr_teacher, addr_student
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

def constructData():
    labs_befor = cont_struct_0.functions.getLaboratories().call({"from":w3.eth.accounts[0]})
    schSubj_befor = cont_struct_0.functions.getSchSubjects().call({"from":w3.eth.accounts[0]})
    if labs_befor !=list(range(100, 107)) and schSubj_befor !=list(range(7)):
        miner_geth(True)
        tx_hash = cont_teacher.functions.constructData().transact({"from":w3.eth.accounts[0]})
        tx_res = w3.eth.waitForTransactionReceipt(tx_hash)
        miner_geth(False)

def unlockUser():
    for user in w3.eth.accounts:
        w3.geth.personal.unlock_account(user, "1", 1000000)


def construct_contracts():
    addr_struct_0 = read_address("MakeStruct0_address")
    addr_struct_1 = read_address("MakeStruct1_address")
    addr_teacher = read_address("Teacher_address")
    addr_student = read_address("Student_address")

    abi_struct_0 = read_abi("MakeStruct0_abi")
    abi_struct_1 = read_abi("MakeStruct1_abi")
    abi_teacher = read_abi("Teacher_abi")
    abi_student = read_abi("Student_abi")

    w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    cont_struct_0 = w3.eth.contract(address=addr_struct_0, abi=abi_struct_0)
    cont_struct_1 = w3.eth.contract(address=addr_struct_1, abi=abi_struct_1)
    cont_teacher = w3.eth.contract(address=addr_teacher, abi=abi_teacher)
    cont_student = w3.eth.contract(address=addr_student, abi=abi_student)
    print("Contracts created")
    w3.geth.miner.set_gas_price('0x0')
    unlockUser()
    return w3, cont_struct_0, cont_struct_1, cont_teacher, cont_student

w3, cont_struct_0, cont_struct_1, cont_teacher, cont_student = construct_contracts()

constructData()


def clear_address(user, login):
    miner_geth(True)
    tx_hash = cont_struct_0.functions.setStatusAddress(user, 2).transact({"from":w3.eth.accounts[0]})
    tx_res = w3.eth.waitForTransactionReceipt(tx_hash)
    tx_hash = cont_struct_1.functions.setUserLogin(user, "").transact({"from":w3.eth.accounts[0]})
    tx_res = w3.eth.waitForTransactionReceipt(tx_hash)
    tx_hash = cont_struct_1.functions.setUserLogin("0x"+"0"*40, login).transact({"from":w3.eth.accounts[0]})
    tx_res = w3.eth.waitForTransactionReceipt(tx_hash)
    miner_geth(False)



class TestSum(unittest.TestCase):
    def test_connected(self):
        self.assertTrue(w3.isConnected(), "Chain is not connected")

    def test_check_constructData_labs_schSubj(self):
        labs = cont_struct_0.functions.getLaboratories().call({"from":w3.eth.accounts[0]})
        schSubj = cont_struct_0.functions.getSchSubjects().call({"from":w3.eth.accounts[0]})
        self.assertTrue(labs, "Labs are not full")
        self.assertTrue(schSubj, "School subjects are not full")

        self.assertEqual(labs, list(range(100, 107)), "Error in labs list")
        self.assertEqual(schSubj, list(range(7)), "Error in school subjects list")

    def test_check_accounts_user(self):
        for user in w3.eth.accounts[1:10]:
            status = cont_struct_0.functions.getStatusAddress(user).call({"from":w3.eth.accounts[0]})
            self.assertTrue(status in (2, 5), "Error in status Teacher")
        
        for user in w3.eth.accounts[10:17]:
            status = cont_struct_0.functions.getStatusAddress(user).call({"from":w3.eth.accounts[0]})
            self.assertTrue(status in (3, 6), "Error in status Teacher")

        for user in w3.eth.accounts[17:]:
            status = cont_struct_0.functions.getStatusAddress(user).call({"from":w3.eth.accounts[0]})
            self.assertEqual(status, 0, "Error in status empty User")

    def test_check_register_wrong(self):
        user = w3.eth.accounts[9]
        login = "tester_0"
        status = cont_struct_0.functions.getStatusAddress(user).call({"from":user})
        if status != 2:
            clear_address(user, login)
        status = cont_struct_0.functions.getStatusAddress(user).call({"from":user})
        self.assertEqual(status, 2, "Error in status Teacher")
        miner_geth(True)
        for data in regTeacher_wrong[:-1]:
            blockNumber = w3.eth.block_number
            tx_hash = cont_teacher.functions.registrationForTeacher(*data).transact({"from":user})
            tx_res = w3.eth.waitForTransactionReceipt(tx_hash)
            ev = cont_teacher.events.Action.createFilter(fromBlock=blockNumber,toBlock="latest")
            if ev.get_all_entries():
                # print(ev.get_all_entries()[0]['blockNumber'])
                print(ev.get_all_entries()[0]['args']['text'])
                # self.assertEqual(ev.get_all_entries()[0]['args']['text'], 2, "Error in message")
            status = cont_struct_0.functions.getStatusAddress(user).call({"from":user})
            self.assertEqual(status, 2, "The teacher didn't have to register")
        tx_hash = cont_teacher.functions.registrationForTeacher(*regTeacher_wrong[-1]).transact(
                {"from":user})
        tx_res = w3.eth.waitForTransactionReceipt(tx_hash)
        ev = cont_teacher.events.Action.createFilter(fromBlock=blockNumber,toBlock="latest")
        if ev.get_all_entries():
            print(ev.get_all_entries()[0]['args']['text'])
        status = cont_struct_0.functions.getStatusAddress(user).call({"from":user})
        self.assertEqual(status, 5, "The teacher did have to register")
        miner_geth(False)
        clear_address(user, login)

    def test_check_register_ok(self):
        user = w3.eth.accounts[9]
        status = cont_struct_0.functions.getStatusAddress(user).call({"from":user})
        if status != 2:
            miner_geth(True)
            tx_hash = cont_struct_0.functions.setStatusAddress(user, 2).transact({"from":w3.eth.accounts[0]})
            tx_res = w3.eth.waitForTransactionReceipt(tx_hash)
            miner_geth(False)
        miner_geth(True)
        status = cont_struct_0.functions.getStatusAddress(user).call({"from":user})
        self.assertEqual(status, 2, "Error in status Teacher")
        for data in regTeacher_wrong:
            blockNumber = w3.eth.block_number
            tx_hash = cont_teacher.functions.registrationForTeacher(*data).transact({"from":w3.eth.accounts[8]})
            tx_res = w3.eth.waitForTransactionReceipt(tx_hash)
            ev = cont_teacher.events.Action.createFilter(fromBlock=blockNumber,toBlock="latest")
            if ev.get_all_entries():
                # print(ev.get_all_entries()[0]['blockNumber'])
                print(ev.get_all_entries()[0]['args']['text'])
                # self.assertEqual(ev.get_all_entries()[0]['args']['text'], 2, "Error in message")
            status = cont_struct_0.functions.getStatusAddress(user).call({"from":user})
            self.assertEqual(status, 2, "The teacher didn't have to register")
        miner_geth(False)



if __name__ == "__main__":
    unittest.main()
