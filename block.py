import hashlib
import json
import time
from typing import List, Dict, Any


class Block:
    """Represents a single block in the blockchain."""

    def __init__(self, index: int, transactions: List[Dict], previous_hash: str, timestamp: float = None):
        """
        Initialize a new block.

        Args:
            index: Position of the block in the chain
            transactions: List of transactions in this block
            previous_hash: Hash of the previous block
            timestamp: Block creation time (defaults to current time)
        """
        self.index = index
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.timestamp = timestamp or time.time()
        self.nonce = 0
        self.hash = None

    def calculate_hash(self) -> str:
        """
        Calculate the SHA-256 hash of the block.

        Returns:
            The hexadecimal hash string
        """
        block_data = {
            'index': self.index,
            'transactions': self.transactions,
            'previous_hash': self.previous_hash,
            'timestamp': self.timestamp,
            'nonce': self.nonce
        }
        block_string = json.dumps(block_data, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty: int) -> None:
        """
        Mine the block by finding a hash with the required difficulty.

        Proof of Work: Find a nonce such that the hash starts with
        'difficulty' number of zeros.

        Args:
            difficulty: Number of leading zeros required in the hash
        """
        target = '0' * difficulty

        while True:
            self.hash = self.calculate_hash()
            if self.hash[:difficulty] == target:
                print(f"Block mined: {self.hash}")
                break
            self.nonce += 1

    def to_dict(self) -> Dict[str, Any]:
        """Convert block to dictionary for serialization."""
        return {
            'index': self.index,
            'transactions': self.transactions,
            'previous_hash': self.previous_hash,
            'timestamp': self.timestamp,
            'nonce': self.nonce,
            'hash': self.hash
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Block':
        """Create a Block from a dictionary."""
        block = cls(
            index=data['index'],
            transactions=data['transactions'],
            previous_hash=data['previous_hash'],
            timestamp=data['timestamp']
        )
        block.nonce = data['nonce']
        block.hash = data['hash']
        return block
