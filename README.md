# Channel Advisor API Python

A strongly typed Pydantic-based Python API client for Channel Advisor with built-in pagination, retries, and AI-enhanced product data improvement capabilities.

## Features

- **Strongly Typed**: Full Pydantic model support with comprehensive type hints
- **Robust Pagination**: Automatic handling of paginated API responses
- **Smart Retries**: Built-in retry logic for reliable API interactions
- **AI Enhancement**: AI-powered functions to improve and optimize product data
- **Easy Authentication**: Simple environment variable-based credential management

## Installation

```bash
# Using pip
pip install channel-advisor-api-python

# Using uv
uv add channel-advisor-api-python
```

## Quick Start

### 1. Set up your environment variables

Create a `.env` file or set the following environment variables:

```bash
CA_REFRESH_TOKEN=your_refresh_token_here
CA_APPLICATION_ID=your_application_id_here
CA_SHARED_SECRET=your_shared_secret_here
```

### 2. Basic Usage

```python
from channel_advisor_api.models.channel_advisor import BaseProduct
from channel_advisor_api.models.channel_advisor_client import ChannelAdvisorClient

# Initialize client
client = ChannelAdvisorClient()

# Get products with automatic pagination and typing
products = BaseProduct.get_client().get_products()

# Access strongly typed product data
for product in products:
    print(f"SKU: {product.sku}")
    print(f"Title: {product.title}")
    print(f"Price: {product.price}")
```

### 3. AI-Enhanced Product Data

```python
from channel_advisor_api.models.channel_advisor_llm import ProductOptimizer

# Use AI to improve product descriptions and titles
optimizer = ProductOptimizer()
improved_product = optimizer.enhance_product_data(product)
```

## API Credentials

To use this library, you need Channel Advisor API credentials:

1. **CA_REFRESH_TOKEN**: Your Channel Advisor refresh token
2. **CA_APPLICATION_ID**: Your application ID from Channel Advisor
3. **CA_SHARED_SECRET**: Your shared secret from Channel Advisor

You can obtain these from your Channel Advisor developer account.

## Development

See [CLAUDE.md](CLAUDE.md) for development setup and contribution guidelines.

## License

This project is licensed under the MIT License.

## Support

For issues and feature requests, please use the GitHub issue tracker.