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
import pandas as pd

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

async def stock_calculate_financial_metrics(*, symbol: str) -> dict:
    # Define default metrics structure with all possible keys
    default_metrics = {
        # Valuation metrics
        'market_cap': 0,
        'enterprise_value': 0,
        'price_to_book': 0,
        'price_to_sales': 0,
        
        # Profitability ratios
        'gross_margin': 0,
        'operating_margin': 0,
        'net_margin': 0,
        'roe': 0,
        'roa': 0,
        
        # Liquidity ratios
        'current_ratio': 0,
        'quick_ratio': 0,
        'cash_ratio': 0,
        
        # Growth metrics
        'revenue_cagr': 0,
        'net_income_cagr': 0
    }
    
    try:
        # Fetch required data
        quotation = await stock_get_quotation(symbol=symbol)
        financials = {
            'income': await stock_get_financials(symbol=symbol, period='annual', statement='income', limit=5),
            'balance_sheet': await stock_get_financials(symbol=symbol, period='annual', statement='balance_sheet', limit=5),
            'cash_flow': await stock_get_financials(symbol=symbol, period='annual', statement='cash_flow', limit=5)
        }
        
        # Convert to DataFrames and validate data existence
        financial_data = {
            'income': pd.DataFrame(financials['income']),
            'balance': pd.DataFrame(financials['balance_sheet']),
            'cashflow': pd.DataFrame(financials['cash_flow'])
        }

        if any(df.empty for df in financial_data.values()):
            raise ValueError(f"Missing financial data for symbol: {symbol}")

        # Calculate market cap
        market_data = {
            'market_cap': quotation['price'] * quotation['share_outstanding'],
            'price': quotation['price']
        }
        
        # Get latest statements
        latest_income = financial_data['income'].iloc[0]
        latest_balance = financial_data['balance'].iloc[0]
        latest_cashflow = financial_data['cashflow'].iloc[0]
        
        metrics = default_metrics.copy()  # Start with a copy of default metrics
        
        # Valuation metrics
        total_stockholders_equity = latest_balance.get('total_stockholders_equity', 0) or 1
        revenue = latest_income.get('revenue', 0) or 1
        
        metrics.update({
            'market_cap': market_data['market_cap'],
            'enterprise_value': (market_data['market_cap'] + 
                               (latest_balance.get('total_debt', 0) or 0) - 
                               (latest_balance.get('cash_and_cash_equivalents', 0) or 0)),
            'price_to_book': market_data['market_cap'] / total_stockholders_equity,
            'price_to_sales': market_data['market_cap'] / revenue
        })
        
        # Profitability ratios
        metrics.update({
            'gross_margin': (latest_income.get('gross_profit', 0) or 0) / revenue,
            'operating_margin': (latest_income.get('operating_income', 0) or 0) / revenue,
            'net_margin': (latest_income.get('net_income', 0) or 0) / revenue,
            'roe': (latest_income.get('net_income', 0) or 0) / total_stockholders_equity,
            'roa': (latest_income.get('net_income', 0) or 0) / (latest_balance.get('total_assets', 0) or 1)
        })
        
        # Liquidity ratios
        current_liabilities = latest_balance.get('total_current_liabilities', 0) or 1
        metrics.update({
            'current_ratio': (latest_balance.get('total_current_assets', 0) or 0) / current_liabilities,
            'quick_ratio': ((latest_balance.get('total_current_assets', 0) or 0) - 
                          (latest_balance.get('inventory', 0) or 0)) / current_liabilities,
            'cash_ratio': (latest_balance.get('cash_and_cash_equivalents', 0) or 0) / current_liabilities
        })
        
        # Growth metrics
        if len(financial_data['income']) > 1:
            years = len(financial_data['income']) - 1
            oldest_income = financial_data['income'].iloc[-1]
            
            def calculate_cagr(start_value: float, end_value: float, years: int) -> float:
                try:
                    if start_value <= 0 or end_value <= 0:
                        return 0
                    return (end_value / start_value) ** (1 / years) - 1
                except Exception:
                    return 0
            
            metrics.update({
                'revenue_cagr': calculate_cagr(
                    oldest_income.get('revenue', 1) or 1,
                    latest_income.get('revenue', 1) or 1,
                    years
                ),
                'net_income_cagr': calculate_cagr(
                    oldest_income.get('net_income', 1) or 1,
                    latest_income.get('net_income', 1) or 1,
                    years
                )
            })
        
        return metrics
    
    except Exception as e:
        # Return default metrics in case of any error
        return default_metrics