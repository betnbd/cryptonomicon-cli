import json
from typing import List, Dict
from block import Block


class Blockchain:
    """Manages the blockchain and validates its integrity."""

    def __init__(self, difficulty: int = 4):
        """
        Initialize a new blockchain.

        Args:
            difficulty: Mining difficulty (number of leading zeros required)
        """
        self.chain: List[Block] = []
        self.difficulty = difficulty
        self.pending_transactions: List[Dict] = []
        self.mining_reward = 50  # Reward for mining a block

        # Create the genesis block
        self.create_genesis_block()

    def create_genesis_block(self) -> None:
        """Create the first block in the blockchain."""
        genesis_block = Block(0, [], "0")
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)

    def get_latest_block(self) -> Block:
        """Get the most recent block in the chain."""
        return self.chain[-1]

    def add_transaction(self, transaction: Dict) -> None:
        """
        Add a transaction to the pending transactions pool.

        Args:
            transaction: Transaction data to add
        """
        required_fields = {'from', 'to', 'amount'}
        missing_fields = required_fields.difference(transaction)
        if missing_fields:
            missing = ", ".join(sorted(missing_fields))
            raise ValueError(f"Transaction is missing required fields: {missing}")

        if transaction['from'] is None:
            raise ValueError("Pending transactions cannot be coinbase transactions")

        if not transaction['to']:
            raise ValueError("Recipient address is required")

        if transaction['amount'] <= 0:
            raise ValueError("Transaction amount must be greater than zero")

        self.pending_transactions.append(transaction)

    def mine_pending_transactions(self, mining_reward_address: str) -> None:
        """
        Mine a new block containing pending transactions.

        Args:
            mining_reward_address: Address to receive the mining reward
        """
        if not mining_reward_address:
            raise ValueError("A mining reward address is required")

        # Create reward transaction
        reward_tx = {
            'from': None,  # Coinbase transaction (mining reward)
            'to': mining_reward_address,
            'amount': self.mining_reward
        }

        # Add all pending transactions plus reward
        transactions = list(self.pending_transactions) + [reward_tx]

        # Create and mine new block
        new_block = Block(
            index=len(self.chain),
            transactions=transactions,
            previous_hash=self.get_latest_block().hash
        )
        new_block.mine_block(self.difficulty)

        # Add to chain and clear pending transactions
        self.chain.append(new_block)
        self.pending_transactions = []

        print(f"Block successfully mined! Reward sent to {mining_reward_address}")

    def get_balance(self, address: str) -> float:
        """
        Calculate the balance of an address.

        Args:
            address: The address to check

        Returns:
            The total balance
        """
        balance = 0

        for block in self.chain:
            for transaction in block.transactions:
                if transaction.get('from') == address:
                    balance -= transaction['amount']
                if transaction.get('to') == address:
                    balance += transaction['amount']

        return balance

    def is_chain_valid(self) -> bool:
        """
        Validate the entire blockchain.

        Returns:
            True if the chain is valid, False otherwise
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # Verify block hash
            if current_block.hash != current_block.calculate_hash():
                print(f"Invalid hash at block {i}")
                return False

            # Verify chain linkage
            if current_block.previous_hash != previous_block.hash:
                print(f"Invalid previous hash at block {i}")
                return False

            # Verify proof of work
            if not current_block.hash.startswith('0' * self.difficulty):
                print(f"Invalid proof of work at block {i}")
                return False

        return True

    def to_json(self) -> str:
        """Serialize the blockchain to JSON."""
        chain_data = [block.to_dict() for block in self.chain]
        return json.dumps({
            'chain': chain_data,
            'difficulty': self.difficulty,
            'pending_transactions': self.pending_transactions,
            'mining_reward': self.mining_reward
        }, indent=2)

    def save_to_file(self, filename: str = 'blockchain.json') -> None:
        """Save the blockchain to a file."""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(self.to_json())
        print(f"Blockchain saved to {filename}")

    @classmethod
    def load_from_file(cls, filename: str = 'blockchain.json') -> 'Blockchain':
        """Load a blockchain from a file."""
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

        blockchain = cls(difficulty=data['difficulty'])
        blockchain.chain = [Block.from_dict(block_data) for block_data in data['chain']]
        blockchain.pending_transactions = data['pending_transactions']
        blockchain.mining_reward = data['mining_reward']

        if not blockchain.chain:
            raise ValueError("Blockchain file must contain at least one block")

        return blockchain
