from typing import Dict, Optional, List
from datetime import date, timedelta
from sipaMetrics.internal.constants import COUNTRY_ISO_TO_ID_MAP, TIME_TO_MATURITY_BUCKETS, CURRENCY_MAP
from sipaMetrics.internal.enums import Product, AppName, TiccsProfiles
from sipaMetrics.endpoints import TAXONOMIES_URL


async def metrics_translation(entity_id: str, metric_id: str):
    params = {"metrics": [{"indexIds": [entity_id], "typeIds": [metric_id]}]}
    return params


async def infra_equity_comparable_translation(
    metric: str,
    currency: Optional[str] = None,
    age_in_months: Optional[int] = None,
    end_date: Optional[date] = None,
    window_in_years: Optional[int] = None,
    industrial_activities: Optional[List[str]] = None,
    business_risk: Optional[str] = None,
    corporate_structure: Optional[str] = None,
    countries: Optional[List[str]] = None,
    size: Optional[str] = None,
    leverage: Optional[str] = None,
    profitability: Optional[str] = None,
    investment: Optional[str] = None,
    time_to_maturity: Optional[str] = None,
    type: str = "mean",
):
    start_date_str = (
        (end_date - timedelta(days=window_in_years * 365)).strftime("%Y-%m-%d") if end_date and window_in_years else None
    )
    end_date_str = end_date.strftime("%Y-%m-%d") if end_date else None

    params = {
        "metric": metric,
        "startDate": start_date_str,
        "endDate": end_date_str,
        "age": age_in_months,
    }

    ticcs_profile_map = _create_ticcs_profile_map(
        industrial_activities=industrial_activities,
        business_risk=business_risk,
        corporate_structure=corporate_structure,
    )
    params["ticcsProfiles"] = ticcs_profile_map

    factors_profile_map = _create_infra_factors_profile_map(
        currency=currency,
        countries=countries,
        size=size,
        leverage=leverage,
        profitability=profitability,
        investment=investment,
        time_to_maturity=time_to_maturity,
        type=type,
    )
    params["factorsProfiles"] = factors_profile_map
    return params


async def infra_debt_comparable_translation(
    metric: str,
    currency: Optional[str] = None,
    age_in_months: Optional[int] = None,
    end_date: Optional[date] = None,
    window_in_years: Optional[int] = None,
    industrial_activities: Optional[List[str]] = None,
    business_risk: Optional[str] = None,
    corporate_structure: Optional[str] = None,
    countries: Optional[List[str]] = None,
    face_value: Optional[str] = None,
    debt_time_to_maturity: Optional[str] = None,
    type: str = "mean",
) -> Dict:
    start_date_str = (
        (end_date - timedelta(days=window_in_years * 365)).strftime("%Y-%m-%d") if end_date and window_in_years else None
    )
    end_date_str = end_date.strftime("%Y-%m-%d") if end_date else None

    ticcs_profiles = _create_ticcs_profile_map(
        industrial_activities=industrial_activities,
        business_risk=business_risk,
        corporate_structure=corporate_structure,
    )

    factors_profiles = _create_infra_factors_profile_map(
        countries=countries,
        face_value=face_value,
        debt_time_to_maturity=debt_time_to_maturity,
        type=type,
    )

    return {
        "metric": metric,
        "startDate": start_date_str,
        "endDate": end_date_str,
        "age": age_in_months,
        "ticcsProfiles": ticcs_profiles,
        "factorsProfiles": factors_profiles,
    }


async def term_structure_translation(country: str, date: str, maturity_date: str):
    params = {"countryName": country, "valueDate": date, "maturityDate": maturity_date}
    return params


async def private_equity_comparable_translation(
    metric: str,
    currency: Optional[str] = None,
    age_in_months: Optional[int] = None,
    end_date: Optional[date] = None,
    window_in_years: Optional[int] = None,
    industrial_activities: Optional[List[str]] = None,
    revenue_models: Optional[List[str]] = None,
    customer_models: Optional[List[str]] = None,
    lifecycle_phases: Optional[List[str]] = None,
    value_chain_types: Optional[List[str]] = None,
    countries: Optional[List[str]] = None,
    size: Optional[str] = None,
    growth: Optional[str] = None,
    leverage: Optional[str] = None,
    profits: Optional[str] = None,
    country_risk: Optional[List[str]] = None,
    universe: Optional[str] = None,
    factor_weight: Optional[str] = None,
    type: Optional[str] = "mean",
    intersect_peccs: Optional[bool] = None,
) -> Dict:
    start_date_str = (
        (end_date - timedelta(days=window_in_years * 365)).strftime("%Y-%m-%d") if end_date and window_in_years else None
    )
    end_date_str = end_date.strftime("%Y-%m-%d") if end_date else None

    peccs_country_profile = {
        "industrialActivities": industrial_activities,
        "revenueModel": revenue_models,
        "customerModel": customer_models,
        "lifecycleModel": lifecycle_phases,
        "valueChain": value_chain_types,
        "countries": countries,
    }
    peccs_country_profile = {key: value for key, value in peccs_country_profile.items() if value is not None}

    factors_profiles = _create_equity_factors_profile_map(
        size=size,
        growth=growth,
        leverage=leverage,
        profits=profits,
        country_risk=country_risk,
    )

    params = {
        "metric": metric,
        "currency": CURRENCY_MAP.get(currency or "USD", 840),
        "startDate": start_date_str,
        "endDate": end_date_str,
        "age": age_in_months,
        "peccsCountryProfile": peccs_country_profile,
        "factorsProfiles": factors_profiles,
        "universe": universe,
        "factorWeight": factor_weight,
        "operation": type,
        "intersectPeccs": intersect_peccs,
    }

    params = {key: value for key, value in params.items() if value is not None}
    return params


async def private_equity_comparable_boundaries_translation(
    metric: str,
    age_in_months: Optional[int] = None,
    end_date: Optional[date] = None,
    window_in_years: Optional[int] = None,
    industrial_activities: Optional[List[str]] = None,
    revenue_models: Optional[List[str]] = None,
    customer_models: Optional[List[str]] = None,
    lifecycle_phases: Optional[List[str]] = None,
    value_chain_types: Optional[List[str]] = None,
    countries: Optional[List[str]] = None,
    universe: Optional[str] = None,
    factor_weight: Optional[float] = None,
    factor_name: Optional[str] = None,
) -> Dict:

    start_date_str = (
        (end_date - timedelta(days=window_in_years * 365)).strftime("%Y-%m-%d") if end_date and window_in_years else None
    )
    end_date_str = end_date.strftime("%Y-%m-%d") if end_date else None

    peccs_country_profile = {
        "industrialActivities": industrial_activities,
        "revenueModel": revenue_models,
        "customerModel": customer_models,
        "lifecycleModel": lifecycle_phases,
        "valueChain": value_chain_types,
        "countries": countries,
    }
    peccs_country_profile = {key: value for key, value in peccs_country_profile.items() if value is not None}

    params = {
        "metric": metric,
        "ageInMonths": age_in_months,
        "startDate": start_date_str,
        "endDate": end_date_str,
        "universe": universe,
        "factorWeight": factor_weight,
        "factorName": factor_name,
        "peccsCountryProfile": peccs_country_profile,
    }
    params = {key: value for key, value in params.items() if value is not None}

    return params


async def taxonomies_translation(taxonomy: str, pillar: str):
    url = TAXONOMIES_URL.format(taxonomy=taxonomy)
    query_params = {"pillar": pillar}
    return url, query_params


async def indices_catalogue_translation(app, product):
    app_filter_map = {
        AppName.INDICES.value: {"marketIndices": 1} if product == Product.SIPA_METRICS.value else {"indexApp": 1},
        AppName.VALUATION.value: {"analytics": 1} if product == Product.SIPA_METRICS.value else {"assetValuation": 1},
        AppName.CLIMATE.value: {"indexApp": 1, "assetValuation": 1},
    }
    return app_filter_map.get(app, {})


def _create_ticcs_profile_map(
    industrial_activities: Optional[List[str]] = None,
    business_risk: Optional[str] = None,
    corporate_structure: Optional[str] = None,
) -> List:
    ticcs_profile_map = {}
    if industrial_activities:
        ticcs_profile_map[TiccsProfiles.INDUSTRIAL_SUPERCLASS.value] = industrial_activities
    if business_risk:
        ticcs_profile_map[TiccsProfiles.BUSINESS_MODEL.value] = business_risk
    if corporate_structure:
        ticcs_profile_map[TiccsProfiles.CORPORATE_STRUCTURE.value] = corporate_structure

    return [{"profile": {key: value}} for key, value in ticcs_profile_map.items()]


def _create_equity_factors_profile_map(
    size: Optional[str] = None,
    growth: Optional[str] = None,
    leverage: Optional[str] = None,
    profits: Optional[str] = None,
    country_risk: Optional[List[str]] = None,
) -> List:
    factors_profiles = []

    if size:
        if size[0] in ["Q", "T"]:
            factors_profiles.append(
                {
                    "factorName": "Size",
                    "quintile": convert_to_quintile_or_time_series(size),
                }
            )
        else:
            factors_profiles.append(
                {
                    "factorName": "Size",
                    "Size": size,
                }
            )
    if growth:
        if growth[0] in ["Q", "T"]:
            factors_profiles.append(
                {
                    "factorName": "Growth",
                    "quintile": convert_to_quintile_or_time_series(growth),
                }
            )
        else:
            factors_profiles.append(
                {
                    "factorName": "Growth",
                    "growth": growth,
                }
            )
    if leverage:
        if leverage[0] in ["Q", "T"]:
            factors_profiles.append(
                {
                    "factorName": "Leverage",
                    "quintile": convert_to_quintile_or_time_series(leverage),
                }
            )
        else:
            factors_profiles.append(
                {
                    "factorName": "Leverage",
                    "leverage": leverage,
                }
            )
    if profits:
        if profits[0] in ["Q", "T"]:
            factors_profiles.append(
                {
                    "factorName": "Profits",
                    "quintile": convert_to_quintile_or_time_series(profits),
                }
            )
        else:
            factors_profiles.append(
                {
                    "factorName": "Profits",
                    "profits": profits,
                }
            )
    if country_risk:
        factors_profiles.append(
            {
                "factorName": "TermSpread",
                "countries": country_risk,
            }
        )

    return factors_profiles


def _create_infra_factors_profile_map(
    currency: Optional[str] = None,
    countries: Optional[List[str]] = None,
    size: Optional[str] = None,
    leverage: Optional[str] = None,
    profitability: Optional[str] = None,
    investment: Optional[str] = None,
    time_to_maturity: Optional[str] = None,
    debt_time_to_maturity: Optional[str] = None,
    face_value: Optional[str] = None,
    type: Optional[str] = None,
) -> List:
    factors_profiles = []
    if countries:
        converted_countries = [COUNTRY_ISO_TO_ID_MAP.get(country, "Unknown") for country in countries]
        factors_profiles.append(
            {
                "profile": {
                    "factor": "countries",
                    "countries": converted_countries,
                }
            }
        )
    if size:
        if size[0] in ["Q", "T"]:
            factors_profiles.append(
                {
                    "profile": {
                        "factor": "size",
                        "quintile": convert_to_quintile_or_time_series(size),
                        "currency": CURRENCY_MAP.get(currency or "USD", 840),
                    }
                }
            )
        else:
            factors_profiles.append(
                {
                    "profile": {
                        "factor": "size",
                        "size": size,
                        "currency": CURRENCY_MAP.get(currency or "USD", 840),
                    }
                }
            )

    if leverage:
        if leverage[0] in ["Q", "T"]:
            factors_profiles.append(
                {
                    "profile": {
                        "factor": "leverage",
                        "quintile": convert_to_quintile_or_time_series(leverage),
                    }
                }
            )
        else:
            factors_profiles.append(
                {
                    "profile": {
                        "factor": "leverage",
                        "leverage": leverage,
                    }
                }
            )

    if profitability:
        if profitability[0] in ["Q", "T"]:
            factors_profiles.append(
                {
                    "profile": {
                        "factor": "profitability",
                        "quintile": convert_to_quintile_or_time_series(profitability),
                    }
                }
            )
        else:
            factors_profiles.append(
                {
                    "profile": {
                        "factor": "profitability",
                        "profitability": profitability,
                    }
                }
            )

    if investment:
        if investment[0] in ["Q", "T"]:
            factors_profiles.append(
                {
                    "profile": {
                        "factor": "investment",
                        "quintile": convert_to_quintile_or_time_series(investment),
                    }
                }
            )
        else:
            factors_profiles.append(
                {
                    "profile": {
                        "factor": "investment",
                        "investment": investment,
                    }
                }
            )

    if time_to_maturity:
        if time_to_maturity[0] in ["Q", "T"]:
            factors_profiles.append(
                {
                    "profile": {
                        "factor": "timeToMaturity",
                        "timeToMaturityBucket": convert_to_quintile_or_time_series(time_to_maturity),
                    }
                }
            )
        else:
            factors_profiles.append(
                {
                    "profile": {
                        "factor": "timeToMaturity",
                        "timeToMaturity": time_to_maturity,
                    }
                }
            )

    if debt_time_to_maturity:
        if debt_time_to_maturity[0] in ["Q", "T"]:
            factors_profiles.append(
                {
                    "profile": {
                        "factor": "debtTimeToMaturity",
                        "timeToMaturityBucket": convert_to_quintile_or_time_series(debt_time_to_maturity),
                    }
                }
            )
        else:
            factors_profiles.append(
                {
                    "profile": {
                        "factor": "debtTimeToMaturity",
                        "timeToMaturity": debt_time_to_maturity,
                    }
                }
            )

    if face_value:
        if face_value[0] in ["Q", "T"]:
            factors_profiles.append(
                {
                    "profile": {
                        "factor": "faceValue",
                        "quintile": convert_to_quintile_or_time_series(face_value),
                    }
                }
            )
        else:
            factors_profiles.append(
                {
                    "profile": {
                        "factor": "faceValue",
                        "faceValue": face_value,
                    }
                }
            )

    return factors_profiles


def convert_to_quintile_or_time_series(value: str):
    if value.upper().startswith("Q"):
        return int(value[1:])
    elif value.upper().startswith("T"):
        return TIME_TO_MATURITY_BUCKETS.get(value, value)
    else:
        return float(value) if value.isdigit() else value
