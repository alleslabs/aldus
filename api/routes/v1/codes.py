from apiflask import APIBlueprint, Schema, abort
from utils import load_aldus_data
from apiflask.fields import String, Integer
from typing import List
import logging
from http import HTTPStatus


class Code(Schema):
    slug = String(required=True)
    id = Integer(required=True)
    name = String(required=True)
    description = String(required=True)
    github = String(required=True)


codes_bp = APIBlueprint("codes", __name__)


def load_codes(chain: str, network: str) -> List[dict]:
    try:
        return load_aldus_data("codes", chain, network)
    except Exception as e:
        logging.error(f"Error loading data: {e}")
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description="Internal server error")


@codes_bp.route("/<chain>/<network>/codes", methods=["GET"])
@codes_bp.doc(
    summary="Get all codes",
    description="Get all code entries for a given chain and network.",
)
@codes_bp.output(Code(many=True), status_code=200)
def get_codes(chain: str, network: str) -> List[Code]:
    """Get codes for a given chain and network.

    Args:
        chain (str): Chain name.
        network (str): Network name.

    Returns:
        List[Code]: List of codes.
    """
    codes_data = load_codes(chain, network)
    return codes_data


@codes_bp.route("/<chain>/<network>/codes/<int:code_id>", methods=["GET"])
@codes_bp.doc(
    summary="Get code by ID",
    description="Get a code entry for a given chain, network, and code ID",
)
@codes_bp.output(Code, status_code=200)
def get_code(chain: str, network: str, code_id: int) -> Code:
    """Get code for a given chain, network, and code_id.

    Args:
        chain (str): Chain name.
        network (str): Network name.
        code_id (int): Code ID.
    """
    codes_data = load_codes(chain, network)
    code = next((item for item in codes_data if item["id"] == code_id), None)
    if code:
        return code
    abort(HTTPStatus.NOT_FOUND, description="Code not found")
