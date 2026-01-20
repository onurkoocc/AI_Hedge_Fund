# Feature Specification: MACD ve Stochastic RSI İndikatörleri

**Feature Branch**: `002-macd-stochrsi-indicators`  
**Created**: 2026-01-20  
**Status**: Draft  
**Phase**: 1 of 4 (Technical Indicators Enhancement)

## Overview

Mevcut teknik analiz sistemine MACD (Moving Average Convergence Divergence) ve Stochastic RSI indikatörlerini ekleyerek sinyal kalitesini artırmak. Bu indikatörler momentum değişimlerini daha erken tespit etmek ve mevcut stratejilere ek doğrulama katmanı sağlamak için kullanılacak.

## User Scenarios & Testing

### User Story 1 - MACD ile Momentum Teyidi (Priority: P1)

Trader olarak, mevcut RSI sinyallerinin MACD ile teyit edilmesini istiyorum, böylece false positive sinyalleri azaltabilirim.

**Why this priority**: MACD, piyasada en yaygın kullanılan momentum indikatörlerinden biri. Mevcut stratejilere eklenmesi sinyal kalitesini doğrudan artırır.

**Independent Test**: Market scanner çalıştırıldığında her varlık için MACD değerleri (macd_line, signal_line, histogram) raporlanmalı ve stratejilerde kullanılabilmeli.

**Acceptance Scenarios**:

1. **Given** 180 günlük OHLCV verisi, **When** calculate_indicators() çalışır, **Then** DataFrame'e macd, macd_signal, macd_histogram sütunları eklenir
2. **Given** MACD histogram pozitiften negatife geçiş, **When** bu durum tespit edilir, **Then** "MACD bearish crossover (MACD: X.XXXX, Signal: X.XXXX)" uyarısı üretilir
3. **Given** MACD line signal line'ı yukarı keserse, **When** fiyat EMA200 üzerindeyse, **Then** bullish momentum teyidi sağlanır

---

### User Story 2 - Stochastic RSI ile Hassas Oversold/Overbought (Priority: P1)

Trader olarak, standart RSI'dan daha hassas oversold/overbought sinyalleri almak istiyorum, böylece dip ve tepe noktalarını daha iyi yakalayabilirim.

**Why this priority**: Stochastic RSI, RSI'ın RSI'ı olarak daha hızlı ve hassas sinyaller verir. Özellikle range-bound piyasalarda etkili.

**Independent Test**: Stochastic RSI 20 altına düştüğünde oversold, 80 üzerine çıktığında overbought olarak işaretlenmeli.

**Acceptance Scenarios**:

1. **Given** 180 günlük OHLCV verisi, **When** calculate_indicators() çalışır, **Then** stoch_rsi_k ve stoch_rsi_d sütunları eklenir (0-100 arası)
2. **Given** Stoch RSI K çizgisi D çizgisini aşağıdan yukarı keserse ve değer 20 altındaysa, **When** bu durum tespit edilir, **Then** "Bullish StochRSI crossover in oversold (K: X.XXXX, D: X.XXXX)" sinyali üretilir
3. **Given** Stoch RSI 80 üzerindeyken K çizgisi D çizgisini yukarıdan aşağı keserse, **When** bu durum tespit edilir, **Then** "Bearish StochRSI crossover in overbought (K: X.XXXX, D: X.XXXX)" sinyali üretilir

---

### User Story 3 - Strateji Entegrasyonu (Priority: P2)

Trader olarak, mevcut stratejilerin MACD ve StochRSI ile güçlendirilmesini istiyorum, böylece daha güvenilir sinyaller alabilirim.

**Why this priority**: İndikatörler tek başına değerli değil, mevcut stratejilere entegre edilmeleri gerekiyor.

**Integration Mode**: Optional filters — strategies work without new indicators (backward compatible), indicators add extra confidence labeling when available.

**Independent Test**: Trend Pullback stratejisi için MACD teyidi eklendiğinde, backtest win rate'i ölçülebilmeli.

**Acceptance Scenarios**:

1. **Given** Trend Pullback sinyali (close > ema_200 and rsi < 35), **When** MACD histogram negatiften pozitife geçiş yapıyorsa, **Then** sinyal "güçlendirilmiş" olarak işaretlenir (optional confidence boost, not required for signal)
2. **Given** Short stratejisi sinyali, **When** StochRSI 80 üzerinde ve düşüş eğilimindeyse, **Then** short sinyali teyit edilir (optional confirmation label)
3. **Given** Any strategy signal, **When** MACD/StochRSI data unavailable, **Then** signal still fires with base confidence (backward compatible)

---

### Edge Cases

- MACD hesaplaması için yeterli veri yoksa (26 bar'dan az) ne olur? → NaN dönmeli, uyarı loglanmalı (WARNING level, includes symbol and missing bar count)
- StochRSI 0 veya 100'de "takılı" kalırsa ne olur? → Aşırı trend durumunu belirtmeli
- Veri boşlukları (gaps) MACD hesaplamasını nasıl etkiler? → Forward fill uygulanmalı
- NaN indikatör değerleri strateji sinyallerini nasıl etkiler? → Sinyal tamamen atlanmalı (skip), log kaydı tutulmalı (INFO level: "{symbol} signal skipped due to insufficient indicator data")

## Requirements

### Functional Requirements

- **FR-001**: Sistem, MACD hesaplaması için standart parametreleri kullanmalı (fast=12, slow=26, signal=9)
- **FR-002**: Sistem, Stochastic RSI hesaplaması için standart parametreleri kullanmalı (period=14, smooth_k=3, smooth_d=3)
- **FR-003**: Yeni indikatörler mevcut analysis.py modülüne entegre edilmeli
- **FR-004**: Market snapshot raporunda yeni indikatör değerleri görüntülenmeli
- **FR-005**: Strateji koşullarında yeni indikatörler kullanılabilmeli (Pandas query syntax)
- **FR-006**: MACD crossover'ları (bullish/bearish) otomatik tespit edilmeli
- **FR-007**: Backtest sistemi yeni indikatörleri desteklemeli
- **FR-008**: Logging stratejisi: ERROR/WARNING for calculation failures, INFO for crossover events detected (balanced observability)

### Key Entities

- **MACD**: macd_line (MACD çizgisi), macd_signal (sinyal çizgisi), macd_histogram (histogram değeri) — all float64, displayed with 4 decimal places
- **Stochastic RSI**: stoch_rsi_k (%K çizgisi), stoch_rsi_d (%D çizgisi - sinyal) — all float64, 0-100 range, displayed with 4 decimal places

## Success Criteria

### Measurable Outcomes

- **SC-001**: Tüm taranmış varlıklar için MACD ve StochRSI değerleri hesaplanabilmeli
- **SC-002**: Market scanner çalışma süresi %10'dan fazla artmamalı
- **SC-003**: Yeni indikatörlerle güçlendirilmiş stratejilerin backtest win rate'i mevcut durumdan düşük olmamalı
- **SC-004**: MACD crossover tespiti %100 doğrulukla çalışmalı (manuel doğrulama ile)

## Assumptions

- ta (Technical Analysis) kütüphanesi MACD ve Stochastic RSI hesaplamalarını destekliyor
- Mevcut 180 günlük veri MACD için yeterli (minimum 26 bar gerekli)
- Kullanıcılar indikatör parametrelerini şimdilik değiştirmek istemeyecek (sabit değerler)

## Out of Scope

- İndikatör parametrelerinin kullanıcı tarafından özelleştirilmesi (gelecek faz)
- MACD divergence tespiti (gelecek faz)
- Görselleştirme/charting (gelecek faz)

## Clarifications

### Session 2026-01-20

- Q: When MACD/StochRSI values are NaN due to insufficient data, what should happen to downstream strategy signals? → A: Skip signal entirely; log at WARNING level for calculation failure (with symbol and missing bar count), log at INFO level when signal is skipped due to insufficient indicator data
- Q: What level of observability/logging is needed for MACD/StochRSI calculations? → A: Balanced - log errors/warnings for failures + INFO level for crossover events detected
- Q: What data types and precision should indicator values use? → A: float64 internally, displayed with 4 decimal places
- Q: Should crossover signal messages include additional context? → A: Label + current values (e.g., "MACD bullish crossover (MACD: 0.0523, Signal: 0.0412)")
- Q: Should new indicators be optional filters or mandatory requirements in enhanced strategies? → A: Optional filters — strategies work without them (backward compatible), indicators add extra confidence when available
