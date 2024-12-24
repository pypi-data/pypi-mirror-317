from decimal import Decimal
from typing import Optional

from pydantic import BaseModel

from ..types import MachChain


class AssetInfo(BaseModel):
    id: str
    symbol: str
    name: str
    image: str
    current_price: Decimal
    market_cap: int
    market_cap_rank: int
    fully_diluted_valuation: int
    total_volume: int
    high_24h: Decimal
    low_24h: Decimal
    price_change_24h: Decimal
    price_change_percentage_24h: Decimal
    market_cap_change_24h: Decimal
    market_cap_change_percentage_24h: Decimal
    circulating_supply: Decimal
    total_supply: Decimal
    max_supply: Optional[Decimal]
    ath: Decimal
    ath_change_percentage: Decimal
    ath_date: str
    atl: Decimal
    atl_change_percentage: Decimal
    atl_date: str
    roi: Optional[Decimal]
    last_updated: str
    decimals: int


class AssetPricingData(BaseModel):
    chain: MachChain
    address: str
    symbol: str
    decimals: int
    price: float
    daily_percent_change: float


class UserAssetData(BaseModel):
    chain: MachChain
    address: str
    balance: int
    symbol: Optional[str] = None
    price: Optional[Decimal]
    daily_percent_change: Optional[Decimal]
