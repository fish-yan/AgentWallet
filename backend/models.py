from pydantic import BaseModel

class Network(BaseModel):
    id: str
    name: str
    family: str
    native_symbol: str
    is_testnet: bool

class ChainIDResponse(BaseModel):
    network_id: str
    chain_id: int

class BalanceResponse(BaseModel):
    network_id: str
    address: str
    balance_wei: int
    balance_eth: str
    decimals: int
    native_symbol: str