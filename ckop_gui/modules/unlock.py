from web3 import Web3, middleware, parity, exceptions
from web3.middleware import geth_poa_middleware



w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)


w3.geth.personal.unlock_account('0xA8368d91ce67D60b9e1288eB2ba2555C0e09EE94', '1', 1000000)
w3.geth.personal.unlock_account('0x52a0024cB03CCB7B787eba15A6f7FF7EF2fCE3f9', '1', 1000000)
w3.geth.personal.unlock_account('0xE2449a03bFa5A89dA6295EB6547e91A15c63Ac8B', '1', 1000000)
w3.geth.personal.unlock_account('0xD08270D7cFd9b50A6E94b40c95175acD9A62c234', '1', 1000000)



