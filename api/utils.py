import os
import logging
import json

from flask import abort, request


def load_aldus_data_raw(path: str) -> list:
    """
    Load data from a JSON file.

    Args:
        path (str): The path to the JSON file.

    Returns:
        list: The data from the JSON file, or an empty list if the file could not be read.
    """
    if not os.path.exists(path):
        logging.error(f"File not found: {path}")
        return []
    try:
        with open(path, "r") as file:
            return json.load(file)
    except Exception as e:
        logging.error(f"Error reading file {path}: {e}")
        return []


def load_aldus_data(data_type: str, chain: str = None, network: str = None) -> list:
    """
    Load Aldus data based on the specified data type, chain, and network.

    Args:
        data_type (str): The type of data to load (e.g., "accounts", "assets", "chains").
        chain (str, optional): The chain to load the data from. Defaults to None.
        network (str, optional): The network to load the data from. Defaults to None.

    Returns:
        list: The loaded Aldus data.

    Raises:
        FileNotFoundError: If the specified data file is not found.

    """
    aldus_data = []
    match data_type:
        case "accounts":
            aldus_data = load_aldus_data_raw(f"../data/{chain}/{network}/accounts.json")
        case "assets":
            aldus_data = load_aldus_data_raw(f"../data/assets.json")
        case "chains":
            aldus_data = load_aldus_data_raw(f"../data/chains.json")
        case "codes":
            print("CODES")
            aldus_data = load_aldus_data_raw(f"../data/{chain}/{network}/codes.json")
        case "contracts":
            aldus_data = load_aldus_data_raw(
                f"../data/{chain}/{network}/contracts.json"
            )
        case "entities":
            aldus_data = load_aldus_data_raw(f"../data/entities.json")
        case "modules":
            aldus_data = load_aldus_data_raw(f"../data/{chain}/{network}/modules.json")
    return aldus_data


def get_query_param(
    name: str,
    type: type,
    default: any = None,
    required: bool = False,
):
    """
    Get the value of a query parameter from the request arguments.

    Args:
        name (str): The name of the query parameter.
        type (type): The expected type of the query parameter value.
        default (any, optional): The default value to return if the query parameter is not found. Defaults to None.
        required (bool, optional): Whether the query parameter is required. If set to True and the query parameter is not found, a 400 error will be raised. Defaults to False.

    Returns:
        The value of the query parameter, converted to the specified type if possible. If the query parameter is not found and a default value is provided, the default value will be returned.

    Raises:
        BadRequest: If the query parameter is required but not found.
    """

    param = request.args.get(name)
    if param is None:
        if required:
            abort(400, f"{name} {type} is required")
        return default

    if type == bool:
        return param.lower() == "true"
    return type(param)
