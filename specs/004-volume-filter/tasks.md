# Implementation Tasks: Volume Filter

**Feature**: Volume Filter - Düşük Hacimde İşlem Engelleme  
**Branch**: `004-volume-filter`  
**Spec**: [spec.md](spec.md) | **Plan**: [plan.md](plan.md)

## Overview

This document breaks down the Volume Filter implementation into executable, independently testable tasks organized by user story priority.

## Implementation Strategy

**MVP First Approach**: Focus on User Story 1 (P1) for the minimum viable product, then incrementally add remaining features. Each user story represents a complete, independently testable increment.

**Suggested MVP Scope**: User Story 1 only - basic volume filtering with default thresholds.

## Phase 1: Setup

**Goal**: Initialize project structure and dependencies.

- [ ] T001 Verify project dependencies (pandas, ccxt, pandas-ta) are installed per requirements.txt
- [ ] T002 Validate existing test infrastructure works (run existing tools to establish baseline)

## Phase 2: Foundational

**Goal**: Core volume calculation infrastructure (blocks all user stories).

- [ ] T003 Add volume_sma_20 calculation in src/analysis.py calculate_indicators function
- [ ] T004 Handle edge cases for volume SMA (NaN at start, insufficient data < 20 bars)
- [ ] T005 Add logging for volume calculation (info level when computed, warning if insufficient data)

## Phase 3: User Story 1 - Düşük Hacimli Sinyalleri Filtreleme (P1)

**Goal**: Filter low-volume signals to prevent fake breakouts.

**Independent Test**: Run market scanner with BTC/USDT on a known low-volume period - signal should be flagged "Low Volume".

### Signal Scanning Enhancement

- [ ] T006 [US1] Extract volume data from completed candle (iloc[-2]) in tools/market_scanner.py scan loop
- [ ] T007 [US1] Calculate volume_ratio = current_volume / volume_sma_20 in tools/market_scanner.py
- [ ] T008 [US1] Apply default threshold check (0.5) and tag signal with volume_status field
- [ ] T009 [US1] Add volume_metrics dictionary to signal object (current_volume, avg_volume_20d, volume_ratio, volume_status)

### Reporting

- [ ] T010 [P] [US1] Update generate_markdown_report in tools/market_scanner.py to include Volume Status column
- [ ] T011 [P] [US1] Add "Low Volume ⚠️" badge styling for filtered signals in report
- [ ] T012 [P] [US1] Display volume ratio percentage in report (e.g., "45% of Avg")

## Phase 4: User Story 2 - Volume Spike Teyidi (P1)

**Goal**: Confirm breakout signals with volume spike detection.

**Independent Test**: Simulate or find a breakout signal with volume > 1.5x average - should show "Volume Confirmed ✓".

- [ ] T013 [P] [US2] Add HIGH volume status detection (ratio > 1.5) in tools/market_scanner.py
- [ ] T014 [P] [US2] Add "Volume Confirmed ✓" badge for HIGH status signals in report
- [ ] T015 [US2] Add logic to detect "Weak Volume" for breakout signals (volume < avg) in tools/market_scanner.py

## Phase 5: User Story 3 - Strateji Bazında Volume Eşiği (P2)

**Goal**: Support custom volume thresholds per strategy.

**Independent Test**: Load a strategy with volume_threshold=1.5, another with 0.8 - verify different thresholds applied correctly.

### Strategy Loading

- [ ] T016 [US3] Update regex pattern in src/strategy_loader.py to capture optional Volume Threshold parameter
- [ ] T017 [US3] Add volume_threshold to strategy params dict with default 0.5 if not specified
- [ ] T018 [US3] Add test logging to confirm volume_threshold parsed correctly

### Integration

- [ ] T019 [US3] Update market_scanner.py to use strategy-specific volume_threshold instead of hardcoded 0.5
- [ ] T020 [P] [US3] Update specs/04_strategies.md to add Volume Threshold parameter to Breakout strategies (set to 1.5)

## Phase 6: User Story 4 - Volume Raporu (P3)

**Goal**: Display volume status for all scanned assets in report.

**Independent Test**: Run scanner on multiple assets - report should show volume metrics for all.

- [ ] T021 [P] [US4] Add Volume Summary section to markdown report showing volume status for all scanned assets
- [ ] T022 [P] [US4] Display "Volume vs Avg" percentage for each asset in summary table

## Phase 7: Backtest Integration

**Goal**: Ensure backtester respects volume filter for historical proof.

**Independent Test**: Run backtest on a strategy with volume filter - should show fewer historical signals (filtered out low-volume ones).

- [ ] T023 [P] Add volume validation in src/backtester.py find_signal_dates function
- [ ] T024 Filter signal indices by volume check (use iloc[i] for completed historical candle)
- [ ] T025 Add logging to show how many signals were filtered by volume check
- [ ] T026 Update backtest_strategy to accept and pass volume_threshold parameter

## Phase 8: Polish & Cross-Cutting

**Goal**: Edge cases, error handling, and documentation.

- [ ] T027 [P] Add error handling for missing volume data in src/analysis.py
- [ ] T028 [P] Add warning log when asset has < 20 bars of data (can't calculate full SMA)
- [ ] T029 Test market scanner end-to-end with volume filter enabled
- [ ] T030 Verify performance impact is < 5% (SC-004) by comparing scan times before/after
- [ ] T031 Update PROJECT_BLUEPRINT.md or progress.md to mark 004-volume-filter as implemented

## Dependencies

### Story Completion Order

```
Phase 1 (Setup) 
  ↓
Phase 2 (Foundational) 
  ↓
Phase 3 (US1 - P1) ────→ MVP Release Point
  ↓
Phase 4 (US2 - P1) ────→ Can be parallel with Phase 5
  ↓
Phase 5 (US3 - P2) ────→ Can be parallel with Phase 4
  ↓
Phase 6 (US4 - P3)
  ↓
Phase 7 (Backtest)
  ↓
Phase 8 (Polish)
```

### Blocking Relationships

- **Phase 2 blocks all user stories**: volume_sma_20 must exist before any filtering logic.
- **Phase 3 blocks Phase 7**: Backtest integration requires understanding of scanning logic.
- **Phase 5 blocks Phase 7 completion**: Backtest must respect strategy-specific thresholds.
- **User Story 2 and 3 are independent**: Can be developed in parallel after US1.

## Parallel Execution Opportunities

### After Phase 2 (Foundational) completes:

**Parallel Group 1 - Core P1 Stories**:
- Work on Phase 3 (US1 Scanning) while simultaneously working on Phase 4 (US2 Volume Spike) reporting components

**Parallel Group 2 - P2 + Reporting**:
- Phase 5 (US3 Strategy Config) can proceed independently of Phase 4
- Phase 6 (US4 Reporting) tasks marked [P] can be done concurrently with other reporting tasks

**Parallel Group 3 - Polish Tasks**:
- Error handling (T027, T028) can be done alongside integration testing

## Task Completion Summary

- **Total Tasks**: 31
- **Setup**: 2 tasks
- **Foundational**: 3 tasks (blocking)
- **User Story 1** (P1): 7 tasks (MVP)
- **User Story 2** (P1): 3 tasks
- **User Story 3** (P2): 5 tasks
- **User Story 4** (P3): 2 tasks
- **Backtest Integration**: 4 tasks
- **Polish**: 5 tasks

## Format Validation

✅ All tasks follow the checklist format: `- [ ] [TaskID] [P?] [Story?] Description with file path`
