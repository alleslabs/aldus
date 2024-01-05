from apiflask import APIBlueprint
from utils import load_aldus_data

codes_bp = APIBlueprint("codes", __name__)


def load_codes(chain, network):
    """Load all codes for a given chain and network.

    Args:
        chain (str): Chain name.
        network (str): Network name.

    Returns:
        list: List of codes.
    """
    return load_aldus_data(f"../data/{chain}/{network}/codes.json")


@codes_bp.route("/<chain>/<network>/codes", methods=["GET"])
@codes_bp.doc(
    summary="Get all codes",
    description="Get all code entries for a given chain and network.",
)
def get_codes(chain, network):
    """Get codes for a given chain and network.

    Args:
        chain (str): Chain name.
        network (str): Network name.

    Returns:
        list: List of codes.
    """
    codes = load_codes(chain, network)
    return codes


@codes_bp.route("/<chain>/<network>/codes/<code_id>", methods=["GET"])
@codes_bp.doc(
    summary="Get a code",
    description="Get a code entry for a given chain, network and code ID",
)
def get_code(chain, network, code_id):
    """Get code for a given chain, network and code_id.

    Args:
        chain (str): Chain name.
        network (str): Network name.
        code_id (int): Code ID.

    Returns:
        dict: Code data.
    """
    code_id = int(code_id)
    codes = load_codes(chain, network)
    code = next((code for code in codes if code["id"] == code_id), None)
    if not code:
        return {"error": "Code not found"}, 404
    return code
