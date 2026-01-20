# Implementation Plan: Market Scanner Core System

**Branch**: `001-market-scanner-core` | **Date**: 2026-01-19 | **Spec**: [specs/001-market-scanner-core/spec.md](specs/001-market-scanner-core/spec.md)
**Input**: Feature specification from `specs/001-market-scanner-core/spec.md`

## Summary

This feature establishes the core infrastructure for the AI-Driven Hedge Fund. It implements a "Market Scanner Core System" that collects market data (crypto, macro, sentiment), scans for trading signals based on defined strategies, verifies them with a mini-backtest (proof engine), and generates a Markdown report for LLM consumption.

The implementation will follow a 4-phase approach:
1.  **Infrastructure**: setup `requirements.txt` and `specs/` configuration files.
2.  **Data Layer**: Implement `src/data_loader.py` for `ccxt` and `yfinance` integration.
3.  **Risk Engine (Proof Engine)**: Implement `src/backtester.py` for signal validation (critical module).
4.  **Tools & Reporting**: Integrate everything into `tools/market_scanner.py` and generate reports.

## Technical Context

**Language/Version**: Python 3.9+
**Primary Dependencies**: `ccxt`, `yfinance`, `pandas-ta`, `textblob`, `feedparser`, `pandas`
**Storage**: Local Files (Markdown output in `output/` directory)
**Testing**: Manual CLI tests, Independent validation scripts as defined in User Stories.
**Target Platform**: Windows / Cross-platform Python environment
**Project Type**: Single project (CLI/Script)
**Performance Goals**: < 2 minutes for full market scan, < 30 seconds for backtest signal verification
**Constraints**: Must use only free data sources. Graceful degradation on internet failure.
**Scale/Scope**: ~5 Crypto assets, ~3 Macro assets, 3 initial strategies.

## Constitution Check

*GATE: Passed*

-   **Vizyon Odaklı Disiplin**: Supports monthly growth by providing databased signals.
-   **Spec-Driven Mimari**: all logic driven by `specs/` files (FR-019 to FR-022).
-   **Kanıtlanabilir Sinyal Üretimi**: Implements `backtester.py` for "Last 3 Signals" verification (FR-011).
-   **Strateji Uyarlanabilirliği**: Strategies are pluggable via `specs/04_strategies.md`.
-   **Ücretsiz Veri Kaynağı Zorunluluğu**: Uses `ccxt` (public API), `yfinance`, `feedparser`.

## Project Structure

### Documentation (this feature)

```text
specs/001-market-scanner-core/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
└── tasks.md             # Phase 2 output
```

### Source Code

```text
src/
├── data_loader.py       # Data fetching (ccxt, yfinance, rss)
├── analysis.py          # Technical analysis (pandas-ta)
├── backtester.py        # Proof engine (signal verification)
└── utils.py             # Helper functions (time, logging)

tools/
└── market_scanner.py    # Main CLI entry point

specs/                   # Configuration & Rules
├── 01_mission.md
├── 02_risk_rules.md
├── 03_data_sources.md
└── 04_strategies.md

output/                  # Generated reports
└── market_snapshot.md
```

**Structure Decision**: Single project structure with `src/` for core logic and `tools/` for CLI execution, adhering to the requested file layout.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None      | N/A        | N/A                                 |
