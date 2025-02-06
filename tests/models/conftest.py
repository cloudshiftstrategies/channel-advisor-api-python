import pytest
from unittest.mock import patch


@pytest.fixture
def mock_ca_client():
    with patch("channel_advisor_api.models.channel_advisor.ChannelAdvisorClient") as client, patch(
        "channel_advisor_api.models.channel_advisor_attributes.ChannelAdvisorClient", new=client
    ):
        yield client


@pytest.fixture
def mock_environ():
    with patch.dict(
        "os.environ",
        {
            "CA_APPLICATION_ID": "test_client_id",
            "CA_SHARED_SECRET": "test_client_secret",
            "CA_REFRESH_TOKEN": "test_refresh_token",
        },
        clear=True,
    ):
        yield


@pytest.fixture
def mock_product_dict():
    return {
        "ID": 12345,
        "ProfileID": 67890,
        "CreateDateUtc": "2024-01-01T00:00:00Z",
        "UpdateDateUtc": "2024-01-02T00:00:00Z",
        "QuantityUpdateDateUtc": "2024-01-02T00:00:00Z",
        "IsAvailableInStore": True,
        "IsBlocked": False,
        "IsBlockedFromAdvertising": False,
        "IsExternalQuantityBlocked": False,
        "InfiniteQuantity": False,
        "BlockComment": None,
        "BlockedDateUtc": None,
        "BlockedFromAdvertisingDateUtc": None,
        "ReceivedDateUtc": None,
        "LastSaleDateUtc": None,
        "ASIN": "B00EXAMPLE",
        "Brand": "Test Brand",
        "Condition": "New",
        "Description": "Test product description",
        "EAN": "1234567890123",
        "FlagDescription": None,
        "Flag": "None",
        "HarmonizedCode": "1234.56.78",
        "ISBN": None,
        "Manufacturer": "Test Manufacturer",
        "MPN": "TEST-123",
        "ShortDescription": "Short desc",
        "Sku": "TEST-SKU-123",
        "Subtitle": "Test Subtitle",
        "Title": "Test Product Title",
        "UPC": "012345678901",
        "WarehouseLocation": "A1-B2-C3",
        "TotalAvailableQuantity": 100,
        "OpenAllocatedQuantity": 0,
        "OpenAllocatedQuantityPooled": 0,
        "PendingCheckoutQuantity": 0,
        "PendingCheckoutQuantityPooled": 0,
        "PendingPaymentQuantity": 0,
        "PendingPaymentQuantityPooled": 0,
        "PendingShipmentQuantity": 0,
        "PendingShipmentQuantityPooled": 0,
        "TotalQuantity": 100,
        "TotalQuantityPooled": 100,
        "IsParent": False,
        "IsInRelationship": False,
        "IsDisplayInStore": True,
        "BundleType": "None",
        "ProductType": "Standard",
        "AliasType": "None",
    }


@pytest.fixture
def mock_attributes_dump():
    return {
        "product_id": 12345,
        "AMZ_Category": "Automotive",
        "AmzProductType": "ProtectiveGear",
        "Bullet_01": (
            "WEATHER PROTECTION: HydrX Pro technology with 10,000mm waterproofing and 8,000g/m² breathability, "
            "plus durable 450D polyester shell construction"
        ),
        "Bullet_02": (
            "INSULATION SYSTEM: F.A.S.T. 3.0 technology with 220g combined insulation and FXR Thermal Flex "
            "provides reliable warmth"
        ),
        "Bullet_03": (
            "VENTILATION DESIGN: FXR Dry Vent system with perforated F.A.S.T. insulation at vents for "
            "effective temperature regulation"
        ),
        "Bullet_04": (
            "PRACTICAL FEATURES: Heavy-duty 2-way front zipper, adjustable hood, multiple storage pockets, "
            "and water-resistant cuff system"
        ),
        "Bullet_05": (
            "RIDER SAFETY: Equipped with tether retention D-ring, line-cutter, and 360° reflective inserts "
            "for visibility"
        ),
        "Department": "mens",
        "ItemType": "powersports-protective-jackets",
        "Model": "Men's Excursion Jacket 2025",
        "Search_1": "FXR Excursion Jacket",
        "Search_2": "winter powersports jacket",
        "Search_3": "mens winter riding jacket",
        "Search_4": "insulated snowmobile gear",
        "Search_5": "250030",
        "Inner_Material_Type": "Fleece",
        "Material_Composition": "Polyester",
        "Outer_Material_Type": "Polyester",
        "eBay_Condition": "New",
        "shopify_category": "Riding Gear",
        "shopify_tag": "Winter Jackets",
        "Optimized_Process": "3 - checking",
        "Optimized_Pictures": "Yes",
        "Optimized_Attributes": "Yes",
        "Status": "CR",
    }


@pytest.fixture
def mock_product_attributes():
    product_id = 12792106
    profile_id = 12003791
    return [
        {"ProductID": product_id, "ProfileID": profile_id, "Name": "AMZ_Category", "Value": "Automotive"},
        {"ProductID": product_id, "ProfileID": profile_id, "Name": "AMZ_Notes", "Value": "PRO FISH,SNOW"},
        {
            "ProductID": product_id,
            "ProfileID": profile_id,
            "Name": "AMZ_Notes_Alex",
            "Value": "PRO FISH,SNOW-MENS-JACKETS-INSULATED,UNINSULATED",
        },
        {"ProductID": product_id, "ProfileID": profile_id, "Name": "AmzProductType", "Value": "ProtectiveGear"},
        {"ProductID": product_id, "ProfileID": profile_id, "Name": "Bullet_01", "Value": "My Test"},
        {"ProductID": product_id, "ProfileID": profile_id, "Name": "Catalog", "Value": "Winter '25"},
        {"ProductID": product_id, "ProfileID": profile_id, "Name": "Department", "Value": "mens"},
        {"ProductID": product_id, "ProfileID": profile_id, "Name": "eBay Condition", "Value": "New"},
        {"ProductID": product_id, "ProfileID": profile_id, "Name": "Inner_Material_Type", "Value": "Fleece"},
        {"ProductID": product_id, "ProfileID": profile_id, "Name": "inventory_status", "Value": "False"},
        {
            "ProductID": product_id,
            "ProfileID": profile_id,
            "Name": "ItemType",
            "Value": "powersports-protective-jackets",
        },
        {"ProductID": product_id, "ProfileID": profile_id, "Name": "Material_Composition", "Value": "Polyester"},
        {"ProductID": product_id, "ProfileID": profile_id, "Name": "Model", "Value": "Men's Excursion Jacket 2025"},
        {"ProductID": product_id, "ProfileID": profile_id, "Name": "Model-Color", "Value": "250030"},
        {"ProductID": product_id, "ProfileID": profile_id, "Name": "Monitor", "Value": "Active"},
        {"ProductID": product_id, "ProfileID": profile_id, "Name": "Optimized Attributes", "Value": "Yes"},
        {"ProductID": product_id, "ProfileID": profile_id, "Name": "Optimized Description Ready", "Value": "Yes"},
        {"ProductID": product_id, "ProfileID": profile_id, "Name": "Optimized Pictures", "Value": "Yes"},
        {"ProductID": product_id, "ProfileID": profile_id, "Name": "Optimized Process", "Value": "3 - Basics check"},
        {"ProductID": product_id, "ProfileID": profile_id, "Name": "Outer_Material_Type", "Value": "Polyester"},
        {"ProductID": product_id, "ProfileID": profile_id, "Name": "PartNumberPBI", "Value": "250030"},
        {
            "ProductID": product_id,
            "ProfileID": profile_id,
            "Name": "Search_1",
            "Value": "FXR Men's Excursion Jacket 2025",
        },
        {
            "ProductID": product_id,
            "ProfileID": profile_id,
            "Name": "Search_2",
            "Value": "protective snowmobile jackets",
        },
        {"ProductID": product_id, "ProfileID": profile_id, "Name": "Search_3", "Value": "FXR snowmobile jackets"},
        {"ProductID": product_id, "ProfileID": profile_id, "Name": "Search_4", "Value": "men's winter jackets"},
        {"ProductID": product_id, "ProfileID": profile_id, "Name": "Search_5", "Value": "250030"},
        {"ProductID": product_id, "ProfileID": profile_id, "Name": "shopify_category", "Value": "Riding Gear"},
        {"ProductID": product_id, "ProfileID": profile_id, "Name": "shopify_tag", "Value": "Winter Jackets"},
        {"ProductID": product_id, "ProfileID": profile_id, "Name": "Status", "Value": "CR W25 New"},
        {"ProductID": product_id, "ProfileID": profile_id, "Name": "Style Keywords", "Value": "all-weather"},
    ]
