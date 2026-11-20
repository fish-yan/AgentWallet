import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(dotenv_path=BASE_DIR / ".env", override=False)

ETHEREUM_RPC_URL = os.getenv("ETHEREUM_RPC_URL", "").strip()
SEPOLIA_RPC_URL = os.getenv("SEPOLIA_RPC_URL", "").strip()

if not ETHEREUM_RPC_URL:
    raise RuntimeError("ETHEREUM_RPC_URL 环境变量未设置或为空")

if not SEPOLIA_RPC_URL:
    raise RuntimeError("缺少环境变量 SEPOLIA_RPC_URL")

class EVMRPCConfig(BaseModel):
    rpc_url: str
    expected_chain_id: int

EVM_RPC_CONFIGS: dict[str, EVMRPCConfig] = {
    "ethereum-mainnet": EVMRPCConfig(rpc_url=ETHEREUM_RPC_URL, expected_chain_id=1),
    "ethereum-sepolia": EVMRPCConfig(rpc_url=SEPOLIA_RPC_URL, expected_chain_id=11155111),
}