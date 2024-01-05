from apiflask import APIBlueprint
from utils import load_aldus_data

globals_bp = APIBlueprint("globals", __name__)


@globals_bp.route("/globals/chains", methods=["GET"])
@globals_bp.doc(summary="Get all chains", description="Get all chain entries")
def get_globals_chains():
    aldus_chain_data = load_aldus_data("../data/chains.json")
    return aldus_chain_data


@globals_bp.route("/globals/assets", methods=["GET"])
@globals_bp.doc(summary="Get assets", description="Get all asset entries")
def get_globals_assets():
    aldus_asset_data = load_aldus_data("../data/assets.json")
    return aldus_asset_data
