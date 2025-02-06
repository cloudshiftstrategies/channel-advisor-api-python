from functools import cached_property
import zipfile
from channel_advisor_api.utils.logger import get_logger
from pydantic import BaseModel, Field
from channel_advisor_api.models.channel_advisor_client import ChannelAdvisorClient
from typing import Optional
import requests
import pandas as pd
from io import BytesIO

logger = get_logger(__name__)


class ProductExportResponse(BaseModel):
    id: str = Field(alias="$id")
    token: str = Field(alias="Token")
    status: str = Field(alias="Status")
    started_on_utc: str = Field(alias="StartedOnUtc")
    response_file_url: Optional[str] = Field(None, alias="ResponseFileUrl")


class ProductExportS3Location(BaseModel):
    s3_bucket: str
    s3_key: str


class ChannelAdvisorExport(BaseModel):
    _base_uri = "ProductExport"
    _client: ChannelAdvisorClient

    def __init__(self, client: ChannelAdvisorClient = None):
        super().__init__()
        self._client = client or ChannelAdvisorClient()

    @cached_property
    def client(self) -> ChannelAdvisorClient:
        return self._client

    def request_export(self, filter: str = None) -> ProductExportResponse:
        params = {"filter": filter} if filter else {}
        response = self.client.request("POST", self._base_uri, params=params)
        logger.info(f"Export request response: {response.json()}")
        return ProductExportResponse(**response.json())

    def get_export_status(self, token: str) -> ProductExportResponse:
        params = {"token": token}
        response = self.client.request("GET", self._base_uri, params=params)
        logger.info(f"Export status response: {response.json()}")
        return ProductExportResponse(**response.json())

    def export_is_complete(self, token: str) -> bool:
        status = self.get_export_status(token).status
        for failure_status in ["Error", "Failed", "Aborted"]:
            if failure_status in status:
                raise ValueError(f"Export token {token} failed with status: {status}")
        logger.info(f"Export token {token} status is: {status}")
        return status == "Complete"

    def export_to_df(self, token: str) -> pd.DataFrame:
        url = self.get_export_status(token).response_file_url
        if not url:
            raise ValueError("Export file URL not available")

        # download export using requests with streaming enabled
        response = requests.get(url, stream=True)
        response.raise_for_status()

        # Try to read as zip file
        with zipfile.ZipFile(BytesIO(response.content), "r") as zip_ref:
            # Find the first .txt file in the zip
            txt_files = [f for f in zip_ref.namelist() if f.endswith(".txt")]
            if not txt_files:
                raise ValueError("No .txt file found in zip archive")

            with zip_ref.open(txt_files[0]) as file:
                return pd.read_csv(file, sep="\t")
