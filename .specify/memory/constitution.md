# AI-Driven Hedge Fund Constitution

## Core Principles

### I. Vizyon Odaklı Disiplin
Projenin tek hedefi ayda kümülatif %7 bakiye büyümesidir. Tüm kararlar duygusuz, matematiksel, veriye dayalı ve disiplinli yaklaşımı korumalıdır.

### II. Spec-Driven Mimari
Tüm iş kuralları `specs/` altında tanımlanır. Uygulama kodu yalnızca bu kuralları uygular; kurallar kodla karıştırılmaz.

### III. Kanıtlanabilir Sinyal Üretimi
Her işlem önerisi, son 3 sinyal üzerinden mini-backtest kanıtı ile desteklenmeden sunulamaz. Kanıt, kullanıcıya açık şekilde raporlanır.

### IV. Strateji Uyarlanabilirliği
Piyasa koşullarına göre Long, Short, Hedge veya Grid stratejileri seçilir. Fanatizm yoktur; sadece veri ve koşullar belirleyicidir.

### V. Ücretsiz Veri Kaynağı Zorunluluğu
Veri temini yalnızca ücretsiz kaynaklardan yapılır ve ücretli/veri lisansı gerektiren kaynaklar kullanılmaz.

## Değiştirilemez Kurallar

1. Ayda %7 kümülatif büyüme hedefi ve disiplinli yaklaşım esastır; bu hedefle çelişen öneri veya davranış üretilemez.
2. Risk/Ödül oranı 1:2'nin altındaki hiçbir işlem önerilemez.
3. Her işlem önerisi öncesi "Son 3 Sinyal" mini-backtest kanıtı sunulmalıdır.
4. Sadece ücretsiz veri kaynakları (ccxt, yfinance, feedparser) kullanılacaktır.

## Spec Dosyaları İçerik Kuralları

- `specs/01_mission.md`: Aylık maksimum 5 "Sniper" işlem hedefi, likit varlıklara odaklanma ve %7 hedefe bağlılık.
- `specs/02_risk_rules.md`: 1:2 R:R kuralı, mini-backtest validasyonu, giriş/stop/TP detaylarının netliği.
- `specs/03_data_sources.md`: Kripto (ccxt), makro (yfinance), sentiment (feedparser + TextBlob) kaynakları.
- `specs/04_strategies.md`: Trend, Pair Trading (Hedge) ve Grid stratejileri koşulları.

## Governance

- Bu anayasa, proje içindeki tüm diğer doküman ve uygulama kararlarının üzerinde kabul edilir.
- Her değişiklik, `specs/` dosyaları ve ilgili kod üzerinde tutarlı güncellemeyi gerektirir.
- Uygulama çıktıları, anayasa ve `specs/` ile çelişmeyecek şekilde doğrulanır.

**Version**: 1.0.0 | **Ratified**: 2026-01-19 | **Last Amended**: 2026-01-19
