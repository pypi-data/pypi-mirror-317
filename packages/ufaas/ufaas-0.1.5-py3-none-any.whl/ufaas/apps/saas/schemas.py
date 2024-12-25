import uuid
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Literal

from fastapi_mongo_base.schemas import BusinessOwnedEntitySchema
from pydantic import BaseModel, ConfigDict, Field


class Bundle(BaseModel):
    asset: str
    quota: Decimal
    unit: str | None = None

    model_config = ConfigDict(allow_inf_nan=True)


class AcquisitionType(str, Enum):
    trial = "trial"
    # credit = "credit"
    purchased = "purchased"
    gifted = "gifted"
    # deferred = "deferred"
    promotion = "promotion"
    # subscription = "subscription"
    # on_demand = "on_demand"
    borrowed = "borrowed"
    # freemium = "freemium"
    postpaid = "postpaid"


class EnrollmentCreateSchema(BaseModel):
    user_id: uuid.UUID
    bundles: list[Bundle]

    price: Decimal = Decimal(0)
    invoice_id: str | None = None
    start_at: datetime = Field(default_factory=datetime.now)
    expire_at: datetime | None = None
    duration: int | None = Field(None, description="Duration in days")
    status: Literal["active", "inactive"] = "active"
    acquisition_type: AcquisitionType = AcquisitionType.purchased

    variant: str | None = None
    meta_data: dict | None = None

    due_date: datetime | None = None


class EnrollmentSchema(EnrollmentCreateSchema, BusinessOwnedEntitySchema):
    user_id: uuid.UUID
    bundles: list[Bundle]

    price: Decimal = Decimal(0)
    invoice_id: str | None = None
    start_at: datetime = Field(default_factory=datetime.now)
    expire_at: datetime | None = None
    duration: int | None = Field(None, description="Duration in days")
    status: Literal["active", "inactive"] = "active"
    acquisition_type: AcquisitionType = AcquisitionType.purchased

    variant: str | None = None
    meta_data: dict | None = None

    due_date: datetime | None = None

    paid_at: datetime | None = None


class UsageCreateSchema(BaseModel):
    user_id: uuid.UUID
    enrollment_id: uuid.UUID | None = None
    asset: str
    amount: Decimal = Decimal(1)
    variant: str | None = None
    meta_data: dict | None = None


class UsageConsumption(BaseModel):
    enrollment_id: uuid.UUID
    amount: Decimal
    leftover_bundles: list[Bundle] = []


class UsageSchema(BusinessOwnedEntitySchema):
    # enrollment_id: uuid.UUID
    # asset: str
    # amount: Decimal

    consumptions: list[UsageConsumption]
    asset: str
    amount: Decimal
    variant: str | None = None
