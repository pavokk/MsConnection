from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, NamedTuple, Tuple, TypeVar, Union, cast

import requests

import MsConnection


def format_filter(attribute: str, value: str, operand: str = "=") -> str:
    return f"?filter[{attribute}][path]={attribute}&filter[{attribute}][value]{operand}{value}"


def not_none(val) -> bool:
    return True if val is not None else False


def validate_object(mandatory: str | tuple | list) -> bool:
    if type(mandatory) == str:
        return not_none(mandatory)
    return False if None in mandatory else True


def convert_if_datetime(date: datetime | str | None) -> str:
    """
    If date argument is a datetime object this function converts it to this format: %Y-%m-%d %H:%M:%S
    :param date: Date as datetime or string
    :return: String of date passed through, formatted or not changed.
    """
    return date.strftime('%Y-%m-%d %H:%M:%S') if type(date) == datetime else date


def get_localized_attribute(attribute: str | dict | None, default_language: str) -> dict | None:
    if attribute is None:
        return None

    if isinstance(attribute, dict):
        return attribute

    return {default_language: attribute}


def build_attributes(simple: dict, localized: dict | None, default_language: str) -> dict:
    attributes = dict()

    for key, value in simple.items():
        if value is not None:
            attributes[key] = value

    if type(localized) == dict:
        for key, value in localized.items():
            loc_value = get_localized_attribute(value, default_language)
            if loc_value is not None:
                attributes[key] = loc_value

    return attributes


def convert_object_to_json_str(object_type: str, attributes: dict, object_id: int | None, relationships: dict | None):
    data = {
        "data": {
            "type": object_type,
        }
    }

    if object_id is not None:
        data["data"]["id"] = str(object_id)

    data["data"]["attributes"] = attributes

    if relationships is not None:
        data["data"]["relationships"] = relationships

    return json.dumps(data, indent=2)


def all_categories_without_children(categories: dict) -> set:
    categories_without_children = set()
    parent_ids = set()

    for category in categories:
        parent = category['relationships']['parent']['data']
        if parent is not None:
            parent_ids.add(parent['id'])

    for category in categories:
        category_id = category['id']
        if category_id not in parent_ids:
            categories_without_children.add(category_id)

    return categories_without_children


def all_categories_without_parents(categories: dict) -> set:
    categories_without_parents = set()

    for category in categories:
        parent = category['relationships']['parent']['data']
        category_id = category['id']
        if parent is None:
            categories_without_parents.add(category_id)

    return categories_without_parents


def move_all_main_categories_into_common_category(session: MsConnection.Client, categories: dict, main_cat: int | str):
    movables = [pid for pid in all_categories_without_parents(categories) if pid != str(main_cat)]

    for cat in movables:
        update = {
            "data": {
                "id": cat,
                "relationships": {
                    "parent": {
                        "data": {
                            "type": "categories",
                            "id": str(main_cat)
                        }
                    }
                }
            }
        }
        session.categories.update_category(int(cat), json.dumps(update, indent=2))


def get_mime(file: str):
    mimes = {
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "png": "image/png",
        "gif": "image/gif",
        "webp": "image/webp"
    }
    return mimes[file.split(".")[-1]]

