import logging
from http import HTTPStatus
from apiflask import APIBlueprint, Schema, abort
from apiflask.fields import String
from utils import load_aldus_data
from typing import List, Union

# Configure logging
logging.basicConfig(level=logging.INFO)


class Account(Schema):
    slug = String(required=True)
    address = String(required=True)
    name = String(required=True)
    description = String(required=True)
    type = String(required=True)


accounts_bp = APIBlueprint("accounts", __name__)


def load_accounts(chain: str, network: str) -> List[dict]:
    try:
        return load_aldus_data("accounts", chain, network)
    except Exception as e:
        logging.error(f"Error loading data: {e}")
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description="Internal server error")


@accounts_bp.route("/<chain>/<network>/accounts", methods=["GET"])
@accounts_bp.doc(
    summary="Get all accounts",
    description="Get all account entries for a given chain and network",
)
@accounts_bp.output(Account(many=True), status_code=HTTPStatus.OK)
def get_accounts(chain: str, network: str) -> List[Account]:
    """Get all accounts for a given chain and network.

    Args:
        chain (str): Chain name.
        network (str): Network name.

    Returns:
        List[Account]: List of accounts.
    """
    accounts_data = load_accounts(chain, network)
    return accounts_data


@accounts_bp.route("/<chain>/<network>/accounts/<address>", methods=["GET"])
@accounts_bp.doc(
    summary="Get account by address",
    description="Get an account entry for a given chain and network by address",
)
@accounts_bp.output(Account, status_code=HTTPStatus.OK)
def get_account(chain: str, network: str, address: str) -> Union[Account, tuple]:
    """Get account for a given chain, network and address.

    Args:
        chain (str): Chain name.
        network (str): Network name.
        address (str): Account address.

    Returns:
        Account or tuple: Account data if found, otherwise error message and 404 status.
    """
    accounts_data = load_accounts(chain, network)
    account = next((acc for acc in accounts_data if acc["address"] == address), None)
    if account:
        return account
    abort(HTTPStatus.NOT_FOUND, description="Account not found")
