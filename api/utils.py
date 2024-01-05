import os
import logging
import json

from flask import abort, request


def load_aldus_data(path):
    """
    Load data from a JSON file.

    Args:
        path (str): The path to the JSON file.

    Returns:
        list/dict: The data from the JSON file, or an empty list if the file could not be read.
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


def get_query_param(
    name: str,
    type: type,
    default: any = None,
    required: bool = False,
):
    param = request.args.get(name)
    if param is None:
        if required:
            abort(400, f"{name} {type} is required")
        return default

    if type == bool:
        return param.lower() == "true"
    return type(param)
