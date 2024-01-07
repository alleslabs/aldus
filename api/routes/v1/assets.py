from apiflask import APIBlueprint, Schema
from apiflask.fields import (
    String,
    Integer,
    List as ListField,
)
from utils import load_aldus_data
from typing import List

assets_bp = APIBlueprint("assets", __name__)


class Asset(Schema):
    coingecko = String(required=True)
    description = String(required=True)
    id = String(required=True)
    logo = String(required=True)
    name = String(required=True)
    precision = Integer(required=True)
    slugs = ListField(String, required=True)
    symbol = String(required=True)
    type = String(required=True)


@assets_bp.route("/<chain>/<network>/assets", methods=["GET"])
@assets_bp.doc(
    summary="Get assets",
    description="Get all assets entries for a given chain and network",
)
@assets_bp.output(Asset(many=True), status_code=200)
def get_assets(chain: str, network: str) -> List[Asset]:
    """
    Get assets for a specific chain and network.

    Args:
      chain (str): The chain name.
      network (str): The network name.

    Returns:
      List[Asset]: A list of assets with their corresponding IDs and price set to 0.00.
    """
    all_assets = load_aldus_data("assets")
    filtered_assets = [
        dict(item, id=item["id"][chain][network])
        for item in all_assets
        if chain in item["id"] and network in item["id"][chain]
    ]
    return filtered_assets
