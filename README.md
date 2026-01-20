# AI-Driven Hedge Fund - Market Scanner Core

A systematic, data-driven trading system that scans crypto markets, verifies signals with historical backtests, and generates actionable reports.

## 🎯 Goal

Achieve **7% monthly cumulative growth** through disciplined, proof-based trading.

## 🏗️ Architecture

This system follows a **Spec-Driven Architecture** where all business rules live in `specs/` files, separate from implementation code.

```
AI_Hedge_Fund/
├── specs/                  # Configuration & Rules (The Constitution)
│   ├── 01_mission.md       # Goals and trading philosophy
│   ├── 02_risk_rules.md    # 1:2 R:R ratio, backtest requirements
│   ├── 03_data_sources.md  # Asset symbols and data feeds
│   └── 04_strategies.md    # Trading strategy definitions
│
├── src/                    # Core Logic Engine
│   ├── utils.py            # Helper functions
│   ├── data_loader.py      # Data fetching (crypto, macro, sentiment)
│   ├── analysis.py         # Technical indicator calculations
│   ├── backtester.py       # Proof engine (signal verification)
│   └── strategy_loader.py  # Strategy configuration parser
│
├── tools/                  # CLI Tools
│   └── market_scanner.py   # Main orchestration script
│
└── output/                 # Generated Reports
    └── market_snapshot.md  # Daily market analysis report
```

## 📋 Features

### 1. **Multi-Source Data Collection**
- **Crypto**: BTC, ETH, SOL, BNB, XRP (via Binance/ccxt)
- **Macro**: Gold (GC=F), DXY, S&P 500 (via yfinance)
- **Sentiment**: RSS news feeds with TextBlob analysis

### 2. **Technical Analysis**
- RSI (14-period)
- EMA (200-period)
- ATR (14-period)
- Bollinger Bands (20-period)
- ADX (14-period)

### 3. **Proof Engine (Backtest Validator)**
- **Core Concept**: Before proposing any trade, verify it by backtesting the last 3 historical occurrences
- Simulates stop-loss and take-profit execution
- Reports win rate and P&L for each historical signal

### 4. **Strategy Framework**
- Strategies defined in plain English in `specs/04_strategies.md`
- Conditions written as Pandas query strings
- Easy to add new strategies without touching code

### 5. **Risk Management**
- Enforces 1:2 minimum Risk/Reward ratio
- Validates all signals against constitution rules
- Max 5 "sniper" trades per month

## 🚀 Quick Start

### Installation

1. **Clone the repository**
```bash
git clone <repo-url>
cd AI_Hedge_Fund
```

2. **Create virtual environment** (optional but recommended)
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Download NLTK data** (required for sentiment analysis)
```python
python -c "import nltk; nltk.download('punkt'); nltk.download('brown')"
```

### Usage

**Run the market scanner:**
```bash
python tools/market_scanner.py
```

This will:
1. Fetch crypto, macro, and sentiment data
2. Calculate technical indicators
3. Scan for strategy signals
4. Verify signals with historical backtests
5. Generate report at `output/market_snapshot.md`

**Custom options:**
```bash
# Scan specific symbols
python tools/market_scanner.py --symbols BTC/USDT ETH/USDT

# Use more historical data
python tools/market_scanner.py --days 365

# Custom output path
python tools/market_scanner.py --output-path reports/today.md
```

**Test the backtester standalone:**
```bash
python src/backtester.py --symbol BTC/USDT --condition "rsi < 30" --days 90
```

## 📊 Understanding the Report

The generated `output/market_snapshot.md` contains:

### Signal Structure
```markdown
### Signal 1: BTC/USDT - Trend Pullback

- **Type**: Trend Following
- **Entry Price**: $45,123.00
- **Timestamp**: 2026-01-19 15:30:00
- **Stop Loss**: 2.0%
- **Take Profit**: 5.0%
- **R:R Ratio**: ✅ 2.5:1
- **Win Rate (Last 3)**: 67%

**Backtest Proof (Last 3 Signals)**:

| Signal Date | Result | P&L | Duration |
|-------------|--------|-----|----------|
| 2026-01-10 12:00:00 | ✅ TP | +5.00% | 48 bars |
| 2025-12-28 09:30:00 | ❌ SL | -2.00% | 12 bars |
| 2025-12-15 14:00:00 | ✅ TP | +5.00% | 72 bars |
```

### Interpretation
- **✅ R:R Ratio**: Meets the 1:2 minimum requirement
- **Win Rate**: 2 out of 3 = 67% (above 50% threshold)
- **PnL**: Historical performance of this exact signal setup

## 🔧 Configuration

### Adding a New Strategy

Edit `specs/04_strategies.md`:

```markdown
### 5. Your Strategy Name

**Type**: Breakout
**Market Condition**: High volume expansion

**Entry Condition**:
```python
"close > bb_upper and volume > volume.rolling(20).mean() * 1.5"
```

**Parameters**:
- Stop Loss: 2% below entry
- Take Profit: 6% above entry (3:1 R:R)
- Position Size: 2% of capital at risk
```

The system will automatically detect and use it on next run.

### Modifying Data Sources

Edit `specs/03_data_sources.md` to add/remove symbols or RSS feeds.

### Adjusting Risk Rules

Edit `specs/02_risk_rules.md` to modify:
- R:R ratio requirements
- Backtest validation criteria
- Position sizing formulas

## 🛡️ Constitution Compliance

Every operation respects the **Constitution** ([.specify/memory/constitution.md](.specify/memory/constitution.md)):

1. ✅ **7% monthly growth goal** - All strategies target this
2. ✅ **1:2 R:R minimum** - Enforced in report validation
3. ✅ **Last 3 signal proof** - Implemented in backtester
4. ✅ **Free data sources only** - ccxt, yfinance, feedparser
5. ✅ **Spec-driven architecture** - Rules separate from code

## 🧪 Testing

### Test individual modules:

**Data Loader:**
```bash
python -c "from src.data_loader import fetch_crypto_data; df = fetch_crypto_data('BTC/USDT', days=7); print(df.head())"
```

**Analysis:**
```bash
python -c "from src.analysis import calculate_indicators; from src.data_loader import fetch_crypto_data; df = fetch_crypto_data('BTC/USDT', days=30); result = calculate_indicators(df); print(result.columns.tolist())"
```

**Strategy Loader:**
```bash
python -c "from src.strategy_loader import load_strategies; strategies = load_strategies(); print(len(strategies), 'strategies loaded')"
```

## 📈 Workflow

```
1. Data Collection
   ↓
2. Technical Analysis
   ↓
3. Strategy Scanning
   ↓
4. Signal Detection
   ↓
5. Backtest Validation (Proof Engine)
   ↓
6. Report Generation
   ↓
7. Human Decision (LLM-assisted)
```

## ⚠️ Important Notes

1. **This is NOT automated trading** - Reports are for analysis only
2. **Always validate signals** - Check macro context, news, etc.
3. **Respect the 5 trades/month limit** - Quality over quantity
4. **API rate limits** - Free APIs have request limits, script includes error handling
5. **Python 3.10-3.13** - pandas-ta doesn't support 3.14 yet (using `ta` library instead)

## 🤝 Contributing

This is a personal project, but suggestions welcome! Follow these principles:

1. **Specs first** - Update `specs/` before changing code
2. **No hardcoded rules** - All logic should reference config files
3. **Error tolerance** - Network issues shouldn't crash the scanner
4. **Constitution compliance** - All changes must respect the core principles

## 📝 License

Personal project - use at your own risk. Not financial advice.

---

**Last Updated**: 2026-01-19
**Version**: 1.0.0 (MVP)
