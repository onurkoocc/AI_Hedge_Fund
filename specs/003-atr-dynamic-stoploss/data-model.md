# Data Model: Dynamic Stop Loss

## Entities

### `DynamicStop` (Conceptual)
Represents the risk management parameters calculated for a specific trade signal.

| Field | Type | Description |
|-------|------|-------------|
| `entry_price` | `float` | Price at signal generation |
| `atr_value` | `float` | ATR(14) value at signal time |
| `atr_multiplier` | `float` | Multiplier used (e.g., 1.5) |
| `stop_loss_price` | `float` | Calculated absolute SL price |
| `take_profit_price` | `float` | Calculated absolute TP price |
| `rr_ratio` | `float` | Calculated Risk/Reward ratio |

## DataFrame Extensions
The main analysis DataFrame will be augmented (or processed per row) with:

| Column | Type | Source | Description |
|--------|------|--------|-------------|
| `atr` | `float` | `analysis.py` | 14-period Average True Range (Already exists) |

## Function Signatures (Design)

### `src.analysis.calculate_risk_levels`
Calculates the dynamic levels for a potential trade.

```python
def calculate_risk_levels(
    entry_price: float, 
    atr: float, 
    side: str, 
    atr_multiplier: float = 1.5,
    min_rr: float = 2.0
) -> Dict[str, float]:
    """
    Returns:
    {
        'stop_loss': float,
        'take_profit': float,
        'stop_distance': float,
        'stop_pct': float,
        'rr_ratio': float,
        'status': str  # 'OK', 'LOW_RR', 'VOLATILITY_TOO_HIGH'
    }
    """
```

### `src.backtester.simulate_trade` (Updated)
Refactored to accept absolute levels.

```python
def simulate_trade(
    df: pd.DataFrame, 
    entry_idx: int, 
    stop_loss_price: float = None, 
    take_profit_price: float = None,
    stop_loss_pct: float = None,  # Legacy support / fallback
    take_profit_pct: float = None # Legacy support / fallback
) -> Dict[str, Any]:
    ...
```
