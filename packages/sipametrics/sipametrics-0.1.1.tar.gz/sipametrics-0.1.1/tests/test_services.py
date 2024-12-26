import pytest
from sipaMetrics.services import sipaMetricsService
from sipaMetrics.endpoints import *
import statics_test as st
import logging
from datetime import date


@pytest.mark.asyncio
async def test_private_equity_comparable_boundaries():
    service = sipaMetricsService(api_key=st.USER_API_KEY, api_secret=st.USER_API_SECRET)
    try:
        response = await service.private_equity_comparable_boundaries(
            metric="PriceToSales",
            age_in_months=None,
            end_date=date(2023, 11, 30),
            window_in_years=2,
            # industrial_activities=["01"],
            # revenue_models=["02"],
            # customer_models=["01"],
            # lifecycle_phases=["02"],
            # value_chain_types=["03"],
            industrial_activities=["AC01"],
            revenue_models=["RM02"],
            customer_models=["CM01"],
            lifecycle_phases=["LP02"],
            value_chain_types=["VC03"],
            countries=["USA"],
            universe="PEU",
            # factor_weight=0.5,
            factor_name="Size",
        )
        logging.info(f"Response: {response}")
        assert response["data"] == {
            "results": {
                "1": {"minimum": 1.03, "maximum": 9.54},
                "2": {"minimum": 9.54, "maximum": 20.6},
                "3": {"minimum": 20.6, "maximum": 35.5},
                "4": {"minimum": 35.5, "maximum": 59.9},
                "5": {"minimum": 59.9, "maximum": 1503.0},
            }
        }
    except Exception as e:
        logging.error(f"Test failed: {e}")
        raise


@pytest.mark.asyncio
async def test_private_equity_comparable():
    service = sipaMetricsService(api_key=st.USER_API_KEY, api_secret=st.USER_API_SECRET)
    try:
        response = await service.private_equity_comparable(
            metric="PriceToSales",
            currency="USD",
            age_in_months=None,
            end_date=date(2023, 12, 31),
            window_in_years=2,
            industrial_activities=None,
            revenue_models=None,
            customer_models=None,
            lifecycle_phases=None,
            value_chain_types=None,
            countries=None,
            size=None,
            growth=None,
            leverage="Q1",
            profits=None,
            country_risk=None,
            universe="MIU",
            factor_weight="1",
            type="mean",
            intersect_peccs=True,
        )
        logging.info(f"Response: {response}")
        assert response["data"] != []

        # Example 2 - raw values
        # =PRIVATEMETRICS.PRIVATE_EQUITY_COMPARABLE("dividendOverRevenue", "USD", , DATE(2022,11,30), "2", , , , , , , \
        # "25", "10", "15", "20",
        # "NGA, EGY, ZAF, BRA, ARG, CHL, COL, MEX, CAN, USA",
        # "MIU", "1", "mean", TRUE)
        response = await service.private_equity_comparable(
            metric="dividendOverRevenue",
            currency="USD",
            age_in_months=None,
            end_date=date(2022, 11, 30),
            window_in_years=2,
            # industrial_activities=["AC01"],
            # revenue_models=["RM02"],
            # customer_models=["CM01"],
            # lifecycle_phases=["LP02"],
            # value_chain_types=["VC03"],
            countries=["NGA", "EGY", "ZAF", "BRA", "ARG", "CHL", "COL", "MEX", "CAN", "USA"],
            size="25",
            growth="10",
            # leverage="Q1",
            profits="15",
            country_risk=[""],
            universe="MIU",
            factor_weight="1",
            type="mean",
            intersect_peccs=True,
        )
        logging.info(f"Response: {response}")
        assert response["data"] != []

    except Exception as e:
        logging.error(f"Test failed: {e}")
        raise


@pytest.mark.asyncio
async def test_infra_debt_comparable():
    service = sipaMetricsService(api_key=st.USER_API_KEY, api_secret=st.USER_API_SECRET)
    try:
        response = await service.infra_debt_comparable(
            metric="credit_spread",
            age_in_months=None,
            end_date=date(2024, 7, 31),
            window_in_years=2,
            industrial_activities=["IC10"],
            business_risk="BR1",
            corporate_structure="CS1",
            countries=["AUS", "NZL"],
            face_value="Q1",
            time_to_maturity="T2",
            type="median",
        )
        logging.info(f"Response: {response}")
        assert response["data"] != []

        # Example 2 - raw values
        # =PRIVATEMETRICS.INFRA_DEBT_COMPARABLE("credit_spread", "USD", , DATE(2024,11,30), "2", , "", "", , "20", "7", "mean")
        response = await service.infra_debt_comparable(
            metric="credit_spread",
            age_in_months=None,
            end_date=date(2024, 7, 31),
            window_in_years=2,
            #    industrial_activities=["IC10"],
            #    business_risk="BR1",
            #    corporate_structure="CS1",
            #    countries=["AUS","NZL"],
            face_value="20",
            time_to_maturity="7",
            type="median",
        )
        logging.info(f"Response: {response}")
        assert response["data"] != []
    except Exception as e:
        logging.error(f"Test failed: {e}")
        raise


@pytest.mark.asyncio
async def test_infra_equity_comparable():
    service = sipaMetricsService(api_key=st.USER_API_KEY, api_secret=st.USER_API_SECRET)
    try:
        # Example 1 - Quintile
        response = await service.infra_equity_comparable(
            metric="ev2ebitda",
            currency="",
            age_in_months=None,
            end_date=date(2024, 7, 31),
            window_in_years=2,
            industrial_activities=["IC10"],
            business_risk="BR1",
            corporate_structure="CS1",
            countries=["AUS", "NZL"],
            size="Q1",
            leverage="Q1",
            profitability="Q1",
            investment="Q1",
            time_to_maturity="T2",
            #  type= "mean"
        )

        logging.info(f"Response: {response}")
        assert response["data"] != []

        # Example 2 - Raw values
        # =PRIVATEMETRICS.INFRA_EQUITY_COMPARABLE("ev2ebitda", "USD", , DATE(2024,11,30), "2", , "", "", , "50", "54", "10", "23", "7", "mean")
        response = await service.infra_equity_comparable(
            metric="ev2ebitda",
            currency="",
            age_in_months=None,
            end_date=date(2024, 7, 31),
            window_in_years=2,
            #  industrial_activities=[""],
            #  business_risk="",
            #  corporate_structure="",
            #  countries=["AUS","NZL"],
            size="50",
            leverage="54",
            profitability="10",
            investment="23",
            time_to_maturity="7",
            type="mean",
        )

        logging.info(f"Response: {response}")
        assert response["data"] != []

    except Exception as e:
        logging.error(f"Test failed: {e}")
        raise


# ======= OK =======
@pytest.mark.asyncio
async def test_metrics():
    service = sipaMetricsService(api_key=st.USER_API_KEY, api_secret=st.USER_API_SECRET)
    try:
        response = await service.metrics(entity_id="INFRBGWX", metric_id="T01414")
        logging.info(f"Response: {response}")
        assert response["data"] != []
    except Exception as e:
        logging.error(f"Test failed: {e}")
        raise


@pytest.mark.asyncio
async def test_countries():
    service = sipaMetricsService(api_key=st.USER_API_KEY, api_secret=st.USER_API_SECRET)
    try:
        response = await service.countries()
        logging.info(f"Response: {response}")
        assert response["data"] != []
    except Exception as e:
        logging.error(f"Test failed: {e}")
        raise


@pytest.mark.asyncio
async def test_taxonomies():
    service = sipaMetricsService(api_key=st.USER_API_KEY, api_secret=st.USER_API_SECRET)
    try:
        response = await service.taxonomies(taxonomy="ticcs", pillar="businessRisk")
        logging.info(f"Response: {response}")
        assert response["data"] != []

        response = await service.taxonomies(taxonomy="peccs", pillar="revenueModel")
        logging.info(f"Response for product 'pe': {response}")
        assert response["data"] != []

    except Exception as e:
        logging.error(f"Test failed: {e}")
        raise


@pytest.mark.asyncio
async def test_indices_catalogue():
    service = sipaMetricsService(api_key=st.USER_API_KEY, api_secret=st.USER_API_SECRET)
    try:
        response_pi = await service.indices_catalogue(product="pi", app="indices")
        logging.info(f"Response: {response_pi}")
        assert response_pi["data"] != []

        response_pe = await service.indices_catalogue(product="pe", app="indices")
        logging.info(f"Response for product 'pe': {response_pe}")
        assert response_pe["data"] != []

    except Exception as e:
        logging.error(f"Test failed: {e}")
        raise


@pytest.mark.asyncio
async def test_private_equity_region_tree():
    service = sipaMetricsService(api_key=st.USER_API_KEY, api_secret=st.USER_API_SECRET)
    try:
        response = await service.private_equity_region_tree()
        logging.info(f"Response: {response}")
        assert response["data"] != []
    except Exception as e:
        logging.error(f"Test failed: {e}")
        raise


@pytest.mark.asyncio
async def test_term_structure():
    service = sipaMetricsService(api_key=st.USER_API_KEY, api_secret=st.USER_API_SECRET)
    try:
        response = await service.term_structure(country="GBR", date="2022-12-31", maturity_date="2023-12-31")
        logging.info(f"Response: {response}")
        assert response["data"] != []
    except Exception as e:
        logging.error(f"Test failed: {e}")
        raise
