from enum import StrEnum
import pytest
from channel_advisor_api.models.channel_advisor import MinProduct
from channel_advisor_api.models.channel_advisor_attributes import AllAttributes, BaseAttr, BaseOptimizeAttributes
from unittest.mock import call


def test_base_attr_description():
    class TestBase1(BaseAttr):
        DESCR = ("NAVY", "Full Description")
        NO_DESCR = "value only"

    assert TestBase1.DESCR == "NAVY"
    assert TestBase1.DESCR.value == "NAVY"
    assert TestBase1.DESCR.description == "Full Description"
    assert TestBase1.NO_DESCR == "value only"
    assert TestBase1.NO_DESCR.value == "value only"
    assert TestBase1.NO_DESCR.description == "value only"


def test_base_attribute_save(mock_ca_client, mock_product_attributes, mock_product_dict):
    product = MinProduct.model_validate(mock_product_dict)
    mock_ca_client().get_all_pages.return_value = mock_product_attributes

    # make sure our mock data hasnt changed
    assert product.attributes.Bullet_01 == "My Test"  # from the mock data
    assert product.attributes.Search_3 == "FXR snowmobile jackets"

    # override some values
    product.attributes.Bullet_01 = None  # Delete this
    product.attributes.Search_3 = "New Value 3"  # Change this

    # make sure the values are what we expect
    assert product.attributes.Bullet_01 is None
    assert product.attributes.Search_3 == "New Value 3"

    expected_calls = []
    expected_post_data = {"Value": {"Attributes": []}}
    update_items = {}
    for k, v in product.attributes.model_dump(exclude="product_id", by_alias=True).items():
        if v is None:
            # Any None values get deleted
            expected_calls.append(call("DELETE", f"Products({product.id})/Attributes('{k}')"))
        else:
            # Any other values get updated
            expected_post_data["Value"]["Attributes"].append({"Name": k, "Value": v})
            update_items[k] = v
    expected_calls.append(call("POST", f"Products({product.id})/UpdateAttributes", data=expected_post_data))
    product.attributes.save()
    mock_ca_client().request.assert_has_calls(expected_calls)
    assert mock_ca_client().request.call_count == len(expected_calls)


@pytest.mark.parametrize("bullet_02_value", [None, ""])
def test_base_attribute_save_to_chidlren(mock_ca_client, mock_product_dict, bullet_02_value):
    class FakeStrEnum(StrEnum):
        Value_1 = "Value 1"
        Value_2 = "Value 2"

    def mock_get_all_pages(*args, **kwargs):
        if "/Children" in args[0]:
            return [
                {"ParentProductID": mock_product_dict["ID"], "ChildProductID": 123},
                {"ParentProductID": mock_product_dict["ID"], "ChildProductID": 456},
            ]
        elif "/Attributes" in args[0]:
            return [
                {"Name": "Bullet_01", "Value": FakeStrEnum.Value_1},
                {"Name": "Bullet_02", "Value": bullet_02_value},
                {"Name": "Bullet_03", "Value": "Something else"},
            ]

    mock_ca_client().get_all_pages.side_effect = mock_get_all_pages
    product = MinProduct.model_validate(mock_product_dict)
    product.attributes.save_to_children(include_fields=["Bullet_01", "Bullet_02"])
    expected_post_data = {"Value": {"Attributes": [{"Name": "Bullet_01", "Value": "Value 1"}]}}
    mock_ca_client().get_all_pages.assert_called_with("Products(12345)/Children")
    mock_ca_client().request.assert_has_calls(
        [
            call("DELETE", "Products(123)/Attributes('Bullet_02')"),
            call("POST", "Products(123)/UpdateAttributes", data=expected_post_data),
            call("DELETE", "Products(456)/Attributes('Bullet_02')"),
            call("POST", "Products(456)/UpdateAttributes", data=expected_post_data),
        ]
    )
    assert mock_ca_client().request.call_count == 4


def test_base_attribute_client(mock_ca_client, mock_product_dict):
    product = MinProduct.model_validate(mock_product_dict)
    assert product.attributes.client == mock_ca_client()


def test_all_attributes(mock_ca_client):
    """Test that we can handle any Attribute type without error"""
    mock_get_all_pages = [
        {"ProductID": 123, "ProfileID": 456, "Name": "Hibity", "Value": "rando 1"},
        {"ProductID": 123, "ProfileID": 455, "Name": "Jibity", "Value": "rando 2"},
    ]
    mock_ca_client().get_all_pages.return_value = mock_get_all_pages
    attributes = AllAttributes.get_attributes_by_id(123)
    assert attributes.product_id == 123
    assert attributes.Hibity == "rando 1"
    assert attributes.Jibity == "rando 2"


def test_optimize_attributes(mock_ca_client):
    """Test that we can handle any Attribute type without error"""
    mock_get_all_pages = [
        {"ProductID": 123, "ProfileID": 456, "Name": "AMZ_Category", "Value": "rando 1"},
    ]
    mock_ca_client().get_all_pages.return_value = mock_get_all_pages
    attributes = BaseOptimizeAttributes.get_attributes_by_id(123)
    assert attributes.product_id == 123
    assert attributes.AMZ_Category == "rando 1"
