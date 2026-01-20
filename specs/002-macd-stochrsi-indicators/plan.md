# Implementation Plan: MACD ve Stochastic RSI İndikatörleri

**Branch**: `002-macd-stochrsi-indicators` | **Date**: 2026-01-20 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/002-macd-stochrsi-indicators/spec.md`

## Summary

Add MACD (Moving Average Convergence Divergence) and Stochastic RSI indicators to the existing technical analysis system. These indicators will improve signal quality by detecting momentum changes earlier and providing optional confirmation layers for existing strategies. Key integration point: `src/analysis.py` already uses the `ta` library for RSI, EMA, ATR, Bollinger Bands, and ADX.

## Technical Context

**Language/Version**: Python 3.11+ (existing project uses pandas, ta library)  
**Primary Dependencies**: ta>=0.11.0 (already installed), pandas>=2.0.0 (already installed)  
**Storage**: N/A (in-memory DataFrame operations)  
**Testing**: Manual verification + backtest validation (no formal test framework yet)  
**Target Platform**: Local development / CLI tools  
**Project Type**: Single project (src/ + tools/)  
**Performance Goals**: Market scanner runtime increase <10% (SC-002)  
**Constraints**: Free data sources only (Constitution rule), 180-day OHLCV data available  
**Scale/Scope**: ~10 crypto assets per scan, 5 existing indicators to extend

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Pre-Design Check (2026-01-20)

| Rule | Status | Notes |
|------|--------|-------|
| Vizyon Odaklı Disiplin (7% monthly growth) | ✅ PASS | Feature improves signal quality toward target |
| Spec-Driven Mimari | ✅ PASS | All rules defined in specs/, code only implements |
| Kanıtlanabilir Sinyal Üretimi | ✅ PASS | Backtest validation supported (FR-007) |
| Strateji Uyarlanabilirliği | ✅ PASS | Optional filters preserve strategy flexibility |
| Ücretsiz Veri Kaynağı Zorunluluğu | ✅ PASS | No new data sources needed |
| Risk/Ödül 1:2 minimum | ✅ PASS | Not affected (existing R:R logic unchanged) |
| Mini-backtest kanıtı | ✅ PASS | Backtest system will support new indicators |

**Gate Result**: ✅ PASS — No violations detected. Proceed to Phase 0.

### Post-Design Re-Check (2026-01-20)

| Rule | Status | Notes |
|------|--------|-------|
| Vizyon Odaklı Disiplin | ✅ PASS | Design adds momentum confirmation for better signals |
| Spec-Driven Mimari | ✅ PASS | All indicator parameters defined in spec, code implements |
| Kanıtlanabilir Sinyal Üretimi | ✅ PASS | Crossover events logged, backtest-compatible columns added |
| Strateji Uyarlanabilirliği | ✅ PASS | Boolean columns enable flexible query-based strategy conditions |
| Ücretsiz Veri Kaynağı | ✅ PASS | Uses existing `ta` library, no new dependencies |
| Risk/Ödül 1:2 minimum | ✅ PASS | Indicator design unchanged from spec |
| Mini-backtest kanıtı | ✅ PASS | New columns work with existing backtest system |

**Post-Design Gate Result**: ✅ PASS — Design complies with all Constitution rules.

## Project Structure

### Documentation (this feature)

```text
specs/002-macd-stochrsi-indicators/
├── plan.md              # This file
├── spec.md              # Feature specification
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (backtest schema extension)
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
src/
├── __init__.py
├── analysis.py          # PRIMARY: Add MACD + StochRSI calculations here
├── backtester.py        # UPDATE: Support new indicator columns
├── data_loader.py
├── strategy_loader.py   # UPDATE: Support new indicator columns in query syntax
└── utils.py

tools/
├── market_scanner.py    # UPDATE: Display new indicator values in output
├── find_signals.py
├── quick_analysis.py
├── short_analysis.py
└── combined_analysis.py
```

**Structure Decision**: Single project structure. Feature extends existing `src/analysis.py` module following the established pattern for RSI, EMA, ATR, Bollinger Bands, and ADX indicators.

## Complexity Tracking

> No Constitution violations detected. This section is not required.
