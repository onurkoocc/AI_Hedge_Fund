# Quickstart: Market Scanner Core

## Prerequisites

- Python 3.9+
- Internet connection (for Binance/Yahoo APIs)

## Installation

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\\Scripts\\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. Review Strategy Rules:
   - Check `specs/04_strategies.md` to see active scanning rules.

2. Review Data Sources:
   - Check `specs/03_data_sources.md` to see which assets are scanned.

## Usage

### Run Market Scanner

To fetch data, calculate indicators, scan for signals, and generate report:

```bash
python tools/market_scanner.py
```

### Output

The report will be generated at:
`output/market_snapshot.md`

### Testing

Run the backtester manually for a specific asset/strategy check:

```bash
# Example syntax (to be implemented)
python src/backtester.py --symbol BTC/USDT --strategy "rsi<30"
```
