from fastapi import FastAPI
import web3
from loguru import logger
from web3_server.types import ContractCall
from web3_server import abi_temp,address_temp

w3 = web3.Web3(web3.Web3.HTTPProvider('https://data-seed-prebsc-2-s3.binance.org:8545/'))

app = FastAPI()


@app.post("/call")
async def read_item(call:ContractCall):
    abi = abi_temp.get_abi(call.contract_name)
    address = address_temp.get_address(call.contract_name)
    Contract = w3.eth.contract(address=address, abi=abi)
    contract_func = Contract.functions[call.func]
    twentyone = contract_func(*call.params).call()
    return twentyone
