import re
import httpx

from config import EVM_RPC_CONFIGS
from services.ethereum import get_evm_chain_id

rpc_config = EVM_RPC_CONFIGS.get("ethereum-mainnet")

assert rpc_config is not None
get_evm_chain_id(
    rpc_url=rpc_config.rpc_url,
    expected_chain_id=rpc_config.expected_chain_id
)

contract_address = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"

payload = {
    "jsonrpc": "2.0",
    "method": "eth_call",
    "params": [
        {
            "to": contract_address,
            "data": "0x313ce567",
        },
        "latest",
    ],
    "id": 1,
}

respinse = httpx.post(rpc_config.rpc_url, json=payload, timeout=10.0)
respinse.raise_for_status()

data = respinse.json()
print("节点响应：", data)

if not isinstance(data, dict):
    raise RuntimeError("节点返回的内容不是 JSON 对象")  

if data.get("jsonrpc") != "2.0" or data.get("id") != 1:
    raise RuntimeError("节点返回的协议版本或请求编号不匹配")

if "error" in data:
    raise RuntimeError(f"RPC调用失败: {data['error']}")

result = data.get("result")

if not isinstance(result, str):
    raise RuntimeError("节点返回的结果不是字符串")

if re.fullmatch(r"0x[0-9a-fA-F]{64}", result) is None:
        raise RuntimeError("预期合约返回一个 32 字节的 ABI 数据")

decimals = int(result, 16)

if decimals > 255:
    raise RuntimeError(f"合约返回的精度不合法: {decimals}")

print(f"合约 {contract_address} 的精度为: {decimals}")