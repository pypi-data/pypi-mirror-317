import pytest
from unittest.mock import MagicMock, patch
from at_common_functions.stock import (
    stock_get_overview,
    stock_get_quotation,
    stock_get_candlesticks,
    stock_get_indicators,
    stock_get_financials
)
from at_common_models.stock.quotation import QuotationModel
from at_common_models.stock.overview import OverviewModel
from at_common_models.stock.daily_candlestick import DailyCandlestickModel
from at_common_models.stock.daily_indicator import DailyIndicatorModel
from at_common_models.stock.financials.annual_balance_sheet_statement import AnnualBalanceSheetStatementModel
from at_common_models.stock.financials.annual_income_statement import AnnualIncomeStatementModel
from at_common_models.stock.financials.annual_cashflow_statement import AnnualCashFlowStatementModel
from at_common_models.stock.financials.quarter_balance_sheet_statement import QuarterBalanceSheetStatementModel
from at_common_models.stock.financials.quarter_income_statement import QuarterlyIncomeStatementModel
from at_common_models.stock.financials.quarter_cashflow_statement import QuarterCashflowStatementModel
from datetime import datetime

TEST_SYMBOL = "AAPL"

@pytest.fixture
def mock_storage():
    storage = MagicMock()
    
    # Sample test data
    overview = OverviewModel(
        symbol=TEST_SYMBOL,
        name="Apple Inc.",
        sector="Technology",
        industry="Consumer Electronics"
    )
    
    quotation = QuotationModel(
        symbol=TEST_SYMBOL,
        price=150.0,
        volume=1000000,
        timestamp=datetime.now()
    )
    
    candlesticks = [
        DailyCandlestickModel(
            symbol=TEST_SYMBOL,
            time=datetime.now(),
            open=150.0,
            high=155.0,
            low=149.0,
            close=152.0,
            volume=1000000
        )
        for _ in range(5)
    ]
    
    indicators = [
        DailyIndicatorModel(
            symbol=TEST_SYMBOL,
            time=datetime.now(),
            sma10=150.0,
            sma20=148.0,
            rsi=65.0
        )
        for _ in range(5)
    ]
    
    financials = {
        'annual_income': [
            AnnualIncomeStatementModel(
                symbol=TEST_SYMBOL,
                fiscal_date_ending=datetime.now(),
                revenue=1000000,
                gross_profit=500000
            )
            for _ in range(3)
        ],
        'annual_balance': [
            AnnualBalanceSheetStatementModel(
                symbol=TEST_SYMBOL,
                fiscal_date_ending=datetime.now(),
                total_assets=2000000,
                total_liabilities=1000000
            )
            for _ in range(3)
        ],
        'annual_cashflow': [
            AnnualCashFlowStatementModel(
                symbol=TEST_SYMBOL,
                fiscal_date_ending=datetime.now(),
                operating_cash_flow=300000
            )
            for _ in range(3)
        ],
        'quarter_income': [
            QuarterlyIncomeStatementModel(
                symbol=TEST_SYMBOL,
                fiscal_date_ending=datetime.now(),
                revenue=250000,
                gross_profit=125000
            )
            for _ in range(3)
        ],
        'quarter_balance': [
            QuarterBalanceSheetStatementModel(
                symbol=TEST_SYMBOL,
                fiscal_date_ending=datetime.now(),
                total_assets=2000000,
                total_liabilities=1000000
            )
            for _ in range(3)
        ],
        'quarter_cashflow': [
            QuarterCashflowStatementModel(
                symbol=TEST_SYMBOL,
                fiscal_date_ending=datetime.now(),
                operating_cash_flow=75000
            )
            for _ in range(3)
        ]
    }

    async def mock_query(model_class, filters, sort=None, limit=None):
        print(f"Model class: {model_class}")
        print(f"Filters: {filters}")
        
        # Extract the actual value from the SQLAlchemy expression
        symbol_value = filters[0].right.value if hasattr(filters[0].right, 'value') else filters[0].right
        print(f"Symbol value: {symbol_value}")
        
        if model_class == OverviewModel:
            should_return = symbol_value == TEST_SYMBOL
            print(f"Should return overview: {should_return}")
            return [overview] if should_return else []
        elif model_class == QuotationModel:
            return [quotation] if symbol_value == TEST_SYMBOL else []
        elif model_class == DailyCandlestickModel:
            return candlesticks if symbol_value == TEST_SYMBOL else []
        elif model_class == DailyIndicatorModel:
            return indicators if symbol_value == TEST_SYMBOL else []
        elif model_class == AnnualIncomeStatementModel:
            return financials['annual_income'] if symbol_value == TEST_SYMBOL else []
        elif model_class == AnnualBalanceSheetStatementModel:
            return financials['annual_balance'] if symbol_value == TEST_SYMBOL else []
        elif model_class == AnnualCashFlowStatementModel:
            return financials['annual_cashflow'] if symbol_value == TEST_SYMBOL else []
        elif model_class == QuarterlyIncomeStatementModel:
            return financials['quarter_income'] if symbol_value == TEST_SYMBOL else []
        elif model_class == QuarterBalanceSheetStatementModel:
            return financials['quarter_balance'] if symbol_value == TEST_SYMBOL else []
        elif model_class == QuarterCashflowStatementModel:
            return financials['quarter_cashflow'] if symbol_value == TEST_SYMBOL else []
        return []

    storage.query = mock_query
    return storage

@pytest.mark.asyncio
@patch('at_common_functions.stock.get_storage')
async def test_stock_get_overview_success(mock_get_storage, mock_storage):
    mock_get_storage.return_value = mock_storage
    result = await stock_get_overview(symbol=TEST_SYMBOL)
    assert isinstance(result, dict)
    assert result["symbol"] == TEST_SYMBOL
    assert result["name"] == "Apple Inc."
    assert result["sector"] == "Technology"

@pytest.mark.asyncio
@patch('at_common_functions.stock.get_storage')
async def test_stock_get_overview_invalid_symbol(mock_get_storage, mock_storage):
    mock_get_storage.return_value = mock_storage
    with pytest.raises(ValueError, match="No overview found for symbol"):
        await stock_get_overview(symbol="INVALID_SYMBOL")

@pytest.mark.asyncio
@patch('at_common_functions.stock.get_storage')
async def test_stock_get_quotation_success(mock_get_storage, mock_storage):
    mock_get_storage.return_value = mock_storage
    result = await stock_get_quotation(symbol=TEST_SYMBOL)
    assert isinstance(result, dict)
    assert result["symbol"] == TEST_SYMBOL
    assert result["price"] == 150.0
    assert result["volume"] == 1000000

@pytest.mark.asyncio
@patch('at_common_functions.stock.get_storage')
async def test_stock_get_candlesticks_daily(mock_get_storage, mock_storage):
    mock_get_storage.return_value = mock_storage
    result = await stock_get_candlesticks(
        symbol=TEST_SYMBOL,
        type="daily",
        limit=5
    )
    assert isinstance(result, list)
    assert len(result) == 5
    for candlestick in result:
        assert candlestick["symbol"] == TEST_SYMBOL
        assert candlestick["open"] == 150.0
        assert candlestick["high"] == 155.0
        assert candlestick["low"] == 149.0
        assert candlestick["close"] == 152.0

@pytest.mark.asyncio
@patch('at_common_functions.stock.get_storage')
async def test_stock_get_indicators_daily(mock_get_storage, mock_storage):
    mock_get_storage.return_value = mock_storage
    result = await stock_get_indicators(
        symbol=TEST_SYMBOL,
        type="daily",
        limit=5
    )
    assert isinstance(result, list)
    assert len(result) == 5
    for indicator in result:
        assert indicator["symbol"] == TEST_SYMBOL
        assert indicator["sma10"] == 150.0
        assert indicator["sma20"] == 148.0
        assert indicator["rsi"] == 65.0

@pytest.mark.asyncio
@patch('at_common_functions.stock.get_storage')
@pytest.mark.parametrize("period,statement", [
    ("annual", "income"),
    ("annual", "balance_sheet"),
    ("annual", "cash_flow"),
    ("quarterly", "income"),
    ("quarterly", "balance_sheet"),
    ("quarterly", "cash_flow"),
])
async def test_stock_get_financials_success(mock_get_storage, mock_storage, period, statement):
    mock_get_storage.return_value = mock_storage
    result = await stock_get_financials(
        symbol=TEST_SYMBOL,
        period=period,
        statement=statement,
        limit=3
    )
    assert isinstance(result, list)
    assert len(result) == 3
    for financial in result:
        assert financial["symbol"] == TEST_SYMBOL
        assert "fiscal_date_ending" in financial
