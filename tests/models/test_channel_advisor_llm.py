from unittest import mock
import pytest
from channel_advisor_api.models.channel_advisor import MinProduct
from channel_advisor_api.models.channel_advisor_attributes import ParentOptimizeAttributes
from channel_advisor_api.models.channel_advisor_llm import BaseProductWithAttributes, llm_product


@pytest.fixture
def aws_client():
    with mock.patch("channel_advisor_api.models.channel_advisor_llm.AwsClient") as mock_client:
        yield mock_client


@pytest.fixture
def min_product(mock_product_dict, mock_attributes_dump) -> MinProduct:
    attributes = ParentOptimizeAttributes(**mock_attributes_dump)
    return MinProduct(**mock_product_dict, attributes=attributes)


def test_llm_product(aws_client, min_product, mock_ca_client):
    response = BaseProductWithAttributes(product=min_product, attributes=min_product.attributes)
    aws_client().claude_client.completions.create_with_completion.return_value = (response, "bar")
    result = llm_product(min_product, False, None, 0.7)
    assert result == min_product


def test_llm_product_removes_restricted_words(aws_client, min_product, mock_ca_client):
    restricted_words = ["™", "©"]
    min_product.description = "description with ™ and ©"
    response = BaseProductWithAttributes(product=min_product, attributes=min_product.attributes)
    aws_client().claude_client.completions.create_with_completion.return_value = (response, "bar")
    result = llm_product(min_product, False, None, 0.7)
    for word in restricted_words:
        assert word not in result.description
