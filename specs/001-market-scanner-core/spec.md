# Feature Specification: Market Scanner Core System

**Feature Branch**: `001-market-scanner-core`  
**Created**: January 19, 2026  
**Status**: Draft  
**Input**: User description: "PROJECT_BLUEPRINT.md dosyasındaki '2. Klasör ve Dosya Mimarisi' ve '4. Python Modül Gereksinimleri' bölümlerini temel al. src/backtester.py: Kanıt Motoru, tools/market_scanner.py: Ana araç, specs/ klasörü: LLM kural setleri. Kütüphaneler: ccxt, yfinance, pandas-ta, textblob, feedparser"

---

## Summary

Bu özellik, AI-Driven Hedge Fund projesinin temel altyapısını oluşturur: Piyasa verilerini toplayan, stratejileri tarayan, geçmiş sinyalleri doğrulayan ve LLM'e sunulacak raporlar üreten bir "Market Scanner Core System".

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Piyasa Taraması ve Rapor Üretimi (Priority: P1)

Bir yatırımcı olarak, tek bir komut çalıştırarak tüm piyasa verilerini (kripto, makro, sentiment) toplayıp, tanımlı stratejilere göre sinyalleri tarayıp, sonuçları Markdown formatında okumak istiyorum.

**Why this priority**: Bu, sistemin ana işlevi. Kullanıcı günlük olarak bu komutu çalıştırarak piyasa durumunu öğrenecek.

**Independent Test**: `python tools/market_scanner.py` komutu çalıştırılır ve `output/market_snapshot.md` dosyası başarıyla oluşturulur.

**Acceptance Scenarios**:

1. **Given** sistem kurulu ve bağımlılıklar yüklenmiş durumda, **When** `python tools/market_scanner.py` çalıştırıldığında, **Then** `output/market_snapshot.md` dosyası Markdown formatında oluşturulur.
2. **Given** internet bağlantısı mevcut, **When** tarama çalıştırıldığında, **Then** BTC, ETH, SOL, BNB, XRP için güncel veriler çekilir.
3. **Given** `specs/04_strategies.md` dosyasında stratejiler tanımlı, **When** tarama yapıldığında, **Then** her strateji için aktif sinyal olup olmadığı kontrol edilir.

---

### User Story 2 - Sinyal Doğrulama (Backtest Kanıtı) (Priority: P1)

Bir yatırımcı olarak, herhangi bir strateji sinyali bulunduğunda, o stratejinin geçmişteki son 3 sinyalinin performansını görmek istiyorum ki kararımı kanıta dayandırabileyim.

**Why this priority**: Risk yönetiminin kritik parçası. Her işlem önerisinin geçmiş performansı ile doğrulanması gerekiyor.

**Independent Test**: Belirli bir strateji koşulu için Backtester çağrılır ve son 3 sinyal sonucu JSON formatında döner.

**Acceptance Scenarios**:

1. **Given** bir strateji koşulu (örn: RSI < 30 ve Close > EMA200) ve bir varlık (BTC), **When** Backtester çalıştırıldığında, **Then** bu koşulun oluştuğu son 3 tarihi bulur.
2. **Given** son 3 sinyal tarihi bulunmuş, **When** her sinyal için simülasyon yapıldığında, **Then** her birinin sonucu (% Kar veya Stop) hesaplanır.
3. **Given** backtest tamamlanmış, **When** sonuç döndürüldüğünde, **Then** JSON formatında `[{tarih, sonuc}, ...]` yapısında rapor oluşturulur.

---

### User Story 3 - Teknik Analiz Hesaplamaları (Priority: P2)

Bir sistem olarak, ham fiyat verilerinden teknik indikatörleri (RSI, EMA, ATR, Bollinger, ADX) hesaplayabilmeli ve makro verilerle eşleştirebilmeliyim.

**Why this priority**: Stratejilerin çalışması için teknik indikatörlerin doğru hesaplanması gerekli.

**Independent Test**: Fiyat verisi verildiğinde, tüm teknik indikatörler doğru şekilde hesaplanır ve DataFrame olarak döner.

**Acceptance Scenarios**:

1. **Given** BTC için OHLCV fiyat verisi, **When** analysis modülü çalıştırıldığında, **Then** RSI, EMA200, ATR, Bollinger Bantları ve ADX değerleri hesaplanır.
2. **Given** makro veriler (DXY, Altın, S&P500) çekilmiş, **When** analiz yapıldığında, **Then** kripto ve makro veriler zaman serisinde eşleştirilir.

---

### User Story 4 - Veri Toplama (Priority: P2)

Bir sistem olarak, farklı kaynaklardan (kripto borsası, makro piyasalar, haber RSS) verileri çekebilmeliyim.

**Why this priority**: Tüm analizler güncel veriye bağlı.

**Independent Test**: Her veri kaynağından bağımsız olarak veri çekilebilir.

**Acceptance Scenarios**:

1. **Given** Binance public API erişimi mevcut, **When** kripto verisi istendiğinde, **Then** ccxt ile OHLCV verisi çekilir.
2. **Given** yfinance erişimi mevcut, **When** makro veriler istendiğinde, **Then** Altın (GC=F), DXY (DX-Y.NYB), S&P 500 verileri çekilir.
3. **Given** RSS feed URL'leri tanımlı, **When** sentiment analizi istendiğinde, **Then** haber başlıkları feedparser ile çekilip TextBlob ile puanlanır.

---

### User Story 5 - Kural Seti Yönetimi (Priority: P3)

Bir LLM olarak, `specs/` klasöründeki kural dosyalarını okuyarak strateji mantıklarını ve risk kurallarını anlayabilmeliyim.

**Why this priority**: LLM'in doğru öneriler yapabilmesi için kuralları anlaması gerekli.

**Independent Test**: `specs/` klasöründeki dosyalar okunabilir ve parse edilebilir yapıda.

**Acceptance Scenarios**:

1. **Given** `specs/04_strategies.md` dosyası mevcut, **When** dosya okunduğunda, **Then** Trend, Pair Trading ve Grid stratejileri tanımları erişilebilir.
2. **Given** `specs/02_risk_rules.md` dosyası mevcut, **When** dosya okunduğunda, **Then** 1:2 R:R kuralı ve Mini-Backtest gereksinimleri erişilebilir.

---

### Edge Cases

- **Yetersiz geçmiş veri**: Bir varlık için 3'ten az sinyal bulunursa, sistem mevcut sinyal sayısını raporlar ve uyarı verir
- **İnternet bağlantı hatası**: Hata mesajı loglanır, mevcut cache varsa kullanılır, kısmi rapor üretilir
- **Sinyal bulunamama**: Strateji koşulu hiç sinyale uymuyorsa "Sinyal yok" durumu raporda belirtilir
- **RSS erişim hatası**: Sentiment skoru "N/A" olarak işaretlenir, diğer veriler işlenmeye devam eder
- **API rate limit**: İstek limitlerine takılındığında bekleyip yeniden deneme yapılır

---

## Requirements *(mandatory)*

### Functional Requirements

#### Veri Toplama (data_loader.py)

- **FR-001**: Sistem, Binance'den ccxt kütüphanesi ile kripto OHLCV verisi çekebilMELİ (BTC, ETH, SOL, BNB, XRP)
- **FR-002**: Sistem, yfinance ile makro verileri çekebilMELİ (Altın GC=F, DXY DX-Y.NYB, S&P 500)
- **FR-003**: Sistem, feedparser ile RSS haber başlıklarını çekebilMELİ
- **FR-004**: Sistem, TextBlob ile haber başlıklarından sentiment skoru hesaplayabilMELİ

#### Teknik Analiz (analysis.py)

- **FR-005**: Sistem, pandas-ta ile RSI indikatörü hesaplayabilMELİ
- **FR-006**: Sistem, EMA (özellikle EMA200) hesaplayabilMELİ
- **FR-007**: Sistem, ATR (Average True Range) hesaplayabilMELİ
- **FR-008**: Sistem, Bollinger Bantları hesaplayabilMELİ
- **FR-009**: Sistem, ADX (Average Directional Index) hesaplayabilMELİ
- **FR-010**: Sistem, kripto ve makro verileri zaman serisinde eşleştirebilMELİ

#### Backtest / Kanıt Motoru (backtester.py)

- **FR-011**: Sistem, verilen strateji koşulu için geçmiş veride son 3 sinyali bulabilMELİ
- **FR-012**: Sistem, her sinyal için işlem simülasyonu yapabilMELİ (TP veya Stop sonucu)
- **FR-013**: Sistem, backtest sonuçlarını JSON formatında döndürMELİ
- **FR-014**: Sistem, yeterli sinyal bulunamazsa (3'ten az) mevcut sayıyı raporlayabilMELİ

#### Market Scanner (tools/market_scanner.py)

- **FR-015**: Sistem, tüm veri kaynaklarını tek komutla güncelleyebilMELİ
- **FR-016**: Sistem, `specs/04_strategies.md` dosyasındaki stratejileri okuyup uygulayabilMELİ
  - Strateji koşulları **Pandas Query String** formatında tanımlanacak (Örn: `"rsi < 30 and close > ema_200"`)
  - Bu format, `df.query()` ile doğrudan uygulanabilir olmalı
- **FR-016a**: Sistem, tüm DataFrame sütun isimlerini **lowercase snake_case** formatına standardize etMELİ (Örn: `Close` → `close`, `EMA200` → `ema_200`)
  - Bu standardizasyon, veri yükleme sonrasında ve strateji değerlendirmesinden önce yapılmalı
  - KeyError hatalarını önlemek için kritik bir gerekliliktir
- **FR-017**: Sistem, sinyal bulunduğunda otomatik olarak Backtester'ı çağırabilMELİ
- **FR-018**: Sistem, sonuçları `output/market_snapshot.md` dosyasına Markdown formatında yazabilMELİ

#### Kural Setleri (specs/ klasörü)

- **FR-019**: Sistem, `specs/01_mission.md` dosyasında hedef ve odak kurallarını tanımlayabilMELİ
- **FR-020**: Sistem, `specs/02_risk_rules.md` dosyasında R:R kuralını ve backtest gereksinimini tanımlayabilMELİ
- **FR-021**: Sistem, `specs/03_data_sources.md` dosyasında veri kaynaklarını tanımlayabilMELİ
- **FR-022**: Sistem, `specs/04_strategies.md` dosyasında Trend, Pair Trading ve Grid stratejilerini tanımlayabilMELİ
  - Her strateji, **Pandas Query String** formatında koşul ifadesi içerMELİ
  - Örnek format: `condition: "rsi < 30 and close > ema_200 and adx > 25"`
  - Tüm sütun adları lowercase snake_case formatında olmalı

### Key Entities (Pandas query string formatında), strateji tipi (Trend/Pair/Grid), hedef varlıklar
  - Örnek: `{"name": "Trend Pullback", "condition": "rsi < 30 and close > ema_200", "type": "Long"}`

- **Asset (Varlık)**: Takip edilen finansal enstrüman (BTC, ETH, Altın vb.). Özellikleri: sembol, kaynak türü (kripto/makro), fiyat verileri
- **Strategy (Strateji)**: Alım/satım sinyali üreten kural seti. Özellikleri: ad, koşullar, strateji tipi (Trend/Pair/Grid)
- **Signal (Sinyal)**: Bir stratejinin ürettiği alım/satım tetikleyicisi. Özellikleri: tarih, varlık, strateji, yön (Long/Short)
- **Backtest Result (Backtest Sonucu)**: Geçmiş sinyalin performansı. Özellikleri: tarih, sonuç (% Kar veya Stop), sinyal referansı
- **Market Snapshot (Piyasa Özeti)**: Güncel durum raporu. Özellikleri: tarih, varlık özetleri, aktif sinyaller, backtest kanıtları

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Kullanıcı, tek bir terminal komutu ile tüm piyasa taramasını tamamlayabilmeli (2 dakika içinde)
- **SC-002**: Her sinyal önerisi, son 3 geçmiş sinyalin performans kanıtı ile desteklenmeli
- **SC-003**: Üretilen rapor, LLM tarafından okunabilir ve yorumlanabilir formatta olmalı (Markdown)
- **SC-004**: Sistem, en az 5 kripto varlık ve 3 makro varlık için veri toplayabilmeli
- **SC-005**: Teknik indikatörler (RSI, EMA, ATR, Bollinger, ADX) %99 doğrulukla hesaplanmalı
- **SC-006**: Sentiment analizi, haber başlıklarından -1 ile +1 arasında skor üretebilmeli
- **SC-007**: Backtest motoru, strateji koşulu verilen herhangi bir varlık için 30 saniye içinde sonuç döndürmeli
- **SC-008**: Sistem, internet erişim hatalarında graceful degradation sağlamalı (kısmi rapor üretebilmeli)

---

## Assumptions

1. Kullanıcının Python 3.9+ kurulu olduğu varsayılır
2. Kullanıcının internet bağlantısı olduğu varsayılır
6. Strateji koşulları Pandas Query String formatında yazılır ve `df.query()` ile değerlendirilir
7. Tüm DataFrame sütun isimleri lowercase snake_case formatında standardize edilir
3. Binance public API'sine erişim için API key gerekmez (sadece market data)
4. RSS feed'ler İngilizce haber başlıkları içerir (TextBlob İngilizce için optimize)
5. Geçmiş veri en az 6 ay geriye gidebilir (3 sinyal bulabilmek için)

---

## Dependencies

### Python Kütüphaneleri

- `ccxt`: Kripto borsa verileri için
- `yfinance`: Makro piyasa verileri için
- `pandas-ta`: Teknik analiz indikatörleri için
- `textblob`: Sentiment analizi için
- `feedparser`: RSS feed parse etmek için
- `pandas`: Veri manipülasyonu için

### Dış Sistemler

- Binance Public API (kripto verileri)
- Yahoo Finance (makro veriler)
- Haber RSS Feed'leri (sentiment)
