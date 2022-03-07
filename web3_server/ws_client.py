
from loguru import logger
from typing import List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import web3


class WsClient:

    def __init__(self):
        self.contract_dict = {}
        self.w3_dict = {}
        self.func_map = {}
        self.id_to_w3_dict = {}
        self.id_to_socket = {}

    def register(self, func):
        self.func_map[func.__name__] = func

    async def receive(self, client_id, data):
        func = self.func_map[data['func']]
        if func:
            await func(client_id, **data['data'])

    async def init_contract(self, address, abi):
        # contract = self.w3.eth.contract(address=address, abi=abi)
        # self.contract_dict[address] = contract
        logger.info(f'init contract to {address} abi:{abi}')

    def get_contract(self, address):
        return self.contract_dict.get(address, None)

    async def init_w3(self, id, uri):
        if uri in self.w3_dict:
            self.id_to_w3_dict[id] = uri
            return
        w3 = web3.Web3(web3.Web3.HTTPProvider(uri))
        self.w3_dict[uri] = w3
        self.id_to_w3_dict[id] = w3

    def connect(self, client_id, socket):
        self.id_to_socket[client_id] = socket

    def disconnect(self, client_id):
        del self.id_to_socket[client_id]
        del self.id_to_w3_dict[client_id]

    def get_w3(self, id):
        return self.id_to_w3_dict[id]


ws_client = WsClient()


@ws_client.register
async def init_contract(client_id, address, abi):
    contract = ws_client.get_contract(address)
    if contract:
        return
    await ws_client.init_contract(address, abi)
