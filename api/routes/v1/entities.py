from apiflask import APIBlueprint
from utils import load_aldus_data, get_query_param
from routes.v1.accounts import get_accounts
from routes.v1.codes import get_codes
from routes.v1.contracts import get_contracts
from routes.v1.modules import get_modules
from constants import ALDUS_URL

entities_bp = APIBlueprint("entities", __name__)


def load_entity(entity_slug):
    """Load an entity by its slug.

    Args:
      entity_slug (str): The slug of the entity.

    Returns:
      dict: The entity data, or None if the entity was not found.
    """
    entity_data = load_aldus_data(f"../data/entities.json")
    entities = [entity for entity in entity_data if entity["slug"] == entity_slug]
    return entities[0] if entities else None


@entities_bp.route("/entities", methods=["GET"])
@entities_bp.doc(summary="Get entities", description="Get all entiy entries")
def get_entities():
    """Get all entity data

    Returns:
      list: List of entities.
    """
    entity_data = load_aldus_data(f"../data/entities.json")
    return entity_data


@entities_bp.route("/entities/<entity_slug>", methods=["GET"])
@entities_bp.doc(
    summary="Get an entity by slug", description="Get an entity entry by slug"
)
def get_entity(entity_slug):
    """Get entity data for a given entity.

    Args:
      entity_slug (str): Entity slug.

    Returns:
      dict: Entity.
    """
    entity = load_entity(entity_slug)
    if not entity:
        return {"error": "Entity not found"}, 404
    return entity


@entities_bp.route("<chain>/<network>/entities/<entity_slug>", methods=["GET"])
@entities_bp.doc(
    summary="Get entity details by slug",
    description="Get entity entry and details by slug",
)
def get_entity_by_network(chain, network, entity_slug):
    """Get entity data for a given chain, network and entity.

    Args:
      chain (str): Chain name.
      network (str): Network name.
      entity_slug (str): Entity slug.

    Returns:
      dict: Entity.
    """
    is_accounts = get_query_param("accounts", default=False, type=bool)
    is_codes = get_query_param("codes", default=False, type=bool)
    is_contracts = get_query_param("contracts", default=False, type=bool)
    is_modules = get_query_param("modules", default=False, type=bool)

    entity_entry = load_entity(entity_slug)
    if not entity_entry:
        return {"error": "Entity not found"}, 404

    entity = {
        "slug": entity_entry["slug"],
        "details": {
            "name": entity_entry["name"],
            "description": entity_entry["description"],
            "website": entity_entry["website"],
            "logo": f'{ALDUS_URL}/assets/entities/{entity_entry["logo"]}',
            "github": entity_entry["github"],
            "socials": entity_entry["socials"],
        },
    }
    if is_accounts:
        accounts = get_accounts(chain, network)
        entity["accounts"] = [
            account for account in accounts if account["slug"] == entity_slug
        ]
    if is_codes:
        codes = get_codes(chain, network)
        entity["codes"] = [code for code in codes if code["slug"] == entity_slug]
    if is_contracts:
        contracts = get_contracts(chain, network)
        entity["contracts"] = [
            contract for contract in contracts if contract["slug"] == entity_slug
        ]
    if is_modules:
        modules = get_modules(chain, network)
        entity["modules"] = [
            module for module in modules if module["slug"] == entity_slug
        ]
    return entity
