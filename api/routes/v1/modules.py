from apiflask import APIBlueprint
from utils import load_aldus_data

modules_bp = APIBlueprint("modules", __name__)


def load_modules(chain, network):
    """Load all modules for a given chain and network.

    Args:
        chain (str): Chain name.
        network (str): Network name.

    Returns:
        list: List of modules.
    """
    if chain != "initia":
        return []
    return load_aldus_data(f"../data/{chain}/{network}/modules.json")


@modules_bp.route("/<chain>/<network>/modules", methods=["GET"])
@modules_bp.doc(
    summary="Get all modules",
    description="Get all module entries for a given chain and network",
)
def get_modules(chain, network):
    """Get modules for a given chain and network.

    Args:
        chain (str): Chain name.
        network (str): Network name.

    Returns:
        list: List of modules.
    """
    modules = load_modules(chain, network)
    return modules


@modules_bp.route(
    "/<chain>/<network>/modules/<module_address>/<module_name>", methods=["GET"]
)
@modules_bp.doc(
    summary="Get module by address and name",
    description="Get a module entry for a given chain, network, module_address, and module_name",
)
def get_module(chain, network, module_address, module_name):
    """Get module for a given chain, network, module_address, and module_name.

    Args:
        chain (str): Chain name.
        network (str): Network name.
        module_address (str): Module Address.
        module_name (str): Module Name.

    Returns:
        dict: Module data.
    """
    if chain != "initia":
        return []
    modules = load_modules(chain, network)
    module = next(
        (
            module
            for module in modules
            if module["address"] == module_address and module["name"] == module_name
        ),
        None,
    )
    if not module:
        return {"error": "Module not found"}, 404
    return module
