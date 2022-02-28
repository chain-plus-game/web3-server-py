import requests
import json

temp_dict = {}


def get_abi(contract_name):
    with open('MiracleCard.json','r') as f:
        data = json.loads(f.read())
    return data['abi']
