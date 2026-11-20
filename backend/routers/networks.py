import re

from fastapi import APIRouter, HTTPException
import httpx
from services.amounts import format_wei_as_eth
from models import ChainIDResponse, Network, BalanceResponse
from network_data import networks
from services.ethereum import RPCError, get_evm_chain_id, get_evm_balance_wei
from config import EVM_RPC_CONFIGS

router = APIRouter(prefix="/networks", tags=["networks"])

@router.get("", response_model=list[Network])
def get_networks(is_testnet: bool | None = None):
    if is_testnet is None:
        return networks
    filtered_networks = []
    for network in networks:
        if network.is_testnet == is_testnet:
            filtered_networks.append(network)
    return filtered_networks

@router.get("/{network_id}", response_model=Network)
def get_network(network_id: str):
    for network in networks:
        if network.id == network_id:
            return network
    raise HTTPException(status_code=404, detail="Network not found")

@router.get("/{network_id}/chain-id", response_model=ChainIDResponse)
def get_mainnet_chain_id(network_id: str):
    rpc_config = EVM_RPC_CONFIGS.get(network_id)

    if rpc_config is None:
        raise HTTPException(
            status_code=404,
            detail="未找到该网络的 EVM RPC 配置",
        )
    
    try:
        chain_id = get_evm_chain_id(
            rpc_url=rpc_config.rpc_url,
            expected_chain_id=rpc_config.expected_chain_id
        )
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Ethereum 节点请求超时")
    except httpx.RequestError:
        raise HTTPException(status_code=502, detail="无法完成 Ethereum 节点请求")
    except httpx.HTTPStatusError:
        raise HTTPException(status_code=502, detail="Ethereum 节点返回 HTTP 错误")
    except RPCError as error:
        raise HTTPException(status_code=502, detail=str(error))
    
    return ChainIDResponse(
        network_id="ethereum-mainnet", 
        chain_id=chain_id
    )

@router.get("/{network_id}/balance", response_model=BalanceResponse)
def get_network_balance(network_id: str, address: str):
    rpc_config = EVM_RPC_CONFIGS.get(network_id)
    
    if rpc_config is None:
        raise HTTPException(status_code=404, detail="未找到该网络的 EVM RPC 配置")

    if re.fullmatch(r"^0x[a-fA-F0-9]{40}$", address) is None:
        raise HTTPException(status_code=400, detail="无效的以太坊地址格式")

    try:
        balance_wei = get_evm_balance_wei(
            rpc_url=rpc_config.rpc_url,
            expected_chain_id=rpc_config.expected_chain_id,
            address=address
        )
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Ethereum 节点请求超时")
    except httpx.RequestError:
        raise HTTPException(status_code=502, detail="无法完成 Ethereum 节点请求")
    except httpx.HTTPStatusError:
        raise HTTPException(status_code=502, detail="Ethereum 节点返回 HTTP 错误")
    except RPCError as error:
        raise HTTPException(status_code=502, detail=str(error))

    return BalanceResponse(
        network_id=network_id,
        address=address,
        balance_wei=balance_wei,
        balance_eth=format_wei_as_eth(balance_wei),
        decimals=18,
        native_symbol="ETH"
    )