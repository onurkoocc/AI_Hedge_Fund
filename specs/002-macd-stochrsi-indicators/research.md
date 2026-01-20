# Research: MACD ve Stochastic RSI İndikatörleri

**Feature Branch**: `002-macd-stochrsi-indicators`  
**Date**: 2026-01-20  
**Status**: Complete

## Research Tasks

### 1. ta Library MACD Support

**Question**: Does the `ta` library support MACD calculation with standard parameters?

**Finding**: ✅ Yes, fully supported

**Details**:
- Class: `ta.trend.MACD`
- Constructor: `MACD(close, window_slow=26, window_fast=12, window_sign=9, fillna=False)`
- Methods:
  - `macd()` → MACD Line (float64)
  - `macd_signal()` → Signal Line (float64)
  - `macd_diff()` → Histogram (MACD - Signal) (float64)
- Default parameters match spec requirements (fast=12, slow=26, signal=9)

**Code Pattern**:
```python
from ta.trend import MACD

macd_indicator = MACD(close=df['close'], window_fast=12, window_slow=26, window_sign=9)
df['macd'] = macd_indicator.macd()
df['macd_signal'] = macd_indicator.macd_signal()
df['macd_histogram'] = macd_indicator.macd_diff()
```

**Decision**: Use `ta.trend.MACD` class  
**Rationale**: Already used in project (`ta` library), consistent API with existing indicators  
**Alternatives Considered**: pandas-ta, ta-lib → Rejected (would add new dependency)

---

### 2. ta Library Stochastic RSI Support

**Question**: Does the `ta` library support Stochastic RSI with standard parameters?

**Finding**: ✅ Yes, fully supported

**Details**:
- Class: `ta.momentum.StochRSIIndicator`
- Constructor: `StochRSIIndicator(close, window=14, smooth1=3, smooth2=3, fillna=False)`
- Methods:
  - `stochrsi()` → Raw StochRSI (0-1 range)
  - `stochrsi_k()` → %K line (0-1 range, needs *100 for 0-100)
  - `stochrsi_d()` → %D line (0-1 range, needs *100 for 0-100)
- Parameters map: `period=14` → `window=14`, `smooth_k=3` → `smooth1=3`, `smooth_d=3` → `smooth2=3`

**Code Pattern**:
```python
from ta.momentum import StochRSIIndicator

stoch_rsi = StochRSIIndicator(close=df['close'], window=14, smooth1=3, smooth2=3)
df['stoch_rsi_k'] = stoch_rsi.stochrsi_k() * 100  # Convert to 0-100 range
df['stoch_rsi_d'] = stoch_rsi.stochrsi_d() * 100  # Convert to 0-100 range
```

**Decision**: Use `ta.momentum.StochRSIIndicator` class with *100 scaling  
**Rationale**: Consistent with existing `ta.momentum.RSIIndicator` usage  
**Alternatives Considered**: Manual calculation → Rejected (error-prone, no benefit)

---

### 3. Minimum Data Requirements

**Question**: What are the minimum data requirements for MACD and StochRSI?

**Finding**:
- **MACD**: Minimum 26 bars (slow EMA period) + 9 bars (signal smoothing) = **35 bars** for first valid signal line value
- **StochRSI**: Minimum 14 bars (RSI period) + 14 bars (stochastic period) = **28 bars** for first valid value

**Impact on Current System**:
- Current system uses 180 days of data → Sufficient for both indicators
- First ~35 rows will have NaN for MACD signal line
- First ~28 rows will have NaN for StochRSI

**Decision**: No data requirement changes needed  
**Rationale**: 180-day lookback exceeds both minimum requirements

---

### 4. Crossover Detection Pattern

**Question**: How to efficiently detect MACD and StochRSI crossovers?

**Finding**: Use pandas shift() for previous value comparison

**MACD Crossover Detection**:
```python
# Bullish: histogram crosses from negative to positive
df['macd_bullish_cross'] = (df['macd_histogram'] > 0) & (df['macd_histogram'].shift(1) <= 0)

# Bearish: histogram crosses from positive to negative
df['macd_bearish_cross'] = (df['macd_histogram'] < 0) & (df['macd_histogram'].shift(1) >= 0)
```

**StochRSI Crossover Detection**:
```python
# Bullish in oversold: K crosses above D when both < 20
df['stoch_rsi_bullish'] = (
    (df['stoch_rsi_k'] > df['stoch_rsi_d']) & 
    (df['stoch_rsi_k'].shift(1) <= df['stoch_rsi_d'].shift(1)) &
    (df['stoch_rsi_k'] < 20)
)

# Bearish in overbought: K crosses below D when both > 80
df['stoch_rsi_bearish'] = (
    (df['stoch_rsi_k'] < df['stoch_rsi_d']) & 
    (df['stoch_rsi_k'].shift(1) >= df['stoch_rsi_d'].shift(1)) &
    (df['stoch_rsi_k'] > 80)
)
```

**Decision**: Implement crossover detection as separate boolean columns  
**Rationale**: Enables use in Pandas query syntax for strategy conditions

---

### 5. Performance Impact Analysis

**Question**: Will adding MACD and StochRSI significantly impact scanner performance?

**Finding**: Minimal impact expected

**Benchmark Data** (estimated):
- Current indicators: RSI, EMA200, ATR, Bollinger Bands, ADX = ~5 indicators
- Adding: MACD (3 outputs), StochRSI (2 outputs) = 5 new columns
- Both use efficient numpy/pandas operations under the hood
- No external API calls or I/O operations

**Calculation Complexity**:
- MACD: O(n) - two EMAs + one EMA on difference
- StochRSI: O(n) - RSI + stochastic formula

**Decision**: Proceed without performance optimization  
**Rationale**: SC-002 allows up to 10% runtime increase; expected increase is <5%

---

### 6. Integration with Existing Code

**Question**: How to integrate new indicators into existing `calculate_indicators()` function?

**Finding**: Follow existing pattern in [src/analysis.py](../../src/analysis.py#L19)

**Current Pattern**:
```python
def calculate_indicators(df: pd.DataFrame) -> pd.DataFrame:
    # RSI
    rsi_indicator = RSIIndicator(close=df['close'], window=14)
    df['rsi'] = rsi_indicator.rsi()
    
    # ... more indicators
```

**Integration Approach**:
1. Add imports at top: `from ta.trend import MACD` and update momentum import
2. Add MACD calculation after existing indicators
3. Add StochRSI calculation after MACD
4. Add crossover detection columns
5. Log INFO for crossover events detected

**Decision**: Extend `calculate_indicators()` function  
**Rationale**: Single entry point for all indicator calculations, consistent pattern

---

## Summary

| Research Task | Status | Decision |
|---------------|--------|----------|
| MACD API | ✅ Resolved | Use `ta.trend.MACD` |
| StochRSI API | ✅ Resolved | Use `ta.momentum.StochRSIIndicator` with *100 |
| Data Requirements | ✅ Resolved | 180-day lookback sufficient |
| Crossover Detection | ✅ Resolved | Boolean columns via shift() |
| Performance Impact | ✅ Resolved | <5% expected, within SC-002 limit |
| Integration Pattern | ✅ Resolved | Extend existing function |

**All NEEDS CLARIFICATION items resolved. Ready for Phase 1.**
