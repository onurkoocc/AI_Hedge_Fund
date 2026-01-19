# Feature Specification: ATR-Bazlı Dinamik Stop-Loss

**Feature Branch**: `003-atr-dynamic-stoploss`  
**Created**: 2026-01-20  
**Status**: Draft  
**Phase**: 2 of 4 (Risk Management Enhancement)

## Overview

Mevcut sabit yüzdelik stop-loss sistemini (örn: %2) volatiliteye duyarlı dinamik bir sisteme dönüştürmek. ATR (Average True Range) kullanarak piyasa koşullarına göre otomatik ayarlanan stop-loss seviyeleri hesaplanacak. Bu, volatil dönemlerde erken stop-out'u önlerken, sakin dönemlerde riski minimize edecek.

## User Scenarios & Testing

### User Story 1 - Volatiliteye Duyarlı Stop-Loss (Priority: P1)

Trader olarak, piyasa volatilitesine göre otomatik ayarlanan stop-loss seviyeleri istiyorum, böylece yüksek volatilitede gereksiz yere stop olmaktan kaçınabilirim.

**Why this priority**: Sabit %2 stop-loss, volatil piyasalarda çok sık tetiklenir ve karlı pozisyonları erken kapatır. ATR-bazlı stop bu sorunu çözer.

**Independent Test**: Sinyal üretildiğinde, stop-loss seviyesi ATR'a göre dinamik olarak hesaplanmalı ve raporda gösterilmeli.

**Acceptance Scenarios**:

1. **Given** BTC/USDT için ATR = $2,500, **When** long sinyal üretilir, **Then** stop-loss = entry_price - (ATR × 1.5) = entry - $3,750
2. **Given** ETH/USDT için ATR = $150, **When** short sinyal üretilir, **Then** stop-loss = entry_price + (ATR × 1.5) = entry + $225
3. **Given** düşük volatilite dönemi (ATR normalin altında), **When** sinyal üretilir, **Then** stop-loss daha dar tutulur

---

### User Story 2 - R:R Oranı Koruması (Priority: P1)

Trader olarak, dinamik stop-loss kullanılsa bile 1:2 minimum R:R oranının korunmasını istiyorum, böylece her işlem hala karlı potansiyele sahip olsun.

**Why this priority**: Specs'teki temel kural olan 1:2 R:R mutlaka korunmalı. Dinamik stop genişlerse, TP de orantılı genişlemeli.

**Independent Test**: Üretilen her sinyalde R:R oranı hesaplanmalı ve 2.0'ın altına düşmemeli.

**Acceptance Scenarios**:

1. **Given** dinamik stop-loss hesaplandı (örn: %3), **When** R:R kontrolü yapılır, **Then** take-profit en az %6 olarak ayarlanır
2. **Given** R:R < 2.0 olacak bir setup, **When** sinyal değerlendirilir, **Then** sinyal "R:R yetersiz" olarak reddedilir veya TP ayarlanır

---

### User Story 3 - ATR Çarpanı Yapılandırması (Priority: P2)

Trader olarak, ATR çarpanını strateji bazında ayarlayabilmek istiyorum, böylece farklı stratejiler için farklı risk profilleri kullanabilirim.

**Why this priority**: Trend stratejileri daha geniş stop isterken, scalp stratejileri daha dar stop gerektirir.

**Independent Test**: Farklı ATR çarpanlarıyla (1.0, 1.5, 2.0) backtest yapıldığında sonuçlar karşılaştırılabilmeli.

**Acceptance Scenarios**:

1. **Given** Trend Pullback stratejisi (ATR multiplier = 1.5), **When** sinyal üretilir, **Then** stop = entry - (ATR × 1.5)
2. **Given** Grid stratejisi (ATR multiplier = 1.0), **When** sinyal üretilir, **Then** stop = entry - (ATR × 1.0)

---

### User Story 4 - Backtest Uyumluluğu (Priority: P2)

Trader olarak, dinamik stop-loss sisteminin backtest motoruyla tam uyumlu çalışmasını istiyorum, böylece tarihsel performansı doğru ölçebilirim.

**Why this priority**: Yeni stop-loss mantığı backtest'te de kullanılmalı ki sonuçlar gerçekçi olsun.

**Independent Test**: Aynı strateji sabit ve dinamik stop ile backtest edildiğinde, sonuçlar farklı olmalı.

**Acceptance Scenarios**:

1. **Given** tarihsel sinyal, **When** backtest yapılır, **Then** o anki ATR değeri kullanılarak dinamik stop hesaplanır
2. **Given** volatil dönem (ATR yüksek), **When** backtest yapılır, **Then** daha az stop-out görülür

---

### Edge Cases

- ATR değeri sıfır veya çok küçükse ne olur? → Minimum stop-loss yüzdesi (%1) uygulanmalı
- ATR değeri aşırı yüksekse ne olur? → Maximum stop-loss yüzdesi (%5) ile sınırlanmalı
- Veri yetersizliğinden ATR hesaplanamazsa ne olur? → Varsayılan sabit stop-loss (%2) kullanılmalı

## Requirements

### Functional Requirements

- **FR-001**: Sistem, her sinyal için ATR değerini kullanarak dinamik stop-loss hesaplamalı
- **FR-002**: Stop-loss formülü: `entry_price ± (ATR × multiplier)` (long için -, short için +)
- **FR-003**: Varsayılan ATR çarpanı 1.5 olmalı
- **FR-004**: Minimum stop-loss %1, maksimum %5 ile sınırlanmalı
- **FR-005**: R:R oranı her zaman minimum 2.0 olmalı, take-profit dinamik stop'a göre ayarlanmalı
- **FR-006**: Strateji tanımlarında ATR çarpanı parametresi eklenebilmeli
- **FR-007**: Backtest motoru dinamik stop-loss mantığını desteklemeli
- **FR-008**: Market snapshot raporunda dinamik stop seviyeleri gösterilmeli

### Key Entities

- **DynamicStop**: entry_price, atr_value, atr_multiplier, calculated_stop, calculated_tp, rr_ratio
- **Strategy.params**: stop_loss_pct yerine atr_multiplier eklenmeli

## Success Criteria

### Measurable Outcomes

- **SC-001**: Tüm sinyaller için dinamik stop-loss ve take-profit seviyeleri hesaplanabilmeli
- **SC-002**: Backtest'te dinamik stop kullanıldığında, volatil dönemlerde stop-out oranı sabit stop'a göre azalmalı
- **SC-003**: Hiçbir sinyal 2.0'ın altında R:R oranıyla üretilmemeli
- **SC-004**: Yüksek volatilite dönemlerinde (%20+ ATR artışı) stop-loss otomatik genişlemeli

## Assumptions

- ATR(14) mevcut analysis.py'de zaten hesaplanıyor
- Strateji dosyası (04_strategies.md) güncellenerek yeni parametre eklenebilir
- Kullanıcılar başlangıçta varsayılan çarpanları kullanacak

## Out of Scope

- Trailing stop-loss implementasyonu (ayrı faz)
- Real-time stop güncelleme (canlı trade yönetimi)
- Kullanıcı arayüzünden ATR çarpanı değiştirme
