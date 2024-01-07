from apiflask import APIBlueprint
from utils import load_aldus_data

assets_bp = APIBlueprint("assets", __name__)


def load_assets():
    """Load all assets

    Args:
        chain (str): Chain name.
        network (str): Network name.

    Returns:
        list: List of assets.
    """
    return load_aldus_data(f"../data/assets.json")


@assets_bp.route("/<chain>/<network>/assets", methods=["GET"])
@assets_bp.doc(
    summary="Get assets",
    description="Get all assets entries for a given chain and network",
)
def get_assets(chain, network):
    """
    Get assets for a specific chain and network.

    Args:
      chain (str): The chain name.
      network (str): The network name.

    Returns:
      list: A list of assets with their corresponding IDs and price set to 0.00.
    """
    all_assets = load_assets()
    filtered_assets = [
        dict(item, id=item["id"][chain][network])
        for item in all_assets
        if chain in item["id"] and network in item["id"][chain]
    ]
    network_assets = [dict(asset, **{"price": 0.00}) for asset in filtered_assets]
    return network_assets
