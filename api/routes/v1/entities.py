from apiflask import APIBlueprint, Schema, abort
from utils import load_aldus_data, get_query_param
from constants import ALDUS_URL
from typing import List
from flask import jsonify
from routes.v1.accounts import Account
from routes.v1.codes import Code
from routes.v1.contracts import Contract
from apiflask.fields import String, Nested, List
from routes.v1.modules import Module
from http import HTTPStatus
import logging


entities_bp = APIBlueprint("entities", __name__)


class Social(Schema):
    name = String(required=True)
    url = String(required=True)


class EntityDetail(Schema):
    description = String(required=True)
    github = String(required=True)
    logo = String(required=True)
    name = String(required=True)
    socials = List(Nested(Social), required=True)
    website = String(required=True)


class Entity(Schema):
    slug = String(required=True)
    details = Nested(EntityDetail, required=True)
    accounts = List(Nested(Account), required=False)
    codes = List(Nested(Code), required=False)
    contracts = List(Nested(Contract), required=False)
    modules = List(Nested(Module), required=False)


class RawEntity(Schema):
    slug = String(required=True)
    name = String(required=True)
    description = String(required=True)
    website = String(required=True)
    logo = String(required=True)
    github = String(required=True)
    socials = List(Nested(Social), required=True)
    accounts = List(Nested(Account), required=False)
    codes = List(Nested(Code), required=False)
    contracts = List(Nested(Contract), required=False)
    modules = List(Nested(Module), required=False)


def get_related_data(entity_slug, chain, network, data_type):
    try:
        data = load_aldus_data(data_type, chain, network)
        return [item for item in data if item["slug"] == entity_slug]
    except Exception as e:
        logging.error(f"Error loading {data_type} data: {e}")
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description="Internal server error")


def get_entity_by_slug(entity_slug: str) -> dict:
    """Get entity data for a given entity.

    Args:
      entity_slug (str): Entity slug.

    Returns:
      Entity: Entity instance.

    Raises:
      ValueError: If the entity is not found.
    """
    entities = load_aldus_data("entities")
    entities_match = [entity for entity in entities if entity["slug"] == entity_slug]
    if not entities_match:
        raise ValueError(f"Entity with slug {entity_slug} not found")
    entity_data = entities_match[0]
    return entity_data


@entities_bp.route("/entities", methods=["GET"])
@entities_bp.doc(summary="Get entities", description="Get all entity entries")
@entities_bp.output(RawEntity(many=True), status_code=200)
def get_entities():
    """
    Get all entity data.

    Returns:
        List[RawEntity]: List of RawEntity instances.
    """
    entity_data = load_aldus_data("entities")
    return [RawEntity(**entity) for entity in entity_data]


@entities_bp.route("<chain>/<network>/entities", methods=["GET"])
@entities_bp.doc(
    summary="Get entities with details",
    description="Get all entities entry and details",
)
@entities_bp.output(Entity(many=True), status_code=200)
def get_entites_details(chain, network):
    """
    Retrieves the details of entities based on the specified chain and network.

    Args:
        chain (str): The chain of the entities.
        network (str): The network of the entities.

    Returns:
        List[Entity]: A list of entity details.

    """

    is_accounts = get_query_param("accounts", default=False, type=bool)
    is_codes = get_query_param("codes", default=False, type=bool)
    is_contracts = get_query_param("contracts", default=False, type=bool)
    is_modules = get_query_param("modules", default=False, type=bool)

    entities = load_aldus_data("entities", chain, network)
    entity_details = []
    for entity in entities:
        entity_accounts = [
            account
            for account in load_aldus_data("accounts", chain, network)
            if account["slug"] == entity["slug"]
        ]
        entity_codes = [
            code
            for code in load_aldus_data("codes", chain, network)
            if code["slug"] == entity["slug"]
        ]
        entity_contracts = [
            contract
            for contract in load_aldus_data("contracts", chain, network)
            if contract["slug"] == entity["slug"]
        ]
        entity_modules = [
            module
            for module in load_aldus_data("modules", chain, network)
            if module["slug"] == entity["slug"]
        ]

        if (
            not entity_accounts
            and not entity_codes
            and not entity_contracts
            and not entity_modules
        ):
            continue
        entity_entry = {}
        entity_entry["slug"] = entity["slug"]
        entity_entry["details"] = {
            "name": entity["name"],
            "description": entity["description"],
            "website": entity["website"],
            "logo": f'{ALDUS_URL}/assets/entities/{entity["logo"]}',
            "github": entity["github"],
            "socials": entity["socials"],
        }
        if is_accounts:
            entity_entry["accounts"] = entity_accounts
        if is_codes:
            entity_entry["codes"] = entity_codes
        if is_contracts:
            entity_entry["contracts"] = entity_contracts
        if is_modules:
            entity_entry["modules"] = entity_modules
        entity_details.append(entity_entry)
    return entity_details


@entities_bp.route("<chain>/<network>/entities/<entity_slug>", methods=["GET"])
@entities_bp.doc(
    summary="Get entity details by slug",
    description="Get entity entry and details by slug",
)
@entities_bp.output(Entity, status_code=200)
def get_entity_by_network(chain: str, network: str, entity_slug: str) -> Entity:
    """
    Get entity data for a given chain, network, and entity.

    Args:
        chain (str): Chain name.
        network (str): Network name.
        entity_slug (str): Entity slug.

    Returns:
        Entity: An instance of the Entity class with the entity data.

    Raises:
        NotFoundError: If the entity with the given slug is not found.
    """
    is_accounts = get_query_param("accounts", default=False, type=bool)
    is_codes = get_query_param("codes", default=False, type=bool)
    is_contracts = get_query_param("contracts", default=False, type=bool)
    is_modules = get_query_param("modules", default=False, type=bool)

    entity_entry = get_entity_by_slug(entity_slug)
    entity = {
        "slug": entity_entry["slug"],
        "details": {
            "name": entity_entry["name"],
            "description": entity_entry["description"],
            "website": entity_entry["website"],
            "logo": f"{ALDUS_URL}/assets/entities/{entity_entry['logo']}",
            "github": entity_entry["github"],
            "socials": entity_entry["socials"],
        },
    }
    if is_accounts:
        entity["accounts"] = [
            account
            for account in load_aldus_data("accounts", chain, network)
            if account["slug"] == entity["slug"]
        ]
    if is_codes:
        entity["codes"] = [
            code
            for code in load_aldus_data("codes", chain, network)
            if code["slug"] == entity["slug"]
        ]
    if is_contracts:
        entity["contracts"] = [
            contract
            for contract in load_aldus_data("contracts", chain, network)
            if contract["slug"] == entity["slug"]
        ]
    if is_modules:
        entity["modules"] = [
            module
            for module in load_aldus_data("modules", chain, network)
            if module["slug"] == entity["slug"]
        ]
    return entity
