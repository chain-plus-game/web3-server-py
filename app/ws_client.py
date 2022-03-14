
import json
import aiohttp
from loguru import logger
from web3 import Web3


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
        msg_data = json.loads(data['data'])
        if func:
            res, msg = await func(client_id, **msg_data)
            socket = self.get_socket(client_id)
            if isinstance(res, (dict, list)):
                res = json.dumps(res)
            else:
                res = str(res)
            await socket.send_json({
                'callBack': data['func'],
                'data': res,
                'messsag': msg
            })

    async def init_contract(self, address, contract):
        self.contract_dict[address] = contract

    def get_contract(self, address):
        return self.contract_dict.get(address, None)

    async def init_w3(self, id, uri):
        if uri in self.w3_dict:
            self.id_to_w3_dict[id] = uri
            return True
        # w3 = Web3(provider=Web3.AsyncHTTPProvider(uri),
        #           modules={'eth': (AsyncEth,),
        #                    'net': (AsyncNet,),
        #                    }, middlewares=[])
        w3 = Web3(Web3.HTTPProvider(uri))
        self.w3_dict[uri] = w3
        self.id_to_w3_dict[id] = uri
        connect = w3.isConnected()
        return connect

    def connect(self, client_id, socket):
        self.id_to_socket[client_id] = socket

    def disconnect(self, client_id):
        del self.id_to_socket[client_id]
        del self.id_to_w3_dict[client_id]

    def get_w3(self, id):
        url = self.id_to_w3_dict[id]
        return self.w3_dict[url]

    def get_w3_url(self, id):
        return self.id_to_w3_dict[id]

    def get_socket(self, client_id):
        return self.id_to_socket[client_id]


ws_client = WsClient()


@ws_client.register
async def init_contract(client_id, address, abi_url):
    contract = ws_client.get_contract(address)
    if contract:
        return {}, 'success'
    async with aiohttp.ClientSession() as session:
        async with session.get(abi_url) as response:
            data = await response.text()
            data = json.loads(data)
    abi = data.get('abi', None)
    if abi is None:
        return {}, 'abi not find'
    logger.info(f'init contract to {address} abi:{abi_url}')
    # w3_url = ws_client.get_w3_url(client_id)
    # w3 = Web3(Web3.HTTPProvider(w3_url))
    w3 = ws_client.get_w3(client_id)
    contract = w3.eth.contract(address=address, abi=abi)
    await ws_client.init_contract(address, contract)
    return {'address': address}, 'success'


@ws_client.register
async def call(client_id, to, func, params):
    contract = ws_client.get_contract(to)
    if contract is None:
        return {}, 'contract not find'
    contract_func = contract.functions[func]
    if not contract_func:
        return {}, 'contract func not find'
    sender = contract_func(**params)
    try:
        # w3 = ws_client.get_w3(client_id)
        # res = await w3.eth.call({
        #     'to': to,
        #     'data': sender._encode_transaction_data()
        # })
        res = sender.call()
    except Exception as e:
        return {}, str(e)
    return {
        'data': res
    }, 'success'
