from session import Requestor
import requests


class BaseClient:
    def __init__(self, session: requests.Session, store: str):
        self._r = Requestor(session, store)


class Client(BaseClient):
    def __init__(self, session: requests.Session, store: str):
        super(Client, self).__init__(session, store)

        self.products = Products(session, store)
        self.customers = Customers(session, store)
        self.orders = Orders(session, store)


class MsConnection:

    def __init__(self, store: str, agent: str, token: str, safe_mode: bool = True):
        self.store = store
        self.api_path = f"https://api.mystore.no/shops/{self.store}"
        self.agent = agent
        self.token = token
        self.safe_mode = safe_mode
        self._test_connection()
        self.default_language = self._settings()["default_language"]

        self.products = Products()
        self.customers = Customers()
        self.orders = Orders()

    def _connect_to_path(
            self,
            path,
            vnd: bool = True,
            method: str = 'get',
            data: str | None = None
    ):

        headers = {
            'Content-Type': 'application/vnd.api+json',
            'Accept': 'application/vnd.api+json' if vnd else 'application/json',
            'User-Agent': self.agent,
            'Authorization': f"Bearer {self.token}"
        }

        response = ''

        if (method == 'post' or method == 'patch') and data is None:
            print(f"Error, no data has been passed for the method {method}")
            return 0

        if method == 'get':
            response = requests.get(path, headers=headers)
        elif method == 'post':
            response = requests.post(path, data=data, headers=headers)
        elif method == 'patch':
            response = requests.patch(path, data=data, headers=headers)
        elif method == 'delete':
            response = requests.delete(path, headers=headers)

        return response

    def _test_connection(self) -> str | int:
        connection = self._connect_to_path(f"{self.api_path}/settings", vnd=False)
        try:
            connection.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(e)
        return connection.status_code

    def _settings(self) -> dict:
        return self._connect_to_path(f"{self.api_path}/settings", vnd=False).json()

    def _get_paginated_data(self, endpoint: str) -> list:
        next_page: str | int = f"{self.api_path}/{endpoint}"
        output = list()

        while type(next_page) == str:  # If theres no next page in the response we set next_page to int 0
            response = self._connect_to_path(next_page).json()

            try:
                for data in response["data"]:
                    output.append(data)
            except KeyError as e:
                print(f"Error, no data in response. ({e})")
                break

            if "next" in response["links"]:
                next_page = response["links"]["next"]
            else:
                next_page = 0

        return output

    # PRODUCT METHODS

    def all_products(self):
        return self._get_paginated_data(f"products")

    def product(self, product_id: int | str) -> dict:
        return self._connect_to_path(f"{self.api_path}/products/{product_id}").json()['data']

    def create_product(self, data: str):
        return self._connect_to_path(f"{self.api_path}/products", method='post', data=data)

    def update_product(self, product_id: int | str, data: str):
        return self._connect_to_path(f"{self.api_path}/products/{product_id}", method='patch', data=data)

    def delete_product(self, product_id):
        return self._connect_to_path(f"{self.api_path}/products/{product_id}", method='delete').status_code

    def products_product_categories(self, product_id: int) -> list:
        return self._get_paginated_data(f"products/{product_id}/categories")

    def products_product_attributes(self, product_id: int) -> list:
        return self._get_paginated_data(f"products/{product_id}/product-attributes")

    def products_product_variants(self, product_id: int) -> list:
        return self._get_paginated_data(f"products/{product_id}/product-variants")

    def products_product_specials(self, product_id: int) -> list:
        return self._get_paginated_data(f"products/{product_id}/product-specials")

    def products_product_properties(self, product_id: int) -> list:
        return self._get_paginated_data(f"products/{product_id}/product-properties")

    def products_product_tags(self, product_id: int) -> list:
        return self._get_paginated_data(f"products/{product_id}/product-tags")

    def products_relationships_categories(self, product_id: int) -> tuple:
        response = self._connect_to_path(f"{self.api_path}/products/{product_id}/relationships/categories").json()
        return tuple(int(item['id']) for item in response['data'])

    def update_products_relationships_categories(self, product_id: int, categories: tuple | list) -> int:
        data = {'data': [{'id': category, 'type': 'categories'} for category in categories]}
        return self._connect_to_path(
            f"{self.api_path}/products/{product_id}/relationships/categories",
            method='patch', data=str(data).replace("'", '"')
        ).status_code

    # CATEGORY METHODS

    def all_categories(self):
        return self._get_paginated_data(f"categories")

    def category(self, category_id: int):
        return self._connect_to_path(f"{self.api_path}/categories/{category_id}").json()['data']

    def create_category(self, data: str):
        return self._connect_to_path(f"{self.api_path}/categories", method='post', data=data)

    def update_category(self, category_id: int, data: str):
        return self._connect_to_path(f"{self.api_path}/categories/{category_id}", method='patch', data=data)

    def delete_category(self, category_id: int):
        return self._connect_to_path(f"{self.api_path}/categories/{category_id}", method='delete')

    def categories_products(self, category_id: int):
        return self._get_paginated_data(f"categories/{category_id}/products")

    def categories_relationships_products(self, category_id: int) -> tuple:
        response = self._connect_to_path(f"{self.api_path}/categories/{category_id}/relationships/products").json()
        return tuple(int(item['id']) for item in response['data'])

    def update_categories_relationships_products(self, category_id: int, products: tuple | list) -> int:
        data = {'data': [{'id': product, 'type': 'products'} for product in products]}
        return self._connect_to_path(
            f"{self.api_path}/products/{category_id}/relationships/categories",
            method='patch', data=str(data).replace("'", '"')
        ).status_code

    # CUSTOMER METHODS

    def all_customers(self):
        return self._get_paginated_data(f"customers")

    def customer(self, customer_id: int):
        return self._connect_to_path(f"{self.api_path}/customers/{customer_id}").json()['data']

    def create_customer(self, data: str):
        return self._connect_to_path(f"{self.api_path}/customers", method='post', data=data)

    def update_customer(self, customer_id: int, data: str):
        return self._connect_to_path(f"{self.api_path}/customers/{customer_id}", method='patch', data=data)

    def delete_customer(self, customer_id: int):
        return self._connect_to_path(f"{self.api_path}/customers/{customer_id}", method='delete')

    def customers_orders(self, customer_id: int):
        return self._get_paginated_data(f"customers/{customer_id}/orders")

    # CUSTOMER GROUP METHODS

    def customer_groups(self):
        return self._get_paginated_data(f"customer-groups")

    # PRODUCT ATTRIBUTES METHODS

    def all_product_attributes(self):
        return self._get_paginated_data(f"product-attributes")

    def product_attribute(self, attribute_id: int):
        return self._connect_to_path(f"{self.api_path}/product-attributes/{attribute_id}").json()['data']

    def create_attribute(self, data: str):
        return self._connect_to_path(f"{self.api_path}/product-attributes", method='post', data=data)

    def update_attribute(self, attribute_id: int, data: str):
        return self._connect_to_path(f"{self.api_path}/product-attributes/{attribute_id}", method='patch', data=data)

    def delete_attribute(self, attribute_id: int):
        return self._connect_to_path(f"{self.api_path}/product-attributes/{attribute_id}", method='delete')


class Products(BaseClient):
    def all_products(self):
        return self._get_paginated_data(f"products")

    def product(self, product_id: int | str) -> dict:
        return self._connect_to_path(f"{self.api_path}/products/{product_id}").json()['data']

    def create_product(self, data: str):
        return self._connect_to_path(f"{self.api_path}/products", method='post', data=data)

    def update_product(self, product_id: int | str, data: str):
        return self._connect_to_path(f"{self.api_path}/products/{product_id}", method='patch', data=data)

    def delete_product(self, product_id):
        return self._connect_to_path(f"{self.api_path}/products/{product_id}", method='delete').status_code

    def products_product_categories(self, product_id: int) -> list:
        return self._get_paginated_data(f"products/{product_id}/categories")

    def products_product_attributes(self, product_id: int) -> list:
        return self._get_paginated_data(f"products/{product_id}/product-attributes")

    def products_product_variants(self, product_id: int) -> list:
        return self._get_paginated_data(f"products/{product_id}/product-variants")

    def products_product_specials(self, product_id: int) -> list:
        return self._get_paginated_data(f"products/{product_id}/product-specials")

    def products_product_properties(self, product_id: int) -> list:
        return self._get_paginated_data(f"products/{product_id}/product-properties")

    def products_product_tags(self, product_id: int) -> list:
        return self._get_paginated_data(f"products/{product_id}/product-tags")

    def products_relationships_categories(self, product_id: int) -> tuple:
        response = self._connect_to_path(f"{self.api_path}/products/{product_id}/relationships/categories").json()
        return tuple(int(item['id']) for item in response['data'])

    def update_products_relationships_categories(self, product_id: int, categories: tuple | list) -> int:
        data = {'data': [{'id': category, 'type': 'categories'} for category in categories]}
        return self._connect_to_path(
            f"{self.api_path}/products/{product_id}/relationships/categories",
            method='patch', data=str(data).replace("'", '"')
        ).status_code


class Orders(BaseClient):
    pass


class Customers(BaseClient):
    pass
