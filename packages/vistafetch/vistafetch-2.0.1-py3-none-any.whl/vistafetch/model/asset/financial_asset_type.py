"""Models the supported types of financial assets."""

from enum import Enum


class FinancialAssetType(Enum):
    """Possible types of financial asset types.

    Attributes
    ----------
        BOND: A debt security that represents a loan made by
            an investor to a borrower.
        DERIVATIVE: A derivative  is a standardized financial contract that
            is listed and traded on a regulated exchange.
        FUND: An investment fund, e.g., mutual fund, ETF, etc.
        INDEX: A basket of securities representing a particular market or
            a segment of it.
        METAL: A precious metal traded via an exchange.
        STOCK: Share of a corporation or company.
        UNKNOWN: Unknown type of financial asset.
            Should only be used for abstract modeling.

    """

    BOND = "BOND"
    DERIVATIVE = "DERIVATIVE"
    FUND = "FUND"
    INDEX = "INDEX"
    METAL = "PRECIOUS_METAL"
    STOCK = "STOCK"
    UNKNOWN = None
