from at_common_functions.utils.storage import get_storage
from at_common_models.news.stock import NewsStockModel
from at_common_models.news.article import NewsArticleModel
from datetime import datetime

async def news_get_stocks_news(*, symbol: str, limit: int, earliest_date: str = None) -> list:
    storage = get_storage()
    
    # Build filters list with symbol condition
    filters = [NewsStockModel.symbol == symbol]
    
    # Convert string date to datetime and add filter if earliest_date is provided
    if earliest_date:
        filters.append(NewsStockModel.published_at >= datetime.strptime(earliest_date, '%Y%m%d'))
    
    stock_news = await storage.query(
        model_class=NewsStockModel,
        filters=filters,
        sort=[NewsStockModel.published_at.desc()],
        limit=limit
    )

    # Get article IDs from stock news results
    article_ids = [news.news_id for news in stock_news]
    
    # Query articles if we have any results
    if article_ids:
        articles = await storage.query(
            model_class=NewsArticleModel,
            filters=[NewsArticleModel.id.in_(article_ids)]
        )
        return [article.to_dict() for article in articles]
    
    return []

    

    