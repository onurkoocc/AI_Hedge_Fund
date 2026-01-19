
```markdown
# 🏛️ AI-Driven Hedge Fund: Project Blueprint & Specs

Bu döküman, kişisel bir "Yapay Zeka Destekli Ticaret Sistemi"nin mimarisini, kurallarını ve teknik gereksinimlerini tanımlar. Bir LLM (Language Model) bu dökümanı okuyarak projenin dosya yapısını kurmalı, kuralları (specs) oluşturmalı ve gerekli Python araçlarını kodlamalıdır.

## 1. Proje Vizyonu
*   **Amaç:** Aylık kümülatif **%7 bakiye büyümesi** sağlamak.
*   **Yaklaşım:** Duygusuz, matematiksel, veriye dayalı ve disiplinli.
*   **Kısıtlar:** Sadece **ücretsiz** veri kaynakları kullanılacak (ccxt, yfinance, feedparser).
*   **Davranış:** Fanatizm yok. Piyasa koşuluna göre Long, Short, Hedge veya Grid stratejileri uygulanır.

---

## 2. Klasör ve Dosya Mimarisi (Spec-Kit Structure)

Proje, kuralların koddan ayrıldığı "Spec-Driven" bir yapıda olacaktır.

```text
AI_Hedge_Fund/
│
├── .cursorrules (veya prompt_instructions.md) # LLM için "Önce specs klasörünü oku" talimatı
├── PROJECT_BLUEPRINT.md       # (BU DOSYA) Projenin ana planı
├── requirements.txt           # Bağımlılıklar: ccxt, yfinance, pandas-ta, textblob, feedparser
│
├── specs/                     # [ANAYASA] Sistemin kuralları (LLM burayı referans alır)
│   ├── 01_mission.md          # Hedefler ve psikoloji
│   ├── 02_risk_rules.md       # 1:2 Kuralı, Stop-Loss ve Pozisyon Büyüklüğü
│   ├── 03_data_sources.md     # Takip edilecek varlıklar ve kaynaklar
│   └── 04_strategies.md       # Strateji mantıkları (Trend, Grid, Pair)
│
├── src/                       # [MOTOR] Hesaplama modülleri
│   ├── data_loader.py         # Veri çekme (Crypto, Macro, News)
│   ├── analysis.py            # Teknik analiz ve Sentiment hesaplamaları
│   └── backtester.py          # (KRİTİK) "Son 3 İşlem" doğrulama motoru
│
├── tools/                     # [ARAÇLAR] Çalıştırılabilir scriptler
│   └── market_scanner.py      # Piyasayı tarar, backtest yapar ve rapor üretir
│
└── output/                    # [ÇIKTI]
    ├── market_snapshot.md     # LLM'e sunulacak günlük özet rapor
    └── trade_journal.json     # İşlem geçmişi

```

---

## 3. Spec Dosyalarının İçeriği (Kurallar)

LLM, `specs/` klasörü altına aşağıdaki dosyaları oluşturmalı ve içeriklerini belirtilen kurallara göre yazmalıdır.

### `specs/01_mission.md`

* **Hedef:** Ayda maksimum **5 adet "Sniper" (seçkin) işlem**.
* **Odak:** BTC, ETH, SOL, BNB, XRP gibi likiditesi yüksek varlıklar.
* **Mantık:** Sadece o ayki %7 hedefine odaklan. Piyasa ne veriyorsa onu al.

### `specs/02_risk_rules.md` (Çok Önemli)

1. **Risk/Ödül (R:R) Kuralı:**
* Her işlemde `(Hedef - Giriş) / (Giriş - Stop)` oranı **minimum 1:2** olmalıdır.
* Bu oranı sağlamayan setup'lar reddedilmelidir.


2. **Mini-Backtest Validasyonu:**
* Bir işlem önerilmeden önce, ilgili stratejinin **son 3 sinyali** simüle edilmelidir.
* Bu 3 işlemin sonucu (Kar/Zarar durumu) kullanıcıya raporlanmalıdır.


3. **İşlem Detayları:**
* Her öneride; Giriş Fiyatı (Limit/Market), Stop-Loss ve Kar Al (TP) noktaları net olarak belirtilmelidir.



### `specs/03_data_sources.md`

* **Kripto:** Binance verileri (`ccxt` kütüphanesi - public API).
* **Makro:** Altın (GC=F), DXY (DX-Y.NYB), S&P 500 (`yfinance` kütüphanesi).
* **Sentiment:**
* RSS Haber Başlıkları (Cointelegraph vb.) -> `feedparser` ile çekilip `TextBlob` ile puanlanacak.
* Fear & Greed Index (API).



### `specs/04_strategies.md`

1. **Trend:** Fiyat > EMA200 ve DXY Düşüşte ise Pullback'lerde Long.
2. **Pair Trading (Hedge):** Piyasa belirsizse; Güçlü olanı LONG, Zayıf olanı SHORT yap (Korelasyon analizi).
3. **Grid:** Piyasa yataysa (ADX < 20), Bollinger bantları arasında işlem aralığı belirle.

---

## 4. Python Modül Gereksinimleri

LLM, `src/` klasöründeki kodları aşağıdaki işlevleri yerine getirecek şekilde yazmalıdır:

### `src/backtester.py` (Kanıt Motoru)

Bu script, klasik bir backtest aracı değil, bir **"Sinyal Doğrulayıcı"**dır.

* **Girdi:** Bir strateji koşulu (Örn: `RSI < 30` ve `Close > EMA200`) ve Coin (BTC).
* **İşlem:** Geçmiş veriyi tarar ve bu koşulun oluştuğu **son 3 zamanı** bulur. Her biri için işlem sonucunu (TP oldu mu, Stop mu oldu?) hesaplar.
* **Çıktı:** `[{tarih: "...", sonuc: "%5 Kar"}, {tarih: "...", sonuc: "Stop"}]`

### `src/analysis.py`

* Teknik indikatörleri hesaplar (RSI, ATR, EMA, Bollinger, ADX).
* Makro verilerle kripto verilerini zaman serisi olarak eşleştirir.

### `tools/market_scanner.py` (Ana Araç)

Bu script çalıştırıldığında:

1. Tüm verileri (Kripto + Makro + Sentiment) günceller.
2. `specs/` altındaki stratejileri tarar.
3. Sinyal bulursa `src/backtester.py`'ı çalıştırarak **"Son 3 İşlem Performansı"nı** rapora ekler.
4. Sonuçları `output/market_snapshot.md` dosyasına Markdown formatında yazar.

---

## 5. İş Akışı (Workflow)

1. **Çalıştır:** `python tools/market_scanner.py` komutu çalıştırılır.
2. **Oku:** Oluşan `output/market_snapshot.md` dosyası LLM tarafından okunur.
3. **Sor:** Kullanıcı sorar: *"Snapshot'a göre BTCUSDT için kurallarıma uyan işlem var mı?"*
4. **Yanıtla:** LLM, `specs/02_risk_rules.md` dosyasındaki 1:2 kuralını ve rapordaki backtest sonucunu kontrol ederek nihai öneriyi sunar.

```

```