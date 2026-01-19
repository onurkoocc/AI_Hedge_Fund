---
name: analyze-btc-eth
description: "BTC/USDT ve ETH/USDT birlikte analiz ve pozisyon önerisi"
---

# BTC/USDT & ETH/USDT Kombine Piyasa Analizi

## Görev

1. **Market Scanner'ı çalıştır** (BTC ve ETH birlikte):
```bash
python tools/market_scanner.py --symbols BTC/USDT ETH/USDT --days 180
```

2. **Oluşan raporu oku**: `output/market_snapshot.md`

3. **Anayasa ve risk kurallarını kontrol et**:
   - [specs/02_risk_rules.md](specs/02_risk_rules.md) - 1:2 R:R kuralı
   - [specs/04_strategies.md](specs/04_strategies.md) - Pair Trading stratejisi
   - [.specify/memory/constitution.md](.specify/memory/constitution.md) - Temel prensipler

4. **Karşılaştırmalı Analiz**:
   - Her iki varlık için teknik göstergeleri karşılaştır
   - BTC/ETH oranını değerlendir (dominans)
   - Hangisi daha güçlü/zayıf? (Pair Trading fırsatı var mı?)
   - Korelasyon analizi yap
   - Her biri için ayrı pozisyon önerisi sun

5. **Strateji Seçimi**:
   - Her ikisi de aynı yönde mi? → Tek pozisyon öner
   - Farklı yönlerde mi? → Pair Trading düşün
   - Belirsizlik mi? → Hedge veya Grid stratejisi öner

## Çıktı Formatı

```markdown
## 📊 BTC/USDT & ETH/USDT Kombine Analiz

**Tarih**: [tarih]
**Piyasa Durumu**: [Trend / Range / Belirsiz]

### Karşılaştırmalı Teknik Analiz

| Gösterge | BTC/USDT | ETH/USDT | Yorum |
|----------|----------|----------|-------|
| Fiyat | $X | $X | - |
| RSI (14) | X | X | Hangisi daha güçlü? |
| EMA 200 | Üstünde/Altında | Üstünde/Altında | Trend uyumu |
| ADX | X | X | Trend gücü |
| Bollinger | Pozisyon | Pozisyon | - |

### BTC/ETH Oranı
- Mevcut: X.XX
- 30 günlük ortalama: X.XX
- Yorum: BTC dominant / ETH dominant / Dengeli

### Makro Korelasyon
- Gold: [trend] → Kripto için [bullish/bearish]
- DXY: [trend] → Kripto için [bullish/bearish]
- S&P 500: [trend] → Risk iştahı [yüksek/düşük]

### Sentiment
Ortalama Skor: X.XX (Bullish/Bearish/Nötr)

---

## 🎯 Pozisyon Önerileri

### Öneri 1: BTC/USDT
**Karar**: [LONG / SHORT / BEKLE]
- Giriş: $X
- Stop Loss: $X (%X)
- Take Profit: $X (%X)
- R:R Oranı: X:1

### Öneri 2: ETH/USDT
**Karar**: [LONG / SHORT / BEKLE]
- Giriş: $X
- Stop Loss: $X (%X)
- Take Profit: $X (%X)
- R:R Oranı: X:1

### Alternatif: Pair Trading (Opsiyonel)
Eğer BTC ve ETH farklı güçte ise:
- **LONG**: [Güçlü olan]
- **SHORT**: [Zayıf olan]
- Net Exposure: Hedge

---

## 📈 Backtest Kanıtları

### BTC/USDT Son 3 Sinyal
| Tarih | Sonuç | P&L |
|-------|-------|-----|
| ... | TP/SL | %X |

### ETH/USDT Son 3 Sinyal
| Tarih | Sonuç | P&L |
|-------|-------|-----|
| ... | TP/SL | %X |

---

## 📋 Özet Tavsiye

| Varlık | Aksiyon | Güven | Öncelik |
|--------|---------|-------|---------|
| BTC/USDT | [LONG/SHORT/BEKLE] | [Yüksek/Orta/Düşük] | [1/2] |
| ETH/USDT | [LONG/SHORT/BEKLE] | [Yüksek/Orta/Düşük] | [1/2] |

**Toplam Pozisyon Sayısı**: X/5 (Aylık limit: 5 Sniper işlem)

**Risk Uyarısı**: Bu analiz yatırım tavsiyesi değildir.
```
