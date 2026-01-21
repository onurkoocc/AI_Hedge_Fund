# Quickstart: Testing Volume Filter

## Prerequisites
- Active Python environment
- Re-run `check-prerequisites.ps1` to ensure environment is clean.

## 1. Verify Indicator Calculation
Run a quick analysis script to check if `volume_sma_20` is generated.
```bash
python tools/quick_analysis.py --symbol BTC/USDT --indicators
# Output should list 'volume_sma_20' in columns
```

## 2. Test Strategy Parsing
Add a test strategy with volume threshold to `specs/04_strategies.md` (temporary) or use existing.
```markdown
### 99. Test Vol Strategy
**Type**: Breakout
**Entry Condition**:
```python
"rsi < 30"
```
**Parameters**:
- Stop Loss: 2%
- Take Profit: 4%
- Position Size: 10%
- Volume Threshold: 0.8
```

## 3. Run Market Scanner
Execute the scanner and check logs for volume validation.
```bash
python tools/market_scanner.py --symbols BTC/USDT ETH/USDT --days 20
```

## 4. Check Output
Open `output/market_snapshot.md` and verify:
- Signals have "Volume" details.
- Low volume signals are marked (if any).

## 5. Verify Backtester
Run the backtest tool explicitly (if applicable) or rely on scanner's integrated proof step.
All "Proof" results in the report should ideally respect the filter (or report that they filtered historical trades). *Note: The backtester update ensures historical validation uses the same logic.*
