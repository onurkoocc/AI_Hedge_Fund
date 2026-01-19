# BTC/USDT & ETH/USDT Kombine Piyasa Analizi

## Görev

1. **Market Scanner'ı çalıştır** (BTC ve ETH birlikte):
```bash
python tools/market_scanner.py --symbols BTC/USDT ETH/USDT --days 180
```

2. **Oluşan raporu oku**: `output/market_snapshot.md`

3. **Anayasa ve risk kurallarını kontrol et**:
   - [specs/02_risk_rules.md](specs/02_risk_rules.md) - 1:2 R:R kuralı
   - [specs/04_strategies.md](specs/04_strategies.md) - Tüm stratejiler (LONG & SHORT)
   - [.specify/memory/constitution.md](.specify/memory/constitution.md) - Temel prensipler

4. **Karşılaştırmalı Analiz**:
   - Her iki varlık için teknik göstergeleri karşılaştır
   - BTC/ETH oranını değerlendir (dominans)
   - Hangisi daha güçlü/zayıf? (Pair Trading fırsatı var mı?)
   - Korelasyon analizi yap
   - **HEM LONG HEM SHORT perspektifinden** değerlendir

5. **Strateji Seçimi** (Decision Matrix):

   | Fiyat vs EMA 200 | RSI Aralığı | ADX | Önerilen Aksiyon |
   |------------------|-------------|-----|------------------|
   | ÜSTÜNDE | < 35 | > 25 | **LONG** (Trend Pullback) |
   | ÜSTÜNDE | > 70 | > 25 | BEKLE (aşırı alım) |
   | ALTINDA | > 60 | > 25 | **SHORT** (Trend Continuation) |
   | ALTINDA | < 35 | > 25 | BEKLE (aşırı satım) |
   | HERHANGİ | 40-60 | < 20 | Grid Trading veya BEKLE |

6. **Her Varlık İçin**:
   - LONG fırsatını değerlendir
   - SHORT fırsatını değerlendir
   - Hangisi daha uygun veya ikisi de mi bekle?

## Çıktı Formatı

```markdown
## 📊 BTC/USDT & ETH/USDT Kombine Analiz

**Tarih**: [tarih]
**Piyasa Durumu**: [Yükseliş Trendi / Düşüş Trendi / Range / Belirsiz]

### Karşılaştırmalı Teknik Analiz

| Gösterge | BTC/USDT | ETH/USDT | Yorum |
|----------|----------|----------|-------|
| Fiyat | $X | $X | - |
| RSI (14) | X | X | Hangisi daha güçlü? |
| EMA 200 | Üstünde/Altında | Üstünde/Altında | Trend uyumu |
| ADX | X | X | Trend gücü |
| Bollinger Pozisyon | %X | %X | Bant içi konum |
| 7 Gün Değişim | %X | %X | Kısa vade momentum |
| 30 Gün Değişim | %X | %X | Orta vade trend |

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

## 🟢 LONG Pozisyon Değerlendirmesi

### BTC/USDT LONG
**Koşullar**:
- Fiyat > EMA 200: [✅/❌]
- RSI < 35: [✅/❌]
- ADX > 25: [✅/❌]

**Karar**: [LONG / BEKLE]
| Parametre | Değer |
|-----------|-------|
| Giriş | $X |
| Stop Loss | $X (%X) |
| Take Profit | $X (%X) |
| R:R Oranı | X:1 |

### ETH/USDT LONG
**Koşullar**:
- Fiyat > EMA 200: [✅/❌]
- RSI < 35: [✅/❌]
- ADX > 25: [✅/❌]

**Karar**: [LONG / BEKLE]
| Parametre | Değer |
|-----------|-------|
| Giriş | $X |
| Stop Loss | $X (%X) |
| Take Profit | $X (%X) |
| R:R Oranı | X:1 |

---

## 🔴 SHORT Pozisyon Değerlendirmesi

### BTC/USDT SHORT
**Koşullar**:
- Fiyat < EMA 200: [✅/❌]
- RSI > 60: [✅/❌]
- ADX > 25: [✅/❌]

**Karar**: [SHORT / BEKLE]
| Parametre | Değer |
|-----------|-------|
| Giriş | $X (bounce bekle) |
| Stop Loss | $X (%X) |
| Take Profit | $X (%X) |
| R:R Oranı | X:1 |

### ETH/USDT SHORT
**Koşullar**:
- Fiyat < EMA 200: [✅/❌]
- RSI > 60: [✅/❌]
- ADX > 25: [✅/❌]

**Karar**: [SHORT / BEKLE]
| Parametre | Değer |
|-----------|-------|
| Giriş | $X (bounce bekle) |
| Stop Loss | $X (%X) |
| Take Profit | $X (%X) |
| R:R Oranı | X:1 |

---

## 🔄 Pair Trading Değerlendirmesi (Opsiyonel)

**30 Günlük Performans Farkı**: X%
- Yeterli fark (>5%): [EVET/HAYIR]
- Öneri: [LONG güçlü / SHORT zayıf] veya [Uygun değil]

---

## 📈 Backtest Kanıtları

### LONG Sinyalleri (Trend Pullback)
**BTC/USDT**:
| Tarih | Sonuç | P&L |
|-------|-------|-----|
| ... | TP/SL | %X |

**ETH/USDT**:
| Tarih | Sonuç | P&L |
|-------|-------|-----|
| ... | TP/SL | %X |

### SHORT Sinyalleri (Trend Continuation)
**BTC/USDT**:
| Tarih | Sonuç | P&L |
|-------|-------|-----|
| ... | TP/SL | %X |

**ETH/USDT**:
| Tarih | Sonuç | P&L |
|-------|-------|-----|
| ... | TP/SL | %X |

---

## 📋 Özet Tavsiye

| Varlık | LONG | SHORT | Aktif Sinyal | Güven |
|--------|------|-------|--------------|-------|
| BTC/USDT | [Uygun/Bekle] | [Uygun/Bekle] | [LONG/SHORT/YOK] | [Yüksek/Orta/Düşük] |
| ETH/USDT | [Uygun/Bekle] | [Uygun/Bekle] | [LONG/SHORT/YOK] | [Yüksek/Orta/Düşük] |

### 🚨 Alarm Seviyeleri

**LONG Fırsatı İçin İzle:**
- BTC: $X (EMA 200 üzeri kapanış)
- ETH: $X (EMA 200 üzeri kapanış)

**SHORT Fırsatı İçin İzle:**
- BTC: $X - $X arası (BB Mid bounce + RSI 55-65)
- ETH: $X - $X arası (BB Mid bounce + RSI 55-65)

**Toplam Pozisyon Sayısı**: X/5 (Aylık limit: 5 Sniper işlem)

**Risk Uyarısı**: Bu analiz yatırım tavsiyesi değildir. 1:2 R:R kuralı sağlanmadan işlem yapılmamalıdır.
```
