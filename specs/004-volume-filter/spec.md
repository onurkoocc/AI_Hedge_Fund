# Feature Specification: Volume Filter - Düşük Hacimde İşlem Engelleme

**Feature Branch**: `004-volume-filter`  
**Created**: 2026-01-20  
**Status**: Draft  
**Phase**: 3 of 4 (Signal Quality Enhancement)

## Overview

Sinyal kalitesini artırmak için hacim (volume) bazlı filtre eklemek. Düşük hacimli dönemlerde üretilen sinyaller genellikle güvenilmez olup "fake breakout" riskini artırır. Bu özellik, belirli bir hacim eşiğinin altındaki sinyalleri filtreleyerek yalnızca yeterli likidite ve piyasa katılımı olan sinyallerin raporlanmasını sağlayacak.

## User Scenarios & Testing

### User Story 1 - Düşük Hacimli Sinyalleri Filtreleme (Priority: P1)

Trader olarak, düşük hacimli dönemlerde üretilen sinyallerin otomatik olarak filtrelenmesini istiyorum, böylece fake breakout'lardan kaçınabilirim.

**Why this priority**: Düşük hacim = düşük güvenilirlik. En temel kalite filtresi.

**Independent Test**: Hacim 20 günlük ortalamanın %50'sinin altındayken sinyal üretildiğinde, raporda "düşük hacim uyarısı" gösterilmeli veya sinyal reddedilmeli.

**Acceptance Scenarios**:

1. **Given** BTC/USDT için mevcut hacim 20-günlük ortalamanın %40'ı, **When** strateji koşulu sağlanır, **Then** sinyal "Low Volume - Filtered" olarak işaretlenir
2. **Given** ETH/USDT için mevcut hacim 20-günlük ortalamanın %120'si, **When** strateji koşulu sağlanır, **Then** sinyal normal olarak üretilir
3. **Given** hafta sonu (düşük likidite), **When** sinyal taranır, **Then** hacim kontrolü yapılır ve uyarı verilir

---

### User Story 2 - Volume Spike Teyidi (Priority: P1)

Trader olarak, breakout sinyallerinin yüksek hacimle desteklenip desteklenmediğini bilmek istiyorum, böylece gerçek breakout'ları fake olanlardan ayırabilirim.

**Why this priority**: Breakout + yüksek hacim = güçlü sinyal. Bu kombinasyon win rate'i önemli ölçüde artırır.

**Independent Test**: Breakout sinyali üretildiğinde, hacim ortalamanın 1.5x üzerindeyse "volume confirmed" etiketi eklenmeli.

**Acceptance Scenarios**:

1. **Given** Breakout Continuation sinyali (fiyat BB upper kırıldı), **When** hacim 20-günlük ortalamanın 1.5x üzerinde, **Then** sinyal "Volume Confirmed ✓" olarak işaretlenir
2. **Given** Breakout sinyali, **When** hacim ortalamanın altında, **Then** sinyal "Weak Volume ⚠️" uyarısı alır

---

### User Story 3 - Strateji Bazında Volume Eşiği (Priority: P2)

Trader olarak, farklı stratejiler için farklı hacim eşikleri belirleyebilmek istiyorum, çünkü breakout stratejileri daha yüksek hacim gerektirirken, trend stratejileri daha esnek olabilir.

**Why this priority**: Her strateji aynı hacim gereksinimi duymaz.

**Independent Test**: Breakout stratejisi için volume_threshold=1.5, Trend Pullback için volume_threshold=0.8 kullanıldığında farklı sonuçlar üretilmeli.

**Acceptance Scenarios**:

1. **Given** Breakout stratejisi (volume_threshold=1.5), **When** hacim ortalamanın 1.2x'i, **Then** sinyal reddedilir
2. **Given** Trend Pullback stratejisi (volume_threshold=0.8), **When** hacim ortalamanın 1.0x'i, **Then** sinyal kabul edilir

---

### User Story 4 - Volume Raporu (Priority: P3)

Trader olarak, market snapshot raporunda her varlık için hacim durumunu görmek istiyorum, böylece genel piyasa aktivitesini anlayabilirim.

**Why this priority**: Bilgilendirici ama kritik değil.

**Independent Test**: Market snapshot'ta her varlık için "Volume vs 20-day Avg" sütunu eklenmeli.

**Acceptance Scenarios**:

1. **Given** market scanner çalıştırıldı, **When** rapor üretilir, **Then** her varlık için hacim yüzdesi (örn: %85 of avg) gösterilir

---

### Edge Cases

- Varlık yeni listelenmiş ve 20 günlük veri yoksa ne olur? → Mevcut veriyle ortalama hesaplanmalı, uyarı verilmeli
- Hacim verisi sıfır veya eksikse ne olur? → Sinyal reddedilmeli, hata loglanmalı
- Hafta sonu / tatil günlerinde hacim doğal olarak düşükse ne olur? → Gün bazlı normalizasyon düşünülebilir (gelecek faz)

## Requirements

### Functional Requirements

- **FR-001**: Sistem, her varlık için 20 günlük ortalama hacmi hesaplamalı
- **FR-002**: Mevcut hacim ortalama hacmin belirli bir yüzdesinin altındaysa sinyal filtrelenmeli
- **FR-003**: Varsayılan minimum hacim eşiği: ortalamanın %50'si
- **FR-004**: Breakout stratejileri için minimum hacim eşiği: ortalamanın %150'si
- **FR-005**: Strateji tanımlarında volume_threshold parametresi eklenebilmeli
- **FR-006**: Filtrelenen sinyaller raporda "Low Volume" olarak gösterilmeli (tamamen gizlenmemeli)
- **FR-007**: Yüksek hacimli sinyaller "Volume Confirmed" etiketi almalı
- **FR-008**: Backtest motoru hacim filtresini desteklemeli

### Key Entities

- **VolumeMetrics**: current_volume, avg_volume_20d, volume_ratio, volume_status (low/normal/high)
- **Strategy.params**: volume_threshold eklenmeli (varsayılan: 0.5)

## Success Criteria

### Measurable Outcomes

- **SC-001**: Tüm sinyaller için hacim durumu raporlanabilmeli
- **SC-002**: Düşük hacimli sinyallerin filtrelenmesiyle backtest false positive oranı azalmalı
- **SC-003**: Volume confirmed breakout sinyallerinin win rate'i normal breakout'lardan yüksek olmalı
- **SC-004**: Market scanner çalışma süresi %5'ten fazla artmamalı

## Assumptions

- Volume verisi ccxt'den OHLCV ile birlikte geliyor (mevcut yapı)
- 20 günlük ortalama yeterli bir referans noktası (daha kısa/uzun dönemler gelecek fazda)
- Kullanıcılar başlangıçta varsayılan eşikleri kullanacak

## Out of Scope

- Gün içi hacim profili (volume by hour)
- On-chain volume analizi (exchange inflow/outflow)
- Order book depth analizi
- Relative Volume (RVOL) karşılaştırmaları
