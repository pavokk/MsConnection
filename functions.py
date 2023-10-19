import json
import Builder
import MsConnection


def make_product(
        name: dict,
        slug: dict,
        category_ids: list | tuple,
        tax_class_id: str | int | None = None,
        manufacturer_id: str | int | None = None,
        product_id: str | int | None = None,
        description: dict | None = None,
        meta_title: dict | None = None,
        meta_description: dict | None = None,
        meta_keywords: dict | None = None,
        viewed_count: dict | None = None,
        price: str | int | float | None = None,
        cost: str | int | float | None = None,
        image: str | None = None,
        image2: str | None = None,
        image3: str | None = None,
        image4: str | None = None,
        image5: str | None = None,
        image6: str | None = None,
        image7: str | None = None,
        image8: str | None = None,
        quantity: str | int | None = None,
        sku: str | int | None = None,
        status: str | int | None = None,
        weight: str | int | float | None = None,
        location: str | None = None,
        country_of_origin: str | None = None,
        button_type: str | None = None,
        ean: str | int | None = None,
        ordered_count: str | int | None = None,
        manufacturer_sku: str | int | None = None,
        notes: str | None = None,
        created_at: str | None = None,
        updated_at: str | None = None,
        sort: str | int | None = None,
) -> str:

    arguments = locals()
    skip = ("product_id", "category_ids", "tax_class_id", "manufacturer_id")

    product = Builder.ProductBuilder()
    product.set_all_attributes(arguments, skip)
    product.set_relationship_from_list("categories", "categories", category_ids)
    product.set_id(product_id)

    if tax_class_id is not None:
        product.set_relationship("tax-class", "tax-classes", tax_class_id)

    if manufacturer_id is not None:
        product.set_relationship("manufacturer", "manufacturers", manufacturer_id)

    return product.build()


def make_product_with_variants(product: str, product_option: str, ):
    pass


def make_category(
        name: dict,
        slug: dict,
        category_id: str | int | None = None,
        image: str | None = None,
        status: str | int | None = None,
        created_at: str | None = None,
        updated_at: str | None = None,
        sort: str | int | None = None,
        description: dict | None = None,
        meta_title: dict | None = None,
        meta_description: dict | None = None,
        parent: str | int | None = None
) -> str:

    arguments = locals()
    skip = ("category_id", "parent")

    category = Builder.CategoryBuilder()
    category.set_all_attributes(arguments, skip)
    category.set_id(category_id)

    if parent is not None:
        category.set_relationship("parent", "categories", parent)

    return category.build()


def make_customer(
        name: str,
        lastname: str,
        email: str,
        address_address: str,
        address_zipcode: str | int,
        address_city: str,
        address_country: str,
        customer_id: str | int | None = None,
        gender: str | None = None,
        phone: str | int | None = None,
        fax: str | int | None = None,
        newsletter: str | int | None = None,
        billing_email: str | None = None,
        dob: str | None = None,
        last_login: str | None = None,
        created_at: str | None = None,
        updated_at: str | None = None,
        address_name: str | None = None,
        address_lastname: str | None = None,
        address_company: str | None = None,
        address_company_co: str | None = None,
        address_company_number: str | int | None = None,
        address_region: str | None = None,
        address_state: str | None = None,
        billing_address_name: str | None = None,
        billing_address_lastname: str | None = None,
        billing_address_company: str | None = None,
        billing_address_company_co: str | None = None,
        billing_address_company_number: str | int | None = None,
        billing_address_address: str | None = None,
        billing_address_region: str | None = None,
        billing_address_state: str | None = None,
        billing_address_zipcode: str | int | None = None,
        billing_address_city: str | None = None,
        billing_address_country: str | None = None
):
    """
    Function to create a customer ready to insert through Customer.create(), will duplicate name and address if
    only one is supplied.
    :return: A Json string with customer data ready to import.
    """

    arguments = locals()

    customer = Builder.CustomerBuilder()
    customer.set_all_attributes(arguments)
    customer.validate_customer()
    customer.set_id(customer_id)

    return customer.build()


def make_product_attribute(
        product_id: str | int,
        product_option_id: str | int,
        product_option_value_id: str | int,
        product_attribute_id: str | int | None = None,
        values_price: str | int | float = 0,
        weight: str | int | float | None = None,
        image: str | None = None,
):
    product_attribute = Builder.ProductAttributeBuilder()

    product_attribute.set_all_attributes({
        "option_values_price": values_price,
        "option_values_price_prefix": "+",
        "weight": weight,
        "image": image,
    })

    product_attribute.set_relationship("product", "products", product_id)
    product_attribute.set_relationship("product-option", "product-options", product_option_id)
    product_attribute.set_relationship("product-option-value", "product-option-values", product_option_value_id)
    product_attribute.set_id(product_attribute_id)

    return product_attribute.build()


def make_product_variant(
        product_id: str | int,
        product_attributes: list | tuple,
        product_variant_id: str | int | None = None,
        quantity: str | int | None = None,
        sku: str | int | None = None,
        cost: str | int | float | None = None,
        ean: str | int | None = None
):
    product_variant = Builder.ProductVariantBuilder()

    product_variant.set_all_attributes({
        "quantity": quantity,
        "sku": sku,
        "cost": cost,
        "ean": ean
    })

    product_variant.set_relationship("product", "products", product_id)
    product_variant.set_relationship_from_list("product-attributes", "product-attributes", product_attributes)
    product_variant.set_id(product_variant_id)

    return product_variant.build()


def make_product_special(
        product_id: str | int,
        specials_price: str | int | float,
        status: str | int,
        special_id: str | int | None = None,
        created_at: str | None = None,
        updated_at: str | None = None,
        expires_at: str | None = None,
        status_changed_at: str | None = None
):
    arguments = locals()
    skip = ("product_id", "special_id")

    product_special = Builder.ProductSpecialBuilder()
    product_special.set_all_attributes(arguments, skip)
    product_special.set_relationship("product", "products", product_id)
    product_special.set_id(special_id)

    return product_special.build()


def make_product_review(
        name: str,
        rating: str | int,
        review: dict,
        product_id: str | int,
        customer_id: str | int,
        review_id: str | int | None = None,
        created_at: str | None = None,
        updated_at: str | None = None,
) -> str:
    arguments = locals()
    skip = ("product_id", "customer_id", "review_id")

    product_review = Builder.ProductReviewBuilder()
    product_review.set_all_attributes(arguments, skip)
    product_review.set_relationship("product", "products", product_id)
    product_review.set_relationship("customer", "customers", customer_id)
    product_review.set_id(review_id)

    return product_review.build()


def make_product_option(
        name: dict,
        track_stock: str | int,
        product_option_id: str | int | None = None,
        sort: str | int | None = None,
        comment: str | None = None,
        element_type: str | None = None,
):
    arguments = locals()
    skip = ("product_option_id", )

    product_option = Builder.ProductOptionBuilder()
    product_option.set_all_attributes(arguments, skip)
    product_option.set_id(product_option_id)

    return product_option.build()


def make_product_suboption(
        name: str,
        product_option_id: str | int,
        suboption_id: str | int | None = None
):
    product_suboption = Builder.ProductSuboptionBuilder()
    product_suboption.set_attribute("name", name)
    product_suboption.set_relationship("product-option", "product-options", product_option_id)
    product_suboption.set_id(suboption_id)

    return product_suboption.build()


def make_product_option_value(
        name: dict,
        product_option_ids: list | tuple,
        product_option_value_id: str | int | None = None,
        sort: str | int | None = None
):
    arguments = locals()
    skip = ("product_option_ids", "product_option_value_id")

    product_option_value = Builder.ProductOptionValueBuilder()
    product_option_value.set_all_attributes(arguments, skip)
    product_option_value.set_relationship_from_list("product-options", "product-options", product_option_ids)
    product_option_value.set_id(product_option_value_id)

    return product_option_value.build()


def make_product_property(
        product_id: str | int,
        property_option_id: str | int,
        property_value_id: str | int,
        property_id: str | int | None = None,
        sort: str | int | None = None,
) -> str:
    product_property = Builder.ProductPropertyBuilder()
    product_property.set_attribute("sort", sort)
    product_property.set_relationship("product", "products", product_id)
    product_property.set_relationship("product-property-option", "product-property-options", property_option_id)
    product_property.set_relationship("product-property-value", "product-property-values", property_value_id)
    product_property.set_id(property_id)

    return product_property.build()


def make_property_option(
        name: str,
        language_code: str,
        property_option_id: str | int | None = None
) -> str:
    property_option = Builder.ProductPropertyOptionBuilder()
    property_option.set_attribute("name", name)
    property_option.set_attribute("language_code", language_code)
    property_option.set_id(property_option_id)

    return property_option.build()


def make_property_value(
        name: str,
        language_code: str,
        property_value_id: str | int | None = None
) -> str:
    property_value = Builder.ProductPropertyValueBuilder()
    property_value.set_attribute("name", name)
    property_value.set_attribute("language_code", language_code)
    property_value.set_id(property_value_id)

    return property_value.build()


def make_product_tag(
        key: str,
        value: str | int,
        product_id: str | int,
        tag_id: str | int | None = None
) -> str:
    product_tag = Builder.ProductTagBuilder()
    product_tag.set_attribute("key", key)
    product_tag.set_attribute("value", value)
    product_tag.set_relationship("product", "products", product_id)
    product_tag.set_id(tag_id)
    return product_tag.build()


def make_customer_group_price(
        price: str | int | float,
        product_id: str | int,
        customer_group_id: str | int,
        tax_class_id: str | int | None = None,
        customer_group_price_id: str | int | None = None
) -> str:
    customer_group_price = Builder.CustomerGroupPriceBuilder()
    customer_group_price.set_attribute("price", price)
    customer_group_price.set_relationship("product", "products", product_id)
    customer_group_price.set_relationship("customer-group", "customer-groups", customer_group_id)
    customer_group_price.set_id(customer_group_price_id)

    if tax_class_id is not None:
        customer_group_price.set_relationship("tax-class", "tax-classes", tax_class_id)

    return customer_group_price.build()


def make_attribute_customer_group_price(
        price: str | int | float,
        product_id: str | int,
        option_id: str | int,
        value_id: str | int,
        customer_group_id: str | int,
        tax_class_id: str | int | None = None,
        attribute_customer_group_price_id: str | int | None = None
) -> str:

    acgp = Builder.AttributeCustomerGroupPriceBuilder()
    acgp.set_attribute("price", price)
    acgp.set_attribute("price_prefix", "+")
    acgp.set_relationship("product", "products", product_id)
    acgp.set_relationship("product-option", "product-options", option_id)
    acgp.set_relationship("product-option-value", "product-option-values", value_id)
    acgp.set_relationship("customer-group", "customer-groups", customer_group_id)

    if tax_class_id is not None:
        acgp.set_relationship("tax-class", "tax-classes", tax_class_id)

    acgp.set_id(attribute_customer_group_price_id)

    return acgp.build()


def make_manufacturer(
        name: str,
        slug: dict,
        manufacturer_id: str | int | None = None,
        image: str | None = None,
        created_at: str | None = None,
        updated_at: str | None = None,
        sort: str | int | None = None,
        description: dict | None = None,
        url: dict | None = None,
        meta_title: dict | None = None,
        meta_description: dict | None = None,
):
    arguments = locals()

    manufacturer = Builder.ManufacturerBuilder()
    manufacturer.set_all_attributes(arguments, ("manufacturer_id", ))
    manufacturer.set_id(manufacturer_id)

    return manufacturer.build()


def make_discount(
        name: dict,
        code: str,
        value: str | int | float,
        discount_id: str | int | None = None,
        value_type: str | int = 2,
        combinable: bool = False,
        treshold_value: str | int | float = 0,
        value_can_transcend_order_total: str | int = 1,
        valid_for_product_specials: str | int = 0,
        valid_from: str | None = None,
        valid_to: str | None = None,
        valid_times: str | int = 0,
        valid_for_all_products: str | int = 1,
        valid_for_product_ids: list | tuple | None = None,
        valid_for_category_ids: list | tuple | None = None,
        valid_for_manufacturer_ids: list | tuple | None = None,
        allow_partial_use: str | int = 1,
        remaining_value: str | int | float | None = None,
        limited_to_customer_id: str | int = 0,
        only_most_expensive_product: str | int = 0,
        use_original_price: str | int = 0
) -> str:

    """
    Create a discount code. PS: There is no practical way to create a quantity discount, as you can't pass values
    through.

    :param name: Description of discount code
    :param code: Code to be entered in checkout
    :param value: Value of the code, purely a number
    :param discount_id: Specify ID of discount if you want
    :param value_type: 1 for percentage, 2 for amount
    :param combinable: Can discount be combined with specials?
    :param treshold_value: Minimum value for discount code to kick in
    :param value_can_transcend_order_total:
    :param valid_for_product_specials:
    :param valid_from:
    :param valid_to:
    :param valid_times:
    :param valid_for_all_products:
    :param valid_for_product_ids:
    :param valid_for_category_ids:
    :param valid_for_manufacturer_ids:
    :param allow_partial_use:
    :param remaining_value:
    :param limited_to_customer_id:
    :param only_most_expensive_product:
    :param use_original_price:
    :return:
    """

    # Turns lists into comma separated strings if there is data in them
    valid_for_product_ids = ",".join(valid_for_product_ids) if valid_for_product_ids is not None else ""
    valid_for_category_ids = ",".join(valid_for_category_ids) if valid_for_category_ids is not None else ""
    valid_for_manufacturer_ids = ",".join(valid_for_manufacturer_ids) if valid_for_manufacturer_ids is not None else ""

    if remaining_value is None:
        remaining_value = value

    arguments = locals()

    discount = Builder.DiscountBuilder()
    discount.set_all_attributes(arguments, ("discount_id", ))
    discount.set_id(discount_id)

    return discount.build()


def make_tax_class(
        tax_rate: str | int,
        tax_class_id: str | int | None = None,
        title: str | None = None,
        description: str | None = None,
        created_at: str | None = None,
        updated_at: str | None = None
) -> str:
    arguments = locals()
    tax_class = Builder.TaxClassBuilder()
    tax_class.set_all_attributes(arguments, ("tax_class_id", ))
    tax_class.set_id(tax_class_id)

    return tax_class.build()


def make_redirect(
        redirect_from: str,
        redirect_to: str,
        redirect_id: str | int | None = None,
        code: str | int = 301,
        scope: str = "global",
        created_at: str | None = None,
        language: str = "no"
) -> str:

    arguments = locals()
    redirect = Builder.RedirectBuilder()
    redirect.set_all_attributes(arguments, ("redirect_id", ))
    redirect.set_id(redirect_id)

    return redirect.build()


def make_order(
        client: MsConnection.Client,
        customer_id: str | int,
        order_status_id: str | int,
        fetch_customer_data: bool,
        order_id: str | int | None = None,
        customer_address_name: str | None = None,
        customer_address_company: str | None = None,
        customer_address_address: str | None = None,
        customer_address_region: str | None = None,
        customer_address_city: str | None = None,
        customer_address_zipcode: str | int | None = None,
        customer_address_state: str | None = None,
        customer_address_country: str | None = None,
        customer_address_phone: str | None = None,
        customer_address_email: str | None = None,
        shipping_address_name: str | None = None,
        shipping_address_company: str | None = None,
        shipping_address_address: str | None = None,
        shipping_address_region: str | None = None,
        shipping_address_city: str | None = None,
        shipping_address_zipcode: str | int | None = None,
        shipping_address_state: str | None = None,
        shipping_address_country: str | None = None,
        billing_address_name: str | None = None,
        billing_address_company: str | None = None,
        billing_address_address: str | None = None,
        billing_address_region: str | None = None,
        billing_address_city: str | None = None,
        billing_address_zipcode: str | int | None = None,
        billing_address_state: str | None = None,
        billing_address_country: str | None = None,
        billing_address_email: str | None = None,
        company_number: str | int | None = None,
        payment_method: str | None = None,
        payment_module: str | None = None,
        updated_at: str | None = None,
        created_at: str | None = None,
        finished_at: str | None = None,
        currency: str = "NOK",
        currency_value: str | int | float = 1.000000,
        invoice_id: str | int | None = None,
        invoice_due_at: str | None = None,
        shipping_method: str | None = None,
        tracking_number: str | None = None,
        overdue_notice: str | None = None,
        overdue_notice_due_at: str | None = None,
        credit_note: str | int | None = None,
        credit_note_created_at: str | None = None,
        reference: str | None = None,
        estimated_delivery_at: str | None = None
):
    order = {
        "data": {
            "type": "orders",
            "attributes": {
                "customer_address_name": customer_address_name,
                "customer_address_company": customer_address_company,
                "customer_address_address": customer_address_address,
                "customer_address_region": customer_address_region,
                "customer_address_city": customer_address_city,
                "customer_address_zipcode": customer_address_zipcode,
                "customer_address_state": customer_address_state,
                "customer_address_country": customer_address_country,
                "customer_address_phone": customer_address_phone,
                "customer_address_email": customer_address_email,
                "shipping_address_name": shipping_address_name,
                "shipping_address_company": shipping_address_company,
                "shipping_address_address": shipping_address_address,
                "shipping_address_region": shipping_address_region,
                "shipping_address_city": shipping_address_city,
                "shipping_address_zipcode": shipping_address_zipcode,
                "shipping_address_state": shipping_address_state,
                "shipping_address_country": shipping_address_country,
                "billing_address_name": billing_address_name,
                "billing_address_company": billing_address_company,
                "billing_address_address": billing_address_address,
                "billing_address_region": billing_address_region,
                "billing_address_city": billing_address_city,
                "billing_address_zipcode": billing_address_zipcode,
                "billing_address_state": billing_address_state,
                "billing_address_country": billing_address_country,
                "billing_address_email": billing_address_email,
                "company_number": company_number,
                "payment_method": payment_method,
                "payment_module": payment_module,
                "updated_at": updated_at,
                "created_at": created_at,
                "finished_at": finished_at,
                "currency": currency,
                "currency_value": currency_value,
                "invoice_id": invoice_id,
                "invoice_due_at": invoice_due_at,
                "shipping_method": shipping_method,
                "tracking_number": tracking_number,
                "overdue_notice": overdue_notice,
                "overdue_notice_due_at": overdue_notice_due_at,
                "credit_note": credit_note,
                "credit_note_created_at": credit_note_created_at,
                "reference": reference,
                "estimated_delivery_at": estimated_delivery_at
            },
            "relationships": {
                "customer": {
                    "data": {
                        "type": "customers",
                        "id": customer_id
                    }
                },
                "order_status": {
                    "data": {
                        "type": "customers",
                        "id": order_status_id
                    }
                }
            }
        }
    }

    if fetch_customer_data:
        customer = client.customers.get(customer_id)

        order["data"]["attributes"]["customer_address_name"] = customer["attributes"]["name"] if \
            customer["attributes"]["address_name"] is None else customer["attributes"]["address_name"]
        order["data"]["attributes"]["customer_address_company"] = customer["attributes"]["address_company"]
        order["data"]["attributes"]["customer_address_address"] = customer["attributes"]["address_address"]
        order["data"]["attributes"]["customer_address_region"] = customer["attributes"]["address_region"]
        order["data"]["attributes"]["customer_address_city"] = customer["attributes"]["address_city"]
        order["data"]["attributes"]["customer_address_zipcode"] = customer["attributes"]["address_zipcode"]
        order["data"]["attributes"]["customer_address_state"] = customer["attributes"]["address_state"]
        order["data"]["attributes"]["customer_address_country"] = customer["attributes"]["address_country"]
        order["data"]["attributes"]["customer_address_phone"] = customer["attributes"]["phone"]
        order["data"]["attributes"]["customer_address_email"] = customer["attributes"]["email"]

        if shipping_address_name is None:
            order["data"]["attributes"]["shipping_address_name"] = customer["attributes"]["name"] if \
                customer["attributes"]["address_name"] is None else customer["attributes"]["address_name"]
            order["data"]["attributes"]["shipping_address_company"] = customer["attributes"]["address_company"]
            order["data"]["attributes"]["shipping_address_address"] = customer["attributes"]["address_address"]
            order["data"]["attributes"]["shipping_address_region"] = customer["attributes"]["address_region"]
            order["data"]["attributes"]["shipping_address_city"] = customer["attributes"]["address_city"]
            order["data"]["attributes"]["shipping_address_zipcode"] = customer["attributes"]["address_zipcode"]
            order["data"]["attributes"]["shipping_address_state"] = customer["attributes"]["address_state"]
            order["data"]["attributes"]["shipping_address_country"] = customer["attributes"]["address_country"]

        order["data"]["attributes"]["billing_address_name"] = customer["attributes"]["billing_address_name"]
        order["data"]["attributes"]["billing_address_company"] = customer["attributes"]["billing_address_company"]
        order["data"]["attributes"]["billing_address_address"] = customer["attributes"]["billing_address_address"]
        order["data"]["attributes"]["billing_address_region"] = customer["attributes"]["billing_address_region"]
        order["data"]["attributes"]["billing_address_city"] = customer["attributes"]["billing_address_city"]
        order["data"]["attributes"]["billing_address_zipcode"] = customer["attributes"]["billing_address_zipcode"]
        order["data"]["attributes"]["billing_address_state"] = customer["attributes"]["billing_address_state"]
        order["data"]["attributes"]["billing_address_country"] = customer["attributes"]["billing_address_country"]
        order["data"]["attributes"]["billing_address_email"] = customer["attributes"]["billing_address_email"]

        order["data"]["attributes"]["company_number"] = customer["attributes"]["address_company_number"]

    if order_id is not None:
        order["data"]["id"] = order_id

    return json.dumps(order)


def make_order_product():
    pass


def make_order_product_attribute():
    pass


def make_order_status_history():
    pass


def make_order_total():
    pass


def make_order_with_known_products(
        client: MsConnection.Client,
        customer_id: str | int,
        product_ids: dict,
        order_status_id: str | int,
        order_status_comment: str | None = None,
        customer_address_name: str | None = None,
        customer_address_company: str | None = None,
        customer_address_address: str | None = None,
        customer_address_region: str | None = None,
        customer_address_city: str | None = None,
        customer_address_zipcode: str | int | None = None,
        customer_address_state: str | None = None,
        customer_address_country: str | None = None,
        customer_address_phone: str | None = None,
        customer_address_email: str | None = None,
        shipping_address_name: str | None = None,
        shipping_address_company: str | None = None,
        shipping_address_address: str | None = None,
        shipping_address_region: str | None = None,
        shipping_address_city: str | None = None,
        shipping_address_zipcode: str | int | None = None,
        shipping_address_state: str | None = None,
        shipping_address_country: str | None = None,
        billing_address_name: str | None = None,
        billing_address_company: str | None = None,
        billing_address_address: str | None = None,
        billing_address_region: str | None = None,
        billing_address_city: str | None = None,
        billing_address_zipcode: str | int | None = None,
        billing_address_state: str | None = None,
        billing_address_country: str | None = None,
        billing_address_email: str | None = None,
        company_number: str | int | None = None,
        payment_method: str | None = None,
        payment_module: str | None = None,
        updated_at: str | None = None,
        created_at: str | None = None,
        finished_at: str | None = None,
        currency: str = "NOK",
        currency_value: str | int | float = 1.000000,
        invoice_id: str | int | None = None,
        invoice_due_at: str | None = None,
        shipping_method: str | None = None,
        tracking_number: str | None = None,
        overdue_notice: str | None = None,
        overdue_notice_due_at: str | None = None,
        credit_note: str | int | None = None,
        credit_note_created_at: str | None = None,
        reference: str | None = None,
        estimated_delivery_at: str | None = None
):
    pass
