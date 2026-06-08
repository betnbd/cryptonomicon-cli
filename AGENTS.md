# AGENTS.md

## Purpose

Educational cryptocurrency/blockchain prototype in Python: proof-of-work mining, RSA wallets, on-chain transfers, JSON persistence, and chain validation. Driven by a single interactive numbered-menu CLI. Not production code.

## Stack

- Python 3
- Single runtime dependency: `pycryptodome==3.19.0` (RSA keys, signing) — `requirements.txt`

## Build / Run / Test

```bash
python3 -m venv venv && source venv/bin/activate
python3 -m pip install -r requirements.txt

python3 main.py            # interactive CLI

python3 -m compileall .    # syntax check
python3 test_basic.py      # smoke test (asserts; no pytest)
```

No pytest/lint config exists. `test_basic.py` is a plain script run directly, not a pytest suite.

## Layout

- `main.py` — interactive CLI menu; entry point. Hardcodes `Blockchain(difficulty=4)`.
- `blockchain.py` — active chain: pending txs, mining, balance scan, JSON save/load, validation. Default `difficulty=4`, fixed `mining_reward=50`.
- `block.py` — `Block` + proof-of-work nonce loop.
- `wallet.py` — RSA keypair, address derivation, sign/verify, JSON save/load.
- `transaction.py` — fuller UTXO transaction model. NOT wired into the runtime CLI flow.

## Gotchas

- Two parallel, inconsistent transaction models. The runtime path (`main.py` + `blockchain.py`) uses plain dicts `{'from', 'to', 'amount'}` with `from: None` for coinbase. The UTXO classes in `transaction.py` are only exercised by `test_basic.py` — don't assume CLI changes touch them or vice versa.
- The CLI's `difficulty=4` makes mining noticeably slow; tests and ad-hoc exploration use `difficulty=2`.
- Runtime path does not enforce cryptographic signature verification on transfers; only basic structural/positive-amount checks. Balances are recomputed by scanning every block.
- Wallet and blockchain state are persisted as JSON files in the working directory (e.g. `wallet.json`, `blockchain.json`, `test_wallet.json`); `test_basic.py` writes `test_wallet.json`.
