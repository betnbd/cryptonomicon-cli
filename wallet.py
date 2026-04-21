import hashlib
import json
from typing import Tuple
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import binascii


class Wallet:
    """
    Represents a cryptocurrency wallet with public/private key pair.

    Similar to Bitcoin, this wallet uses asymmetric cryptography for
    signing transactions and generating addresses.
    """

    def __init__(self, private_key: str = None):
        """
        Initialize a wallet with a new or existing key pair.

        Args:
            private_key: Optional existing private key (PEM format)
        """
        if private_key:
            self.private_key = RSA.import_key(private_key)
        else:
            # Generate new 2048-bit RSA key pair
            self.private_key = RSA.generate(2048)

        self.public_key = self.private_key.publickey()
        self.address = self.generate_address()

    def generate_address(self) -> str:
        """
        Generate a wallet address from the public key.

        Similar to Bitcoin, we hash the public key to create an address.

        Returns:
            The wallet address (hex string)
        """
        # Export public key and hash it
        public_key_bytes = self.public_key.export_key(format='DER')
        sha256_hash = hashlib.sha256(public_key_bytes).digest()
        ripemd160_hash = hashlib.new('ripemd160', sha256_hash).digest()

        # Convert to hex for readability
        address = binascii.hexlify(ripemd160_hash).decode('utf-8')
        return address

    def get_public_key(self) -> str:
        """
        Get the public key in PEM format.

        Returns:
            Public key as string
        """
        return self.public_key.export_key(format='PEM').decode('utf-8')

    def get_private_key(self) -> str:
        """
        Get the private key in PEM format.

        WARNING: Keep this secret! Anyone with the private key can spend your coins.

        Returns:
            Private key as string
        """
        return self.private_key.export_key(format='PEM').decode('utf-8')

    def sign_transaction(self, transaction_data: dict) -> str:
        """
        Sign a transaction with the private key.

        Args:
            transaction_data: The transaction to sign

        Returns:
            Signature as hex string
        """
        # Create a hash of the transaction data
        tx_string = json.dumps(transaction_data, sort_keys=True)
        tx_hash = SHA256.new(tx_string.encode('utf-8'))

        # Sign the hash with private key
        signature = pkcs1_15.new(self.private_key).sign(tx_hash)
        return binascii.hexlify(signature).decode('utf-8')

    @staticmethod
    def verify_signature(transaction_data: dict, signature: str, public_key_pem: str) -> bool:
        """
        Verify that a transaction was signed by the owner of the public key.

        Args:
            transaction_data: The transaction to verify
            signature: The signature to check
            public_key_pem: Public key in PEM format

        Returns:
            True if signature is valid, False otherwise
        """
        try:
            # Import the public key
            public_key = RSA.import_key(public_key_pem)

            # Hash the transaction
            tx_string = json.dumps(transaction_data, sort_keys=True)
            tx_hash = SHA256.new(tx_string.encode('utf-8'))

            # Verify the signature
            signature_bytes = binascii.unhexlify(signature)
            pkcs1_15.new(public_key).verify(tx_hash, signature_bytes)
            return True
        except (ValueError, TypeError):
            return False

    def save_to_file(self, filename: str) -> None:
        """
        Save wallet to a file.

        Args:
            filename: Path to save the wallet
        """
        wallet_data = {
            'private_key': self.get_private_key(),
            'public_key': self.get_public_key(),
            'address': self.address
        }

        with open(filename, 'w') as f:
            json.dump(wallet_data, f, indent=2)

        print(f"Wallet saved to {filename}")
        print(f"Address: {self.address}")

    @classmethod
    def load_from_file(cls, filename: str) -> 'Wallet':
        """
        Load a wallet from a file.

        Args:
            filename: Path to the wallet file

        Returns:
            Wallet instance
        """
        with open(filename, 'r') as f:
            wallet_data = json.load(f)

        return cls(private_key=wallet_data['private_key'])

    def __repr__(self) -> str:
        return f"Wallet(address={self.address})"
