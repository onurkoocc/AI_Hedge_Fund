# Tasks: MACD ve Stochastic RSI İndikatörleri

**Input**: Design documents from `/specs/002-macd-stochrsi-indicators/`
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, contracts/ ✅

**Tests**: Not explicitly requested in spec — test tasks NOT included. Validation via manual verification + backtest.

**Organization**: Tasks grouped by user story for independent implementation and testing.

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3)
- Exact file paths included in descriptions

---

## Phase 1: Setup (No Changes Required)

**Purpose**: Project already initialized, dependencies already installed

No setup tasks needed — `ta>=0.11.0` and `pandas>=2.0.0` already in requirements.txt.

**Checkpoint**: ✅ Setup complete — proceed to Foundational.

---

## Phase 2: Foundational (Import Updates)

**Purpose**: Add required imports to analysis.py before indicator implementation

- [ ] T001 Add MACD import from ta.trend in src/analysis.py
- [ ] T002 Add StochRSIIndicator import from ta.momentum in src/analysis.py

**Checkpoint**: Imports ready — user story implementation can begin.

---

## Phase 3: User Story 1 - MACD ile Momentum Teyidi (Priority: P1) 🎯 MVP

**Goal**: Add MACD indicator calculation with crossover detection to calculate_indicators()

**Independent Test**: Run `python tools/market_scanner.py` and verify macd, macd_signal, macd_histogram columns appear with valid values (not all NaN)

### Implementation for User Story 1

- [ ] T003 [US1] Add MACD calculation using ta.trend.MACD class in src/analysis.py (after ADX calculation block)
- [ ] T004 [US1] Add MACD crossover detection (macd_bullish_cross, macd_bearish_cross) using shift() pattern in src/analysis.py
- [ ] T005 [US1] Add INFO logging for MACD crossover events with values in src/analysis.py
- [ ] T006 [US1] Add WARNING logging for insufficient MACD data (<35 rows) in src/analysis.py
- [ ] T007 [US1] Update calculate_indicators() docstring to include new MACD columns in src/analysis.py

**Checkpoint**: MACD indicator fully functional — verify with market_scanner.py

---

## Phase 4: User Story 2 - Stochastic RSI ile Hassas Oversold/Overbought (Priority: P1)

**Goal**: Add StochRSI indicator calculation with zone-based crossover detection

**Independent Test**: Run `python tools/market_scanner.py` and verify stoch_rsi_k, stoch_rsi_d columns appear with values in 0-100 range

### Implementation for User Story 2

- [ ] T008 [US2] Add StochRSI calculation using ta.momentum.StochRSIIndicator in src/analysis.py (after MACD block)
- [ ] T009 [US2] Apply *100 scaling to convert StochRSI from 0-1 to 0-100 range in src/analysis.py
- [ ] T010 [US2] Add StochRSI crossover detection (stoch_rsi_bullish, stoch_rsi_bearish) with zone thresholds in src/analysis.py
- [ ] T011 [US2] Add INFO logging for StochRSI crossover events with K/D values in src/analysis.py
- [ ] T012 [US2] Add WARNING logging for insufficient StochRSI data (<28 rows) in src/analysis.py
- [ ] T013 [US2] Update calculate_indicators() docstring to include new StochRSI columns in src/analysis.py

**Checkpoint**: StochRSI indicator fully functional — verify with market_scanner.py

---

## Phase 5: User Story 3 - Strateji Entegrasyonu (Priority: P2)

**Goal**: Enable new indicators in strategy conditions and market scanner output

**Independent Test**: Run `python tools/market_scanner.py` and verify new indicator values appear in output; run backtest with MACD condition

### Implementation for User Story 3

- [ ] T014 [US3] Update strategy_loader.py to include new indicator columns in test DataFrame for query validation in src/strategy_loader.py
- [ ] T015 [US3] Update market_scanner.py to display MACD and StochRSI values in analysis output in tools/market_scanner.py
- [ ] T016 [US3] Add crossover event messages to market scanner signal output with formatted values in tools/market_scanner.py
- [ ] T017 [US3] Verify backtest system works with new indicator columns by testing a MACD-based condition

**Checkpoint**: Full integration complete — all indicators visible in scanner output and usable in strategies

---

## Phase 6: Polish & Validation

**Purpose**: Final validation and documentation updates

- [ ] T018 [P] Run market_scanner.py on all assets and verify no errors
- [ ] T019 [P] Verify performance: scanner runtime increase <10% (SC-002)
- [ ] T020 [P] Run quickstart.md validation scenarios manually
- [ ] T021 Update output/market_snapshot.md format documentation if needed

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1: Setup ─────────────────────► (already complete)
                                          │
Phase 2: Foundational ◄───────────────────┘
    │
    ├──► Phase 3: User Story 1 (MACD) ──────────► Checkpoint
    │
    ├──► Phase 4: User Story 2 (StochRSI) ──────► Checkpoint  
    │         (can run in parallel with US1 after T001-T002)
    │
    └──► Phase 5: User Story 3 (Integration) ───► Checkpoint
              (depends on US1 and US2 completion)
                                          │
Phase 6: Polish ◄─────────────────────────┘
```

### User Story Dependencies

- **User Story 1 (P1)**: Depends on Foundational (T001-T002) — No dependencies on other stories
- **User Story 2 (P1)**: Depends on Foundational (T001-T002) — Can run in parallel with US1
- **User Story 3 (P2)**: Depends on US1 AND US2 completion — Integration layer

### Within Each User Story

- Core calculation before crossover detection
- Crossover detection before logging
- Logging before docstring updates

### Parallel Opportunities

```bash
# After T001-T002 complete, can run in parallel:
T003-T007 (User Story 1: MACD)  ──┬──► Phase 5
T008-T013 (User Story 2: StochRSI) ─┘

# Phase 6 tasks can all run in parallel:
T018, T019, T020, T021
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete T001-T002 (Foundational)
2. Complete T003-T007 (User Story 1: MACD)
3. **STOP and VALIDATE**: Test with `python tools/market_scanner.py`
4. MACD is usable in strategies at this point

### Full Feature Delivery

1. Complete T001-T002 (Foundational)
2. Complete T003-T013 (User Stories 1 & 2 in parallel)
3. Complete T014-T017 (User Story 3: Integration)
4. Complete T018-T021 (Polish)
5. All indicators fully integrated

---

## Notes

- All implementation in single file: src/analysis.py (US1, US2)
- Integration touches: src/strategy_loader.py, tools/market_scanner.py (US3)
- No new dependencies required — ta library already installed
- Display precision: 4 decimal places for all indicator values
- Commit after each task or logical group
- Test with market_scanner.py after each user story checkpoint
