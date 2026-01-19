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
2. **Given** MACD histogram pozitiften negatife geçiş, **When** bu durum tespit edilir, **Then** "MACD bearish crossover" uyarısı üretilir
3. **Given** MACD line signal line'ı yukarı keserse, **When** fiyat EMA200 üzerindeyse, **Then** bullish momentum teyidi sağlanır

---

### User Story 2 - Stochastic RSI ile Hassas Oversold/Overbought (Priority: P1)

Trader olarak, standart RSI'dan daha hassas oversold/overbought sinyalleri almak istiyorum, böylece dip ve tepe noktalarını daha iyi yakalayabilirim.

**Why this priority**: Stochastic RSI, RSI'ın RSI'ı olarak daha hızlı ve hassas sinyaller verir. Özellikle range-bound piyasalarda etkili.

**Independent Test**: Stochastic RSI 20 altına düştüğünde oversold, 80 üzerine çıktığında overbought olarak işaretlenmeli.

**Acceptance Scenarios**:

1. **Given** 180 günlük OHLCV verisi, **When** calculate_indicators() çalışır, **Then** stoch_rsi_k ve stoch_rsi_d sütunları eklenir (0-100 arası)
2. **Given** Stoch RSI K çizgisi D çizgisini aşağıdan yukarı keserse ve değer 20 altındaysa, **When** bu durum tespit edilir, **Then** "Bullish StochRSI crossover in oversold" sinyali üretilir
3. **Given** Stoch RSI 80 üzerindeyken K çizgisi D çizgisini yukarıdan aşağı keserse, **When** bu durum tespit edilir, **Then** "Bearish StochRSI crossover in overbought" sinyali üretilir

---

### User Story 3 - Strateji Entegrasyonu (Priority: P2)

Trader olarak, mevcut stratejilerin MACD ve StochRSI ile güçlendirilmesini istiyorum, böylece daha güvenilir sinyaller alabilirim.

**Why this priority**: İndikatörler tek başına değerli değil, mevcut stratejilere entegre edilmeleri gerekiyor.

**Independent Test**: Trend Pullback stratejisi için MACD teyidi eklendiğinde, backtest win rate'i ölçülebilmeli.

**Acceptance Scenarios**:

1. **Given** Trend Pullback sinyali (close > ema_200 and rsi < 35), **When** MACD histogram negatiften pozitife geçiş yapıyorsa, **Then** sinyal "güçlendirilmiş" olarak işaretlenir
2. **Given** Short stratejisi sinyali, **When** StochRSI 80 üzerinde ve düşüş eğilimindeyse, **Then** short sinyali teyit edilir

---

### Edge Cases

- MACD hesaplaması için yeterli veri yoksa (26 bar'dan az) ne olur? → NaN dönmeli, uyarı loglanmalı
- StochRSI 0 veya 100'de "takılı" kalırsa ne olur? → Aşırı trend durumunu belirtmeli
- Veri boşlukları (gaps) MACD hesaplamasını nasıl etkiler? → Forward fill uygulanmalı

## Requirements

### Functional Requirements

- **FR-001**: Sistem, MACD hesaplaması için standart parametreleri kullanmalı (fast=12, slow=26, signal=9)
- **FR-002**: Sistem, Stochastic RSI hesaplaması için standart parametreleri kullanmalı (period=14, smooth_k=3, smooth_d=3)
- **FR-003**: Yeni indikatörler mevcut analysis.py modülüne entegre edilmeli
- **FR-004**: Market snapshot raporunda yeni indikatör değerleri görüntülenmeli
- **FR-005**: Strateji koşullarında yeni indikatörler kullanılabilmeli (Pandas query syntax)
- **FR-006**: MACD crossover'ları (bullish/bearish) otomatik tespit edilmeli
- **FR-007**: Backtest sistemi yeni indikatörleri desteklemeli

### Key Entities

- **MACD**: macd_line (MACD çizgisi), macd_signal (sinyal çizgisi), macd_histogram (histogram değeri)
- **Stochastic RSI**: stoch_rsi_k (%K çizgisi), stoch_rsi_d (%D çizgisi - sinyal)

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
