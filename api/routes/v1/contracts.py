from apiflask import APIBlueprint, Schema, abort
from utils import load_aldus_data
from typing import List
from apiflask.fields import String, Integer
import logging
from http import HTTPStatus


class Contract(Schema):
    slug = String(required=True)
    name = String(required=True)
    description = String(required=True)
    address = String(required=True)
    code = Integer(required=True)
    github = String(required=True)


contracts_bp = APIBlueprint("contracts", __name__)


def load_contracts(chain: str, network: str) -> List[dict]:
    try:
        return load_aldus_data("contracts", chain, network)
    except Exception as e:
        logging.error(f"Error loading data: {e}")
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description="Internal server error")


@contracts_bp.route("/<chain>/<network>/contracts", methods=["GET"])
@contracts_bp.doc(
    summary="Get all contracts",
    description="Get all contract entries for a given chain and network",
)
@contracts_bp.output(Contract(many=True), status_code=200)
def get_contracts(chain: str, network: str) -> List[Contract]:
    """Get contracts for a given chain and network.

    Args:
        chain (str): Chain name.
        network (str): Network name.

    Returns:
        List[Contract]: List of contracts.
    """
    contracts_data = load_contracts(chain, network)
    return contracts_data


@contracts_bp.route("/<chain>/<network>/contracts/<contract_address>", methods=["GET"])
@contracts_bp.doc(
    summary="Get contract by address",
    description="Get a contract entry for a given chain and network by address",
)
@contracts_bp.output(Contract, status_code=200)
def get_contract(chain: str, network: str, contract_address: str) -> Contract:
    """Get contract for a given chain, network and contract_address.

    Args:
        chain (str): Chain name.
        network (str): Network name.
        contract_address (str): Contract address.

    Returns:
        Contract: Contract data.
    """
    contracts_data = load_contracts(chain, network)
    contract = next(
        (c for c in contracts_data if c["address"] == contract_address), None
    )
    if contract:
        return contract
    abort(HTTPStatus.NOT_FOUND, description="Contract not found")
