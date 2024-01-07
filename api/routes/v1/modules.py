from apiflask import APIBlueprint, Schema, abort
from typing import List
from utils import load_aldus_data
from apiflask.fields import String
import logging
from http import HTTPStatus


class Module(Schema):
    slug = String(required=True)
    address = String(required=True)
    name = String(required=True)
    description = String(required=True)
    github = String(required=True)


modules_bp = APIBlueprint("modules", __name__)


def load_modules(chain: str, network: str) -> List[dict]:
    try:
        return load_aldus_data("modules", chain, network)
    except Exception as e:
        logging.error(f"Error loading data: {e}")
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description="Internal server error")


@modules_bp.route("/<chain>/<network>/modules", methods=["GET"])
@modules_bp.doc(
    summary="Get all modules",
    description="Get all module entries for a given chain and network",
)
@modules_bp.output(Module(many=True), status_code=200)
def get_modules(chain: str, network: str) -> List[Module]:
    """Get modules for a given chain and network.

    Args:
        chain (str): Chain name.
        network (str): Network name.

    Returns:
        List[Module]: List of modules.
    """
    modules_data = load_modules(chain, network)
    return modules_data


@modules_bp.route(
    "/<chain>/<network>/modules/<module_address>/<module_name>", methods=["GET"]
)
@modules_bp.doc(
    summary="Get module by address and name",
    description="Get a module entry for a given chain, network, module_address, and module_name",
)
@modules_bp.output(Module, status_code=200)
def get_module(
    chain: str, network: str, module_address: str, module_name: str
) -> Module:
    """Get module for a given chain, network, module_address, and module_name.

    Args:
        chain (str): Chain name.
        network (str): Network name.
        module_address (str): Module Address.
        module_name (str): Module Name.

    Returns:
        Module: Module data.
    """
    modules_data = load_modules(chain, network)
    module = next(
        (
            m
            for m in modules_data
            if m["address"] == module_address and m["name"] == module_name
        ),
        None,
    )
    if module:
        return module
    abort(HTTPStatus.NOT_FOUND, description="Module not found")
