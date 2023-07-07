from bitcoinutils.setup import setup
from bitcoinutils.utils import to_satoshis
from bitcoinutils.transactions import Transaction, TxInput, TxOutput
from bitcoinutils.keys import PrivateKey, PublicKey, P2wshAddress, P2wpkhAddress
from bitcoinutils.script import Script

def main():
    # always remember to setup the network
    setup('testnet')

    # TODO: Set values:
    alicePriv = PrivateKey('TODO')
    alicePub = alicePriv.get_public_key()
    bobPub = PublicKey('TODO')
    txid = 'TODO'  # Previous transaction ID
    vout = 2  # Previous transaction ouput index
    amount = 0.00001850   # Amount in output
    fee = 0.00000125      # Fee in new transaction
    x = 'f00cfd8df5f92d5e94d1ecbd9b427afd14e03f8a3292ca4128cd59ef7b9643bc'
    xHash = '1908c59a71781b7a44182ec39dd84a8a9e13dc31691fead8631730f5f5ab7b65'
    nBlocksLocked = '06'  # 6 blocks ~ 1 hr

    # HTLC script:
    htlc_redeem_script = Script(
        ['OP_IF',
            'OP_SHA256',
            xHash,
            'OP_EQUALVERIFY',
            bobPub.to_hex(),
            'OP_CHECKSIG',
        'OP_ELSE',
            nBlocksLocked,
            'OP_CHECKSEQUENCEVERIFY',
            'OP_DROP',
            alicePriv.get_public_key().to_hex(),
            'OP_CHECKSIG',
        'OP_ENDIF']
    )
    toAddress = P2wshAddress.from_script(htlc_redeem_script)

    # Create transaction input from tx id of utxo.
    txIn = TxInput(txid, vout)
    redeem_script1 = Script(
        ['OP_DUP', 'OP_HASH160', alicePub.to_hash160(), 'OP_EQUALVERIFY', 'OP_CHECKSIG'])

    # Create transaction output, which contains the P2WSH for the HTLC script.
    txOut = TxOutput(to_satoshis(amount - fee), toAddress.to_script_pub_key())

    # Create transaction.
    tx = Transaction([txIn], [txOut], has_segwit=True)

    # Sign transaction.
    sig1 = alicePriv.sign_segwit_input(tx, 0, redeem_script1, to_satoshis(amount))
    tx.witnesses.append(Script([sig1, alicePub.to_hex()]))

    # Print raw signed transaction ready to be broadcast.
    print("\nRaw signed transaction:\n" + tx.serialize())
    print("\nTxId:", tx.get_txid())

if __name__ == "__main__":
    main()
