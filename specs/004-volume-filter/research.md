# Research: Volume Filter

## 1. Technical Approach for Volume Average
**Decision**: use Simple Moving Average (SMA) over 20 periods.
**Rationale**: Standard industry practice for volume baselines. EMA weights recent volume too heavily which can distort the baseline during breakout sequences.
**Implementation**: `df['volume_sma_20'] = df['volume'].rolling(window=20).mean()` in `src/analysis.py`.

## 2. Preventing Repainting (The `i-1` Rule)
**Problem**: The "current" candle (tail(1)) is forming. Its volume starts at 0 and grows. Comparing forming volume to completed average always triggers "Low Volume".
**Solution**: 
- Valid Signal Check: `Strategy Condition` -> applies to `tail(1)` (Current Price).
- Valid Volume Check: `Volume` -> applies to `iloc[-2]` (Last Completed Candle).
- **Logic**: "Is the potential signal aimed at a market that WAS liquid in the last completed period?" 
- **Refinement**: Actually, for a *breakout*, we want to know if *current* move has volume. But verifying current volume is tricky.
- **Revised Logic per Spec**: Spec Clarification says "Validate volume based on the last fully closed bar [i-1]". We will strictly follow this.
- **Constraint**: This means we are confirming "Pre-move liquidity" or "Sustained liquidity", not necessarily the "breakout spike" itself if it's just happening. However, `Volume Confirmed` usually implies concurrent volume. 
- **Trade-off**: Using [i-1] is safer for automation. We accept this trade-off.

## 3. Backtest Integration
**Challenge**: `backtester.py` uses `df.query(condition)`.
**Solution**: 
- We cannot easily inject `volume > volume_sma * threshold` into the text query because `threshold` varies.
- Instead, `find_signal_dates` returns indices. 
- We will filter these indices *after* finding them. 
- `filtered_indices = [idx for idx in indices if df['volume'].iloc[idx-1] > df['volume_sma_20'].iloc[idx-1] * threshold]`
- Wait, backtest usually looks at the signal candle `idx`. If `idx` is "time of signal", and signal includes "close", then `idx` usually refers to the completed candle in historical data.
- **Decision**: In historical backtest, row `idx` is a COMPLETED candle. Therefore `df['volume'].iloc[idx]` IS the completed volume.
- **Distinction**:
    - **Live (Market Scanner)**: `tail(1)` is OPEN. Use `iloc[-2]`.
    - **Backtest**: `df` is history. Row `i` is COMPLETED. Use `iloc[i]`.
    - **CRITICAL**: We must align this. If `market_scanner.py` validates `i-1` for live, then backtester must validate `i-1` for history? 
    - Spec says: "Validate volume based on the last fully closed bar".
    - If I am backtesting a signal at time `T`, and in live mode at time `T` (while T is forming) I looked at `T-1`, then in backtest at time `T` (completed), I should look at `T-1`?
    - **Resolution**: Yes. To match Live behavior, Backtest at index `i` should check `volume` at `i-1`. (Or `i` if we assume the signal generates at CLOSE of `i`).
    - Standard convention: Signal generates at CLOSE of `i`. In live code, we often check `tail(1)` which is `i+1` (next open) or `i` (current open)? `ccxt` returns incomplete candles.
    - If `market_scanner` checks `df.tail(1)` (the forming candle), and uses `iloc[-2]` (the previous completed), then for a historical row `i`, the "previous completed" relative to "forming i" is `i-1`.
    - **Correction**: If backtest iterates over *completed* candles `0..N`. A signal at `i` means "At catch `i`, condition satisfied". This corresponds to "Just after `i` closed". 
    - If we assume `find_signal_dates` returns indices of *closed* candles meeting condition:
        - We should check Volume of `i` (the candle that triggered the signal).
    - BUT `market_scanner` checks `tail(1)` (forming). And uses `iloc[-2]` (previous completed).
    - `tail(1)` forming is `i+1`. `iloc[-2]` is `i`.
    - So, checking `iloc[-2]` in Live is equivalent to checking `Volume[i]` (Signal Candle) in Backtest.
    - **Conclusion**: 
        - **Live**: Check `iloc[-2]` (Last Closed).
        - **Backtest**: Check `iloc[i]` (Signal Candle).

## 4. Strategy Loader Regex
**Pattern**:
```regex
-\s+ATR Multiplier:\s*([\d.]+))?(?:.*?\n-\s+Volume Threshold:\s*([\d.]+))?
```
Need to make sure it captures the optional volume threshold at the end of the parameters list.

