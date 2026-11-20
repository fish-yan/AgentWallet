import httpx

rpc_url = "https://ethereum-rpc.publicnode.com"

payload = {
    "jsonrpc": "2.0",
    "method": "eth_chainId",
    "params": [],
    "id": 1
}

response = httpx.post(rpc_url, json=payload, timeout=10.0)
response.raise_for_status()

data = response.json()
print("节点响应：", data)

if "error" in data:
    raise RuntimeError(f"RPC调用失败: {data['error']}")

chain_id_hex = data.get("result")
chain_id = int(chain_id_hex, 16)

print(f"链ID: {chain_id} (十进制), {chain_id_hex} (十六进制)")

if chain_id != 1:
    raise RuntimeError(f"链ID不匹配: 预期1, 实际{chain_id}")

print("RPC调用成功，链ID匹配。")