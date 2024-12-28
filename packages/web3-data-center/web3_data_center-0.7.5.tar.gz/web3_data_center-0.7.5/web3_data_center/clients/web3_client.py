from typing import Optional, Any, Dict
from web3 import Web3
from web3.providers import HTTPProvider
from .base_client import BaseClient

class Web3Client(BaseClient):
    """Client for interacting with Web3, wrapping the original Web3 package functionality"""
    
    def __init__(self, config_path: str = "config.yml", use_proxy: bool = False):
        super().__init__('web3', config_path=config_path, use_proxy=use_proxy)
        self._web3: Optional[Web3] = None
        
    @property
    def web3(self) -> Web3:
        """Get or create Web3 instance"""
        if self._web3 is None:
            self._web3 = Web3(HTTPProvider(self.config['api']['web3']['base_url']))
        return self._web3
    
    def __getattr__(self, name: str) -> Any:
        """Forward any undefined attributes to the underlying Web3 instance"""
        return getattr(self.web3, name)
    
    async def get_balance(self, address: str) -> int:
        """Get balance for an address"""
        return self.web3.eth.get_balance(address)
    
    async def get_transaction(self, tx_hash: str) -> Dict[str, Any]:
        """Get transaction details"""
        return dict(self.web3.eth.get_transaction(tx_hash))
    
    async def get_block(self, block_identifier: Any) -> Dict[str, Any]:
        """Get block details"""
        return dict(self.web3.eth.get_block(block_identifier))
    
    async def get_contract(self, address: str, abi: Any) -> Any:
        """Get contract instance"""
        return self.web3.eth.contract(address=address, abi=abi)
    
    def is_connected(self) -> bool:
        """Check if connected to node"""
        return self.web3.is_connected()