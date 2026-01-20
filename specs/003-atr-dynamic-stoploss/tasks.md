# Tasks: ATR Dynamic Stop Loss

**Branch**: `003-atr-dynamic-stoploss` | **Date**: 2026-01-20
**Input**: Design documents from `/specs/003-atr-dynamic-stoploss/`
**Prerequisites**: plan.md, spec.md, data-model.md, contracts/risk-level-schema.json

**Tests**: Not explicitly requested in spec - focusing on implementation and integration testing via backtesting

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and validation of existing structure

- [X] T001 Verify ATR calculation exists in src/analysis.py (already implemented)
- [X] T002 Review existing simulate_trade function in src/backtester.py

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core risk calculation infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T003 Implement calculate_risk_levels function in src/analysis.py
- [X] T004 Add input validation for calculate_risk_levels (entry_price > 0, atr >= 0, side in ['long', 'short'])
- [X] T005 Implement minimum stop-loss constraint (1%) in calculate_risk_levels
- [X] T006 Implement maximum stop-loss constraint (5%) with VOLATILITY_TOO_HIGH status
- [X] T007 Implement R:R ratio calculation in calculate_risk_levels
- [X] T008 Implement LOW_RR status flag when R:R < 2.0
- [X] T009 Add logging for risk calculation edge cases in src/analysis.py

**Checkpoint**: Foundation ready - calculate_risk_levels returns valid risk levels per schema

---

## Phase 3: User Story 1 - Volatiliteye Duyarlı Stop-Loss (Priority: P1) 🎯 MVP

**Goal**: Enable dynamic stop-loss calculation based on ATR for each signal

**Independent Test**: Generate a signal and verify stop-loss is calculated using ATR × multiplier instead of fixed percentage

### Implementation for User Story 1

- [X] T010 [US1] Refactor simulate_trade in src/backtester.py to accept stop_loss_price parameter
- [X] T011 [US1] Refactor simulate_trade in src/backtester.py to accept take_profit_price parameter
- [X] T012 [US1] Maintain backward compatibility in simulate_trade (keep stop_loss_pct and take_profit_pct as fallback)
- [X] T013 [US1] Update simulate_trade logic to use absolute prices when provided in src/backtester.py
- [X] T014 [US1] Integrate calculate_risk_levels into signal generation workflow in tools/market_scanner.py
- [X] T015 [US1] Update signal output format to display ATR value, multiplier, and calculated stop/TP levels in tools/market_scanner.py
- [X] T016 [US1] Handle VOLATILITY_TOO_HIGH status by skipping signal generation in tools/market_scanner.py
- [X] T017 [US1] Add validation that all signals include dynamic stop-loss and take-profit prices

**Checkpoint**: market_scanner.py generates signals with dynamic ATR-based stop-loss levels

---

## Phase 4: User Story 2 - R:R Oranı Koruması (Priority: P1)

**Goal**: Ensure minimum 2:1 Risk/Reward ratio is maintained for all signals

**Independent Test**: Generate signals with varying volatility and verify R:R ratio is calculated and displayed; signals with R:R < 2.0 show warning

### Implementation for User Story 2

- [X] T018 [US2] Add R:R ratio display to signal output format in tools/market_scanner.py
- [X] T019 [US2] Implement LOW_RR warning flag display in signal output ("⚠️ Low R:R") in tools/market_scanner.py
- [X] T020 [US2] Update calculate_risk_levels to auto-adjust TP to maintain min_rr when possible in src/analysis.py
- [X] T021 [US2] Add R:R validation to signal generation workflow in tools/market_scanner.py
- [X] T022 [US2] Update market snapshot report format to include R:R ratio column in output/market_snapshot.md

**Checkpoint**: All signals display R:R ratio; Low R:R warnings shown when R:R < 2.0

---

## Phase 5: User Story 3 - ATR Çarpanı Yapılandırması (Priority: P2)

**Goal**: Enable configuration of ATR multiplier per strategy

**Independent Test**: Run backtest with different ATR multipliers (1.0, 1.5, 2.0) and verify results differ

### Implementation for User Story 3

- [X] T023 [P] [US3] Add atr_multiplier parameter to strategy configuration schema in specs/04_strategies.md
- [X] T024 [US3] Update strategy_loader.py to read atr_multiplier from strategy definitions in src/strategy_loader.py
- [X] T025 [US3] Pass atr_multiplier from strategy config to calculate_risk_levels in signal generation
- [ ] T026 [US3] Add --atr-multiplier CLI argument to tools/market_scanner.py
- [ ] T027 [US3] Add --atr-multiplier CLI argument to tools/backtest_signals.py
- [X] T028 [US3] Update strategy examples in specs/04_strategies.md with atr_multiplier values

**Checkpoint**: Different strategies can use different ATR multipliers; CLI override works

---

## Phase 6: User Story 4 - Backtest Uyumluluğu (Priority: P2)

**Goal**: Integrate dynamic stop-loss into backtesting engine

**Independent Test**: Run same strategy with fixed vs dynamic stop and verify different outcomes

### Implementation for User Story 4

- [X] T029 [US4] Update backtest_strategy function to use calculate_risk_levels before each trade in src/backtester.py
- [X] T030 [US4] Pass dynamic stop_loss_price and take_profit_price to simulate_trade in src/backtester.py
- [X] T031 [US4] Store ATR value and multiplier used in backtest results in src/backtester.py
- [X] T032 [US4] Add dynamic vs static stop comparison to backtest summary output in src/backtester.py
- [X] T033 [US4] Update backtest result JSON to include risk parameters per trade in src/backtester.py
- [ ] T034 [US4] Test backtest with high volatility period and verify reduced stop-outs in tools/backtest_signals.py

**Checkpoint**: Backtest engine fully supports dynamic stop-loss; results show ATR-based risk management

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T035 [P] Update quickstart.md with actual CLI examples and usage patterns
- [ ] T036 [P] Add comprehensive logging for risk calculation decisions in src/analysis.py
- [ ] T037 Document edge case handling (ATR=0, missing data, extreme volatility) in specs/003-atr-dynamic-stoploss/
- [ ] T038 Run end-to-end validation per quickstart.md
- [ ] T039 Update progress.md with feature completion status
- [ ] T040 Code review and refactoring for consistency across src/analysis.py and src/backtester.py

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - validation only
- **Foundational (Phase 2)**: Depends on Setup - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational - Core dynamic stop implementation
- **User Story 2 (Phase 4)**: Depends on User Story 1 - Builds on dynamic stop with R:R enforcement
- **User Story 3 (Phase 5)**: Depends on User Story 1 - Adds configuration flexibility
- **User Story 4 (Phase 6)**: Depends on User Story 1 - Integrates into backtest engine
- **Polish (Phase 7)**: Depends on all user stories

### User Story Dependencies

- **User Story 1 (P1)**: MUST complete first - foundation for all other stories
- **User Story 2 (P1)**: Can start immediately after US1 - enhances risk validation
- **User Story 3 (P2)**: Can start after US1 - adds configurability
- **User Story 4 (P2)**: Can start after US1 - adds backtest integration
- **US3 and US4 can proceed in parallel** once US1 is complete

### Within Each User Story

- Foundational phase tasks must be sequential (T003-T009) to build complete calculate_risk_levels
- US1: simulate_trade refactor (T010-T013) before integration (T014-T017)
- US2: Display logic (T018-T019) before auto-adjustment (T020-T022)
- US3: Schema update (T023) before implementation (T024-T028)
- US4: Function updates (T029-T031) before testing (T032-T034)

### Parallel Opportunities

Within phases, tasks marked [P] can run in parallel:
- Phase 1: T001 and T002 can be reviewed in parallel
- Phase 5: T023 (schema) and T028 (examples) can be done in parallel
- Phase 7: T035, T036, T037 can all be done in parallel

Once User Story 1 completes:
- User Story 3 and User Story 4 can be worked on in parallel by different team members
- User Story 2 should complete before US3/US4 to ensure R:R validation is in place

---

## Implementation Strategy

### MVP Scope (Minimum Viable Product)

**Deliver First**: User Story 1 only
- Dynamic stop-loss calculation based on ATR
- Basic signal generation with ATR-based levels
- This provides immediate value: volatility-aware risk management

**Then**: User Story 2 (P1)
- Ensures quality of signals with R:R validation

**Then**: User Stories 3 & 4 in parallel (P2)
- Configurability and backtest integration

### Suggested Execution Sequence

1. **Week 1**: Phases 1-2 (Setup + Foundational) - Build calculate_risk_levels
2. **Week 2**: Phase 3 (User Story 1) - Dynamic stop in market scanner
3. **Week 3**: Phase 4 (User Story 2) - R:R protection
4. **Week 4**: Phases 5-6 (User Stories 3 & 4 in parallel) - Config + Backtest
5. **Week 5**: Phase 7 (Polish) - Documentation and validation

### Test Validation Points

- After Phase 2: Verify calculate_risk_levels with sample data (ATR=2500, entry=50000)
- After Phase 3: Generate real BTC/USDT signal and verify dynamic stop calculation
- After Phase 4: Verify all signals display R:R and appropriate warnings
- After Phase 5: Run backtest with multiplier=1.0 vs 1.5 and compare
- After Phase 6: Backtest volatile period (e.g., May 2021) and verify reduced stop-outs vs fixed 2%
- After Phase 7: Complete quickstart.md validation end-to-end

---

## Summary

- **Total Tasks**: 40
- **User Story 1 (MVP)**: 8 implementation tasks
- **User Story 2**: 5 enhancement tasks
- **User Story 3**: 6 configuration tasks
- **User Story 4**: 6 backtest integration tasks
- **Foundational**: 7 critical tasks (blocking)
- **Polish**: 6 final tasks

**Parallel Opportunities**:
- Within Foundational: Sequential dependencies
- After US1: US3 and US4 can proceed in parallel
- Polish phase: Most tasks can run in parallel

**Independent Test Criteria**:
- US1: Signal with dynamic ATR-based stop displayed
- US2: R:R ratio calculated and displayed with warnings
- US3: Different multipliers produce different stop levels
- US4: Backtest results differ between fixed and dynamic stop

**MVP Delivery**: Phases 1-3 deliver core value (volatility-aware stop-loss)
