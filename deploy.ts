import { CrossChainSwap } from './src/contracts/crossChainSwap'
import {
    bsv,
    TestWallet,
    DefaultProvider,
    sha256,
    toByteString,
    PubKey,
} from 'scrypt-ts'

import * as dotenv from 'dotenv'

// Load the .env file
dotenv.config()

// Read the private key from the .env file.
// The default private key inside the .env file is meant to be used for the Bitcoin testnet.
// See https://scrypt.io/docs/bitcoin-basics/bsv/#private-keys
const privateKey = bsv.PrivateKey.fromWIF(process.env.PRIVATE_KEY || '')

// Prepare signer.
// See https://scrypt.io/docs/how-to-deploy-and-call-a-contract/#prepare-a-signer-and-provider
const signer = new TestWallet(
    privateKey,
    new DefaultProvider({
        network: bsv.Networks.testnet,
    })
)

async function main() {
    // TODO: Adjust values:
    const alicePubKey = bsv.PublicKey.fromHex('TODO')

    const bobPrivKey = privateKey
    const bobPubKey = bobPrivKey.publicKey

    // Amount to be locked in the contract
    const amount = 10000

    // LockTime after which the contracts "cancel" method can be called.
    // Make sure the person who generates the secret value "x" has a longer timeout
    // duration to avoid them unlocking and withdrawing at the same time to steal funds.
    const lockTimeMin = 1673510000n

    const x = toByteString(
        'f00cfd8df5f92d5e94d1ecbd9b427afd14e03f8a3292ca4128cd59ef7b9643bc'
    )
    const xHash = sha256(x)

    await CrossChainSwap.compile()

    const crossChainSwap = new CrossChainSwap(
        PubKey(alicePubKey.toHex()),
        PubKey(bobPubKey.toHex()),
        xHash,
        lockTimeMin
    )

    // Connect Bob signer.
    await crossChainSwap.connect(signer)

    // Contract deployment.
    const deployTx = await crossChainSwap.deploy(amount)
    console.log('CrossChainSwap contract deployed: ', deployTx.id)
}

main()
