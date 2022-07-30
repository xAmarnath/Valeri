from requests import post

r = post(
    "https://voucherpub.com/wp-admin/admin-ajax.php",
    data={
        "attribute_package": "12 Months",
        "quantity": "1",
        "add-to-cart": "1514",
        "product_id": "1514",
        "variation_id": "1517",
        "action": "basel_ajax_add_to_cart",
    },
)

print(r.headers)
