from enum import Enum


class SupplierType(str, Enum):
    MANUFACTURER = "MANUFACTURER"
    DISTRIBUTOR = "DISTRIBUTOR"
    WHOLESALER = "WHOLESALER"
    IMPORTER = "IMPORTER"
