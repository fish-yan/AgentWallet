from models import Network

networks = [
    Network(
        id="ethereum-mainnet", 
        name="Ethereum", 
        family="EVM", 
        native_symbol="ETH", 
        is_testnet=False
    ),
    Network(
        id="ethereum-sepolia", 
        name="Sepolia", 
        family="EVM", 
        native_symbol="ETH", 
        is_testnet=True
    )
]