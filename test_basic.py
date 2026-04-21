#!/usr/bin/env python3
"""
Basic test script to verify the cryptocurrency implementation.

Run this to test that all components are working correctly.
"""

from blockchain import Blockchain
from wallet import Wallet
from transaction import Transaction, TransactionInput, TransactionOutput


def test_blockchain():
    """Test basic blockchain functionality."""
    print("\n" + "="*50)
    print("Testing Blockchain")
    print("="*50)

    # Create blockchain with low difficulty for faster testing
    bc = Blockchain(difficulty=2)
    print("✓ Blockchain created")

    # Check genesis block
    assert len(bc.chain) == 1
    assert bc.chain[0].index == 0
    print("✓ Genesis block exists")

    # Add transaction and mine
    bc.add_transaction({'from': 'Alice', 'to': 'Bob', 'amount': 10})
    bc.mine_pending_transactions('Miner1')
    print("✓ Block mined successfully")

    # Verify chain
    assert bc.is_chain_valid()
    print("✓ Blockchain is valid")

    # Check balance
    balance = bc.get_balance('Miner1')
    assert balance == 50  # Mining reward
    print(f"✓ Miner balance correct: {balance}")


def test_wallet():
    """Test wallet functionality."""
    print("\n" + "="*50)
    print("Testing Wallet")
    print("="*50)

    # Create wallet
    wallet = Wallet()
    print(f"✓ Wallet created with address: {wallet.address[:16]}...")

    # Test signing
    test_data = {'from': wallet.address, 'to': 'someone', 'amount': 10}
    signature = wallet.sign_transaction(test_data)
    print("✓ Transaction signed")

    # Verify signature
    is_valid = Wallet.verify_signature(test_data, signature, wallet.get_public_key())
    assert is_valid
    print("✓ Signature verified")

    # Test save/load
    wallet.save_to_file('test_wallet.json')
    loaded_wallet = Wallet.load_from_file('test_wallet.json')
    assert loaded_wallet.address == wallet.address
    print("✓ Wallet save/load works")


def test_transaction():
    """Test transaction functionality."""
    print("\n" + "="*50)
    print("Testing Transactions")
    print("="*50)

    # Create wallets
    alice = Wallet()
    bob = Wallet()
    print("✓ Wallets created")

    # Create coinbase transaction (mining reward for Alice)
    coinbase = Transaction.create_coinbase_transaction(alice.address, 50)
    print(f"✓ Coinbase transaction created: {coinbase.tx_id[:16]}...")

    # Create UTXO set
    utxo_set = {
        f"{coinbase.tx_id}:0": coinbase.outputs[0]
    }

    # Create transaction from Alice to Bob
    inputs = [TransactionInput(coinbase.tx_id, 0)]
    outputs = [
        TransactionOutput(bob.address, 30),    # Send 30 to Bob
        TransactionOutput(alice.address, 20)   # Change back to Alice
    ]

    tx = Transaction(inputs, outputs)
    print("✓ Transaction created")

    # Sign transaction
    tx.sign_transaction(alice, utxo_set)
    print("✓ Transaction signed")

    # Verify transaction
    is_valid = tx.verify_transaction(utxo_set)
    assert is_valid
    print("✓ Transaction verified")


def main():
    """Run all tests."""
    print("\n🔧 Running Cryptonomicon Tests\n")

    try:
        test_blockchain()
        test_wallet()
        test_transaction()

        print("\n" + "="*50)
        print("✅ All tests passed!")
        print("="*50 + "\n")

    except AssertionError as e:
        print(f"\n❌ Test failed: {e}\n")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")


if __name__ == "__main__":
    main()
