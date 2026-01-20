# Quickstart: MACD ve Stochastic RSI İndikatörleri

**Feature Branch**: `002-macd-stochrsi-indicators`  
**Date**: 2026-01-20

## Prerequisites

- Python 3.11+ with virtual environment activated
- `ta>=0.11.0` (already in requirements.txt)
- Existing market scanner working

## Quick Verification

After implementation, verify the feature works:

```bash
# Run market scanner and check for new indicator columns
cd C:\Users\kocon\AI_Hedge_Fund
python tools/market_scanner.py
```

Expected output should include MACD and StochRSI values in the analysis.

## Using New Indicators in Strategies

### Example 1: MACD Confirmation for Trend Pullback

```python
# In strategy YAML or query syntax
condition: "close > ema_200 and rsi < 35 and macd_bullish_cross == True"
```

### Example 2: StochRSI Oversold Signal

```python
# Check for oversold bounce
condition: "stoch_rsi_k < 20 and stoch_rsi_bullish == True"
```

### Example 3: Combined Short Signal

```python
# Short with StochRSI overbought confirmation
condition: "close < ema_200 and rsi > 65 and stoch_rsi_bearish == True"
```

## New DataFrame Columns

After calling `calculate_indicators(df)`:

| Column | Type | Description |
|--------|------|-------------|
| `macd` | float64 | MACD Line |
| `macd_signal` | float64 | Signal Line |
| `macd_histogram` | float64 | Histogram |
| `macd_bullish_cross` | bool | Bullish crossover detected |
| `macd_bearish_cross` | bool | Bearish crossover detected |
| `stoch_rsi_k` | float64 | %K Line (0-100) |
| `stoch_rsi_d` | float64 | %D Line (0-100) |
| `stoch_rsi_bullish` | bool | Bullish crossover in oversold |
| `stoch_rsi_bearish` | bool | Bearish crossover in overbought |

## Logging

Events are logged at INFO level:

```
INFO - MACD bullish crossover (MACD: 0.0523, Signal: 0.0412) for BTC/USDT
INFO - Bullish StochRSI crossover in oversold (K: 15.2345, D: 12.1234) for ETH/USDT
```

Calculation failures are logged at WARNING level:

```
WARNING - Insufficient data for MACD calculation: 20 rows (need 35+) for XRP/USDT
```

## Backtest Integration

New indicators work automatically with existing backtest system:

```bash
python tools/backtest_signals.py --condition "macd_bullish_cross == True and close > ema_200"
```

## Troubleshooting

### All indicator values are NaN

**Cause**: Insufficient data (need 35+ rows for MACD, 28+ for StochRSI)

**Solution**: Ensure 180-day lookback is used (default)

### StochRSI values outside 0-100 range

**Cause**: Library returns 0-1 range by default

**Solution**: Implementation multiplies by 100 automatically

### Crossover signals not appearing

**Cause**: Need at least 2 rows for crossover detection (uses shift)

**Solution**: Normal behavior for first row; signals appear from row 2 onward
