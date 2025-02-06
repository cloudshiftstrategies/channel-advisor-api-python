from urllib.parse import urlencode
from channel_advisor_api.models.channel_advisor import MinProduct, FullProduct
from unittest.mock import patch, MagicMock
import pytest
import json
from unittest.mock import call


def test_product_model(mock_product_dict):
    product = MinProduct.model_validate(mock_product_dict)
    assert product.sku == "TEST-SKU-123"
    assert product.id == 12345
    assert product.title == "Test Product Title"


@patch("channel_advisor_api.models.channel_advisor_client.requests")
def test_product_client(mock_requests, mock_product_dict, mock_environ):
    product = MinProduct.model_validate(mock_product_dict)
    client = product.client
    client.request("get", "Products(123)")
    mock_requests.request.assert_called_once()


def test_product_get_property_names():
    property_names = [field.alias for field in MinProduct.model_fields.values()]
    assert MinProduct.get_property_names() == property_names
    assert MinProduct.get_property_names(as_param=True) == {"$select": ",".join(property_names)}


@patch("channel_advisor_api.models.channel_advisor_client.requests")
def test_product_get_client(mock_requests, mock_environ):
    client = MinProduct.get_client()
    client.request("get", "Products(123)")
    mock_requests.request.assert_called_once()


def test_product_by_id(mock_ca_client, mock_product_dict):
    # Mock the get_client class method
    mock_req_res = MagicMock()
    mock_req_res.content = json.dumps(mock_product_dict)
    mock_ca_client().request.return_value = mock_req_res
    product = MinProduct.by_id(123)
    assert product.id == 12345  # from the mock_product_dict


def test_product_by_id_not_found(mock_ca_client, mock_product_dict):
    # Mock the get_client class method
    mock_ca_client().request.return_value = None
    with pytest.raises(ValueError):
        MinProduct.by_id(123)


def test_product_by_id_no_content(mock_ca_client, mock_product_dict):
    mock_req_res = MagicMock()
    mock_req_res.content = json.dumps({})
    mock_ca_client().request.return_value = mock_req_res
    with pytest.raises(ValueError):
        MinProduct.by_id(123)


def test_product_all(mock_ca_client, mock_product_dict):
    mock_ca_client().get_all_pages.return_value = [mock_product_dict]
    products = MinProduct.all()
    assert len(products) == 1
    assert products[0].id == 12345


def test_product_all_args(mock_ca_client, mock_product_dict):
    mock_ca_client().get_all_pages.return_value = [mock_product_dict]
    MinProduct.all(limit=10, filter="my-filter", order_by="my-order-by")
    expected_params = {
        "$orderby": "my-order-by",
        "$select": ",".join(MinProduct.get_property_names()),
        "$filter": "my-filter",
    }
    expected_uri = f"Products?{urlencode(expected_params, doseq=True)}"
    mock_ca_client().get_all_pages.assert_called_once_with(expected_uri, limit=10)


def test_product_by_sku(mock_ca_client, mock_product_dict):
    mock_ca_client().get_all_pages.return_value = [mock_product_dict]
    MinProduct.by_sku("TEST-SKU-123")
    expected_params = {
        "$orderby": "Sku",
        "$select": ",".join(MinProduct.get_property_names()),
        "$filter": "Sku eq 'TEST-SKU-123'",
    }
    expected_uri = f"Products?{urlencode(expected_params, doseq=True)}"
    mock_ca_client().get_all_pages.assert_called_once_with(expected_uri, limit=None)


def test_product_by_sku_not_found(mock_ca_client):
    mock_ca_client().get_all_pages.return_value = []
    with pytest.raises(ValueError):
        MinProduct.by_sku("TEST-SKU-123")


def test_product_search_by_sku(mock_ca_client, mock_product_dict):
    response = MagicMock()
    response.ok = True
    response.content = json.dumps({"value": [mock_product_dict]})
    mock_ca_client().request.return_value = response
    MinProduct.search_by_sku("TEST-SKU-123")
    expected_params = {
        "$orderby": "Sku",
        "$filter": "Sku ge 'TEST-SKU-123' and (IsParent eq true or IsInRelationship eq false)",
        "$select": ",".join(MinProduct.get_property_names()),
    }
    expected_uri = f"Products?{urlencode(expected_params, doseq=True)}"
    mock_ca_client().request.assert_called_once_with("get", expected_uri)


def test_product_search_by_sku_paged(mock_ca_client, mock_product_dict):
    response_1 = MagicMock()
    response_1.ok = True
    response_1.content = json.dumps({"value": [mock_product_dict], "@odata.nextLink": "next-link"})
    response_2 = MagicMock()
    response_2.ok = True
    response_2.content = json.dumps({"value": [mock_product_dict]})
    mock_ca_client().request.side_effect = [response_1, response_2]
    products = MinProduct.search_by_sku("TEST-SKU-123")
    expected_params = {
        "$orderby": "Sku",
        "$filter": "Sku ge 'TEST-SKU-123' and (IsParent eq true or IsInRelationship eq false)",
        "$select": ",".join(MinProduct.get_property_names()),
    }
    expected_uri = f"Products?{urlencode(expected_params, doseq=True)}"
    mock_ca_client().request.assert_has_calls(
        [
            call("get", expected_uri),
            call("get", "next-link"),
        ]
    )
    assert len(products) == 2


def test_product_search_by_sku_paged_partial_match(mock_ca_client, mock_product_dict):
    response_1 = MagicMock()
    response_1.ok = True
    response_1.content = json.dumps({"value": [mock_product_dict], "@odata.nextLink": "next-link"})
    response_2 = MagicMock()
    response_2.ok = True
    # change the 2nd product sku to a partial match
    mock_product_dict["Sku"] = "TEZZZ"
    response_2.content = json.dumps({"value": [mock_product_dict]})
    mock_ca_client().request.side_effect = [response_1, response_2]
    products = MinProduct.search_by_sku("TEST-SKU-123")
    expected_params = {
        "$orderby": "Sku",
        "$filter": "Sku ge 'TEST-SKU-123' and (IsParent eq true or IsInRelationship eq false)",
        "$select": ",".join(MinProduct.get_property_names()),
    }
    expected_uri = f"Products?{urlencode(expected_params, doseq=True)}"
    mock_ca_client().request.assert_has_calls(
        [
            call("get", expected_uri),
            call("get", "next-link"),
        ]
    )
    assert len(products) == 1


def test_product_search_by_sku_limit(mock_ca_client, mock_product_dict):
    response = MagicMock()
    response.ok = True
    response.content = json.dumps({"value": [mock_product_dict]})
    mock_ca_client().request.return_value = response
    MinProduct.search_by_sku("TEST-SKU-123", limit=5)
    expected_params = {
        "$orderby": "Sku",
        "$filter": "Sku ge 'TEST-SKU-123' and (IsParent eq true or IsInRelationship eq false)",
        "$select": ",".join(MinProduct.get_property_names()),
        "$top": [5],
    }
    expected_uri = f"Products?{urlencode(expected_params, doseq=True)}"
    assert mock_ca_client().request.call_count == 1
    mock_ca_client().request.assert_called_once_with("get", expected_uri)


def test_product_search_by_sku_with_include_children(mock_ca_client, mock_product_dict):
    response = MagicMock()
    response.ok = True
    response.content = json.dumps({"value": [mock_product_dict]})
    mock_ca_client().request.return_value = response
    MinProduct.search_by_sku("TEST-SKU-123", include_children=True)
    expected_params = {
        "$orderby": "Sku",
        "$filter": "Sku ge 'TEST-SKU-123'",
        "$select": ",".join(MinProduct.get_property_names()),
    }
    expected_uri = f"Products?{urlencode(expected_params, doseq=True)}"
    mock_ca_client().request.assert_called_once_with("get", expected_uri)


def test_product_base(mock_ca_client, mock_product_dict):
    mock_ca_client().get_all_pages.return_value = [mock_product_dict]
    MinProduct.model_validate(mock_product_dict)
    assert len(MinProduct.get_property_names()) == len(MinProduct.get_property_names())


def test_product_full(mock_ca_client, mock_product_dict):
    mock_ca_client().get_all_pages.return_value = [mock_product_dict]
    FullProduct.model_validate(mock_product_dict)
    assert len(FullProduct.get_property_names()) == len(FullProduct.get_property_names())


def test_product_base_save(mock_ca_client, mock_product_dict):
    product = MinProduct.model_validate(mock_product_dict)
    product.save()
    expected_data = {
        "Sku": "TEST-SKU-123",
        "Title": "Test Product Title",
        "Subtitle": "Test Subtitle",
        "Brand": "Test Brand",
        "Description": "Test product description",
        "ShortDescription": "Short desc",
        "ASIN": "B00EXAMPLE",
        "ProductType": "Standard",
        "IsParent": False,
        "IsInRelationship": False,
    }
    mock_ca_client().request.assert_has_calls([call("put", f"Products({product.id})", data=expected_data)])
    mock_ca_client().get_all_pages.assert_not_called()
    mock_ca_client().request.assert_called_once


@pytest.mark.parametrize(
    "include_fields",
    [None, ["sku", "title", "short_description"], ["Sku"]],  # This will raise an exception
)
def test_product_base_save_to_children(mock_ca_client, mock_product_dict, include_fields):
    mock_ca_client().get_all_pages.return_value = [
        {"ParentProductID": mock_product_dict["ID"], "ChildProductID": 123},
        {"ParentProductID": mock_product_dict["ID"], "ChildProductID": 456},
    ]
    product = MinProduct.model_validate(mock_product_dict)
    if include_fields and "Sku" in include_fields:
        with pytest.raises(ValueError):
            # Sku is not a valid field for children, so model_data will be empty and raise an exception
            product.save_to_children(include_fields=include_fields)
        return
    else:
        product.save_to_children(include_fields=include_fields)
    if not include_fields:
        expected_data = {
            "Sku": "TEST-SKU-123",
            "Title": "Test Product Title",
            "Subtitle": "Test Subtitle",
            "Brand": "Test Brand",
            "Description": "Test product description",
            "ShortDescription": "Short desc",
            "ASIN": "B00EXAMPLE",
            "ProductType": "Standard",
            "IsParent": False,
            "IsInRelationship": False,
        }
    else:
        expected_data = {
            "Sku": "TEST-SKU-123",
            "Title": "Test Product Title",
            "ShortDescription": "Short desc",
        }
    mock_ca_client().get_all_pages.assert_called_once_with(f"Products({product.id})/Children")
    mock_ca_client().request.assert_has_calls(
        [
            call("put", "Products(123)", data=expected_data),
            call("put", "Products(456)", data=expected_data),
        ]
    )
    assert mock_ca_client().request.call_count == 2


def test_product_attributes(mock_product_attributes, mock_ca_client, mock_product_dict):
    product = MinProduct.model_validate(mock_product_dict)
    # Add an arbitrary attribute to the mock_product_attributes
    mock_product_attributes.append({"ProductID": product.id, "ProfileID": product.id, "Name": "foo", "Value": "bar"})
    mock_ca_client().get_all_pages.return_value = mock_product_attributes
    attributes = product.attributes
    assert attributes.AMZ_Category == "Automotive"
    assert attributes.Bullet_01 == "My Test"
    # Not currently allowing extra attributes
    # assert attributes.foo == "bar"
    assert attributes.product_id == product.id
