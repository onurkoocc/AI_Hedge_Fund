---
description: "Implementation tasks for Market Scanner Core System"
---

# Tasks: Market Scanner Core System

**Input**: Design documents from `/specs/001-market-scanner-core/`
**Feature Branch**: `001-market-scanner-core`
**Prerequisites**: plan.md, spec.md, data-model.md, research.md, contracts/backtest-schema.json

**Tests**: No formal test framework requested. Manual verification steps included in each task.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `- [ ] [ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4, US5)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create root directory structure: `src/`, `tools/`, `specs/`, `output/`
- [X] T002 Create requirements.txt with dependencies: ccxt, yfinance, pandas, pandas-ta, textblob, feedparser
- [X] T003 [P] Create src/__init__.py (empty module marker)
- [X] T004 [P] Create tools/__init__.py (empty module marker)
- [X] T005 [P] Create output/.gitkeep (ensure output directory exists in git)
- [X] T006 [P] Create specs/01_mission.md with hedge fund goals and monthly growth targets
- [X] T007 [P] Create specs/02_risk_rules.md with 1:2 R:R ratio and mini-backtest requirements
- [X] T008 [P] Create specs/03_data_sources.md listing crypto symbols (BTC, ETH, SOL, BNB, XRP) and macro symbols (GC=F, DX-Y.NYB, ^GSPC)
- [X] T009 Create specs/04_strategies.md with initial strategies (Trend Pullback, Pair Trading, Grid) in Pandas Query String format

**Verification**: Run `dir src tools specs output` (Windows) and verify all directories exist. Check requirements.txt contains all 6 dependencies.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core utilities that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T010 Create src/utils.py with `standardize_columns(df)` function to convert all column names to lowercase snake_case (e.g., 'Close' → 'close', 'EMA_200' → 'ema_200')
- [X] T011 Add `setup_logging()` function to src/utils.py with INFO level console logging
- [X] T012 Add `get_timestamp()` function to src/utils.py returning ISO-8601 formatted current datetime

**Verification**: Run `python -c "from src.utils import standardize_columns, setup_logging, get_timestamp; import pandas as pd; df = pd.DataFrame({'Close': [100], 'EMA_200': [95]}); print(standardize_columns(df).columns.tolist())"` and verify output is `['close', 'ema_200']`.

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 4 - Veri Toplama (Data Collection) (Priority: P2) 

**Goal**: Fetch market data from multiple sources (crypto, macro, RSS feeds)

**Why First**: Data collection is a prerequisite for all other user stories. Even though it's P2, it must be implemented before P1 stories can run.

**Independent Test**: Run `python -c "from src.data_loader import fetch_crypto_data; df = fetch_crypto_data('BTC/USDT', days=7); print(df.shape, df.columns.tolist())"` and verify DataFrame has OHLCV columns.

### Implementation for User Story 4

- [X] T013 [P] [US4] Create src/data_loader.py file with module docstring
- [X] T014 [US4] Implement `fetch_crypto_data(symbol, days=180)` function in src/data_loader.py using ccxt.binance to fetch OHLCV data
- [X] T015 [US4] Add column standardization to `fetch_crypto_data()` using `utils.standardize_columns()` to ensure lowercase snake_case format
- [X] T016 [US4] Add error handling to `fetch_crypto_data()` for network failures, API errors, and invalid symbols (log error and return empty DataFrame)
- [X] T017 [P] [US4] Implement `fetch_macro_data(symbol, days=180)` function in src/data_loader.py using yfinance to fetch macro data (GC=F, DX-Y.NYB, ^GSPC)
- [X] T018 [US4] Add column standardization to `fetch_macro_data()` using `utils.standardize_columns()` to ensure lowercase snake_case format
- [X] T019 [US4] Add error handling to `fetch_macro_data()` for network failures and invalid symbols
- [X] T020 [P] [US4] Implement `fetch_rss_headlines(feed_urls)` function in src/data_loader.py using feedparser to fetch news headlines from RSS feeds
- [X] T021 [US4] Add error handling to `fetch_rss_headlines()` for network failures and invalid feed URLs (return empty list on failure)
- [X] T022 [US4] Implement `calculate_sentiment(headlines)` function in src/data_loader.py using TextBlob to compute average polarity score (-1 to +1)
- [X] T023 [US4] Add error handling to `calculate_sentiment()` for empty headlines list (return 0.0 as neutral)

**Verification for T014-T016**: Run `python -c "from src.data_loader import fetch_crypto_data; df = fetch_crypto_data('BTC/USDT', days=7); assert 'close' in df.columns; assert df.shape[0] > 0; print('✓ Crypto data fetch OK')"`.

**Verification for T017-T019**: Run `python -c "from src.data_loader import fetch_macro_data; df = fetch_macro_data('GC=F', days=7); assert 'close' in df.columns; print('✓ Macro data fetch OK')"`.

**Verification for T020-T023**: Run `python -c "from src.data_loader import fetch_rss_headlines, calculate_sentiment; headlines = fetch_rss_headlines(['https://news.google.com/rss']); score = calculate_sentiment(headlines); assert -1 <= score <= 1; print(f'✓ Sentiment score: {score}')"`.

**Checkpoint**: At this point, all data sources are accessible and return standardized DataFrames

---

## Phase 4: User Story 3 - Teknik Analiz Hesaplamaları (Priority: P2)

**Goal**: Calculate technical indicators (RSI, EMA, ATR, Bollinger, ADX) from price data

**Independent Test**: Run `python -c "from src.analysis import calculate_indicators; import pandas as pd; df = pd.DataFrame({'close': range(100, 200), 'high': range(101, 201), 'low': range(99, 199), 'open': range(100, 200), 'volume': [1000]*100}); result = calculate_indicators(df); assert 'rsi' in result.columns; print('✓ Indicators calculated')"`.

### Implementation for User Story 3

- [X] T024 [P] [US3] Create src/analysis.py file with module docstring
- [X] T025 [US3] Implement `calculate_indicators(df)` function in src/analysis.py that takes standardized OHLCV DataFrame and adds all indicator columns
- [X] T026 [US3] Add RSI calculation to `calculate_indicators()` using `pandas_ta.rsi(df['close'], length=14)` and rename column to 'rsi'
- [X] T027 [US3] Add EMA200 calculation to `calculate_indicators()` using `pandas_ta.ema(df['close'], length=200)` and rename column to 'ema_200'
- [X] T028 [US3] Add ATR calculation to `calculate_indicators()` using `pandas_ta.atr(df['high'], df['low'], df['close'], length=14)` and rename column to 'atr'
- [X] T029 [US3] Add Bollinger Bands calculation to `calculate_indicators()` using `pandas_ta.bbands(df['close'], length=20)` and rename columns to 'bb_lower', 'bb_mid', 'bb_upper'
- [X] T030 [US3] Add ADX calculation to `calculate_indicators()` using `pandas_ta.adx(df['high'], df['low'], df['close'], length=14)` and rename column to 'adx'
- [X] T031 [US3] Add column standardization pass at end of `calculate_indicators()` using `utils.standardize_columns()` to ensure all new columns are lowercase snake_case
- [X] T032 [US3] Add error handling to `calculate_indicators()` for insufficient data (< 200 rows for EMA200) and return original DataFrame with warning log
- [X] T033 [P] [US3] Implement `merge_macro_data(crypto_df, macro_dfs)` function in src/analysis.py to merge macro columns into crypto DataFrame with forward fill for weekends
- [X] T034 [US3] Add reindexing logic to `merge_macro_data()` using `pd.merge_asof()` to align crypto (24/7) with macro (M-F) timestamps
- [X] T035 [US3] Add forward fill (`ffill()`) logic to `merge_macro_data()` for weekend gaps in macro data
- [X] T036 [US3] Add column prefixing to `merge_macro_data()` for macro columns (e.g., 'close' → 'gold_close', 'dxy_close') to avoid name collisions

**Verification for T025-T032**: Run `python -c "from src.analysis import calculate_indicators; from src.data_loader import fetch_crypto_data; df = fetch_crypto_data('BTC/USDT', days=30); result = calculate_indicators(df); assert all(col in result.columns for col in ['rsi', 'ema_200', 'atr', 'bb_lower', 'adx']); print('✓ All indicators present:', result.columns.tolist())"`.

**Verification for T033-T036**: Run `python -c "from src.analysis import merge_macro_data; from src.data_loader import fetch_crypto_data, fetch_macro_data; crypto = fetch_crypto_data('BTC/USDT', days=7); gold = fetch_macro_data('GC=F', days=7); merged = merge_macro_data(crypto, {'gold': gold}); assert 'gold_close' in merged.columns; print('✓ Macro merge OK')"`.

**Checkpoint**: At this point, all technical indicators can be calculated and macro data can be merged

---

## Phase 5: User Story 2 - Sinyal Doğrulama (Backtest Proof Engine) (Priority: P1)

**Goal**: Verify trading signals by backtesting last 3 historical occurrences

**Why Critical**: This is the "proof engine" - the core value proposition of the system per constitution.

**Independent Test**: Run `python src/backtester.py` as standalone script with test data and verify JSON output with 3 signals.

### Implementation for User Story 2

#### Subtask Group 1: Core Backtester Structure

- [X] T037 [P] [US2] Create src/backtester.py file with module docstring explaining backtest logic
- [X] T038 [US2] Implement `find_signal_dates(df, condition_str)` function in src/backtester.py to find dates where `df.query(condition_str)` returns True
- [X] T039 [US2] Add validation to `find_signal_dates()` to check if condition_str is valid Pandas query syntax (try/except on df.query())
- [X] T040 [US2] Add logic to `find_signal_dates()` to return last 3 True indices (using `df.index[mask][-3:]`)
- [X] T041 [US2] Add handling for < 3 signals case in `find_signal_dates()` (return all found signals with warning log)

**Verification for T037-T041**: Run `python -c "from src.backtester import find_signal_dates; import pandas as pd; df = pd.DataFrame({'rsi': [20, 35, 25, 40, 28], 'close': [100, 105, 102, 110, 108]}); dates = find_signal_dates(df, 'rsi < 30'); print('✓ Found', len(dates), 'signals'); assert len(dates) <= 3"`.

#### Subtask Group 2: Trade Simulation Logic

- [X] T042 [US2] Implement `simulate_trade(df, entry_idx, stop_loss_pct=0.02, take_profit_pct=0.04)` function in src/backtester.py
- [X] T043 [US2] Add logic to `simulate_trade()` to get entry price from `df.loc[entry_idx, 'close']`
- [X] T044 [US2] Add logic to `simulate_trade()` to calculate stop loss price: `entry_price * (1 - stop_loss_pct)`
- [X] T045 [US2] Add logic to `simulate_trade()` to calculate take profit price: `entry_price * (1 + take_profit_pct)`
- [X] T046 [US2] Add forward iteration logic to `simulate_trade()` to scan bars after entry_idx checking if low <= stop_loss or high >= take_profit
- [X] T047 [US2] Add early exit logic to `simulate_trade()` for insufficient future data (return {"result": "Open", "pnl_percent": 0.0, "duration_bars": 0})
- [X] T048 [US2] Add result packaging to `simulate_trade()` returning dict with keys: result ("TP"/"SL"/"Open"), pnl_percent (float), duration_bars (int)

**Verification for T042-T048**: Run `python -c "from src.backtester import simulate_trade; import pandas as pd; import numpy as np; df = pd.DataFrame({'close': [100, 105, 110, 95, 90], 'high': [102, 107, 112, 97, 92], 'low': [98, 103, 108, 93, 88]}); result = simulate_trade(df, 0, stop_loss_pct=0.05, take_profit_pct=0.10); print('✓ Trade result:', result); assert result['result'] in ['TP', 'SL', 'Open']"`.

#### Subtask Group 3: Main Backtest Function

- [X] T049 [US2] Implement `backtest_strategy(df, condition_str, stop_loss_pct=0.02, take_profit_pct=0.04)` function in src/backtester.py
- [X] T050 [US2] Add call to `find_signal_dates(df, condition_str)` in `backtest_strategy()` to get list of signal indices
- [X] T051 [US2] Add loop in `backtest_strategy()` to call `simulate_trade()` for each signal date
- [X] T052 [US2] Add result aggregation in `backtest_strategy()` to build list of dicts matching backtest-schema.json format
- [X] T053 [US2] Add JSON serialization to `backtest_strategy()` with date formatting (ISO-8601 strings)
- [X] T054 [US2] Add error handling to `backtest_strategy()` for empty DataFrame or invalid condition_str (return empty list with error log)

**Verification for T049-T054**: Run `python -c "from src.backtester import backtest_strategy; from src.data_loader import fetch_crypto_data; from src.analysis import calculate_indicators; df = fetch_crypto_data('BTC/USDT', days=30); df = calculate_indicators(df); results = backtest_strategy(df, 'rsi < 30', stop_loss_pct=0.02, take_profit_pct=0.04); import json; print('✓ Backtest results:', json.dumps(results, indent=2))"`.

#### Subtask Group 4: Standalone Testing

- [X] T055 [US2] Add `if __name__ == '__main__':` block to src/backtester.py with example usage
- [X] T056 [US2] Add command-line argument parsing to backtester.py for --symbol, --condition, --days parameters using argparse
- [X] T057 [US2] Add full pipeline test in __main__ block: fetch data → calculate indicators → run backtest → print JSON results

**Verification for T055-T057**: Run `python src/backtester.py --symbol BTC/USDT --condition "rsi < 30" --days 90` and verify JSON output with signal_date, result, pnl_percent keys.

**Checkpoint**: At this point, the backtest engine is fully functional and can verify any strategy signal

---

## Phase 6: User Story 5 - Kural Seti Yönetimi (Priority: P3)

**Goal**: Parse and load strategy rules from specs/ directory

**Independent Test**: Run `python -c "from src.strategy_loader import load_strategies; strategies = load_strategies(); print(strategies); assert len(strategies) > 0"`.

### Implementation for User Story 5

- [X] T058 [P] [US5] Create src/strategy_loader.py file with module docstring
- [X] T059 [US5] Implement `load_strategies()` function in src/strategy_loader.py to read specs/04_strategies.md file
- [X] T060 [US5] Add Markdown parsing logic to `load_strategies()` to extract strategy blocks (name, type, condition, params)
- [X] T061 [US5] Add JSON/YAML parsing alternative if strategies are defined in structured format within specs/04_strategies.md
- [X] T062 [US5] Add validation to `load_strategies()` to check condition strings are valid (test with empty DataFrame.query())
- [X] T063 [US5] Add return format to `load_strategies()` as list of dicts: `[{"name": str, "type": str, "condition": str, "params": dict}]`
- [X] T064 [US5] Add error handling to `load_strategies()` for missing file or parse errors (return empty list with error log)

**Verification for T058-T064**: Run `python -c "from src.strategy_loader import load_strategies; strategies = load_strategies(); print('✓ Loaded', len(strategies), 'strategies'); print(strategies[0] if strategies else 'No strategies found')"`.

**Checkpoint**: Strategy rules can be loaded from configuration files

---

## Phase 7: User Story 1 - Piyasa Taraması ve Rapor Üretimi (Priority: P1) 🎯 MVP

**Goal**: Main CLI tool that orchestrates data collection, analysis, signal scanning, backtest verification, and report generation

**Why MVP**: This is the user-facing entry point that delivers end-to-end value.

**Independent Test**: Run `python tools/market_scanner.py` and verify `output/market_snapshot.md` is created with valid Markdown content.

### Implementation for User Story 1

#### Subtask Group 1: Market Scanner Structure

- [X] T065 [P] [US1] Create tools/market_scanner.py file with module docstring and CLI description
- [X] T066 [US1] Add import statements to tools/market_scanner.py for all src modules (data_loader, analysis, backtester, strategy_loader, utils)
- [X] T067 [US1] Implement `main()` function in tools/market_scanner.py with high-level workflow steps as comments
- [X] T068 [US1] Add setup_logging() call at start of `main()` function

#### Subtask Group 2: Data Collection Step

- [X] T069 [US1] Add crypto data collection loop to `main()` in tools/market_scanner.py for symbols from specs/03_data_sources.md (BTC/USDT, ETH/USDT, SOL/USDT, BNB/USDT, XRP/USDT)
- [X] T070 [US1] Add macro data collection loop to `main()` in tools/market_scanner.py for symbols GC=F, DX-Y.NYB, ^GSPC
- [X] T071 [US1] Add RSS feed collection to `main()` in tools/market_scanner.py with sentiment calculation
- [X] T072 [US1] Add progress logging after each data fetch (e.g., "✓ Fetched BTC/USDT data")
- [X] T073 [US1] Add error recovery logic to continue scanning even if one symbol fails (log error and skip)

**Verification for T065-T073**: Run `python tools/market_scanner.py` and verify console logs show data fetching progress. Interrupt before completion to test partial execution.

#### Subtask Group 3: Analysis Step

- [X] T074 [US1] Add technical indicator calculation loop to `main()` in tools/market_scanner.py calling `calculate_indicators()` for each crypto DataFrame
- [X] T075 [US1] Add macro data merging to `main()` in tools/market_scanner.py calling `merge_macro_data()` for each crypto DataFrame
- [X] T076 [US1] Add validation step after analysis to check for NaN values in critical columns (rsi, ema_200) and log warnings
- [X] T077 [US1] Add progress logging after analysis (e.g., "✓ Calculated indicators for BTC/USDT")

**Verification for T074-T077**: Add `breakpoint()` after analysis step and inspect DataFrames to ensure all indicator columns are present.

#### Subtask Group 4: Signal Scanning Step

- [X] T078 [US1] Add strategy loading to `main()` in tools/market_scanner.py calling `load_strategies()`
- [X] T079 [US1] Add nested loop to `main()` to scan each strategy against each crypto DataFrame
- [X] T080 [US1] Add signal detection logic using `df.query(strategy['condition'])` to check if current row matches strategy condition
- [X] T081 [US1] Add signal collection to list when detected: `{"asset": symbol, "strategy": name, "timestamp": current_date, "entry_price": close}`
- [X] T082 [US1] Add progress logging for each strategy scan (e.g., "↻ Scanning Trend Pullback on BTC/USDT")

**Verification for T078-T082**: Add debug print of `found_signals` list and verify format matches expected structure.

#### Subtask Group 5: Backtest Verification Step

- [X] T083 [US1] Add backtest loop to `main()` in tools/market_scanner.py for each found signal
- [X] T084 [US1] Add call to `backtest_strategy()` for each signal with strategy condition and parameters
- [X] T085 [US1] Add backtest results attachment to signal dict: `signal['proof'] = backtest_results`
- [X] T086 [US1] Add error handling for backtest failures (log error and mark signal proof as "N/A")
- [X] T087 [US1] Add progress logging for backtest completion (e.g., "✓ Verified BTC/USDT Trend Pullback: 2/3 wins")

**Verification for T083-T087**: Add debug print of signals with proof data and verify backtest results are attached.

#### Subtask Group 6: Report Generation Step

- [X] T088 [US1] Implement `generate_markdown_report(signals, sentiment_score, timestamp)` function in tools/market_scanner.py
- [X] T089 [US1] Add Markdown header generation to `generate_markdown_report()`: title, generation timestamp, sentiment score
- [X] T090 [US1] Add loop in `generate_markdown_report()` to create a section for each signal with asset, strategy, entry price
- [X] T091 [US1] Add backtest proof section to each signal with table of last 3 signals (date, result, PnL%)
- [X] T092 [US1] Add summary section to report with total signals found, overall win rate from backtests
- [X] T093 [US1] Add "No Signals Found" section if signals list is empty
- [X] T094 [US1] Add file writing logic to save report to `output/market_snapshot.md`
- [X] T095 [US1] Add call to `generate_markdown_report()` in `main()` function

**Verification for T088-T095**: Run `python tools/market_scanner.py` and open `output/market_snapshot.md` in text editor. Verify Markdown formatting is correct and contains signal data.

#### Subtask Group 7: Error Handling & Finalization

- [X] T096 [US1] Add try-except wrapper around entire `main()` function to catch unexpected errors
- [X] T097 [US1] Add final logging message on success: "✓ Market scan complete. Report saved to output/market_snapshot.md"
- [X] T098 [US1] Add execution time tracking (start/end timestamps) and log total duration
- [X] T099 [US1] Add `if __name__ == '__main__':` block calling `main()`
- [X] T100 [US1] Add command-line argument parsing for optional flags: --symbols, --strategies, --output-path (using argparse)

**Verification for T096-T100**: Run `python tools/market_scanner.py` and verify:
1. Script completes without errors
2. Execution time is logged
3. Report file exists at `output/market_snapshot.md`
4. Report contains valid Markdown with signal data and backtest proofs

**Full End-to-End Verification**: 
```bash
python tools/market_scanner.py
# Expected output:
# ✓ Fetched BTC/USDT data
# ✓ Fetched ETH/USDT data
# ... (more data fetches)
# ✓ Calculated indicators for BTC/USDT
# ↻ Scanning Trend Pullback on BTC/USDT
# ✓ Verified BTC/USDT Trend Pullback: 2/3 wins
# ✓ Market scan complete. Report saved to output/market_snapshot.md (45.2s)

# Then verify report file:
type output\market_snapshot.md  # Windows
```

**Checkpoint**: At this point, the entire system is functional end-to-end. User can run one command and get a complete market analysis report with verified signals.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T101 [P] Add comprehensive docstrings to all functions in src/data_loader.py (Google style)
- [ ] T102 [P] Add comprehensive docstrings to all functions in src/analysis.py (Google style)
- [ ] T103 [P] Add comprehensive docstrings to all functions in src/backtester.py (Google style)
- [ ] T104 [P] Add comprehensive docstrings to all functions in src/strategy_loader.py (Google style)
- [ ] T105 [P] Add comprehensive docstrings to all functions in tools/market_scanner.py (Google style)
- [ ] T106 Add README.md to project root with installation instructions, usage examples, and project structure
- [ ] T107 Add example strategy definitions to specs/04_strategies.md with proper Pandas query format
- [ ] T108 Add example data source list to specs/03_data_sources.md with current symbols
- [ ] T109 Add performance optimization: cache fetched data for 5 minutes to avoid repeated API calls during development
- [ ] T110 Add rate limiting logic to data_loader.py to respect API limits (sleep between requests)
- [ ] T111 Validate all tasks by running through quickstart.md scenarios
- [ ] T112 Test edge case: run scanner with no internet connection and verify graceful degradation
- [ ] T113 Test edge case: run scanner with symbol that has < 200 days of data and verify EMA200 warning
- [ ] T114 Test edge case: run scanner when no strategies match and verify "No Signals Found" report

**Verification for T101-T105**: Run `python -c "import src.data_loader; help(src.data_loader.fetch_crypto_data)"` and verify docstring is displayed.

**Verification for T111-T114**: Follow each test scenario from quickstart.md and verify expected behavior.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
  - Creates directory structure and configuration files
  
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
  - Creates utility functions needed by all modules
  
- **User Story 4 (Phase 3)**: Depends on Foundational phase - Must complete before other user stories
  - Data collection is prerequisite for all analysis and backtest operations
  
- **User Story 3 (Phase 4)**: Depends on User Story 4
  - Analysis requires data from data_loader
  
- **User Story 2 (Phase 5)**: Depends on User Story 4 and User Story 3
  - Backtester requires data fetching and indicator calculation
  
- **User Story 5 (Phase 6)**: Depends on Foundational phase only - Can run in parallel with Phases 3-5
  - Strategy loading is independent of data operations
  
- **User Story 1 (Phase 7)**: Depends on ALL previous user stories
  - Market scanner orchestrates all components
  
- **Polish (Phase 8)**: Depends on Phase 7 completion
  - Documentation and optimization after core functionality is complete

### User Story Dependencies

```
Setup (Phase 1)
    ↓
Foundational (Phase 2)
    ↓
    ├─→ User Story 4: Data Collection (Phase 3) [BLOCKING]
    │       ↓
    │   User Story 3: Technical Analysis (Phase 4)
    │       ↓
    │   User Story 2: Backtest Engine (Phase 5)
    │       ↓
    ├─→ User Story 5: Strategy Loader (Phase 6) [PARALLEL]
    │       ↓
    └─→ User Story 1: Market Scanner (Phase 7) [MVP COMPLETE]
            ↓
        Polish (Phase 8)
```

### Within Each User Story

**User Story 4 (Data Collection)**:
- T013 (file creation) → T014-T016 (crypto) || T017-T019 (macro) || T020-T023 (sentiment) [all parallel after file exists]

**User Story 3 (Technical Analysis)**:
- T024 (file creation) → T025 (function skeleton) → T026-T031 (indicators, all depend on T025) → T032 (error handling) || T033-T036 (macro merge, parallel)

**User Story 2 (Backtest Engine)**:
- Subtask Group 1 (T037-T041) → Subtask Group 2 (T042-T048) [parallel if different function]
- Subtask Group 3 (T049-T054) depends on Groups 1 & 2
- Subtask Group 4 (T055-T057) depends on Group 3

**User Story 5 (Strategy Loader)**:
- Sequential: T058 → T059 → T060 → T061 → T062 → T063 → T064

**User Story 1 (Market Scanner)**:
- Subtask Groups 1-7 are mostly sequential due to workflow dependencies
- Within each group, some tasks can be parallel (e.g., T069-T070 both fetch data)

### Parallel Opportunities

**Within Setup Phase**:
```bash
# All T003-T009 can run in parallel (different files)
Task: T003 Create src/__init__.py
Task: T004 Create tools/__init__.py  
Task: T005 Create output/.gitkeep
Task: T006 Create specs/01_mission.md
Task: T007 Create specs/02_risk_rules.md
Task: T008 Create specs/03_data_sources.md
```

**Within Foundational Phase**:
```bash
# T010, T011, T012 all edit same file, must be sequential
```

**Within User Story 4**:
```bash
# After T013 completes, these can run in parallel (different functions):
Task: T014-T016 Implement fetch_crypto_data with error handling
Task: T017-T019 Implement fetch_macro_data with error handling
Task: T020-T023 Implement RSS sentiment analysis
```

**Within User Story 3**:
```bash
# T026-T031 can partially parallel if implemented as separate function calls:
Task: T026 Add RSI calculation
Task: T027 Add EMA200 calculation
Task: T028 Add ATR calculation
Task: T029 Add Bollinger Bands
Task: T030 Add ADX calculation
```

**Within Polish Phase**:
```bash
# T101-T105 can all run in parallel (different files):
Task: T101 Docstrings for data_loader.py
Task: T102 Docstrings for analysis.py
Task: T103 Docstrings for backtester.py
Task: T104 Docstrings for strategy_loader.py
Task: T105 Docstrings for market_scanner.py
```

---

## Parallel Example: User Story 4 (Data Collection)

After completing T013 (file creation), launch these in parallel:

```bash
# Crypto data fetcher (T014-T016):
Task: "Implement fetch_crypto_data(symbol, days) using ccxt in src/data_loader.py"
Task: "Add column standardization and error handling to fetch_crypto_data"

# Macro data fetcher (T017-T019):  
Task: "Implement fetch_macro_data(symbol, days) using yfinance in src/data_loader.py"
Task: "Add column standardization and error handling to fetch_macro_data"

# Sentiment analyzer (T020-T023):
Task: "Implement fetch_rss_headlines() and calculate_sentiment() in src/data_loader.py"
Task: "Add error handling for RSS feeds and empty headlines"
```

---

## Implementation Strategy

### MVP First (Minimum Viable Product)

**Goal**: Get end-to-end system working as fast as possible

**Order**:
1. ✅ Complete Phase 1: Setup (T001-T009) - ~30 minutes
2. ✅ Complete Phase 2: Foundational (T010-T012) - ~20 minutes
3. ✅ Complete Phase 3: User Story 4 (T013-T023) - ~2 hours
4. ✅ Complete Phase 4: User Story 3 (T024-T036) - ~2 hours  
5. ✅ Complete Phase 6: User Story 5 (T058-T064) - ~1 hour [parallel with below]
6. ✅ Complete Phase 5: User Story 2 (T037-T057) - ~3 hours
7. ✅ Complete Phase 7: User Story 1 (T065-T100) - ~3 hours
8. ✅ **VALIDATE MVP**: Run `python tools/market_scanner.py` and verify complete report

**Total MVP Time Estimate**: ~11-12 hours of focused development

**At this point, you have a working system that delivers the core value proposition.**

### Incremental Delivery

Each user story adds value independently:

1. **After Phase 3**: You can fetch all market data manually
2. **After Phase 4**: You can calculate indicators on fetched data
3. **After Phase 5**: You can backtest any strategy condition
4. **After Phase 6**: You can load strategy definitions from files
5. **After Phase 7**: You can run complete market scan with one command ✨

### Testing Strategy

**Unit Level (Per Task)**:
- Each task has a verification step
- Run verification immediately after completing the task
- Don't move to next task until verification passes

**Integration Level (Per Phase)**:
- Each phase has a checkpoint verification
- Test full phase functionality before moving to next phase

**System Level (End of MVP)**:
- Full end-to-end test with real API calls
- Verify report generation
- Test edge cases (no internet, no signals, insufficient data)

### Recommended Implementation Order for Solo Developer

**Day 1 (4 hours)**:
- Morning: T001-T036 (Setup through Technical Analysis)
- Afternoon: T058-T064 (Strategy Loader)

**Day 2 (4 hours)**:
- Morning: T037-T057 (Backtest Engine - most complex module)
- Afternoon: T065-T083 (Market Scanner through Signal Scanning)

**Day 3 (3 hours)**:
- Morning: T084-T100 (Complete Market Scanner)
- Afternoon: T101-T114 (Polish and Testing)

---

## Notes

- **[P] marker**: Tasks that can run in parallel (different files or independent functions)
- **[Story] marker**: Maps each task to its user story for traceability (US1-US5)
- **Atomic tasks**: Each task is small enough to complete in < 30 minutes
- **Verification steps**: Every task or task group includes a concrete test command
- **Complex module breakdown**: 
  - `backtester.py` broken into 4 subtask groups (21 atomic tasks)
  - `market_scanner.py` broken into 7 subtask groups (36 atomic tasks)
- **Error handling**: Each module includes explicit error handling tasks
- **Column standardization**: Critical requirement (FR-016a) enforced in multiple tasks
- **Constitution alignment**: Backtest engine (US2) prioritized as "Kanıtlanabilir Sinyal" requirement

---

## Risk Mitigation

**High Risk Areas**:
1. **Column name mismatches**: Mitigated by strict standardization in T010, T015, T018, T031
2. **API rate limits**: Mitigated by error handling in T016, T019, T110
3. **Insufficient historical data**: Mitigated by validation in T032, T041, T054
4. **Complex backtest logic**: Mitigated by breaking into 4 subtask groups with individual verification

**Testing Coverage**:
- Each phase has independent test criteria
- Each task has verification command
- Edge cases explicitly tested in Phase 8 (T112-T114)
- Quickstart scenarios validate full workflow (T111)

---

**Total Tasks**: 114 atomic tasks
**Estimated Completion Time**: 11-14 hours (solo developer)
**Parallelization Potential**: ~40% of tasks can run in parallel with proper tooling
**Critical Path**: Setup → Foundational → Data Collection → Analysis → Backtest → Market Scanner

---

*Generated by speckit.tasks on 2026-01-19*
