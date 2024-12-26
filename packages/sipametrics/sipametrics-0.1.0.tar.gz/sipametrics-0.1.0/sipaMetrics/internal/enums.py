from enum import Enum


class TiccsProfiles(Enum):
    INDUSTRIAL_SUPERCLASS = "industrialSuperclass"
    BUSINESS_MODEL = "businessModel"
    CORPORATE_STRUCTURE = "corporateStructure"
    COUNTRY = "countries"


class Product(Enum):
    SIPA_METRICS = "pe"
    INFRA_METRICS = "pi"


class AppName(Enum):
    INDICES = "indices"
    VALUATION = "valuation"
    CLIMATE = "climate"
