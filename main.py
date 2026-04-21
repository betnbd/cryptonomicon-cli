#!/usr/bin/env python3
"""
Cryptonomicon - A cryptocurrency and blockchain implementation in Python.

This CLI provides an interface to interact with the blockchain,
create wallets, and send transactions.
"""

import sys
from blockchain import Blockchain
from wallet import Wallet


def print_menu():
    """Display the main menu."""
    print("\n" + "="*50)
    print("    CRYPTONOMICON - Cryptocurrency CLI")
    print("="*50)
    print("\n1. Create new wallet")
    print("2. Load wallet")
    print("3. Check balance")
    print("4. Mine a block")
    print("5. Send transaction")
    print("6. View blockchain")
    print("7. Validate blockchain")
    print("8. Save blockchain")
    print("9. Load blockchain")
    print("0. Exit")
    print("\n" + "="*50)


def create_wallet():
    """Create a new wallet and save it."""
    wallet = Wallet()
    filename = input("Enter filename to save wallet (e.g., wallet.json): ")

    if not filename:
        filename = "wallet.json"

    wallet.save_to_file(filename)
    print(f"\n✓ Wallet created!")
    print(f"Address: {wallet.address}")
    print(f"\nIMPORTANT: Keep {filename} safe! It contains your private key.")

    return wallet


def load_wallet():
    """Load an existing wallet from file."""
    filename = input("Enter wallet filename: ")

    try:
        wallet = Wallet.load_from_file(filename)
        print(f"\n✓ Wallet loaded!")
        print(f"Address: {wallet.address}")
        return wallet
    except FileNotFoundError:
        print(f"\n✗ Wallet file '{filename}' not found!")
        return None
    except Exception as e:
        print(f"\n✗ Error loading wallet: {e}")
        return None


def check_balance(blockchain, address):
    """Check the balance of an address."""
    if not address:
        address = input("Enter address to check: ")

    balance = blockchain.get_balance(address)
    print(f"\nBalance for {address}: {balance} coins")


def mine_block(blockchain, wallet):
    """Mine a new block."""
    if not wallet:
        print("\n✗ You need to load a wallet first!")
        return

    print("\n⛏  Mining block...")
    blockchain.mine_pending_transactions(wallet.address)
    print("✓ Block mined! Reward credited in the newly mined block.")


def send_transaction(blockchain, wallet):
    """Create and send a transaction."""
    if not wallet:
        print("\n✗ You need to load a wallet first!")
        return

    # Get transaction details
    recipient = input("Recipient address: ").strip()
    if not recipient:
        print("\n✗ Recipient address is required.")
        return

    try:
        amount = float(input("Amount to send: "))
    except ValueError:
        print("\n✗ Amount must be a number.")
        return

    if amount <= 0:
        print("\n✗ Amount must be greater than zero.")
        return

    # Check balance
    balance = blockchain.get_balance(wallet.address)
    if balance < amount:
        print(f"\n✗ Insufficient funds! Balance: {balance}, Required: {amount}")
        return

    # Create simple transaction (in the current implementation)
    transaction = {
        'from': wallet.address,
        'to': recipient,
        'amount': amount
    }

    try:
        blockchain.add_transaction(transaction)
    except ValueError as exc:
        print(f"\n✗ {exc}")
        return

    print("\n✓ Transaction added to pending transactions.")
    print("It will be included in the next mined block.")


def view_blockchain(blockchain):
    """Display the blockchain."""
    print("\n" + "="*50)
    print("BLOCKCHAIN")
    print("="*50)

    for block in blockchain.chain:
        print(f"\nBlock #{block.index}")
        print(f"Hash: {block.hash}")
        print(f"Previous Hash: {block.previous_hash}")
        print(f"Timestamp: {block.timestamp}")
        print(f"Nonce: {block.nonce}")
        print(f"Transactions ({len(block.transactions)}):")

        for tx in block.transactions:
            if tx.get('from') is None:
                print(f"  [COINBASE] → {tx['to']}: {tx['amount']} coins")
            else:
                print(f"  {tx['from']} → {tx['to']}: {tx['amount']} coins")

    print("\n" + "="*50)


def validate_blockchain(blockchain):
    """Validate the blockchain integrity."""
    print("\n⚙  Validating blockchain...")

    if blockchain.is_chain_valid():
        print("✓ Blockchain is valid!")
    else:
        print("✗ Blockchain is INVALID!")


def main():
    """Main program loop."""
    # Initialize blockchain
    print("\n🔗 Initializing blockchain...")
    blockchain = Blockchain(difficulty=4)
    print("✓ Blockchain initialized!")

    wallet = None

    while True:
        print_menu()
        choice = input("\nEnter choice: ")

        if choice == '1':
            wallet = create_wallet()
        elif choice == '2':
            wallet = load_wallet()
        elif choice == '3':
            if wallet:
                check_balance(blockchain, wallet.address)
            else:
                check_balance(blockchain, None)
        elif choice == '4':
            mine_block(blockchain, wallet)
        elif choice == '5':
            send_transaction(blockchain, wallet)
        elif choice == '6':
            view_blockchain(blockchain)
        elif choice == '7':
            validate_blockchain(blockchain)
        elif choice == '8':
            filename = input("Enter filename (default: blockchain.json): ") or "blockchain.json"
            blockchain.save_to_file(filename)
        elif choice == '9':
            filename = input("Enter filename (default: blockchain.json): ") or "blockchain.json"
            try:
                blockchain = Blockchain.load_from_file(filename)
                print("✓ Blockchain loaded!")
            except FileNotFoundError:
                print(f"✗ File '{filename}' not found!")
            except Exception as e:
                print(f"✗ Error loading blockchain: {e}")
        elif choice == '0':
            print("\nGoodbye! 👋")
            sys.exit(0)
        else:
            print("\n✗ Invalid choice! Please try again.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nGoodbye! 👋")
        sys.exit(0)
