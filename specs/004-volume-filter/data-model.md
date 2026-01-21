# Data Model: Volume Filter

## Entities

### VolumeContext
Derived technical data used for filtering.

| Field | Type | Description |
|-------|------|-------------|
| `current_volume` | float | Volume of the reference candle (Live: `i-1`, Backtest: `i`) |
| `avg_volume_20d` | float | 20-period Simple Moving Average of volume |
| `volume_ratio` | float | `current_volume / avg_volume_20d` |
| `volume_status` | enum | `LOW` (< threshold), `NORMAL`, `HIGH` (> 1.5x) |

### StrategyConfig (Extension)
Updates to the Strategy definition.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `volume_threshold` | float | 0.5 | Minimum required `volume_ratio` to pass filter |

### TradeSignal (Extension)
Updates to the output signal object.

| Field | Type | Description |
|-------|------|-------------|
| `volume_metrics` | VolumeContext | Detailed volume analysis data |
| `filter_status` | enum | `PASSED`, `WARNING_LOW_VOLUME` |

## Data Flow

1. **Analysis**: `calculate_indicators` adds `volume_sma_20` column.
2. **Scanning**: 
   - Extract `strategy['volume_threshold']`.
   - Calculate `ratio = volume / sma`.
   - if `ratio < threshold` -> tag as `WARNING`.
3. **Reporting**:
   - Report includes `Volume: 45% of Avg (LOW)` styling.
