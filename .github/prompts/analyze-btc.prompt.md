# BTC/USDT Piyasa Analizi ve Pozisyon Önerisi

## Görev

1. **Market Scanner'ı çalıştır** (sadece BTC/USDT için):
```bash
python tools/market_scanner.py --symbols BTC/USDT --days 180
```

2. **Oluşan raporu oku**: `output/market_snapshot.md`

3. **Anayasa ve risk kurallarını kontrol et**:
   - [specs/02_risk_rules.md](specs/02_risk_rules.md) - 1:2 R:R kuralı
   - [specs/04_strategies.md](specs/04_strategies.md) - Tüm stratejiler (LONG & SHORT)
   - [.specify/memory/constitution.md](.specify/memory/constitution.md) - Temel prensipler

4. **Analiz ve Öneri**:
   - Mevcut piyasa durumunu özetle (RSI, EMA200, ADX, Bollinger)
   - Sentiment skorunu değerlendir
   - Makro verilerle korelasyonu analiz et (Gold, DXY, S&P 500)
   - **HEM LONG HEM SHORT perspektifinden** değerlendir
   - 1:2 R:R kuralına uygun pozisyon önerisi sun

5. **Strateji Seçimi** (Decision Matrix):

   | Fiyat vs EMA 200 | RSI Aralığı | ADX | Önerilen Aksiyon |
   |------------------|-------------|-----|------------------|
   | ÜSTÜNDE | < 35 | > 25 | **LONG** (Trend Pullback) |
   | ÜSTÜNDE | > 70 | > 25 | BEKLE (aşırı alım) |
   | ALTINDA | > 60 | > 25 | **SHORT** (Trend Continuation) |
   | ALTINDA | < 35 | > 25 | BEKLE (aşırı satım) |
   | HERHANGİ | 40-60 | < 20 | Grid Trading veya BEKLE |

## Çıktı Formatı

```markdown
## 📊 BTC/USDT Analiz Özeti

**Tarih**: [tarih]
**Fiyat**: $[fiyat]
**Trend**: [Yükseliş / Düşüş / Yatay]

### Teknik Göstergeler
| Gösterge | Değer | Yorum |
|----------|-------|-------|
| RSI (14) | X | Aşırı alım/satım/nötr |
| EMA 200 | $X | Fiyat üstünde/altında |
| ADX | X | Trend güçlü/zayıf |
| Bollinger Pozisyon | %X | Alt/orta/üst banda yakın |
| ATR | $X | Volatilite seviyesi |

### Makro Korelasyon
- Gold: [trend] → Kripto için [bullish/bearish]
- DXY: [trend] → Kripto için [bullish/bearish]
- S&P 500: [trend] → Risk iştahı [yüksek/düşük]

### Sentiment
Skor: X.XX (Bullish/Bearish/Nötr)

---

## 🟢 LONG Değerlendirmesi

**Koşullar**:
- Fiyat > EMA 200: [✅/❌] ($X vs $X)
- RSI < 35: [✅/❌] (RSI: X)
- ADX > 25: [✅/❌] (ADX: X)

**Karar**: [LONG / BEKLE]

Eğer LONG uygunsa:
| Parametre | Değer |
|-----------|-------|
| Giriş | $X |
| Stop Loss | $X (%X risk) |
| Take Profit | $X (%X reward) |
| R:R Oranı | X:1 [✅ Uygun / ⚠️ Yetersiz] |

---

## 🔴 SHORT Değerlendirmesi

**Koşullar**:
- Fiyat < EMA 200: [✅/❌] ($X vs $X)
- RSI > 60: [✅/❌] (RSI: X)
- ADX > 25: [✅/❌] (ADX: X)

**Karar**: [SHORT / BEKLE]

Eğer SHORT uygunsa:
| Parametre | Değer |
|-----------|-------|
| Giriş | $X (bounce bekle) |
| Stop Loss | $X (%X risk) |
| Take Profit | $X (%X reward) |
| R:R Oranı | X:1 [✅ Uygun / ⚠️ Yetersiz] |

---

## 📈 Backtest Kanıtları

### LONG Sinyalleri (Son 3)
| Tarih | Sonuç | P&L |
|-------|-------|-----|
| ... | TP/SL | %X |

**Win Rate**: X/3 = X%

### SHORT Sinyalleri (Son 3)
| Tarih | Sonuç | P&L |
|-------|-------|-----|
| ... | TP/SL | %X |

**Win Rate**: X/3 = X%

---

## 📋 Özet

| Yön | Durum | Güven | Aksiyon |
|-----|-------|-------|---------|
| LONG | [Uygun/Bekle] | [Yüksek/Orta/Düşük] | [Giriş/İzle] |
| SHORT | [Uygun/Bekle] | [Yüksek/Orta/Düşük] | [Giriş/İzle] |

### 🚨 Alarm Seviyeleri
- LONG için izle: $X (EMA 200 üzeri)
- SHORT için izle: $X (RSI > 60 bounce)

**Risk Uyarısı**: Bu analiz yatırım tavsiyesi değildir. 1:2 R:R kuralı sağlanmadan işlem yapılmamalıdır.
```
