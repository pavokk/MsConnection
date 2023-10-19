import json
from typing import Any

import MsConnection

"""
These are typically used for the make functions in functions.py
"""


class Builder:
    def __init__(
            self,
            type_name: str,
            mandatory_attributes: list | tuple | None,
            mandatory_relationships: list | tuple | None
    ):
        self.data = {
            "data": {
                "type": type_name,
                "attributes": {}
            }
        }
        self.mandatory_attributes = mandatory_attributes
        self.mandatory_relationships = mandatory_relationships

    def set_id(self, item_id: str | int | None):
        if item_id is not None:
            self.data["data"]["id"] = item_id

    def set_attribute(self, attribute_name: str, value: Any):
        self.data["data"]["attributes"][attribute_name] = value

    def set_all_attributes(self, attributes: dict, skip: tuple | None = None):
        for key, value in attributes.items():
            if skip is not None and key in skip:
                continue
            self.set_attribute(key, value)

    def set_relationship(self, relationship_name: str, relationship_type: str, id_value: str | int):
        self.validate_relationships()
        self.data["data"]["relationships"][relationship_name] = {
            "data": {
                "type": relationship_type,
                "id": id_value
            }
        }

    def set_relationship_from_list(self, relationship_name: str, relationship_type: str, ids: list | tuple):
        # Some relationships point to more than 1 point.
        self.validate_relationships()
        self.data["data"]["relationships"][relationship_name] = {
            "data": [
                {
                    "type": relationship_type,
                    "id": relationship_id
                } for relationship_id in ids
            ]
        }

    def validate_relationships(self):
        # Adds relationships = {} to data if it does not exist.
        if "relationships" not in self.data["data"]:
            self.data["data"]["relationships"] = {}

    def validate_mandatory_fields(self):
        if self.mandatory_attributes is not None:
            for attribute in self.mandatory_attributes:
                if attribute not in self.data["data"]["attributes"]:
                    raise ValueError(f"Mandatory attribute '{attribute}' is missing.")
        if self.mandatory_relationships is not None:
            for relationship in self.mandatory_relationships:
                if relationship not in self.data["data"]["relationships"]:
                    raise ValueError(f"Mandatory relationship '{relationship}' is missing.")

    def build(self):
        self.validate_mandatory_fields()
        return json.dumps(self.data)


class BatchBuilder:
    def __init__(self):
        self.batch = list()

    def build(self):
        return json.dumps(self.batch)


class ProductBuilder(Builder):
    def __init__(self):
        mandatory_attributes = ("name", "slug", )
        mandatory_relationships = ("categories", )
        super().__init__("products", mandatory_attributes, mandatory_relationships)


class CategoryBuilder(Builder):
    def __init__(self):
        mandatory_attributes = ("name", "slug")
        mandatory_relationships = None
        super().__init__("categories", mandatory_attributes, mandatory_relationships)


class CustomerBuilder(Builder):
    def __init__(self):
        mandatory_attributes = (
            "name", "lastname", "email",
            "address_address", "address_zipcode", "address_city",
            "address_country"
        )
        mandatory_relationships = None
        super().__init__("customers", mandatory_attributes, mandatory_relationships)

    def validate_customer(self):
        # Duplicates values if specific data is set to None
        replacements = {
            "address_name": "name",
            "address_lastname": "lastname",
            "billing_address_name": "name",
            "billing_address_lastname": "lastname",
            "billing_address_company": "address_company",
            "billing_address_company_co": "address_company_co",
            "billing_address_company_number": "address_company_number",
            "billing_address_address": "address_address",
            "billing_address_zipcode": "address_zipcode",
            "billing_address_city": "address_city",
            "billing_address_country": "address_country"
        }

        for key, value in replacements.items():
            if self.data["data"]["attributes"][key] is None:
                self.data["data"]["attributes"][key] = self.data["data"]["attributes"][value]

        for key, value in self.data["data"]["attributes"].items():
            if type(value) != str and value is not None:
                self.data["data"]["attributes"][key] = str(value)


class ProductAttributeBuilder(Builder):
    def __init__(self):
        mandatory_attributes = ("option_values_price", )
        mandatory_relationships = ("product", "product-option", "product-option-value")
        super().__init__("product-attributes", mandatory_attributes, mandatory_relationships)


class ProductVariantBuilder(Builder):
    def __init__(self):
        mandatory_attributes = None
        mandatory_relationships = ("product", "product-attributes")
        super().__init__("product-variants", mandatory_attributes, mandatory_relationships)


class ProductSpecialBuilder(Builder):
    def __init__(self):
        mandatory_attributes = ("specials_price", "status")
        mandatory_relationships = ("product", )
        super().__init__("product-specials", mandatory_attributes, mandatory_relationships)


class ProductReviewBuilder(Builder):
    def __init__(self):
        mandatory_attributes = ("name", "rating", "review")
        mandatory_relationships = ("product", "customer")
        super().__init__("product-reviews", mandatory_attributes, mandatory_relationships)


class ProductOptionBuilder(Builder):
    def __init__(self):
        mandatory_attributes = ("name", "track_stock")
        mandatory_relationships = None
        super().__init__("product-options", mandatory_attributes, mandatory_relationships)


class ProductSuboptionBuilder(Builder):
    def __init__(self):
        mandatory_attributes = ("name", )
        mandatory_relationships = ("product-option", )
        super().__init__("product-suboptions", mandatory_attributes, mandatory_relationships)


class ProductOptionValueBuilder(Builder):
    def __init__(self):
        mandatory_attributes = ("name", )
        mandatory_relationships = ("product-options", )
        super().__init__("product-option-values", mandatory_attributes, mandatory_relationships)


class ProductPropertyBuilder(Builder):
    def __init__(self):
        mandatory_attributes = None
        mandatory_relationships = ("product", "product-property-option", "product-property-value")
        super().__init__("product_properties", mandatory_attributes, mandatory_relationships)


class ProductPropertyOptionBuilder(Builder):
    def __init__(self):
        mandatory_attributes = ("name", "language_code")
        mandatory_relationships = None
        super().__init__("product-property-options", mandatory_attributes, mandatory_relationships)


class ProductPropertyValueBuilder(Builder):
    def __init__(self):
        mandatory_attributes = ("name", "language_code")
        mandatory_relationships = None
        super().__init__("product-property-values", mandatory_attributes, mandatory_relationships)


class ProductTagBuilder(Builder):
    def __init__(self):
        mandatory_attributes = ("key", "value")
        mandatory_relationships = ("product", )
        super().__init__("product-tags", mandatory_attributes, mandatory_relationships)


class CustomerGroupPriceBuilder(Builder):
    def __init__(self):
        mandatory_attributes = ("price", )
        mandatory_relationships = ("product", "customer-group")
        super().__init__("product-customer-group-prices", mandatory_attributes, mandatory_relationships)


class AttributeCustomerGroupPriceBuilder(Builder):
    def __init__(self):
        mandatory_attributes = ("price", "price_prefix")
        mandatory_relationships = ("product", "product-option", "product-option-value", "customer-group")
        super().__init__("product-attribute-customer-group-prices", mandatory_attributes, mandatory_relationships)


class ManufacturerBuilder(Builder):
    def __init__(self):
        mandatory_attributes = ("name", "slug")
        mandatory_relationships = None
        super().__init__("manufacturers", mandatory_attributes, mandatory_relationships)


class DiscountBuilder(Builder):
    def __init__(self):
        mandatory_attributes = ("name", "code", "value")
        mandatory_relationships = None
        super().__init__("discounts", mandatory_attributes, mandatory_relationships)


class TaxClassBuilder(Builder):
    def __init__(self):
        mandatory_attributes = ("tax_rate", "title", "description")
        mandatory_relationships = None
        super().__init__("tax-classes", mandatory_attributes, mandatory_relationships)


class RedirectBuilder(Builder):
    def __init__(self):
        mandatory_attributes = ("code", "scope", "redirect_from", "redirect_to")
        mandatory_relationships = None
        super().__init__("redirects", mandatory_attributes, mandatory_relationships)
