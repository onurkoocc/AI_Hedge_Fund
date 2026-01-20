# Data Model: Market Scanner Core

## Entities

### 1. Asset (`Asset`)
Represents a financial instrument being tracked.
- **Source**: `ccxt` or `yfinance`
- **Identifier**: `symbol` (e.g., 'BTC/USDT', 'GC=F')
- **Data**: `df` (Pandas DataFrame with `datetime` index and columns `open`, `high`, `low`, `close`, `volume`)

### 2. Market Data (`MarketData`)
Aggregated collection of all Assets.
- **Structure**: Dictionary `{symbol: Asset}`
- **Macro Data**: Merged columns into main crypto DataFrame for correlation strategies (e.g., `btc_df['gold_close']`).

### 3. Strategy (`Strategy`)
A rule set defined in `specs/04_strategies.md`.
- **Name**: String (e.g., "Trend Pullback")
- **Type**: Enum (`Trend`, `Pair`, `Grid`)
- **Condition**: String (Pandas Query, e.g., `"rsi < 30 and close > ema_200"`)
- **Params**: Dict (e.g., `{'stop_loss': 0.02, 'take_profit': 0.04}`)

### 4. Signal (`Signal`)
A discrete event where a Strategy Condition became True.
- **Timestamp**: Datetime
- **Asset**: String
- **Strategy Name**: String
- **Direction**: `Long` | `Short`
- **Entry Price**: Float

### 5. Backtest Result (`BacktestResult`)
Verification of a Signal based on historical simulation.
- **Signal Timestamp**: Datetime
- **Exit Timestamp**: Datetime
- **Result**: `Win` | `Loss`
- **PnL**: Float (Percentage, e.g., 0.05 for 5%)
- **Duration**: Timedelta

## Database Schema (In-Memory / DataFrame)

The system operates primarily on Pandas DataFrames.

**Standardized OHLCV Schema**:
| Column | Type | Description |
|--------|------|-------------|
| date | datetime | Index |
| open | float64 | Open price |
| high | float64 | High price |
| low | float64 | Low price |
| close | float64 | Close price |
| volume | float64 | Volume |
| rsi | float64 | RSI Indicator |
| ema_200| float64 | 200-period EMA |
| ... | ... | Other indicators |

**Report Schema (JSON representation in Markdown)**:
```json
{
  "market_snapshot": {
    "generated_at": "ISO-8601",
    "signals": [
      {
        "asset": "BTC/USDT",
        "strategy": "Trend Pullback",
        "timestamp": "ISO-8601",
        "proof": {
           "last_3_signals": [
              {"date": "...", "pnl": 0.05, "status": "TP"},
              {"date": "...", "pnl": -0.02, "status": "SL"},
              {"date": "...", "pnl": 0.05, "status": "TP"}
           ]
        }
      }
    ]
  }
}
```
