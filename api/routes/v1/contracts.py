from apiflask import APIBlueprint
from utils import load_aldus_data

contracts_bp = APIBlueprint("contracts", __name__)


def load_contracts(chain, network):
    """Load all contracts for a given chain and network.

    Args:
        chain (str): Chain name.
        network (str): Network name.

    Returns:
        list: List of contracts.
    """
    return load_aldus_data(f"../data/{chain}/{network}/contracts.json")


@contracts_bp.route("/<chain>/<network>/contracts", methods=["GET"])
@contracts_bp.doc(
    summary="Get all contracts",
    description="Get all contract entries for a given chain and network.",
)
def get_contracts(chain, network):
    """Get contracts for a given chain and network.

    Args:
        chain (str): Chain name.
        network (str): Network name.

    Returns:
        list: List of contracts.
    """
    contracts = load_contracts(chain, network)
    return contracts


@contracts_bp.route("/<chain>/<network>/contracts/<contract_address>", methods=["GET"])
@contracts_bp.doc(
    summary="Get a contract by address",
    description="Get a contract entry for a given chain and network by address.",
)
def get_contract(chain, network, contract_address):
    """Get contract for a given chain, network and contract_address.

    Args:
        chain (str): Chain name.
        network (str): Network name.
        contract_address (str): Contract address.

    Returns:
        dict: Contract data.
    """
    contracts = load_contracts(chain, network)
    contract = next(
        (contract for contract in contracts if contract["address"] == contract_address),
        None,
    )
    if not contract:
        return {"error": "Contract not found"}, 404
    return contract
