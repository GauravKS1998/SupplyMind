from enum import Enum


class WarehouseType(str, Enum):
    CENTRAL = "CENTRAL"
    REGIONAL = "REGIONAL"
    DISTRIBUTION = "DISTRIBUTION"
    RETAIL = "RETAIL"
