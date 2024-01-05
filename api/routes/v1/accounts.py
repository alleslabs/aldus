from apiflask import APIBlueprint
from utils import load_aldus_data

accounts_bp = APIBlueprint("accounts", __name__)


def load_accounts(chain, network):
    """Load all accounts for a given chain and network.

    Args:
        chain (str): Chain name.
        network (str): Network name.

    Returns:
        list: List of accounts.
    """
    return load_aldus_data(f"../data/{chain}/{network}/accounts.json")


@accounts_bp.route("/<chain>/<network>/accounts", methods=["GET"])
@accounts_bp.doc(
    summary="Get all accounts",
    description="Get all accounts entries for a given chain and network.",
)
def get_accounts(chain, network):
    """Get accounts for a given chain and network.

    Args:
        chain (str): Chain name.
        network (str): Network name.

    Returns:
        list: List of accounts.
    """
    accounts = load_accounts(chain, network)
    return accounts


@accounts_bp.route("/<chain>/<network>/accounts/<address>", methods=["GET"])
@accounts_bp.doc(
    summary="Get an account by address",
    description="Get an account entry for a given chain and network by address.",
)
def get_account(chain, network, address):
    """Get account for a given chain, network and address.

    Args:
        chain (str): Chain name.
        network (str): Network name.
        address (str): Account address.

    Returns:
        dict: Account data.
    """
    accounts = [
        account
        for account in load_accounts(chain, network)
        if account["address"] == address
    ]
    account = accounts[0] if accounts else None
    if not account:
        return {"error": "Account not found"}, 404
    return account
