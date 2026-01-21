# Implementation Checklist

## Data & Analysis
- [ ] `calculate_indicators` computes 20-period Volume SMA (`volume_sma_20`)
- [ ] Volume SMA calculation handles `NaN` correctly (start of dataframe)

## Strategy Loading
- [ ] Regex pattern captures `Volume Threshold` parameter optionally
- [ ] Default `volume_threshold` is 0.5 if not specified
- [ ] Loaded strategies dictionary contains `params['volume_threshold']`

## Signal Scanning (Live)
- [ ] Scanner identifies `last_completed_candle` (i-1) correctly
- [ ] Volume Ratio calculated as `vol[i-1] / sma[i-1]`
- [ ] Logic tags signal as `LOW_VOLUME` if ratio < threshold
- [ ] `VOL_TOO_LOW` signals are NOT discarded but marked (FR-006)
- [ ] Signal object includes `volume_metrics` (ratio, status)

## Backtesting
- [ ] Backtest engine retrieves `volume_threshold` from params
- [ ] Historical trace validates volume at Signal Candle index
- [ ] Backtest ignores/rejects trades where volume condition failed (Proof logic)

## Reporting
- [ ] Markdown report displays Volume Status column/badge
- [ ] "Volume Confirmed" badge for high volume (> 1.5x)
- [ ] "Low Volume" warning for filtered signals

## Integration
- [ ] `check-prerequisites` passes
- [ ] No regression in existing strategy execution
