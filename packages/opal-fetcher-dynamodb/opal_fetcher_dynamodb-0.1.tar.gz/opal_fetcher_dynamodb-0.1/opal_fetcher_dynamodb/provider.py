import boto3
from typing import List, Optional
from decimal import Decimal
from pydantic import Field
from boto3.dynamodb.types import TypeDeserializer
from botocore.exceptions import ClientError
from tenacity import wait, stop, retry_unless_exception_type

from opal_common.fetcher.fetch_provider import BaseFetchProvider
from opal_common.fetcher.events import FetcherConfig, FetchEvent
from opal_common.logger import logger


class DynamoDBFetcherConfig(FetcherConfig):
    fetcher: str = "DynamoDBFetchProvider"
    region: str = Field(..., description="AWS region name")
    endpoint_url: str = Field(..., description="DynamoDB endpoint URL")
    tableName: str = Field(..., description="DynamoDB table name")
    client: Optional[str] = Field(..., description="OPAL client identifier")


class DynamoDBFetchEvent(FetchEvent):
    fetcher: str = "DynamoDBFetchProvider"
    config: DynamoDBFetcherConfig = None


class DynamoDBFetchProvider(BaseFetchProvider):

    RETRY_CONFIG = {
        "wait": wait.wait_fixed(1200),
        "stop": stop.stop_after_attempt(5),
        "retry": retry_unless_exception_type(ClientError),
        "reraise": True,
    }

    def __init__(self, event: DynamoDBFetchEvent):
        if event.config is None:
            event.config = DynamoDBFetcherConfig()
        super().__init__(event)

    def parse_event(self, event: FetchEvent) -> DynamoDBFetchEvent:
        config_data = event.config
        config_instance = DynamoDBFetcherConfig(**config_data)
        return DynamoDBFetchEvent(**event.dict(exclude={"config"}), config=config_instance)

    async def _fetch_(self) -> List[dict]:
        logger.info(f"Fetching data for client: {self._event.config.client}")

        scan_kwargs = {"TableName": self._event.config.tableName}
        if self._event.config.tableName == "Entitlements" and self._event.config.client:
            scan_kwargs.update(
                {
                    "FilterExpression": "contains(clientTags, :tagValue)",
                    "ExpressionAttributeValues": {":tagValue": {"S": self._event.config.client}},
                }
            )

        try:
            response = self.client.scan(**scan_kwargs)
            items = response.get("Items", [])
            logger.info(f"Fetched {len(items)} items from table {self._event.config.tableName}")
            return items
        except Exception as e:
            logger.error(f"Error fetching data: {e}")
            raise

    async def __aenter__(self) -> "DynamoDBFetchProvider":
        logger.info(f"Entering DynamoDB Fetch Provider context with config: {self._event.config}")
        self.client = boto3.client(
            "dynamodb",
            region_name=self._event.config.region,
            endpoint_url=self._event.config.endpoint_url,
        )
        self.serializer = TypeDeserializer()
        return self

    async def __aexit__(self, exc_type=None, exc_val=None, tb=None):
        logger.info("Exiting DynamoDB Fetch Provider context...")

    async def _process_(self, records: List[dict]) -> dict:
        deserialized_data = self.deserialize(records)
        return self.transform_response(deserialized_data)

    def convert_decimal(self, obj: Decimal) -> float:
        if isinstance(obj, Decimal):
            return float(obj)
        raise TypeError("Unexpected type for decimal conversion")

    def deserialize(self, data: dict | list | str) -> dict | list | str:
        if isinstance(data, list):
            return [self.deserialize(v) for v in data]
        if isinstance(data, dict):
            try:
                return self.serializer.deserialize(data)
            except TypeError:
                return {k: self.deserialize(v) for k, v in data.items()}
        return data

    def transform_response(self, data: List[dict]) -> dict:
        if self._event.config.tableName == "Entitlements":
            return self._transform_entitlements(data)
        return self._transform_assignments(data)

    def _transform_entitlements(self, data: List[dict]) -> dict:
        transformed = {}
        for item in data:
            entitlement_id = item.pop("entitlementId", None)
            if entitlement_id:
                transformed[entitlement_id] = item
        return transformed

    def _transform_assignments(self, data: List[dict]) -> dict:
        transformed = {}
        for item in data:
            user_id = item.get("userId")
            if not user_id:
                continue

            assignment = {
                "createdAt": item.get("createdAt"),
                "entitlementId": item.get("entitlementId"),
                "expiryDate": item.get("expiryDate"),
                "credits": item.get("credits"),
            }

            if user_id not in transformed:
                transformed[user_id] = {"assignments": []}

            transformed[user_id]["assignments"].append(assignment)
        return transformed
