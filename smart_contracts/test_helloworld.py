import algokit_utils as utils
import beaker as bk
from algosdk.atomic_transaction_composer import AccountTransactionSigner
from algosdk.util import algos_to_microalgos

import smart_contracts.helloworld as hw


def test_helloworld() -> None:
    creator = utils.get_account(client=bk.sandbox.get_algod_client(), fund_with_algos=100, name="CREATOR")
    creator_signer = AccountTransactionSigner(creator.private_key)

    app_client = bk.client.ApplicationClient(client=bk.sandbox.get_algod_client(), app=hw.app, signer=creator_signer)

    app_id, app_addr, txn_id = app_client.create()

    utils.transfer(
        client=bk.sandbox.get_algod_client(),
        parameters=utils.TransferParameters(
            from_account=creator, to_address=app_addr, micro_algos=algos_to_microalgos(10)
        ),
    )

    result = app_client.call(hw.hello, name="World", boxes=[(app_id, "name")])

    assert result.return_value == "Hello, World"
