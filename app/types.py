from pydantic import BaseModel

class ContractCall(BaseModel):
    id:int
    contract_name:str
    func:str
    params:list