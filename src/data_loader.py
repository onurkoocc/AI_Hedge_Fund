"""
Data collection module for Market Scanner Core System.

This module fetches market data from multiple sources:
- Crypto: Binance via ccxt (OHLCV data)
- Macro: Yahoo Finance via yfinance (Gold, DXY, S&P 500)
- Sentiment: RSS feeds via feedparser + TextBlob analysis
"""

import logging
import pandas as pd
import ccxt
import yfinance as yf
import feedparser
from textblob import TextBlob
from typing import List, Dict
from .utils import standardize_columns

logger = logging.getLogger(__name__)


def fetch_crypto_data(symbol: str, days: int = 180) -> pd.DataFrame:
    """
    Fetch cryptocurrency OHLCV data from Binance using ccxt.
    
    Args:
        symbol: Trading pair (e.g., 'BTC/USDT')
        days: Number of days to fetch (default: 180)
        
    Returns:
        DataFrame with columns: open, high, low, close, volume
        Returns empty DataFrame on error
    """
    try:
        exchange = ccxt.binance()
        timeframe = '1h'
        
        # Calculate how many candles to fetch
        candles_needed = days * 24  # 1-hour candles
        
        logger.info(f"Fetching {symbol} data for {days} days...")
        
        # Fetch OHLCV data
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=candles_needed)
        
        # Convert to DataFrame
        df = pd.DataFrame(
            ohlcv,
            columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']
        )
        
        # Convert timestamp to datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        
        # Standardize column names
        df = standardize_columns(df)
        
        logger.info(f"✓ Successfully fetched {len(df)} candles for {symbol}")
        return df
        
    except ccxt.NetworkError as e:
        logger.error(f"Network error fetching {symbol}: {e}")
        return pd.DataFrame()
    except ccxt.ExchangeError as e:
        logger.error(f"Exchange error fetching {symbol}: {e}")
        return pd.DataFrame()
    except Exception as e:
        logger.error(f"Unexpected error fetching {symbol}: {e}")
        return pd.DataFrame()


def fetch_macro_data(symbol: str, days: int = 180) -> pd.DataFrame:
    """
    Fetch macro asset data from Yahoo Finance.
    
    Args:
        symbol: Yahoo Finance symbol (e.g., 'GC=F', 'DX-Y.NYB', '^GSPC')
        days: Number of days to fetch (default: 180)
        
    Returns:
        DataFrame with columns: open, high, low, close, volume
        Returns empty DataFrame on error
    """
    try:
        logger.info(f"Fetching macro data for {symbol}...")
        
        # Calculate period string
        period = f"{days}d"
        
        # Fetch data using yfinance
        ticker = yf.Ticker(symbol)
        df = ticker.history(period=period, interval='1d')
        
        if df.empty:
            logger.warning(f"No data returned for {symbol}")
            return pd.DataFrame()
        
        # yfinance returns columns: Open, High, Low, Close, Volume
        # Standardize column names to lowercase
        df = standardize_columns(df)
        
        logger.info(f"✓ Successfully fetched {len(df)} days for {symbol}")
        return df
        
    except Exception as e:
        logger.error(f"Error fetching macro data for {symbol}: {e}")
        return pd.DataFrame()


def fetch_rss_headlines(feed_urls: List[str]) -> List[str]:
    """
    Fetch news headlines from RSS feeds.
    
    Args:
        feed_urls: List of RSS feed URLs
        
    Returns:
        List of headline strings. Returns empty list on error.
    """
    headlines = []
    
    for url in feed_urls:
        try:
            logger.info(f"Fetching RSS feed: {url}")
            feed = feedparser.parse(url)
            
            # Extract titles from entries
            for entry in feed.entries[:10]:  # Limit to 10 headlines per feed
                if hasattr(entry, 'title'):
                    headlines.append(entry.title)
            
            logger.info(f"✓ Fetched {len(feed.entries[:10])} headlines from {url}")
            
        except Exception as e:
            logger.error(f"Error fetching RSS feed {url}: {e}")
            continue
    
    return headlines


def calculate_sentiment(headlines: List[str]) -> float:
    """
    Calculate average sentiment score from news headlines using TextBlob.
    
    Args:
        headlines: List of headline strings
        
    Returns:
        Average polarity score from -1 (negative) to +1 (positive)
        Returns 0.0 (neutral) if headlines is empty
    """
    try:
        if not headlines:
            logger.warning("No headlines provided for sentiment analysis")
            return 0.0
        
        # Calculate polarity for each headline
        polarities = []
        for headline in headlines:
            try:
                blob = TextBlob(headline)
                polarities.append(blob.sentiment.polarity)
            except Exception as e:
                logger.warning(f"Error analyzing headline '{headline[:50]}...': {e}")
                continue
        
        if not polarities:
            return 0.0
        
        # Return average sentiment
        avg_sentiment = sum(polarities) / len(polarities)
        logger.info(f"✓ Calculated sentiment: {avg_sentiment:.3f} from {len(polarities)} headlines")
        
        return avg_sentiment
        
    except Exception as e:
        logger.error(f"Error calculating sentiment: {e}")
        return 0.0
