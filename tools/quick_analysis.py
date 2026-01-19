"""Quick BTC/USDT Analysis Script"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data_loader import fetch_crypto_data, fetch_macro_data
from src.analysis import calculate_indicators

# Fetch BTC data
print("Fetching BTC/USDT data...")
df = fetch_crypto_data('BTC/USDT', days=180)
df = calculate_indicators(df)

# Get latest values
last = df.tail(1).iloc[0]
prev = df.tail(2).iloc[0]

print("=" * 60)
print("BTC/USDT TEKNIK ANALIZ")
print("=" * 60)
print(f"Tarih: {df.index[-1]}")
print(f"Fiyat: ${last['close']:,.2f}")
print(f"RSI (14): {last['rsi']:.2f}")
print(f"EMA 200: ${last['ema_200']:,.2f}")
print(f"ADX: {last['adx']:.2f}")
print(f"Bollinger Lower: ${last['bb_lower']:,.2f}")
print(f"Bollinger Mid: ${last['bb_mid']:,.2f}")
print(f"Bollinger Upper: ${last['bb_upper']:,.2f}")
print(f"ATR: ${last['atr']:,.2f}")
print()

# Analysis
price_vs_ema = "ÜSTÜNDE ✅" if last['close'] > last['ema_200'] else "ALTINDA ⚠️"
rsi_status = "Aşırı Satım ✅" if last['rsi'] < 30 else ("Aşırı Alım ⚠️" if last['rsi'] > 70 else "Nötr")
adx_status = "Güçlü Trend ✅" if last['adx'] > 25 else "Zayıf/Yatay"

# Bollinger position
bb_range = last['bb_upper'] - last['bb_lower']
bb_position = (last['close'] - last['bb_lower']) / bb_range * 100

print("YORUMLAR:")
print(f"  Fiyat vs EMA200: {price_vs_ema}")
print(f"  RSI Durumu: {rsi_status}")
print(f"  ADX Trend: {adx_status}")
print(f"  Bollinger Pozisyonu: %{bb_position:.1f} (0=alt, 100=üst)")
print()

# Strategy conditions check
print("STRATEJİ KONTROL:")

# Trend Pullback: close > ema_200 and rsi < 35 and adx > 25
trend_pullback = last['close'] > last['ema_200'] and last['rsi'] < 35 and last['adx'] > 25
print(f"  1. Trend Pullback (Long): {'✅ SİNYAL!' if trend_pullback else '❌ Koşul yok'}")
print(f"     close({last['close']:.0f}) > ema_200({last['ema_200']:.0f}): {last['close'] > last['ema_200']}")
print(f"     rsi({last['rsi']:.1f}) < 35: {last['rsi'] < 35}")
print(f"     adx({last['adx']:.1f}) > 25: {last['adx'] > 25}")

# Grid Trading: adx < 20 and close > bb_lower and close < bb_upper
grid = last['adx'] < 20 and last['close'] > last['bb_lower'] and last['close'] < last['bb_upper']
print(f"  2. Grid Trading: {'✅ SİNYAL!' if grid else '❌ Koşul yok'}")

print()
print("SON 7 GÜN:")
print("-" * 60)
for idx, row in df.tail(7).iterrows():
    print(f"  {idx.strftime('%Y-%m-%d')}: Close=${row['close']:,.0f}, RSI={row['rsi']:.1f}, ADX={row['adx']:.1f}")

# Fetch macro data
print()
print("MAKRO VERİLER:")
print("-" * 60)
try:
    gold = fetch_macro_data('GC=F', days=30)
    if not gold.empty:
        gold_last = gold['close'].iloc[-1]
        gold_prev = gold['close'].iloc[-5]
        gold_change = (gold_last - gold_prev) / gold_prev * 100
        print(f"  Gold: ${gold_last:,.2f} ({gold_change:+.2f}% 5 gün)")
except Exception as e:
    print(f"  Gold: Hata - {e}")

try:
    dxy = fetch_macro_data('DX-Y.NYB', days=30)
    if not dxy.empty:
        dxy_last = dxy['close'].iloc[-1]
        dxy_prev = dxy['close'].iloc[-5]
        dxy_change = (dxy_last - dxy_prev) / dxy_prev * 100
        print(f"  DXY: {dxy_last:.2f} ({dxy_change:+.2f}% 5 gün)")
except Exception as e:
    print(f"  DXY: Hata - {e}")

try:
    sp500 = fetch_macro_data('^GSPC', days=30)
    if not sp500.empty:
        sp_last = sp500['close'].iloc[-1]
        sp_prev = sp500['close'].iloc[-5]
        sp_change = (sp_last - sp_prev) / sp_prev * 100
        print(f"  S&P 500: {sp_last:,.2f} ({sp_change:+.2f}% 5 gün)")
except Exception as e:
    print(f"  S&P 500: Hata - {e}")
