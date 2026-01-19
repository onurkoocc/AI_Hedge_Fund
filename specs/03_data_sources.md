# Data Sources Configuration

## Crypto Assets (Primary Targets)

**Source**: Binance via `ccxt` library (public API - free)

Tracked symbols:
- `BTC/USDT` - Bitcoin (Market Leader)
- `ETH/USDT` - Ethereum (DeFi Proxy)
- `SOL/USDT` - Solana (High Beta)
- `BNB/USDT` - Binance Coin (Exchange Token)
- `XRP/USDT` - Ripple (Institutional Play)

**Data Format**: OHLCV (Open, High, Low, Close, Volume)
**Timeframe**: 1-hour candles
**Lookback**: 180 days (sufficient for EMA200 and historical signal detection)

## Macro Indicators (Context & Correlation)

**Source**: Yahoo Finance via `yfinance` library (free)

Tracked symbols:
- `GC=F` - Gold Futures (Risk-off/Risk-on indicator)
- `DX-Y.NYB` - US Dollar Index (Currency strength)
- `^GSPC` - S&P 500 Index (Traditional market sentiment)

**Purpose**: 
- Gold ↑ + DXY ↓ = Risk-on environment (bullish for crypto)
- S&P correlation check (when stocks dump, crypto often follows)

## Sentiment Data

### RSS News Feeds
**Source**: RSS feeds via `feedparser` library

Recommended feeds:
- Cointelegraph: `https://cointelegraph.com/rss`
- CoinDesk: `https://www.coindesk.com/arc/outboundfeeds/rss/`
- Decrypt: `https://decrypt.co/feed`

**Processing**: Extract headlines → TextBlob sentiment analysis → Average polarity score (-1 to +1)

### Fear & Greed Index
**Source**: Alternative.me API (free)

**Endpoint**: `https://api.alternative.me/fng/?limit=1`

**Interpretation**:
- 0-25: Extreme Fear (potential buy opportunity)
- 25-45: Fear
- 45-55: Neutral
- 55-75: Greed
- 75-100: Extreme Greed (potential sell/short opportunity)

## Data Refresh Schedule

- **Market Scanner**: Run once per day (evening)
- **Manual Refresh**: On-demand via CLI when needed
- **Historical Data**: Fetch 180 days on first run, then append new candles

## Error Handling

All data fetch operations must include:
1. Try-catch blocks for network failures
2. Fallback to cached data if available
3. Log errors but continue with available data
4. Never crash the scanner due to one failed data source
