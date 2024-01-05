from apiflask import APIBlueprint

from . import accounts, codes, contracts, globals, modules, entities

v1_bp = APIBlueprint("v1", __name__, url_prefix="/v1")

v1_bp.register_blueprint(accounts.accounts_bp)
v1_bp.register_blueprint(codes.codes_bp)
v1_bp.register_blueprint(contracts.contracts_bp)
v1_bp.register_blueprint(globals.globals_bp)
v1_bp.register_blueprint(modules.modules_bp)
v1_bp.register_blueprint(entities.entities_bp)
