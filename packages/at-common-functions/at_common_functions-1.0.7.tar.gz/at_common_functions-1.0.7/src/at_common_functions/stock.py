from at_common_functions.utils.storage import get_storage
from at_common_models.stock.quotation import QuotationModel
from at_common_models.stock.overview import OverviewModel
from at_common_models.stock.daily_candlestick import DailyCandlestickModel
from at_common_models.stock.daily_indicator import DailyIndicatorModel
from at_common_models.stock.financials.annual_balance_sheet_statement import AnnualBalanceSheetStatementModel
from at_common_models.stock.financials.quarter_balance_sheet_statement import QuarterBalanceSheetStatementModel
from at_common_models.stock.financials.annual_cashflow_statement import AnnualCashFlowStatementModel
from at_common_models.stock.financials.quarter_cashflow_statement import QuarterCashflowStatementModel
from at_common_models.stock.financials.annual_income_statement import AnnualIncomeStatementModel
from at_common_models.stock.financials.quarter_income_statement import QuarterlyIncomeStatementModel

async def stock_get_overview(*, symbol: str) -> dict:
    storage = get_storage()
    overviews = await storage.query(
        model_class=OverviewModel,
        filters=[OverviewModel.symbol == symbol]
    )

    if len(overviews) == 0:
        raise ValueError(f"No overview found for symbol: {symbol}")

    if len(overviews) > 1:
        raise ValueError(f"Multiple overviews found for symbol: {symbol}, got {len(overviews)}")
    
    return overviews[0].to_dict()

async def stock_get_quotation(*, symbol: str) -> dict:
    storage = get_storage()
    quotations = await storage.query(
        model_class=QuotationModel,
        filters=[QuotationModel.symbol == symbol]
    )

    if len(quotations) == 0:
        raise ValueError(f"No quotation found for symbol: {symbol}")
    
    if len(quotations) > 1:
        raise ValueError(f"Multiple quotations found for symbol: {symbol}, got {len(quotations)}")
    
    return quotations[0].to_dict()

async def stock_get_candlesticks(*, symbol: str, type: str, limit: int) -> list:
    storage = get_storage()

    candlesticks = None
    if type == 'daily':
        candlesticks = await storage.query(
            model_class=DailyCandlestickModel,
            filters=[DailyCandlestickModel.symbol == symbol],
            sort=[DailyCandlestickModel.time.desc()],
            limit=limit
        )
    
    if candlesticks is None:
        raise ValueError(f"Invalid type for candlesticks: {type}")

    return [c.to_dict() for c in candlesticks]

async def stock_get_indicators(*, symbol: str, type: str, limit: int) -> list:
    storage = get_storage()

    indicators = None
    if type == 'daily':
        indicators = await storage.query(
            model_class=DailyIndicatorModel,
            filters=[DailyIndicatorModel.symbol == symbol],
            sort=[DailyIndicatorModel.time.desc()],
            limit=limit
        )

    if indicators is None: 
        raise ValueError(f"Invalid type for indicators: {type}")
    
    return [i.to_dict() for i in indicators]

async def stock_get_financials(*, symbol: str, period: str, statement: str, limit: int) -> list:
    storage = get_storage()

    clazz = None
    if period == 'annual':
        if statement == 'income':
            clazz = AnnualIncomeStatementModel
        elif statement == 'balance_sheet':
            clazz = AnnualBalanceSheetStatementModel
        elif statement == 'cash_flow':
            clazz = AnnualCashFlowStatementModel
    elif period == 'quarterly':
        if statement == 'income':
            clazz = QuarterlyIncomeStatementModel
        elif statement == 'balance_sheet':
            clazz = QuarterBalanceSheetStatementModel
        elif statement == 'cash_flow':
            clazz = QuarterCashflowStatementModel
    
    if clazz is None:
        raise ValueError("Invalid period or statement for financials")

    statements = await storage.query(
        model_class=clazz,
        filters=[clazz.symbol == symbol],
        sort=[clazz.fiscal_date_ending.desc()],
        limit=limit
    )

    return [statement.to_dict() for statement in statements]