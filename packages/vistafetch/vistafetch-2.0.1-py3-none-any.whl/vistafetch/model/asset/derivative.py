"""Model a derivative."""
import logging
from typing import Literal

from vistafetch.model.asset.financial_asset import FinancialAsset
from vistafetch.model.asset.financial_asset_type import FinancialAssetType

__all__ = [
    "Derivative",
]

logger = logging.getLogger(__name__)


class Derivative(FinancialAsset):
    """Models a derivative within the scope of this library.

    An exchange-traded derivative is a standardized
    financial contract that is listed and traded on a regulated exchange.

    """

    _type = FinancialAssetType.DERIVATIVE

    entity_type: Literal[_type.value]  # type: ignore
