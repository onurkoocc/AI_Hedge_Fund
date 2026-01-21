# AI_Hedge_Fund Development Guidelines

Auto-generated from all feature plans. Last updated: 2026-01-19

## Active Technologies
- Python 3.11+ (existing project uses pandas, ta library) + ta>=0.11.0 (already installed), pandas>=2.0.0 (already installed) (002-macd-stochrsi-indicators)
- N/A (in-memory DataFrame operations) (002-macd-stochrsi-indicators)
- Python 3.10+ + `ccxt`, `yfinance`, `pandas`, `ta` library (for ATR) (003-atr-dynamic-stoploss)
- CSV/Markdown files (output), In-memory Pandas DataFrames (003-atr-dynamic-stoploss)
- [e.g., Python 3.11, Swift 5.9, Rust 1.75 or NEEDS CLARIFICATION] + [e.g., FastAPI, UIKit, LLVM or NEEDS CLARIFICATION] (master)
- [if applicable, e.g., PostgreSQL, CoreData, files or N/A] (master)
- CSV/Markdown reports (No DB changes) (master)

- Python 3.9+ + `ccxt`, `yfinance`, `pandas-ta`, `textblob`, `feedparser`, `pandas` (001-market-scanner-core)

## Project Structure

```text
src/
tests/
```

## Commands

cd src; pytest; ruff check .

## Code Style

Python 3.9+: Follow standard conventions

## Recent Changes
- master: Added Python 3.10+
- master: Added Python 3.10+
- master: Added [e.g., Python 3.11, Swift 5.9, Rust 1.75 or NEEDS CLARIFICATION] + [e.g., FastAPI, UIKit, LLVM or NEEDS CLARIFICATION]


<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->
