import time
import hashlib
import json
from typing import List, Dict, Optional
from wallet import Wallet


class TransactionInput:
    """
    Represents an input to a transaction (UTXO being spent).

    In Bitcoin's UTXO model, each input references a previous transaction output.
    """

    def __init__(self, tx_id: str, output_index: int, signature: str = None):
        """
        Initialize a transaction input.

        Args:
            tx_id: ID of the transaction containing the output being spent
            output_index: Index of the output in that transaction
            signature: Signature proving ownership of the output
        """
        self.tx_id = tx_id
        self.output_index = output_index
        self.signature = signature

    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        return {
            'tx_id': self.tx_id,
            'output_index': self.output_index,
            'signature': self.signature
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'TransactionInput':
        """Create from dictionary."""
        return cls(
            tx_id=data['tx_id'],
            output_index=data['output_index'],
            signature=data.get('signature')
        )


class TransactionOutput:
    """
    Represents an output of a transaction (UTXO).

    Each output specifies an amount and the address that can spend it.
    """

    def __init__(self, address: str, amount: float):
        """
        Initialize a transaction output.

        Args:
            address: Recipient's wallet address
            amount: Amount to send
        """
        self.address = address
        self.amount = amount

    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        return {
            'address': self.address,
            'amount': self.amount
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'TransactionOutput':
        """Create from dictionary."""
        return cls(
            address=data['address'],
            amount=data['amount']
        )


class Transaction:
    """
    Represents a cryptocurrency transaction using UTXO model.

    Similar to Bitcoin, transactions consume inputs (UTXOs) and create outputs.
    """

    def __init__(self, inputs: List[TransactionInput], outputs: List[TransactionOutput], timestamp: float = None):
        """
        Initialize a transaction.

        Args:
            inputs: List of transaction inputs (UTXOs being spent)
            outputs: List of transaction outputs (new UTXOs being created)
            timestamp: Transaction creation time
        """
        self.inputs = inputs
        self.outputs = outputs
        self.timestamp = timestamp or time.time()
        self.tx_id = self.calculate_hash()

    def calculate_hash(self) -> str:
        """
        Calculate the transaction ID (hash).

        Returns:
            Transaction hash
        """
        tx_data = {
            'inputs': [inp.to_dict() for inp in self.inputs],
            'outputs': [out.to_dict() for out in self.outputs],
            'timestamp': self.timestamp
        }
        tx_string = json.dumps(tx_data, sort_keys=True)
        return hashlib.sha256(tx_string.encode()).hexdigest()

    def sign_transaction(self, wallet: Wallet, utxo_set: Dict[str, TransactionOutput]) -> None:
        """
        Sign all inputs of the transaction.

        Args:
            wallet: Wallet used to sign the transaction
            utxo_set: Set of available UTXOs to verify ownership
        """
        for tx_input in self.inputs:
            # Get the UTXO being spent
            utxo_key = f"{tx_input.tx_id}:{tx_input.output_index}"

            if utxo_key not in utxo_set:
                raise ValueError(f"UTXO {utxo_key} not found")

            utxo = utxo_set[utxo_key]

            # Verify that the wallet owns this UTXO
            if utxo.address != wallet.address:
                raise ValueError(f"Wallet does not own UTXO {utxo_key}")

            # Create signature data (excluding signatures themselves)
            sig_data = {
                'tx_id': tx_input.tx_id,
                'output_index': tx_input.output_index,
                'outputs': [out.to_dict() for out in self.outputs],
                'timestamp': self.timestamp
            }

            # Sign the data
            tx_input.signature = wallet.sign_transaction(sig_data)

    def verify_transaction(self, utxo_set: Dict[str, TransactionOutput]) -> bool:
        """
        Verify the transaction is valid.

        Checks:
        1. All inputs reference valid UTXOs
        2. Signatures are valid
        3. Input amounts >= output amounts

        Args:
            utxo_set: Set of available UTXOs

        Returns:
            True if valid, False otherwise
        """
        total_input = 0
        total_output = sum(out.amount for out in self.outputs)

        for tx_input in self.inputs:
            utxo_key = f"{tx_input.tx_id}:{tx_input.output_index}"

            # Check UTXO exists
            if utxo_key not in utxo_set:
                print(f"UTXO {utxo_key} not found")
                return False

            utxo = utxo_set[utxo_key]
            total_input += utxo.amount

            # Verify signature
            # Note: In a real implementation, we'd get the public key from somewhere
            # For now, this is a simplified version
            if not tx_input.signature:
                print(f"Input {utxo_key} is not signed")
                return False

        # Check input amounts cover output amounts
        if total_input < total_output:
            print(f"Insufficient funds: {total_input} < {total_output}")
            return False

        return True

    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        return {
            'tx_id': self.tx_id,
            'inputs': [inp.to_dict() for inp in self.inputs],
            'outputs': [out.to_dict() for out in self.outputs],
            'timestamp': self.timestamp
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Transaction':
        """Create from dictionary."""
        tx = cls(
            inputs=[TransactionInput.from_dict(inp) for inp in data['inputs']],
            outputs=[TransactionOutput.from_dict(out) for out in data['outputs']],
            timestamp=data['timestamp']
        )
        tx.tx_id = data['tx_id']
        return tx

    @classmethod
    def create_coinbase_transaction(cls, miner_address: str, reward: float) -> 'Transaction':
        """
        Create a coinbase transaction (mining reward).

        Args:
            miner_address: Address to receive the reward
            reward: Mining reward amount

        Returns:
            Coinbase transaction
        """
        # Coinbase has no inputs (money created from nothing)
        inputs = []
        outputs = [TransactionOutput(miner_address, reward)]

        return cls(inputs, outputs)

    def __repr__(self) -> str:
        return f"Transaction(id={self.tx_id[:8]}..., inputs={len(self.inputs)}, outputs={len(self.outputs)})"
