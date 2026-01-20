# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement dynamic stop-loss and take-profit calculation using ATR (Average True Range).
Detailed approach:
1. Leverage existing `ta.volatility` ATR calculation in `analysis.py`.
2. Introduce a new risk calculation function in `analysis.py` (`calculate_risk_levels`) that outputs absolute price levels for SL/TP based on entry price and ATR.
3. Refactor `simulate_trade` in `backtester.py` to accept absolute price levels, enabling dynamic risk management per trade signal.
4. Update `market_scanner` and `backtest_signals` tools to utilize the new logic and display/log the dynamic levels.


## Technical Context

**Language/Version**: Python 3.10+
**Primary Dependencies**: `ccxt`, `yfinance`, `pandas`, `ta` library (for ATR)
**Storage**: CSV/Markdown files (output), In-memory Pandas DataFrames
**Testing**: `pytest` (implied standard), Custom backtesting scripts in `tools/`
**Target Platform**: Windows (Dev), Cross-platform Python (Prod)
**Project Type**: Python CLI / Analysis Scripts
**Performance Goals**: Support backtesting 1 year of 1h data in <10s implies vectorized operations where possible, but `simulate_trade` is iterative.
**Constraints**: Must integrate with existing `simulate_trade` function in `src/backtester.py`.
**Scale/Scope**: Feature enhancement to existing scanner and backtester.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **Library-First**: Core logic (ATR calculation, dynamic stop resolution) should be in `src/` modules, not just scripts.
- [x] **CLI Interface**: `backtest_signals.py` and `market_scanner.py` likely act as CLIs. Configuration should be passable via args.
- [x] **Test-First**: Will define test cases in `tasks.md`.
- [x] **Integration Testing**: Backtest compatibility ensures integration.
- [x] **Simplicity**: Reusing `ta` library for ATR avoids reimplementation.

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
src/
├── analysis.py            # Contains ATR calculation and will hold new risk logic
├── backtester.py          # Will be refactored for dynamic SL/TP
├── data_loader.py
├── strategy_loader.py
└── utils.py

tools/
├── market_scanner.py      # Entry point consuming new logic
└── backtest_signals.py    # Entry point consuming new logic
```

**Structure Decision**: Extending the existing flat Python package structure. Logic resides in `src/`, execution in `tools/`.


## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
