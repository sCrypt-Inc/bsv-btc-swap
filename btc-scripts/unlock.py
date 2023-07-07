from bitcoinutils.setup import setup
from bitcoinutils.utils import to_satoshis
from bitcoinutils.transactions import Transaction, TxInput, TxOutput
from bitcoinutils.keys import PrivateKey, PublicKey, P2wshAddress, P2wpkhAddress
from bitcoinutils.script import Script

def main():
    # always remember to setup the network
    setup('testnet')

    # TODO: Set values:
    bobPriv = PrivateKey('TODO')
    bobPub = bobPriv.get_public_key()
    alicePub = PublicKey('TODO')
    txid = 'TODO'  # Previous transaction ID
    vout = 0 # Previous transaction ouput index
    amount = 0.00001725   # Amount in output
    fee = 0.00000125      # Fee in new transaction
    x = 'f00cfd8df5f92d5e94d1ecbd9b427afd14e03f8a3292ca4128cd59ef7b9643bc'
    xHash = '1908c59a71781b7a44182ec39dd84a8a9e13dc31691fead8631730f5f5ab7b65'
    nBlocksLocked = '06'  # 6 blocks ~ 1 hr
    toAddress = P2wpkhAddress.from_address('TODO')

    # HTLC Script:
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
            alicePub.to_hex(),
            'OP_CHECKSIG',
        'OP_ENDIF']
    )

    fromAddress = P2wshAddress.from_script(htlc_redeem_script)

    # Create transaction input from tx id of UTXO
    txin = TxInput(txid, vout)

    txOut1 = TxOutput(to_satoshis(amount - fee), toAddress.to_script_pub_key())

    tx = Transaction([txin], [txOut1], has_segwit=True)

    # NOTE: In P2WSH, the argument for OP_IF and OP_NOTIF MUST be exactly an empty vector or 0x01, or the script evaluation fails immediately.

    # Normal unlock:
    sig1 = bobPriv.sign_segwit_input(tx, 0, htlc_redeem_script, to_satoshis(amount))
    tx.witnesses.append(Script([
        sig1,
        x,
        '01',  # OP_TRUE
        htlc_redeem_script.to_hex()]))

    # print raw signed transaction ready to be broadcasted
    print("\nRaw signed transaction:\n" + tx.serialize())
    print("\nTxId:", tx.get_txid())

if __name__ == "__main__":
    main()
