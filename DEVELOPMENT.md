# Development Notes

This repository contains a small educational cryptocurrency prototype written in
Python. The focus is readability and experimentation rather than production use.

## Environment

```bash
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
```

Run the CLI with:

```bash
python3 main.py
```

## Architecture

### `block.py`

Defines the `Block` type and the proof-of-work loop. Each block stores:

- `index`
- `transactions`
- `previous_hash`
- `timestamp`
- `nonce`
- `hash`

`mine_block()` increments the nonce until the block hash has the configured
number of leading zeroes.

### `blockchain.py`

Owns the active chain, pending transaction list, mining reward, serialization,
and validation logic. The active chain currently stores transactions as simple
dictionaries with `from`, `to`, and `amount` keys.

### `wallet.py`

Creates RSA key pairs, derives an address from the public key, signs payloads,
and saves or loads wallets from JSON files.

### `transaction.py`

Contains a more detailed UTXO-oriented transaction model. These classes are
useful for experimentation and tests, but they are not yet wired into the
runtime blockchain flow used by `main.py`.

### `main.py`

Provides the interactive command-line interface for wallet creation, mining,
balance checks, chain inspection, and saving or loading blockchain data.

## Current Limits

- Pending transactions are validated only for basic structure and positive
  amounts.
- The runtime blockchain path does not yet enforce cryptographic transaction
  verification.
- Balances are recomputed by scanning the chain rather than maintaining a UTXO
  set.
- Difficulty and mining reward are fixed unless changed in code.

## Verification

Syntax check:

```bash
python3 -m compileall .
```

Behavioral smoke test:

```bash
python3 test_basic.py
```
