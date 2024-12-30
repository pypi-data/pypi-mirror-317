import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from at_common_functions.news import news_get_stocks_news
from at_common_models.news.stock import NewsStockModel
from at_common_models.news.article import NewsArticleModel
from datetime import datetime
import pytest_asyncio

TEST_SYMBOL = "AAPL"

@pytest_asyncio.fixture
async def mock_storage():
    storage = MagicMock()
    
    # Sample test data with specific dates
    global stock_news  # Make it accessible in mock_query
    stock_news = [
        NewsStockModel(
            news_id="article1",
            symbol=TEST_SYMBOL,  # Only AAPL symbol
            published_at=datetime(2024, 3, 15)
        ),
        NewsStockModel(
            news_id="article2",
            symbol=TEST_SYMBOL,  # Only AAPL symbol
            published_at=datetime(2024, 2, 1)
        )
    ]
    
    global articles  # Make it accessible in mock_query
    articles = [
        NewsArticleModel(
            id="article1",
            source="Test Source",
            headline="Test Headline 1",
            summary="Test Summary 1",
            url="http://test1.com",
            published_at=datetime(2024, 3, 15)
        ),
        NewsArticleModel(
            id="article2",
            source="Test Source",
            headline="Test Headline 2",
            summary="Test Summary 2",
            url="http://test2.com",
            published_at=datetime(2024, 2, 1)
        )
    ]
    
    async def mock_query(model_class, filters, sort=None, limit=None):
        if model_class == NewsStockModel:
            filtered_news = stock_news.copy()
            
            for filter_condition in filters:
                if hasattr(filter_condition.left, 'key') and filter_condition.left.key == 'symbol':
                    # Extract the symbol value
                    symbol_value = filter_condition.right.value if hasattr(filter_condition.right, 'value') else filter_condition.right
                    print(f"Filtering by symbol: {symbol_value}")  # Debug
                    filtered_news = [n for n in filtered_news if n.symbol == symbol_value]
                    print(f"Filtered news count: {len(filtered_news)}")  # Debug
                elif hasattr(filter_condition.left, 'key') and filter_condition.left.key == 'published_at':
                    # Extract the date value
                    date_value = filter_condition.right.value if hasattr(filter_condition.right, 'value') else filter_condition.right
                    print(f"Filtering by date: {date_value}")  # Debug
                    filtered_news = [n for n in filtered_news if n.published_at >= date_value]
                    print(f"Filtered news count after date: {len(filtered_news)}")  # Debug
            
            if sort:
                filtered_news.sort(key=lambda x: x.published_at, reverse=True)
            
            return filtered_news[:limit] if limit else filtered_news
            
        elif model_class == NewsArticleModel:
            # Extract article IDs from the SQLAlchemy in_() expression
            article_ids = filters[0].right.value if hasattr(filters[0].right, 'value') else filters[0].right
            print(f"Article IDs to filter: {article_ids}")  # Debug
            
            # Filter articles based on IDs
            filtered_articles = [a for a in articles if a.id in article_ids]
            print(f"Filtered articles count: {len(filtered_articles)}")  # Debug
            return filtered_articles
        
        return []

    storage.query = AsyncMock(side_effect=mock_query)
    return storage

@pytest.mark.asyncio
@patch('at_common_functions.news.get_storage')
async def test_news_get_stocks_news_success(mock_get_storage, mock_storage):
    mock_get_storage.return_value = mock_storage
    
    result = await news_get_stocks_news(symbol=TEST_SYMBOL, limit=2)
    
    assert isinstance(result, list)
    assert len(result) == 2
    
    for article in result:
        assert isinstance(article, dict)
        assert "id" in article
        assert "source" in article
        assert "headline" in article
        assert "summary" in article
        assert "url" in article
        assert "published_at" in article

@pytest.mark.asyncio
@patch('at_common_functions.news.get_storage')
async def test_news_get_stocks_news_no_results(mock_get_storage, mock_storage):
    mock_get_storage.return_value = mock_storage
    
    result = await news_get_stocks_news(symbol="INVALID_SYMBOL", limit=5)
    
    assert isinstance(result, list)
    assert len(result) == 0

@pytest.mark.asyncio
@patch('at_common_functions.news.get_storage')
async def test_news_get_stocks_news_with_limit(mock_get_storage, mock_storage):
    mock_get_storage.return_value = mock_storage
    
    result = await news_get_stocks_news(symbol=TEST_SYMBOL, limit=1)
    
    assert isinstance(result, list)
    assert len(result) == 1

@pytest.mark.asyncio
@patch('at_common_functions.news.get_storage')
async def test_news_get_stocks_news_with_earliest_date(mock_get_storage, mock_storage):
    mock_get_storage.return_value = mock_storage
    
    result = await news_get_stocks_news(
        symbol=TEST_SYMBOL, 
        limit=2,
        earliest_date="20240101"
    )
    
    assert isinstance(result, list)
    assert len(result) == 2

@pytest.mark.asyncio
@patch('at_common_functions.news.get_storage')
async def test_news_get_stocks_news_invalid_date_format(mock_get_storage, mock_storage):
    mock_get_storage.return_value = mock_storage
    
    with pytest.raises(ValueError):
        await news_get_stocks_news(
            symbol=TEST_SYMBOL, 
            limit=2,
            earliest_date="2024-01-01"  # Wrong format
        )
