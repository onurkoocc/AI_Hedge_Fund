# Research: Market Scanner Core System

## Unknowns & Clarifications

### 1. Data Standardization for `df.query()`
**Question**: How to standardize column names from `ccxt` (lowercase), `yfinance` (PascalCase), and `pandas-ta` (UpperCase with length) to single format for `df.query("close > ema_200")`?
**Findings**:
- `ccxt` returns `['timestamp', 'open', 'high', 'low', 'close', 'volume']` (lowercase).
- `yfinance` returns `['Open', 'High', 'Low', 'Close', 'Volume']` (PascalCase).
- `pandas-ta` by default appends columns like `RSI_14`, `EMA_200` (Uppercase).
**Decision**: Implement a strict column mapping and renaming step in `data_loader` and `analysis` modules.
- Convert all to **lowercase**.
- Rename `pandas-ta` outputs: `RSI_14` -> `rsi`, `EMA_200` -> `ema_200` (removing length suffix if fixed, or keeping it `rsi_14` if strategy requires definition. Spec says `ema_200`, so we will rename `EMA_200` to `ema_200`).
- **Rationale**: User explicitly requested `close > ema_200` query string format and lowercase snake_case in FR-016a.

### 2. Timezone Alignment
**Question**: `ccxt` (Crypto) runs 24/7, `yfinance` (Macro) runs M-F. How to merge?
**Findings**:
- Crypto has more rows. Macro has gaps (weekends).
- `pandas.merge_asof` or `reindex` might be needed.
**Decision**: Use `concat`/`merge` on DatetimeIndex. Forward fill (`ffill`) macro data for weekends to allow Crypto signals to be checked against last known macro state (e.g. Friday's close).
- **Rationale**: Crypto markets don't stop. A "Gold < 2000" condition should check Friday's Gold price on Saturday.

## Technology Choices

| Area | Choice | Rationale | Alternatives |
|------|--------|-----------|--------------|
| Crypto Data | `ccxt` | Supports multiple exchanges (Binance), free public API access for market data. | `binance-python` (vendor lock-in) |
| Macro Data | `yfinance` | Free, easy access to Yahoo Finance for Gold/DXY. | `alpha_vantage` (API key limits) |
| Analysis | `pandas-ta` | Pandas extension, incredibly fast, supports all needed indicators (RSI, ADX, etc). | `ta-lib` (binary dependency issues) |
| Sentiment | `TextBlob` | Simple lexicon-based sentiment, sufficient for MVP. | `VADER`, `Transformers` (too heavy) |

## Implementation Strategy

1.  **Shared Utils**: Create `utils.standardize_columns(df)` function to handle the lowercasing and renaming logic centrally.
2.  **Backtest Logic**: "Last 3 signals" requires fetching enough historical data. 
    - `ccxt`: fetch ~1000 candles to ensure coverage.
    - `backtester.py`: Use vectorization to find signal indices, then take last 3 `True` indices.

