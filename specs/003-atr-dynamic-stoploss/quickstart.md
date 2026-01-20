# Quickstart: ATR Dynamic Stop Loss

## Validation

To verify the dynamic stop loss logic is working:

1. **Check Analysis Output**:
   The market snapshot or signal output should now show "Dynamic SL" and "Dynamic TP".
   
   ```bash
   python tools/market_scanner.py --symbol BTC/USDT --timeframe 1h
   ```
   
   Look for:
   > Signal: LONG @ 50000
   > ATR: 200 | Multiplier: 1.5
   > Stop: 49700 (Dist: 300, 0.6%) | TP: 50600

2. **Run Backtest with Dynamic Stop**:
   (Assumes CLI argument support is implemented)
   
   ```bash
   python tools/backtest_signals.py --strategy "rsi_oversold" --atr-multiplier 1.5
   ```

## Integration Guide

### Using in Custom Scripts

```python
from src.analysis import calculate_risk_levels

# Assuming you have a standard analysis dataframe 'df'
last_row = df.iloc[-1]
entry_price = last_row['close']
atr = last_row['atr']

# Calculate levels
levels = calculate_risk_levels(
    entry_price=entry_price,
    atr=atr,
    side='long',
    atr_multiplier=1.5
)

if levels['status'] == 'OK':
    print(f"Place Stop Loss at {levels['stop_loss']}")
else:
    print(f"Signal Rejected: {levels['status']}")
```
