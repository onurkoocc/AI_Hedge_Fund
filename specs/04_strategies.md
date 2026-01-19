# Trading Strategies

## Strategy Format

Each strategy is defined with:
- **Name**: Human-readable identifier
- **Type**: Category (Trend, Pair, Grid, Breakout)
- **Condition**: Pandas query string (e.g., `"rsi < 30 and close > ema_200"`)
- **Parameters**: Stop loss %, Take profit %, Position size %

## Active Strategies

### 1. Trend Pullback (Long)

**Type**: Trend Following  
**Market Condition**: Clear uptrend with temporary dips

**Entry Condition**:
```python
"close > ema_200 and rsi < 35 and adx > 25"
```

**Logic**:
- Price above 200 EMA confirms uptrend
- RSI below 35 indicates oversold pullback
- ADX above 25 confirms strong trend (not ranging)

**Parameters**:
- Stop Loss: 2% below entry
- Take Profit: 5% above entry (2.5:1 R:R)
- Position Size: 2% of capital at risk

**Macro Filter**: DXY declining (dollar weakness is crypto positive)

---

### 2. Pair Trading (Market Neutral Hedge)

**Type**: Relative Strength  
**Market Condition**: Uncertain/choppy markets

**Entry Condition**:
```python
"btc_strength > eth_strength and btc_strength > 0.6"
```

**Logic**:
- Calculate 30-day rate of change for each asset
- Long the stronger asset (e.g., BTC)
- Short the weaker asset (e.g., ETH)
- Profit from relative performance, not absolute direction

**Parameters**:
- Stop Loss: 3% relative divergence
- Take Profit: 6% relative convergence (2:1 R:R)
- Position Size: 1.5% per leg (3% total)

**Macro Filter**: S&P 500 volatility > 20 (uncertain traditional markets)

---

### 3. Grid Trading (Range-Bound)

**Type**: Mean Reversion  
**Market Condition**: Sideways/consolidation

**Entry Condition**:
```python
"adx < 20 and close > bb_lower and close < bb_upper"
```

**Logic**:
- ADX below 20 indicates no strong trend (ranging)
- Price within Bollinger Bands confirms range
- Buy near lower band, sell near upper band

**Grid Setup**:
- 5 levels between BB lower and BB upper
- Buy at levels 1-2 (bottom 40% of range)
- Sell at levels 4-5 (top 40% of range)

**Parameters**:
- Stop Loss: Below BB lower band (invalidation of range)
- Take Profit: Opposite band (e.g., buy at lower, sell at upper)
- Position Size: 0.5% per grid level (2.5% max exposure)

**Macro Filter**: Gold stable (no major risk events)

---

### 4. Breakout Continuation (High Conviction)

**Type**: Momentum  
**Market Condition**: After consolidation, strong volume breakout

**Entry Condition**:
```python
"close > bb_upper and volume > volume.rolling(20).mean() * 1.5 and rsi > 60"
```

**Logic**:
- Price breaks above Bollinger Band (expansion)
- Volume 50% above 20-day average (conviction)
- RSI above 60 confirms momentum (not overbought yet)

**Parameters**:
- Stop Loss: Below BB upper band (retest failure)
- Take Profit: 1.5x ATR above breakout (volatility-adjusted)
- Position Size: 2.5% of capital at risk

**Macro Filter**: Positive sentiment score (> 0.3) and S&P rising

---

## Strategy Selection Logic

The market scanner evaluates all strategies for each asset. Priority order:

1. **Primary**: Trend Pullback (highest win rate in backtests)
2. **Secondary**: Breakout Continuation (high R:R but lower frequency)
3. **Hedge**: Pair Trading (only when market uncertain)
4. **Fallback**: Grid Trading (low return but consistent in chop)

## Mini-Backtest Parameters

When validating signals:
- Lookback: 180 days
- Number of historical signals: Last 3 occurrences
- Minimum signal gap: 7 days (avoid overfitting to clustered signals)

## Strategy Performance Tracking

After each trade (manual entry for now):
- Record in `output/trade_journal.json`
- Track: Entry date, Exit date, Strategy used, P&L, R:R achieved
- Monthly review: Disable strategies with < 50% win rate over 10+ trades
