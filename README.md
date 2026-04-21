# Cryptonomicon

A Bitcoin-like cryptocurrency prototype in Python for educational purposes.

## Motivation

Understanding how cryptocurrencies work at a systems level is difficult when the
only available references are production codebases built for performance and scale.
Cryptonomicon exists to close that gap. It implements a readable subset of a
Bitcoin-like system in a single Python project: proof-of-work mining, RSA-based
wallets, simple on-chain transfers, serialization, and chain validation. The
goal is not to build a production currency, but to make the moving parts easy to
inspect and modify.

## Features

- **Proof of Work**: Mining blocks with adjustable difficulty
- **Wallets**: RSA key generation, address derivation, signing, and JSON export/import
- **Transactions**: Simple transfer records in the active blockchain flow
- **Validation**: Block hash, link, and proof-of-work verification
- **Serialization**: Save and load wallets and blockchain state from disk

## Quick Start

```bash
# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
python3 -m pip install -r requirements.txt

# Launch the interactive CLI
python3 main.py
```

## Usage

Cryptonomicon ships a single interactive CLI in `main.py` that exposes all
functionality through a numbered menu:

| Option | Action |
|--------|--------|
| 1 | Create a new wallet (generates an RSA key pair and saves it to a JSON file) |
| 2 | Load an existing wallet from a JSON file |
| 3 | Check the balance of an address |
| 4 | Mine a new block (collects pending transactions + mining reward) |
| 5 | Send a transaction to another address |
| 6 | View the full blockchain |
| 7 | Validate blockchain integrity |
| 8 | Save the blockchain to a JSON file |
| 9 | Load a blockchain from a JSON file |
| 0 | Exit |

**Typical workflow:**

```bash
python3 main.py

# 1 — create a wallet (save as miner.json)
# 4 — mine a block to earn coins
# 1 — create a second wallet (save as recipient.json)
# 5 — send coins to the recipient address
# 4 — mine another block to confirm the transaction
# 6 — view the chain to inspect both blocks
```

You can also import the core classes directly in a Python shell for scripting or
exploration:

```python
from blockchain import Blockchain
from wallet import Wallet

bc = Blockchain(difficulty=2)   # lower difficulty for quick testing
w  = Wallet()
print(w.address)

bc.mine_pending_transactions(w.address)
print(bc.get_balance(w.address))  # 50 coins
```

## Project Structure

- `block.py` - Block class and proof-of-work logic
- `blockchain.py` - Chain management, pending transactions, persistence, and validation
- `transaction.py` - Experimental UTXO-style transaction classes not yet used by the CLI flow
- `wallet.py` - Wallet with RSA key management
- `main.py` - Interactive CLI interface
- `test_basic.py` - Basic smoke test script
- `DEVELOPMENT.md` - Development and architecture notes

## Current Limitations

- The active blockchain path stores transactions as simple dictionaries rather
  than full UTXO objects.
- The richer transaction model in `transaction.py` is only partially integrated.
- Pending transactions receive basic structural validation, but the chain does
  not yet enforce full signature verification.
- Balances are computed by scanning every block, which is fine for a teaching
  project but not efficient at scale.

## Testing

Install dependencies first, then run:

```bash
python3 -m compileall .
python3 test_basic.py
```

`pytest`-style tests are not currently included as a dependency or maintained as
part of the default workflow.

## Contributing

Contributions are welcome. To get started:

1. Fork the repository and create a feature branch from `main`.
2. Set up your environment using the steps in [Quick Start](#quick-start).
3. Make your changes. Keep commits focused and atomic.
4. Run the verification commands from [Testing](#testing).
5. Open a pull request against `main` with a short description of the change and
   why it is useful.
