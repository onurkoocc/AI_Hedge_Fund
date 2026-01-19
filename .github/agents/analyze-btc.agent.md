---
name: analyze-btc
description: "BTC/USDT tekil analiz ve pozisyon önerisi"
---

# BTC/USDT Piyasa Analizi ve Pozisyon Önerisi

## Görev

1. **Market Scanner'ı çalıştır** (sadece BTC/USDT için):
```bash
python tools/market_scanner.py --symbols BTC/USDT --days 180
```

2. **Oluşan raporu oku**: `output/market_snapshot.md`

3. **Anayasa ve risk kurallarını kontrol et**:
   - [specs/02_risk_rules.md](specs/02_risk_rules.md) - 1:2 R:R kuralı
   - [.specify/memory/constitution.md](.specify/memory/constitution.md) - Temel prensipler

4. **Analiz ve Öneri**:
   - Mevcut piyasa durumunu özetle (RSI, EMA200, ADX, Bollinger)
   - Sentiment skorunu değerlendir
   - Makro verilerle korelasyonu analiz et (Gold, DXY, S&P 500)
   - Aktif sinyal varsa backtest kanıtını göster
   - 1:2 R:R kuralına uygun pozisyon önerisi sun (veya "Bekle" de)

## Çıktı Formatı

```markdown
## 📊 BTC/USDT Analiz Özeti

**Tarih**: [tarih]
**Fiyat**: $[fiyat]

### Teknik Göstergeler
| Gösterge | Değer | Yorum |
|----------|-------|-------|
| RSI (14) | X | Aşırı alım/satım/nötr |
| EMA 200 | $X | Fiyat üstünde/altında |
| ADX | X | Trend güçlü/zayıf |
| Bollinger | X | Alt/orta/üst banda yakın |

### Makro Korelasyon
- Gold: [trend]
- DXY: [trend]
- S&P 500: [trend]

### Sentiment
Skor: X.XX (Bullish/Bearish/Nötr)

### 🎯 Pozisyon Önerisi
**Karar**: [LONG / SHORT / BEKLE]
- Giriş: $X
- Stop Loss: $X (%X)
- Take Profit: $X (%X)
- R:R Oranı: X:1

### 📈 Backtest Kanıtı (Son 3 Sinyal)
| Tarih | Sonuç | P&L |
|-------|-------|-----|
| ... | TP/SL | %X |

**Risk Uyarısı**: Bu analiz yatırım tavsiyesi değildir.
```
