# BSV-BTC Atomic Swap Using HTLC

## Prepare

Install project dependencies:

```sh
npm i
pip install bitcoin-utils==0.5.9
```

Compile contract:

```sh
npx scrypt-cli compile
```

## Deployment

For BTC, adjust TODOs in `btc-scripts` and run:

```sh
python3 btc-scripts/deploy.py
```

You can broadcast the generated TX using [this site](https://blockstream.info/tx/push).

To deploy the sCrypt contract, configure your values in `deploy.ts` and run:

```sh
npx scrypt-cli deploy
```

Don't forget to fund your key beforehand. You can use [our faucet](https://scrypt.io/faucet).

## Tests

To run **local** tests for the sCrypt smart contract, run:

```sh
npm t
```

To run a test (deployment and contract calls) on the BSV testnet, run:

```
npm run testnet
```
