"""BTC/USDT & ETH/USDT Combined Analysis Script"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data_loader import fetch_crypto_data, fetch_macro_data
from src.analysis import calculate_indicators
import pandas as pd

def analyze_asset(symbol, days=180):
    """Analyze a single asset and return metrics"""
    df = fetch_crypto_data(symbol, days=days)
    df = calculate_indicators(df)
    last = df.tail(1).iloc[0]
    
    # Calculate 30-day change
    prev_30d = df.iloc[-30]['close'] if len(df) >= 30 else df.iloc[0]['close']
    change_30d = (last['close'] - prev_30d) / prev_30d * 100
    
    # Calculate 7-day change
    prev_7d = df.iloc[-7]['close'] if len(df) >= 7 else df.iloc[0]['close']
    change_7d = (last['close'] - prev_7d) / prev_7d * 100
    
    # Bollinger position
    bb_range = last['bb_upper'] - last['bb_lower']
    bb_position = (last['close'] - last['bb_lower']) / bb_range * 100 if bb_range > 0 else 50
    
    return {
        'df': df,
        'last': last,
        'price': last['close'],
        'rsi': last['rsi'],
        'ema_200': last['ema_200'],
        'adx': last['adx'],
        'atr': last['atr'],
        'bb_lower': last['bb_lower'],
        'bb_mid': last['bb_mid'],
        'bb_upper': last['bb_upper'],
        'bb_position': bb_position,
        'above_ema': last['close'] > last['ema_200'],
        'change_30d': change_30d,
        'change_7d': change_7d,
    }

print("=" * 80)
print("BTC/USDT & ETH/USDT KOMBINE PIYASA ANALIZI")
print("=" * 80)
print()

# Fetch and analyze both assets
print("Fetching BTC/USDT data...")
btc = analyze_asset('BTC/USDT')
print("Fetching ETH/USDT data...")
eth = analyze_asset('ETH/USDT')

print()
print("KARSILASTIRMALI TEKNIK ANALIZ")
print("-" * 80)
print(f"{'Gosterge':<20} {'BTC/USDT':<25} {'ETH/USDT':<25}")
print("-" * 80)
print(f"{'Fiyat':<20} ${btc['price']:>20,.2f} ${eth['price']:>20,.2f}")
print(f"{'RSI (14)':<20} {btc['rsi']:>23.2f} {eth['rsi']:>23.2f}")
print(f"{'EMA 200':<20} ${btc['ema_200']:>20,.2f} ${eth['ema_200']:>20,.2f}")
print(f"{'ADX':<20} {btc['adx']:>23.2f} {eth['adx']:>23.2f}")
print(f"{'ATR':<20} ${btc['atr']:>20,.2f} ${eth['atr']:>20,.2f}")
print(f"{'BB Lower':<20} ${btc['bb_lower']:>20,.2f} ${eth['bb_lower']:>20,.2f}")
print(f"{'BB Upper':<20} ${btc['bb_upper']:>20,.2f} ${eth['bb_upper']:>20,.2f}")
print(f"{'BB Pozisyon %':<20} {btc['bb_position']:>23.1f} {eth['bb_position']:>23.1f}")
print(f"{'EMA 200 Uzerinde':<20} {'EVET' if btc['above_ema'] else 'HAYIR':>23} {'EVET' if eth['above_ema'] else 'HAYIR':>23}")
print(f"{'7 Gun Degisim':<20} {btc['change_7d']:>22.2f}% {eth['change_7d']:>22.2f}%")
print(f"{'30 Gun Degisim':<20} {btc['change_30d']:>22.2f}% {eth['change_30d']:>22.2f}%")

print()
print("BTC/ETH ORANI")
print("-" * 80)
btc_eth_ratio = btc['price'] / eth['price']
print(f"  Mevcut BTC/ETH Orani: {btc_eth_ratio:.4f}")

# Calculate 30-day average ratio
btc_30 = btc['df'].tail(30)['close'].values
eth_30 = eth['df'].tail(30)['close'].values
min_len = min(len(btc_30), len(eth_30))
ratios = btc_30[:min_len] / eth_30[:min_len]
avg_ratio = ratios.mean()
print(f"  30 Gunluk Ortalama: {avg_ratio:.4f}")

if btc_eth_ratio > avg_ratio * 1.02:
    ratio_comment = "BTC nispeten guclu (ETH zayif)"
elif btc_eth_ratio < avg_ratio * 0.98:
    ratio_comment = "ETH nispeten guclu (BTC zayif)"
else:
    ratio_comment = "Dengeli"
print(f"  Yorum: {ratio_comment}")

# Determine stronger asset
if btc['change_30d'] > eth['change_30d']:
    stronger = "BTC"
    stronger_pct = btc['change_30d'] - eth['change_30d']
else:
    stronger = "ETH"
    stronger_pct = eth['change_30d'] - btc['change_30d']
print(f"  30 Gunluk Performansta Guclu: {stronger} (+{stronger_pct:.2f}% fark)")

print()
print("MAKRO KORELASYON")
print("-" * 80)
try:
    gold = fetch_macro_data('GC=F', days=30)
    if not gold.empty:
        gold_last = gold['close'].iloc[-1]
        gold_prev = gold['close'].iloc[-5]
        gold_change = (gold_last - gold_prev) / gold_prev * 100
        gold_trend = "Yukselis" if gold_change > 0 else "Dusus"
        gold_crypto = "Bullish (guvenli liman talebi)" if gold_change > 0 else "Notr"
        print(f"  Gold: ${gold_last:,.2f} ({gold_change:+.2f}% 5 gun) - {gold_trend} -> Kripto icin {gold_crypto}")
except Exception as e:
    print(f"  Gold: Veri alinamadi")

try:
    dxy = fetch_macro_data('DX-Y.NYB', days=30)
    if not dxy.empty:
        dxy_last = dxy['close'].iloc[-1]
        dxy_prev = dxy['close'].iloc[-5]
        dxy_change = (dxy_last - dxy_prev) / dxy_prev * 100
        dxy_trend = "Yukselis" if dxy_change > 0 else "Dusus"
        dxy_crypto = "Bearish (dolar gucleniyor)" if dxy_change > 0 else "Bullish (dolar zayifliyor)"
        print(f"  DXY: {dxy_last:.2f} ({dxy_change:+.2f}% 5 gun) - {dxy_trend} -> Kripto icin {dxy_crypto}")
except Exception as e:
    print(f"  DXY: Veri alinamadi")

try:
    sp500 = fetch_macro_data('^GSPC', days=30)
    if not sp500.empty:
        sp_last = sp500['close'].iloc[-1]
        sp_prev = sp500['close'].iloc[-5]
        sp_change = (sp_last - sp_prev) / sp_prev * 100
        sp_trend = "Yukselis" if sp_change > 0 else "Dusus"
        risk_appetite = "Yuksek risk istahi" if sp_change > 0 else "Dusuk risk istahi"
        print(f"  S&P 500: {sp_last:,.2f} ({sp_change:+.2f}% 5 gun) - {sp_trend} -> {risk_appetite}")
except Exception as e:
    print(f"  S&P 500: Veri alinamadi")

print()
print("STRATEJI KONTROLU")
print("-" * 80)

# Trend Pullback: close > ema_200 and rsi < 35 and adx > 25
btc_trend = btc['above_ema'] and btc['rsi'] < 35 and btc['adx'] > 25
eth_trend = eth['above_ema'] and eth['rsi'] < 35 and eth['adx'] > 25
print(f"  Trend Pullback (Long):")
print(f"    BTC: {'SINYAL VAR!' if btc_trend else 'Kosul yok'} (EMA:{btc['above_ema']}, RSI<35:{btc['rsi']<35}, ADX>25:{btc['adx']>25})")
print(f"    ETH: {'SINYAL VAR!' if eth_trend else 'Kosul yok'} (EMA:{eth['above_ema']}, RSI<35:{eth['rsi']<35}, ADX>25:{eth['adx']>25})")

# Grid Trading: adx < 20 and close > bb_lower and close < bb_upper
btc_grid = btc['adx'] < 20 and btc['price'] > btc['bb_lower'] and btc['price'] < btc['bb_upper']
eth_grid = eth['adx'] < 20 and eth['price'] > eth['bb_lower'] and eth['price'] < eth['bb_upper']
print(f"  Grid Trading:")
print(f"    BTC: {'SINYAL VAR!' if btc_grid else 'Kosul yok'} (ADX<20:{btc['adx']<20})")
print(f"    ETH: {'SINYAL VAR!' if eth_grid else 'Kosul yok'} (ADX<20:{eth['adx']<20})")

# Breakout: close > bb_upper and rsi > 60
btc_breakout = btc['price'] > btc['bb_upper'] and btc['rsi'] > 60
eth_breakout = eth['price'] > eth['bb_upper'] and eth['rsi'] > 60
print(f"  Breakout:")
print(f"    BTC: {'SINYAL VAR!' if btc_breakout else 'Kosul yok'} (BB ustunde:{btc['price']>btc['bb_upper']}, RSI>60:{btc['rsi']>60})")
print(f"    ETH: {'SINYAL VAR!' if eth_breakout else 'Kosul yok'} (BB ustunde:{eth['price']>eth['bb_upper']}, RSI>60:{eth['rsi']>60})")

print()
print("POZISYON ONERILERI")
print("-" * 80)

# Determine BTC recommendation
btc_reco = "BEKLE"
btc_confidence = "Dusuk"
btc_reason = []

if btc['above_ema']:
    if btc['rsi'] < 35:
        btc_reco = "LONG"
        btc_confidence = "Yuksek"
        btc_reason.append("RSI asiri satim bolgesi")
    elif btc['rsi'] < 45:
        btc_reco = "LONG"
        btc_confidence = "Orta"
        btc_reason.append("RSI orta-dusuk seviyelerde")
else:
    if btc['rsi'] < 30:
        btc_reco = "LONG"
        btc_confidence = "Orta"
        btc_reason.append("RSI asiri satim")
    elif btc['rsi'] > 70:
        btc_reco = "SHORT"
        btc_confidence = "Orta"
        btc_reason.append("RSI asiri alim")
    else:
        btc_reason.append("EMA altinda, trend belirsiz")

if btc['adx'] > 25:
    btc_reason.append("Guclu trend mevcut")
else:
    btc_reason.append("Zayif trend")

# Determine ETH recommendation
eth_reco = "BEKLE"
eth_confidence = "Dusuk"
eth_reason = []

if eth['above_ema']:
    if eth['rsi'] < 35:
        eth_reco = "LONG"
        eth_confidence = "Yuksek"
        eth_reason.append("RSI asiri satim bolgesi")
    elif eth['rsi'] < 45:
        eth_reco = "LONG"
        eth_confidence = "Orta"
        eth_reason.append("RSI orta-dusuk seviyelerde")
else:
    if eth['rsi'] < 30:
        eth_reco = "LONG"
        eth_confidence = "Orta"
        eth_reason.append("RSI asiri satim")
    elif eth['rsi'] > 70:
        eth_reco = "SHORT"
        eth_confidence = "Orta"
        eth_reason.append("RSI asiri alim")
    else:
        eth_reason.append("EMA altinda, trend belirsiz")

if eth['adx'] > 25:
    eth_reason.append("Guclu trend mevcut")
else:
    eth_reason.append("Zayif trend")

# Calculate stop loss and take profit levels
# Stop Loss: Below recent low or 2% from entry
# Take Profit: Based on ATR or 5% from entry

btc_stop = btc['bb_lower'] - btc['atr'] * 0.5
btc_tp = btc['price'] + btc['atr'] * 3
btc_risk = (btc['price'] - btc_stop) / btc['price'] * 100
btc_reward = (btc_tp - btc['price']) / btc['price'] * 100
btc_rr = btc_reward / btc_risk if btc_risk > 0 else 0

eth_stop = eth['bb_lower'] - eth['atr'] * 0.5
eth_tp = eth['price'] + eth['atr'] * 3
eth_risk = (eth['price'] - eth_stop) / eth['price'] * 100
eth_reward = (eth_tp - eth['price']) / eth['price'] * 100
eth_rr = eth_reward / eth_risk if eth_risk > 0 else 0

print(f"  BTC/USDT:")
print(f"    Karar: {btc_reco}")
print(f"    Guven: {btc_confidence}")
print(f"    Nedenler: {', '.join(btc_reason)}")
if btc_reco != "BEKLE":
    print(f"    Giris: ${btc['price']:,.2f}")
    print(f"    Stop Loss: ${btc_stop:,.2f} ({btc_risk:.2f}%)")
    print(f"    Take Profit: ${btc_tp:,.2f} ({btc_reward:.2f}%)")
    print(f"    R:R Orani: {btc_rr:.2f}:1 {'(Uygun)' if btc_rr >= 2 else '(Yetersiz - 2:1 gerekli)'}")

print()
print(f"  ETH/USDT:")
print(f"    Karar: {eth_reco}")
print(f"    Guven: {eth_confidence}")
print(f"    Nedenler: {', '.join(eth_reason)}")
if eth_reco != "BEKLE":
    print(f"    Giris: ${eth['price']:,.2f}")
    print(f"    Stop Loss: ${eth_stop:,.2f} ({eth_risk:.2f}%)")
    print(f"    Take Profit: ${eth_tp:,.2f} ({eth_reward:.2f}%)")
    print(f"    R:R Orani: {eth_rr:.2f}:1 {'(Uygun)' if eth_rr >= 2 else '(Yetersiz - 2:1 gerekli)'}")

print()
print("PAIR TRADING FIRSATI")
print("-" * 80)
strength_diff = abs(btc['change_30d'] - eth['change_30d'])
if strength_diff > 5:
    print(f"  Fark: {strength_diff:.2f}% - PAIR TRADING UYGUN!")
    if btc['change_30d'] > eth['change_30d']:
        print(f"  Oneri: LONG BTC / SHORT ETH")
    else:
        print(f"  Oneri: LONG ETH / SHORT BTC")
else:
    print(f"  Fark: {strength_diff:.2f}% - Pair trading icin yeterli fark yok")

print()
print("=" * 80)
print("OZET")
print("=" * 80)
print(f"  BTC/USDT: {btc_reco} (Guven: {btc_confidence})")
print(f"  ETH/USDT: {eth_reco} (Guven: {eth_confidence})")
print()
print("  UYARI: Bu analiz yatirim tavsiyesi degildir!")
print("  1:2 R:R kurali saglanmadan islem yapilmamalidir.")
print("=" * 80)
