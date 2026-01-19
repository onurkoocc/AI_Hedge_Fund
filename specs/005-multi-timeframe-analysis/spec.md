# Feature Specification: Multi-Timeframe Analiz Sistemi

**Feature Branch**: `005-multi-timeframe-analysis`  
**Created**: 2026-01-20  
**Status**: Draft  
**Phase**: 4 of 4 (Advanced Analysis)

## Overview

Mevcut tek zaman dilimli (1H) analiz sistemini çoklu zaman dilimi (1H + 4H + 1D) analizi destekleyecek şekilde genişletmek. Farklı zaman dilimlerindeki trend uyumu, sinyal kalitesini ve güvenilirliğini önemli ölçüde artırır. "Higher timeframe trend direction + Lower timeframe entry" yaklaşımı profesyonel trading'in temel prensiplerinden biridir.

## User Scenarios & Testing

### User Story 1 - Multi-Timeframe Trend Uyumu (Priority: P1)

Trader olarak, farklı zaman dilimlerinde trend yönlerinin uyumlu olup olmadığını bilmek istiyorum, böylece trende karşı işlem açmaktan kaçınabilirim.

**Why this priority**: Günlük trend yukarıyken 1 saatlik timeframe'de short sinyali takip etmek riskli. MTF uyumu temel kalite filtresi.

**Independent Test**: 1D trend bullish, 4H trend bullish, 1H pullback sinyali üretildiğinde "MTF Aligned ✓" etiketi görülmeli.

**Acceptance Scenarios**:

1. **Given** BTC 1D trend bullish (fiyat > EMA200), 4H trend bullish, 1H RSI < 35, **When** Trend Pullback sinyali üretilir, **Then** sinyal "MTF Aligned (3/3)" olarak etiketlenir
2. **Given** ETH 1D trend bearish, 4H trend bearish, 1H long sinyali, **When** sinyal değerlendirilir, **Then** "MTF Conflict ⚠️" uyarısı verilir
3. **Given** SOL 1D sideways, 4H bullish, 1H bullish sinyal, **When** sinyal değerlendirilir, **Then** "Partial MTF Alignment (2/3)" etiketi verilir

---

### User Story 2 - Higher Timeframe Destek/Direnç (Priority: P1)

Trader olarak, 1 saatlik sinyalin günlük veya 4 saatlik önemli seviyelere yakın olup olmadığını bilmek istiyorum, böylece daha iyi giriş noktaları seçebilirim.

**Why this priority**: Günlük destek seviyesinde long girmek, rastgele bir seviyede girmekten çok daha güvenli.

**Independent Test**: 1H long sinyali, 4H veya 1D destek seviyesine yakınsa (ATR mesafesi içinde) "Near HTF Support" etiketi almalı.

**Acceptance Scenarios**:

1. **Given** BTC 1H long sinyal, fiyat 4H BB lower'a %2 mesafede, **When** sinyal değerlendirilir, **Then** "Near 4H Support ✓" etiketi eklenir
2. **Given** ETH 1H short sinyal, fiyat 1D EMA200'e %1 mesafede, **When** sinyal değerlendirilir, **Then** "Near 1D Resistance" etiketi eklenir

---

### User Story 3 - Çoklu Timeframe İndikatör Raporu (Priority: P2)

Trader olarak, her varlık için 1H, 4H ve 1D RSI değerlerini yan yana görmek istiyorum, böylece genel momentum durumunu anlayabilirim.

**Why this priority**: Hızlı karar verme için özet görünüm gerekli.

**Independent Test**: Market snapshot'ta her varlık için RSI_1H, RSI_4H, RSI_1D sütunları görülmeli.

**Acceptance Scenarios**:

1. **Given** market scanner çalıştırıldı, **When** rapor üretilir, **Then** her varlık için 3 timeframe RSI değeri gösterilir
2. **Given** tüm timeframe'lerde RSI < 40, **When** rapor incelenir, **Then** "Oversold on all TFs" özet notu eklenir

---

### User Story 4 - MTF-Bazlı Strateji Koşulları (Priority: P2)

Trader olarak, strateji koşullarında higher timeframe değerlerini kullanabilmek istiyorum, örneğin "1D RSI < 50 and 1H RSI < 30".

**Why this priority**: Daha sofistike strateji tanımları için gerekli.

**Independent Test**: Strateji koşulunda `rsi_1d < 50 and rsi_1h < 30` kullanıldığında doğru çalışmalı.

**Acceptance Scenarios**:

1. **Given** strateji koşulu "close_1h > ema_200_1d and rsi_1h < 35", **When** sinyal taranır, **Then** günlük EMA200 ve saatlik RSI birlikte değerlendirilir
2. **Given** strateji koşulu "adx_4h > 25 and adx_1h > 20", **When** sinyal taranır, **Then** her iki timeframe ADX değeri kontrol edilir

---

### User Story 5 - Timeframe Hiyerarşisi Belirleme (Priority: P3)

Trader olarak, hangi timeframe'in birincil (entry), hangisinin referans (trend) olduğunu bilmek istiyorum.

**Why this priority**: Netlik ve tutarlılık için gerekli.

**Independent Test**: Sinyal detayında "Entry TF: 1H, Trend TF: 4H, Bias TF: 1D" bilgisi gösterilmeli.

**Acceptance Scenarios**:

1. **Given** Trend Pullback sinyali, **When** detay görüntülenir, **Then** timeframe hiyerarşisi açıkça belirtilir

---

### Edge Cases

- 4H veya 1D veri yetersizse (yeni listelenen coin) ne olur? → Mevcut timeframe'lerle devam edilmeli, uyarı verilmeli
- Timeframe'ler arası çelişki varsa (1D up, 4H down, 1H up) ne olur? → "Mixed signals" uyarısı, düşük öncelik
- API rate limit'e takılırsa (çok fazla veri çekme) ne olur? → Önbellek kullanılmalı, sıralı fetch

## Requirements

### Functional Requirements

- **FR-001**: Sistem, her varlık için 1H, 4H ve 1D OHLCV verisi çekebilmeli
- **FR-002**: Her timeframe için bağımsız teknik indikatörler hesaplanmalı (RSI, EMA, ADX, BB)
- **FR-003**: Timeframe-bazlı sütun isimlendirmesi: rsi_1h, rsi_4h, rsi_1d şeklinde
- **FR-004**: MTF trend uyumu skoru hesaplanmalı (örn: 3/3 aligned)
- **FR-005**: Strateji koşullarında MTF değişkenler kullanılabilmeli
- **FR-006**: Market snapshot raporunda MTF özet tablosu gösterilmeli
- **FR-007**: Higher timeframe destek/direnç seviyelerine yakınlık tespit edilmeli
- **FR-008**: Veri çekme optimize edilmeli (caching, rate limit handling)

### Key Entities

- **TimeframeData**: timeframe (1h/4h/1d), ohlcv_data, indicators (rsi, ema, adx, bb)
- **MTFAlignment**: trend_1h, trend_4h, trend_1d, alignment_score (0-3), conflicts[]
- **HTFLevels**: support_4h, resistance_4h, support_1d, resistance_1d, ema_200_1d

## Success Criteria

### Measurable Outcomes

- **SC-001**: 3 timeframe verisi başarıyla çekilip analiz edilebilmeli
- **SC-002**: MTF uyumlu sinyallerin backtest win rate'i tek timeframe sinyallerden yüksek olmalı
- **SC-003**: Market scanner çalışma süresi 3x'ten fazla artmamalı (caching ile)
- **SC-004**: MTF conflict uyarısı verilen sinyallerin kaybetme oranı daha yüksek olmalı (doğrulama)

## Assumptions

- ccxt 4H ve 1D OHLCV verisi çekebilir (Binance destekler)
- 180 günlük veri her timeframe için yeterli
- Kullanıcılar başlangıçta varsayılan 3 timeframe'i kullanacak (1H, 4H, 1D)

## Out of Scope

- Kullanıcı tarafından özel timeframe seçimi (örn: 15M, 2H)
- Timeframe arası divergence tespiti (gelecek faz)
- Gerçek zamanlı MTF güncelleme (canlı trading için)
- 5+ timeframe desteği
