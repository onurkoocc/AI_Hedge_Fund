# Phase 0: Research Findings

## ATR Implementation
- **Decision**: Use existing `ta.volatility.AverageTrueRange` implementation in `src/analysis.py`.
- **Rationale**: The library is already a dependency and the code is already present in `analysis.py` (line 53). Reusing it ensures consistency.
- **Current State**: `analysis.py` adds an `'atr'` column to the DataFrame.

## Backtester Integration
- **Decision**: Refactor `simulate_trade` in `src/backtester.py` to accept explicit `stop_loss_price` and `take_profit_price` arguments (optional/overloaded) instead of just percentages.
- **Rationale**: Dynamic Stop Loss is not a fixed percentage. It is `Entry ± (ATR * Multiplier)`. The resulting percentage varies per trade. Passing the calculated absolute price is the most flexible approach for the simulation engine.
- **Proposed Change**: 
  - Update `simulate_trade(df, entry_idx, stop_loss_pct, take_profit_pct)` to `simulate_trade(df, entry_idx, stop_loss_price=None, take_profit_price=None, stop_loss_pct=None, take_profit_pct=None)`.
  - If `*_price` is provided, use it. If `*_pct` is provided, calculate price.
  - This maintains backward compatibility if needed, or we can refactor all callers.

## Signal Generation Logic
- **Decision**: The calculation of SL/TP levels happens in the strategy/scanner layer (before calling `simulate_trade`).
- **Rationale**: Separates "Trading Logic" (where to set stop) from "Execution Simulation" (did the price hit the stop).
- **Impact**: `backtest_strategy` function in `src/backtester.py` (which currently iterates and calls `simulate_trade`) will need to be updated to:
    1. Look up the ATR value for the entry row.
    2. Calculate dynamic SL/TP prices.
    3. Pass these prices to `simulate_trade`.

## Configuration
- **Decision**: Strategy configuration (likely in script arguments or strategy definitions) needs to support `atr_multiplier` (float, default 1.5).
