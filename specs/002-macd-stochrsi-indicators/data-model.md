# Data Model: MACD ve Stochastic RSI İndikatörleri

**Feature Branch**: `002-macd-stochrsi-indicators`  
**Date**: 2026-01-20  
**Status**: Final

## Entity Overview

This feature adds two indicator groups to the existing DataFrame structure. No new database tables or persistent storage required — all values are calculated in-memory on OHLCV data.

## Entities

### 1. MACD Indicator Columns

Added to the main DataFrame returned by `calculate_indicators()`.

| Column Name | Type | Range | Description |
|-------------|------|-------|-------------|
| `macd` | float64 | Unbounded (typically -5 to +5 for crypto) | MACD Line: 12-period EMA minus 26-period EMA |
| `macd_signal` | float64 | Unbounded | Signal Line: 9-period EMA of MACD Line |
| `macd_histogram` | float64 | Unbounded | Histogram: MACD Line minus Signal Line |
| `macd_bullish_cross` | bool | True/False | True when histogram crosses from ≤0 to >0 |
| `macd_bearish_cross` | bool | True/False | True when histogram crosses from ≥0 to <0 |

**Display Precision**: 4 decimal places

**Calculation Parameters** (fixed, per FR-001):
- `window_fast`: 12
- `window_slow`: 26
- `window_sign`: 9

---

### 2. Stochastic RSI Indicator Columns

Added to the main DataFrame returned by `calculate_indicators()`.

| Column Name | Type | Range | Description |
|-------------|------|-------|-------------|
| `stoch_rsi_k` | float64 | 0-100 | %K Line: Fast stochastic of RSI |
| `stoch_rsi_d` | float64 | 0-100 | %D Line: 3-period SMA of %K (signal) |
| `stoch_rsi_bullish` | bool | True/False | True when K crosses above D in oversold zone (<20) |
| `stoch_rsi_bearish` | bool | True/False | True when K crosses below D in overbought zone (>80) |

**Display Precision**: 4 decimal places

**Calculation Parameters** (fixed, per FR-002):
- `window`: 14 (RSI period)
- `smooth1`: 3 (%K smoothing)
- `smooth2`: 3 (%D smoothing)

**Zone Thresholds**:
- Oversold: < 20
- Overbought: > 80

---

## Validation Rules

### MACD

1. If input data has < 35 rows, MACD columns will contain NaN
2. NaN values should not trigger crossover signals
3. Crossover detection requires valid previous row (shift(1))

### Stochastic RSI

1. If input data has < 28 rows, StochRSI columns will contain NaN
2. Values must be scaled to 0-100 range (library returns 0-1)
3. Zone checks must use scaled values

---

## State Transitions

### MACD Histogram State Machine

```
[Negative] --histogram > 0--> [Positive] → Emit "MACD bullish crossover"
[Positive] --histogram < 0--> [Negative] → Emit "MACD bearish crossover"
```

### StochRSI Zone State Machine

```
[Normal] --K crosses above D && K < 20--> [Bullish Signal] → Emit "Bullish StochRSI crossover in oversold"
[Normal] --K crosses below D && K > 80--> [Bearish Signal] → Emit "Bearish StochRSI crossover in overbought"
```

---

## Relationships

### Integration with Existing Entities

| Existing Column | Relationship | Usage |
|-----------------|--------------|-------|
| `close` | Input → MACD, StochRSI | Both indicators use close price |
| `ema_200` | Combined with MACD | Bullish momentum confirmation when close > ema_200 AND MACD bullish |
| `rsi` | Compared with StochRSI | StochRSI provides faster signals than RSI |

### Strategy Integration (Optional Filters)

| Strategy | MACD Usage | StochRSI Usage |
|----------|------------|----------------|
| Trend Pullback | `macd_bullish_cross` adds confidence | Not used |
| Short Strategy | `macd_bearish_cross` adds confidence | `stoch_rsi_bearish` adds confirmation |

---

## DataFrame Schema After Feature

```python
# Existing columns (unchanged)
df.columns = [
    'open', 'high', 'low', 'close', 'volume',  # OHLCV
    'rsi', 'ema_200', 'atr', 'bb_lower', 'bb_mid', 'bb_upper', 'adx',  # Existing indicators
    
    # NEW: MACD columns
    'macd',              # float64, MACD line
    'macd_signal',       # float64, Signal line
    'macd_histogram',    # float64, Histogram
    'macd_bullish_cross',  # bool, Bullish crossover
    'macd_bearish_cross',  # bool, Bearish crossover
    
    # NEW: StochRSI columns
    'stoch_rsi_k',       # float64, %K line (0-100)
    'stoch_rsi_d',       # float64, %D line (0-100)
    'stoch_rsi_bullish', # bool, Bullish crossover in oversold
    'stoch_rsi_bearish', # bool, Bearish crossover in overbought
]
```

**Total New Columns**: 9
