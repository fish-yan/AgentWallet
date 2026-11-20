import httpx
import re

class RPCError(Exception):
    pass

def _get_evm_quantity(rpc_url: str, method: str, params: list[str]) -> int:
    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": 1
    }
    response = httpx.post(rpc_url, json=payload, timeout=10.0)
    response.raise_for_status()

    try:
        data = response.json()
    except ValueError as error:
        raise RPCError("节点返回的内容不是合法 JSON") from error

    if not isinstance(data, dict):
        raise RPCError("节点返回的内容不是 JSON 对象")

    if data.get("jsonrpc") != "2.0" or data.get("id") != 1:
        raise RPCError(f"节点返回的协议版本或请求编号不匹配")

    if "error" in data:
        raise RPCError("节点返回了 RPC 错误")

    result = data.get("result")

    if not isinstance(result, str):
        raise RPCError("节点返回的数量不是字符串")

    if re.fullmatch(r"0x(?:0|[1-9a-fA-F][0-9a-fA-F]*)", result) is None:
        raise RPCError("节点返回的数量不是合法十六进制格式")

    return int(result, 16)

def get_evm_chain_id(rpc_url: str, expected_chain_id: int) -> int:
    chain_id = _get_evm_quantity(rpc_url, "eth_chainId", [])

    if chain_id != expected_chain_id:
        raise RPCError(f"节点网络不匹配，预期为 {expected_chain_id}，实际为 {chain_id}")

    return chain_id

def get_evm_balance_wei(rpc_url: str, expected_chain_id: int, address: str) -> int:
    get_evm_chain_id(rpc_url, expected_chain_id)
    return _get_evm_quantity(rpc_url, "eth_getBalance", [address, "latest"])

