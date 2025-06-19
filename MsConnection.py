import json
import os

import requests
from .session import Requestor
from .MsExceptions import MsExceptions


class BaseClient:
    endpoint = None
    vnd = True
    permissions = {
        "all": False,
        "get": False,
        "create": False,
        "update": False,
        "delete": False,
    }

    def __init__(self, session: requests.Session, store: str):
        self._r = Requestor(session, store)

    def all_items(self, endpoint: str, only_id: bool = False):
        all_items = self._r.get_paginated(endpoint)

        if only_id:
            return [item['id'] for item in all_items]

        return all_items

    def _validate_call(self, permission: str):
        if self.endpoint is None:
            raise NotImplementedError("Endpoint not defined")
        if not self.permissions[permission]:
            raise MsExceptions.EndpointPermissionError("Subclass does not have permission to use this method")

    def all(self, only_id: bool = False, endpoint: str | None = None) -> list:

        self._validate_call("all")
        all_items = self._r.get_paginated(self.endpoint if endpoint is None else endpoint)

        return [item['id'] for item in all_items] if only_id else all_items

    def get(self, item_id: int | str | None, endpoint: str | None = None):

        if item_id is None and endpoint is None:
            raise MsExceptions.MissingID("Call has no item_id")

        self._validate_call("get")
        return self._r.get(f"{self.endpoint}/{item_id}" if endpoint is None else endpoint, vnd=self.vnd).json()['data']

    def create(self, data: str | dict, endpoint: str | None = None):

        self._validate_call("create")
        return self._r.post(self.endpoint if endpoint is None else endpoint, data, vnd=self.vnd)

    def update(self, item_id: str | int, data: str | dict):

        self._validate_call("update")
        return self._r.patch(f"{self.endpoint}/{item_id}", data, vnd=self.vnd)

    def delete(self, item_id) -> int:

        self._validate_call("delete")
        return self._r.delete(f"{self.endpoint}/{item_id}", vnd=self.vnd).status_code
    
    def get_singleton(self, endpoint : str | None = None):
        self._validate_call("all")
        return self._r.get(f"{self.endpoint}" if endpoint is None else endpoint, vnd=self.vnd).json()


class Client(BaseClient):
    def __init__(self, session: requests.Session, store: str):
        super().__init__(session, store)
        self.batch = Batch(session, store)
        self.products = Products(session, store)
        self.categories = Categories(session, store)
        self.customers = Customers(session, store)
        self.customer_groups = CustomerGroups(session, store)
        self.customer_login_tokens = CustomerLoginTokens(session, store)
        self.images = Images(session, store)
        self.product_attributes = ProductAttributes(session, store)
        self.product_variants = ProductVariants(session, store)
        self.product_specials = ProductSpecials(session, store)
        self.product_reviews = ProductReviews(session, store)
        self.product_options = ProductOptions(session, store)
        self.product_suboptions = ProductSuboptions(session, store)
        self.product_option_values = ProductOptionValues(session, store)
        self.product_properties = ProductProperties(session, store)
        self.product_property_options = ProductPropertyOptions(session, store)
        self.product_property_values = ProductPropertyValues(session, store)
        self.product_tags = ProductTags(session, store)
        self.product_customer_group_prices = ProductCustomerGroupPrices(session, store)
        self.product_attribute_customer_group_prices = ProductAttributeCustomerGroupPrices(session, store)
        self.orders = Orders(session, store)
        self.order_products = OrderProducts(session, store)
        self.order_product_attributes = OrderProductAttributes(session, store)
        self.order_status = OrderStatus(session, store)
        self.order_status_history = OrderStatusHistory(session, store)
        self.order_tags = OrderTags(session, store)
        self.order_totals = OrderTotals(session, store)
        self.manufacturers = Manufacturers(session, store)
        self.suppliers = Suppliers(session, store)
        self.discounts = Discounts(session, store)
        self.tax_classes = TaxClasses(session, store)
        self.visitors = Visitors(session, store)
        self.redirects = Redirects(session, store)
        self.settings = Settings(session, store)
        self.shipping = Shipping(session, store)
        self.payment = Payment(session, store)
        self.currencies = Currencies(session, store)
        self.languages = Languages(session, store)
        self.product_tabs = ProductTabs(session, store)
        self.campaigns = Campaigns(session, store)
        self.campaign_products = CampaignProducts(session, store)
        self.stock_groups = StockGroups(session, store)
        self.stock_group_rules = StockGroupRules(session, store)
        self.product_tab_descriptions = ProductTabDescriptions(session, store)
        self.product_sets = ProductSets(session, store)


class Batch(BaseClient):
    endpoint = "atomic-batch"
    vnd = False
    permissions = {
        "all": False,
        "get": False,
        "create": True,
        "update": False,
        "delete": False,
    }

    def non_atomic(self, data: str):
        return self.create(data=data, endpoint="non-atomic-batch")

    def atomic(self, data: str):
        return self.create(data=data)


class Products(BaseClient):

    """
    Connecting to the endpoint '/products'.
    """

    endpoint = "products"
    permissions = {
        "all": True,
        "get": True,
        "create": True,
        "update": True,
        "delete": True,
    }

    # Relationships

    def categories(self, product_id: int, only_id: bool = False) -> list:

        """
        Returns all categories that product is in.
        :param product_id: ID of product
        :param only_id: If you only want the category ID's set this to True
        :return: All categories connected to the product, as list.
        """

        return self.all_items(f"products/{product_id}/categories", only_id)

    def product_attributes(self, product_id: int) -> list:
        return self.all_items(f"products/{product_id}/product-attributes")

    def product_variants(self, product_id: int) -> list:
        return self.all_items(f"products/{product_id}/product-variants")

    def product_specials(self, product_id: int) -> list:
        return self.all_items(f"products/{product_id}/product-specials")

    def product_properties(self, product_id: int) -> list:
        return self.all_items(f"products/{product_id}/product-properties")

    def product_tags(self, product_id: int | str) -> list:
        return self.all_items(f"products/{product_id}/product-tags")

    def relationships_categories(self, product_id: int) -> tuple:
        response = self._r.get(f"products/{product_id}/relationships/categories").json()
        return tuple(int(item['id']) for item in response['data'])

    def update_relationships_categories(self, product_id: int, categories: tuple | list) -> int:
        data = {'data': [{'id': category, 'type': 'categories'} for category in categories]}
        return self._r.patch(f"products/{product_id}/relationships/categories", json.dumps(data)).status_code


class Categories(BaseClient):
    endpoint = "categories"
    permissions = {
        "all": True,
        "get": True,
        "create": True,
        "update": True,
        "delete": True,
    }

    # Relationships
    def products(self, category_id: int | str, only_id: bool = False):
        return self.all_items(f"categories/{category_id}/products", only_id)

    def update_relationships_products(self, category_id: int, products: tuple | list) -> int:
        data = {'data': [{'id': product, 'type': 'products'} for product in products]}
        return self._r.patch(f"products/{category_id}/relationships/products", str(data).replace("'", '"')).status_code


class Customers(BaseClient):

    """
    Notes for now:
    email
    name, lastname x3 (can use same for all 3)
    address, zip, city, country x2 (can use same for both)
    """

    endpoint = "customers"
    permissions = {
        "all": True,
        "get": True,
        "create": True,
        "update": True,
        "delete": True,
    }

    # Relationships
    def product_reviews(self, customer_id: int | str):
        return self.all_items(f"customers/{customer_id}/product-reviews")

    def orders(self, customer_id: int | str):
        return self.all_items(f"customers/{customer_id}/orders", False)


class CustomerGroups(BaseClient):
    endpoint = "customer-groups"
    permissions = {
        "all": True,
        "get": False,
        "create": False,
        "update": False,
        "delete": False,
    }


class CustomerLoginTokens(BaseClient):
    endpoint = "customer-login-tokens"
    permissions = {
        "all": True,
        "get": False,
        "create": True,
        "update": False,
        "delete": False,
    }


class Images(BaseClient):
    endpoint = "images"
    vnd = False
    permissions = {
        "all": False,
        "get": False,
        "create": False,
        "update": False,
        "delete": False,
    }

    def upload_image(self, path: str, file_path: str):

        body = (
            "-----BOUNDARY\r\n"
            "Content-Disposition: form-data; name=\"image\"; filename=\"image.jpeg\"\r\n"
            "Content-Type: image/jpeg\r\n"
            "\r\n"
            "-----BOUNDARY\r\n"
        )

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        file_type = file_path.split('.')[-1]

        if file_type not in ('jpg', 'jpeg', 'gif', 'png', 'webp'):
            raise FileNotFoundError(f"File not an image file, filetype: {file_type}")

        with open(file_path, 'rb') as file:
            files = {
                'image': (os.path.basename(file_path), file, f"image/{file_type}")  # Adjust content type accordingly
            }

            return Requestor._request('POST', path, vnd=False, data=body, content_type=None, files=files)


class ProductAttributes(BaseClient):
    endpoint = "product-attributes"
    permissions = {
        "all": True,
        "get": True,
        "create": True,
        "update": True,
        "delete": True,
    }


class ProductVariants(BaseClient):
    endpoint = "product-variants"
    permissions = {
        "all": True,
        "get": True,
        "create": True,
        "update": True,
        "delete": True,
    }


class ProductSpecials(BaseClient):
    endpoint = "product-specials"
    permissions = {
        "all": True,
        "get": True,
        "create": True,
        "update": True,
        "delete": True,
    }


class ProductReviews(BaseClient):
    endpoint = "product-reviews"
    permissions = {
        "all": True,
        "get": True,
        "create": True,
        "update": False,
        "delete": True,
    }


class ProductOptions(BaseClient):
    endpoint = "product-options"
    permissions = {
        "all": True,
        "get": True,
        "create": True,
        "update": True,
        "delete": True,
    }

    # TODO: Add relationships for product-options
    def all_suboptions(self, product_option_id: str | int, only_id: bool = False):
        return self.all_items(f"product-options/{product_option_id}/product-suboptions", only_id)

    def all_option_values(self, product_option_id: str | int, only_id: bool = False):
        return self.all_items(f"product-options/{product_option_id}/product-option-values", only_id)

    def list_option_value_pivots(self, product_option_id: str | int):
        return self.get(f"product-options/{product_option_id}/relationships/product-option-values")

    def update_option_value_pivots(
            self,
            product_option_id: str | int,
            option_values: list[str | int] | tuple[str | int]
    ):
        pivots = {
            "data": [
                {
                    "id": option_value,
                    "type": "product-option-values"
                } for option_value in option_values
            ]
        }

        return self._r.patch(
            f"product-options/{product_option_id}/relationships/product-option-values",
            data=json.dumps(pivots)
        )


class ProductSuboptions(BaseClient):
    endpoint = "product-suboptions"
    permissions = {
        "all": True,
        "get": False,
        "create": True,
        "update": True,
        "delete": True,
    }

    # TODO: Add relationships for product-suboptions


class ProductOptionValues(BaseClient):
    endpoint = "product-option-values"
    permissions = {
        "all": True,
        "get": True,
        "create": True,
        "update": True,
        "delete": True,
    }

    def all_product_options(self, product_option_value_id: str | int):
        return self.get(f"{product_option_value_id}/relationships/product-options")

    def all_product_suboptions(self, product_option_value_id: str | int):
        return self.get(f"{product_option_value_id}/relationships/product-suboptions")

    def update_product_suboptions(self, product_option_value_id: str | int, suboption_id: str | int):
        data = {
            "data": [
                {
                    "id": suboption_id,
                    "type": "product-suboptions"
                }
            ]
        }

        return self._r.patch(
            f"product-option-values/{product_option_value_id}/relationships/product-suboptions",
            data=json.dumps(data)
        )


class ProductProperties(BaseClient):
    endpoint = "product-properties"
    permissions = {
        "all": True,
        "get": True,
        "create": True,
        "update": False,
        "delete": True,
    }


class ProductPropertyOptions(BaseClient):
    endpoint = "product-property-options"
    permissions = {
        "all": True,
        "get": True,
        "create": True,
        "update": True,
        "delete": True,
    }


class ProductPropertyValues(BaseClient):
    endpoint = "product-property-values"
    permissions = {
        "all": True,
        "get": True,
        "create": True,
        "update": True,
        "delete": True,
    }


class ProductTags(BaseClient):
    endpoint = "product-tags"
    permissions = {
        "all": True,
        "get": True,
        "create": True,
        "update": False,
        "delete": True,
    }

    # Convencience
    def add_tag_to_product(self, product_id: str | int, tag_name: str, tag_value: str):
        tag = {
            "data": {
                "type": "product-tags",
                "attributes": {
                    "key": tag_name,
                    "value": tag_value
                },
                "relationships": {
                    "product": {
                        "data": {
                            "type": "products",
                            "id": str(product_id)
                        }
                    }
                }
            }
        }
        return self.create(json.dumps(tag))


class ProductCustomerGroupPrices(BaseClient):
    endpoint = "product-customer-group-prices"
    permissions = {
        "all": True,
        "get": False,
        "create": True,
        "update": True,
        "delete": True,
    }


class ProductAttributeCustomerGroupPrices(BaseClient):
    endpoint = "product-attribute-customer-group-prices"
    permissions = {
        "all": True,
        "get": False,
        "create": True,
        "update": True,
        "delete": True,
    }


class Orders(BaseClient):
    endpoint = "orders"
    permissions = {
        "all": True,
        "get": True,
        "create": True,
        "update": True,
        "delete": True,
    }

    # Relationships
    def complete_order(self, order_id: int | str, data: str | dict):
        return self._r.patch(f"orders/{order_id}/complete", data, vnd=False)

    def order_totals(self, order_id: int | str):
        return self.all_items(f"orders/{order_id}/order-totals")

    def order_products(self, order_id: int | str):
        return self.all_items(f"orders/{order_id}/order-products")

    def order_status_history(self, order_id: int | str):
        return self.all_items(f"orders/{order_id}/order-status-history")

    def order_tags(self, order_id: int | str):
        return self.all_items(f"orders/{order_id}/order-tags")

    # TODO: Figure out convenience methods for orders


class OrderProducts(BaseClient):
    """
    On the POST /order-products and PATCH /order-products/{id} endpoints,
    it's possible to send a meta object in the request body to toggle the adjust inventory setting on and off.

    When the adjust inventory setting is on, it will automatically decrement (or increment) the inventory
    of a product or product variant that the order product has a relationship to,
    adjusting its inventory count by the quantity that is set on the order product.

    For more information on how to use this feature and its known limitations,
    please refer to this appendix: http://docs.mystoreapi.apiary.io/#introduction/appendices/6.-adjust-inventory-meta.
    """

    endpoint = "order-products"
    permissions = {
        "all": True,
        "get": True,
        "create": True,
        "update": True,
        "delete": True,
    }

    # TODO: More relationships

    def order_product_attributes(self, order_product_id: str | int):
        return self._r.get(f"order-products/{order_product_id}/order-product-attributes")


class OrderProductAttributes(BaseClient):
    endpoint = "order-product-attributes"
    permissions = {
        "all": True,
        "get": True,
        "create": True,
        "update": False,
        "delete": True,
    }


class OrderStatus(BaseClient):
    endpoint = "order-status"
    permissions = {
        "all": True,
        "get": True,
        "create": False,
        "update": False,
        "delete": False,
    }


class OrderStatusHistory(BaseClient):
    endpoint = "order-status-history"
    permissions = {
        "all": False,
        "get": False,
        "create": True,
        "update": False,
        "delete": False,
    }


class OrderTags(BaseClient):
    endpoint = "order-tags"
    permissions = {
        "all": True,
        "get": False,
        "create": True,
        "update": False,
        "delete": False,
    }


class OrderTotals(BaseClient):
    endpoint = "order-totals"
    permissions = {
        "all": True,
        "get": True,
        "create": True,
        "update": True,
        "delete": True,
    }


class Manufacturers(BaseClient):
    endpoint = "manufacturers"
    permissions = {
        "all": True,
        "get": True,
        "create": True,
        "update": False,
        "delete": True,
    }


class Suppliers(BaseClient):
    endpoint = "suppliers"
    permissions = {
        "all": True,
        "get": False,
        "create": False,
        "update": False,
        "delete": False,
    }


class Discounts(BaseClient):
    endpoint = "discounts"
    permissions = {
        "all": True,
        "get": False,
        "create": True,
        "update": False,
        "delete": False,
    }


class TaxClasses(BaseClient):
    endpoint = "tax-classes"
    permissions = {
        "all": True,
        "get": True,
        "create": True,
        "update": False,
        "delete": True,
    }


class Visitors(BaseClient):

    """
    The visitors resource is newsletter subscriptions for users that has only signed up for the
    newsletter without purchasing anything to becoming a customer of that shop.
    """

    endpoint = "visitors"
    permissions = {
        "all": True,
        "get": False,
        "create": False,
        "update": False,
        "delete": False,
    }


class Redirects(BaseClient):
    endpoint = "redirects"
    permissions = {
        "all": True,
        "get": True,
        "create": True,
        "update": False,
        "delete": True,
    }


class Settings(BaseClient):
    endpoint = "settings"
    vnd = False
    permissions = {
        "all": True,
        "get": False,
        "create": False,
        "update": False,
        "delete": False,
    }


class Shipping(BaseClient):

    """
    Endpoint to get installed shipping methods, for each method you get "name" and "method"
    """

    endpoint = "shipping"
    vnd = False
    permissions = {
        "all": True,
        "get": False,
        "create": False,
        "update": False,
        "delete": False,
    }


class Payment(BaseClient):

    """
    Endpoint to get all payment modules, for each module you get "name" and "method".
    This only returns modules installed through /kontrollpanel/modules.php?selected_box=modules&set=payment
    Klarna Checkout and other full checkouts won't be listed here.
    """

    endpoint = "payment"
    vnd = False
    permissions = {
        "all": True,
        "get": False,
        "create": False,
        "update": False,
        "delete": False,
    }


class Currencies(BaseClient):
    endpoint = "currencies"
    permissions = {
        "all": True,
        "get": False,
        "create": False,
        "update": False,
        "delete": False,
    }


class Languages(BaseClient):
    endpoint = "languages"
    permissions = {
        "all": True,
        "get": False,
        "create": False,
        "update": False,
        "delete": False,
    }


class Campaigns(BaseClient):
    endpoint = "campaigns"
    permissions = {
        "all": True,
        "get": False,
        "create": False,
        "update": False,
        "delete": False,
    }

    def campaign_products(self, campaign_id: str | int):
        return self._r.get(f"campaigns/{campaign_id}/campaign-products")


class CampaignProducts(BaseClient):
    endpoint = "campaign-products"
    permissions = {
        "all": True,
        "get": False,
        "create": False,
        "update": False,
        "delete": False,
    }


class StockGroups(BaseClient):
    endpoint = "stock-groups"
    permissions = {
        "all": True,
        "get": False,
        "create": False,
        "update": False,
        "delete": False,
    }

    def stock_group_rules(self, stock_group_id: str | int):
        return self._r.get(f"stock-groups/{stock_group_id}/stock-group-rules")


class StockGroupRules(BaseClient):
    endpoint = "stock-group-rules"
    permissions = {
        "all": True,
        "get": False,
        "create": False,
        "update": False,
        "delete": False,
    }


class ProductTabs(BaseClient):
    endpoint = 'product-tabs'
    permissions = {
        "all": True,
        "get": False,
        "create": True,
        "update": False,
        "delete": False,
    }

    def product_tabs_description(self, product_tab_id: str | int):
        return self._r.get(f"product-tabs/{product_tab_id}/product-tabs-description")


class ProductTabDescriptions(BaseClient):
    endpoint = 'product-tabs-description'
    permissions = {
        "all": True,
        "get": False,
        "create": True,
        "update": False,
        "delete": False,
    }

class ProductSets(BaseClient):
    endpoint = 'product-sets'
    permissions = {
        "all": True,
        "get": True,
        "create": True,
        "update": False,
        "delete": True,
    }