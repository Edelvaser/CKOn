import pytest
from web3 import Web3
from web3.middleware import geth_poa_middleware
import json

def read_abi(name_file, path = "../ckop_gui/Contract/abi_address/"):
    with open (path + name_file) as fp:
        abi = json.load(fp)
    return abi

def read_address(name_file, path = "../ckop_gui/Contract/abi_address/"):
    with open (path + name_file) as fp:
        address = json.load(fp)
    return address

def unlockUser(w3):
    for user in w3.eth.accounts:
        w3.geth.personal.unlock_account(user, "1", 1000000)

@pytest.fixture()
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
    w3.geth.miner.set_gas_price('0x0')
    unlockUser(w3)
    return w3, cont_struct_0, cont_struct_1, cont_teacher_0, cont_teacher_1, cont_student

@pytest.fixture()
def miner_geth(construct_contracts):
    w3 = construct_contracts[0]
    w3.geth.miner.start()
    
    yield
    
    w3.geth.miner.stop()

@pytest.fixture(scope="module")
def constructData(miner_geth, construct_contracts):
    """"""
    w3, cont_struct_0, cont_teacher = construct_contracts[0], construct_contracts[1], construct_contracts[3]
    labs_befor = cont_struct_0.functions.getLaboratories().call({"from":w3.eth.accounts[0]})
    schSubj_befor = cont_struct_0.functions.getSchSubjects().call({"from":w3.eth.accounts[0]})
    if labs_befor !=list(range(100, 107)) and schSubj_befor !=list(range(7)):
        tx_hash = cont_teacher.functions.constructData().transact({"from":w3.eth.accounts[0]})
        tx_res = w3.eth.wait_for_transaction_receipt(tx_hash)

# w3, cont_struct_0, cont_struct_1, cont_teacher, cont_student = construct_contracts()
@pytest.fixture()
def test_connected(construct_contracts):
    """Проверяем, что сеть запущена и мы подключены"""
    w3 = construct_contracts[0]
    assert w3.isConnected()

@pytest.fixture()
def data_teacher_0():
    return ["testTeacher", "testPassword12", "Иванов Иван Иванович", [0,1], [101]]

@pytest.fixture()
def data_teacher_1():
    return ["test2Teacher", "testPassword12", "Иванов Иван Иванович", [0,1], [101]]

@pytest.fixture()
def data_teacher_2():
    return ["test2Teacher", "testPassword12", "Иванов Иван Иванович", [0,1], [101]]

def clear_address(user, login, w3, cont_struct_0, cont_struct_1, status=2):
    tx_hash = cont_struct_0.functions.setStatusAddress(user, status).transact({"from":w3.eth.accounts[0]})
    tx_res = w3.eth.wait_for_transaction_receipt(tx_hash)
    tx_hash = cont_struct_1.functions.setUserLogin(user, "").transact({"from":w3.eth.accounts[0]})
    tx_res = w3.eth.wait_for_transaction_receipt(tx_hash)
    tx_hash = cont_struct_1.functions.setUserLogin("0x"+"0"*40, login).transact({"from":w3.eth.accounts[0]})
    tx_res = w3.eth.wait_for_transaction_receipt(tx_hash)

def test_check_constructData_labs_schSubj(construct_contracts):
    """Проверка, что школьные предметы и лаборатории есть в системе"""
    w3, cont_struct_0 = construct_contracts[0], construct_contracts[1]
    labs = cont_struct_0.functions.getLaboratories().call({"from":w3.eth.accounts[0]})
    schSubj = cont_struct_0.functions.getSchSubjects().call({"from":w3.eth.accounts[0]})

    assert labs, "Лаборатории пусты"
    assert schSubj, "Школьных предметов нет"
    assert labs == list(range(100, 107)), "Ошибка в списве лабораторий"
    assert schSubj == list(range(7)), "Ошибка в списке школьных предметов"

def test_check_accounts_user(construct_contracts):
    """Проверяем что тестовые аккаунты свободны и в нужных статусах"""
    w3, cont_struct_0 = construct_contracts[0], construct_contracts[1]
    for user in w3.eth.accounts[1:10]:
        status = cont_struct_0.functions.getStatusAddress(user).call({"from":w3.eth.accounts[0]})
        assert status in (2, 5), "Ошибка в статусах учителя"

    for user in w3.eth.accounts[17:]:
        status = cont_struct_0.functions.getStatusAddress(user).call({"from":w3.eth.accounts[0]})
        assert status == 0, "Ошибка в статусах свободных адресов"

def test_successful_registration(construct_contracts, test_connected, data_teacher_0, miner_geth):
    """Проверка возможности учителя зарегистрироваться в системе"""
    w3, cont_struct_0, cont_struct_1, cont_teacher = \
        construct_contracts[0], construct_contracts[1], construct_contracts[2], construct_contracts[3]
    user = w3.eth.accounts[9]
    status = cont_struct_0.functions.getStatusAddress(user).call({"from":user})
    if status != 2:
        clear_address(user, data_teacher_0[0], w3, cont_struct_0, cont_struct_1)
    status = cont_struct_0.functions.getStatusAddress(user).call({"from":user})
    assert status == 2, "Не выполнены стартовые условия. Ошибка в статусе адреса"

    blockNumber = w3.eth.block_number
    tx_hash = cont_teacher.functions.registrationForTeacher(*data_teacher_0).transact({"from":user})
    tx_res = w3.eth.wait_for_transaction_receipt(tx_hash)
    ev = cont_teacher.events.Action.createFilter(fromBlock=blockNumber,toBlock="latest")
    if ev.get_all_entries():
        assert ev.get_all_entries()[0]['args']['text']=="Teacher successfully registered", \
            "Неверное сообщение об ошибке"
    status = cont_struct_0.functions.getStatusAddress(user).call({"from":user})
    assert status == 5, "Неверный статус, учитель должен был быть зарегистрирован"
    login_in_system = cont_struct_0.functions.getUsingAddress(user).call({"from":user})
    assert login_in_system == data_teacher_0[0], "Логин не привязан к адресу"

def test_re_registration_same_data(test_connected, construct_contracts, data_teacher_0, miner_geth):
    """Регистрация по уже зарегистрированному адресу и логину"""
    w3, cont_struct_0, cont_struct_1, cont_teacher = \
        construct_contracts[0], construct_contracts[1], construct_contracts[2], construct_contracts[3]
    user = w3.eth.accounts[9]
    status = cont_struct_0.functions.getStatusAddress(user).call({"from":user})
    assert status == 5, "Не выполнены стартовые условия. Статус пользователя должен быть - зарегистрированный учитель"
    login_in_system = cont_struct_0.functions.getUsingAddress(user).call({"from":user})
    assert login_in_system == data_teacher_0[0], "Не выполнены стартовые условия. Логин должен быть привязан к адресу {0}".format(user)
    
    blockNumber = w3.eth.block_number
    tx_hash = cont_teacher.functions.registrationForTeacher(*data_teacher_0).transact({"from":user})
    tx_res = w3.eth.wait_for_transaction_receipt(tx_hash)
    ev = cont_teacher.events.Action.createFilter(fromBlock=blockNumber,toBlock="latest")
    if ev.get_all_entries():
        assert ev.get_all_entries()[0]['args']['text']=="ERROR: login occupied", "Неверное сообщение об ошибке"
    status = cont_struct_0.functions.getStatusAddress(user).call({"from":user})
    assert status == 5, "Статус не должен был измениться"
    login_in_system = cont_struct_0.functions.getUsingAddress(user).call({"from":user})
    assert login_in_system == data_teacher_0[0], "Логин не привязан к прежнему адресу"

def test_already_registered_address_new_login(test_connected, construct_contracts, data_teacher_1, miner_geth):
    """Регистрация по уже зарегистрированному адресу и не зарегистрированному логину"""
    w3, cont_struct_0, cont_teacher = construct_contracts[0], construct_contracts[1], construct_contracts[3]
    user = w3.eth.accounts[9]
    status = cont_struct_0.functions.getStatusAddress(user).call({"from":user})
    assert status == 5, "Не выполнены стартовые условия. Статус пользователя должен быть - зарегистрированный учитель"
    login_in_system = cont_struct_0.functions.getUsingAddress(user).call({"from":user})
    assert login_in_system != data_teacher_1[0], "Не выполнены стартовые условия. Логин должен быть не привязан к адресу {0}".format(user)

    blockNumber = w3.eth.block_number
    tx_hash = cont_teacher.functions.registrationForTeacher(*data_teacher_1).transact({"from":user})
    tx_res = w3.eth.wait_for_transaction_receipt(tx_hash)
    ev = cont_teacher.events.Action.createFilter(fromBlock=blockNumber,toBlock="latest")
    if ev.get_all_entries():
        assert ev.get_all_entries()[0]['args']['text'] in ("ERROR: address occupied", "ERROR: login occupied"), \
"Неверное сообщение об ошибке"
    status = cont_struct_0.functions.getStatusAddress(user).call({"from":user})
    assert status == 5, "Статус не должен был измениться"
    login_in_system = cont_struct_0.functions.getUsingAddress(user).call({"from":user})
    assert login_in_system != data_teacher_1[0], "Логин не должен быть привязан к этому адресу"

def test_new_address_already_registered_login(test_connected, construct_contracts, data_teacher_0, miner_geth):
    """Регистрация по не зарегистрированному адресу и зарегистрированному логину"""
    w3, cont_struct_0, cont_struct_1, cont_teacher = \
        construct_contracts[0], construct_contracts[1], construct_contracts[2], construct_contracts[3]
    user = w3.eth.accounts[8]
    status = cont_struct_0.functions.getStatusAddress(user).call({"from":user})
    if status != 2:
        clear_address(user, "", w3, cont_struct_0, cont_struct_1)
    status = cont_struct_0.functions.getStatusAddress(user).call({"from":user})

    assert status == 2, "Не выполнены стартовые условия. \
        Статус пользователя должен быть - под регистрацию учителя"
    login_in_system = cont_struct_0.functions.getUsingAddress(user).call({"from":user})
    assert login_in_system != data_teacher_0[0], \
        "Не выполнены стартовые условия. Логин должен быть не привязан к адресу {0}".format(user)

    blockNumber = w3.eth.block_number
    tx_hash = cont_teacher.functions.registrationForTeacher(*data_teacher_0).transact({"from":user})
    tx_res = w3.eth.wait_for_transaction_receipt(tx_hash)
    ev = cont_teacher.events.Action.createFilter(fromBlock=blockNumber,toBlock="latest")
    if ev.get_all_entries():
        assert ev.get_all_entries()[0]['args']['text'] in ("ERROR: address occupied", "ERROR: login occupied"), \
"Неверное сообщение об ошибке"
    status = cont_struct_0.functions.getStatusAddress(user).call({"from":user})
    assert status == 2, "Статус не должен был измениться"
    login_in_system = cont_struct_0.functions.getUsingAddress(user).call({"from":user})
    assert login_in_system != data_teacher_0[0], "Логин не должен быть привязан к этому адресу"

def test_bad_address_not_registered_login(test_connected, construct_contracts, data_teacher_1, miner_geth):
    """Регистрация по несуществующему в системе адресу"""
    w3, cont_struct_0, cont_teacher = construct_contracts[0], construct_contracts[1], construct_contracts[3]
    user = w3.eth.accounts[17]
    status = cont_struct_0.functions.getStatusAddress(user).call({"from":user})
    assert status == 0, "Не выполнены стартовые условия. \
        Статус пользователя должен быть - не в системе"
    login_in_system = cont_struct_0.functions.getUsingAddress(user).call({"from":user})
    assert login_in_system != data_teacher_1[0], \
        "Не выполнены стартовые условия. Логин должен быть не привязан к адресу {0}".format(user)

    blockNumber = w3.eth.block_number
    tx_hash = cont_teacher.functions.registrationForTeacher(*data_teacher_1).transact({"from":user})
    tx_res = w3.eth.wait_for_transaction_receipt(tx_hash)
    ev = cont_teacher.events.Action.createFilter(fromBlock=blockNumber,toBlock="latest")
    if ev.get_all_entries():
        assert ev.get_all_entries()[0]['args']['text'] in ("ERROR: address occupied", "ERROR: login occupied"), \
"Неверное сообщение об ошибке"
    status = cont_struct_0.functions.getStatusAddress(user).call({"from":user})
    assert status == 0, "Статус не должен был измениться"
    login_in_system = cont_struct_0.functions.getUsingAddress(user).call({"from":user})
    assert login_in_system != data_teacher_1[0], "Логин не должен быть привязан к этому адресу"

@pytest.mark.bad_test
# @pytest.mark.skip
def test_empty_password(test_connected, construct_contracts, data_teacher_2, miner_geth):
    """Регистрация с пустым паролем"""
    w3, cont_struct_0, cont_struct_1, cont_teacher = \
        construct_contracts[0], construct_contracts[1], construct_contracts[2], construct_contracts[3]
    user = w3.eth.accounts[8]
    status = cont_struct_0.functions.getStatusAddress(user).call({"from":user})
    if status != 2:
        clear_address(user, data_teacher_2[0], w3, cont_struct_0, cont_struct_1)
    status = cont_struct_0.functions.getStatusAddress(user).call({"from":user})
    assert status == 2, "Не выполнены стартовые условия. \
Статус пользователя должен быть - под регистрацию учителя"
    login_in_system = cont_struct_0.functions.getUsingAddress(user).call({"from":user})
    assert login_in_system != data_teacher_2[0], \
        "Не выполнены стартовые условия. Логин должен быть не привязан к адресу {0}".format(user)

    blockNumber = w3.eth.block_number
    data_teacher_2[1] = ""
    tx_hash = cont_teacher.functions.registrationForTeacher(*data_teacher_2).transact({"from":user})
    tx_res = w3.eth.wait_for_transaction_receipt(tx_hash)
    ev = cont_teacher.events.Action.createFilter(fromBlock=blockNumber,toBlock="latest")
    if ev.get_all_entries():
        assert ev.get_all_entries()[0]['args']['text']=="ERROR: empty password or login", \
            "Неверное сообщение об ошибке"
    status = cont_struct_0.functions.getStatusAddress(user).call({"from":user})
    assert status == 2, "Статус не должен был измениться"
    login_in_system = cont_struct_0.functions.getUsingAddress(user).call({"from":user})
    assert login_in_system != data_teacher_2[0], "Логин не должен быть привязан к этому адресу"