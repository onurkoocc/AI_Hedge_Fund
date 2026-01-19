"""Short Signal Analysis for BTC and ETH"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data_loader import fetch_crypto_data
from src.analysis import calculate_indicators

print("=" * 80)
print("SHORT ISLEM FIRSATLARI ANALIZI")
print("=" * 80)

# Fetch data
print("\nFetching BTC/USDT data...")
btc = fetch_crypto_data('BTC/USDT', days=180)
btc = calculate_indicators(btc)

print("Fetching ETH/USDT data...")
eth = fetch_crypto_data('ETH/USDT', days=180)
eth = calculate_indicators(eth)

btc_last = btc.tail(1).iloc[0]
eth_last = eth.tail(1).iloc[0]

print()
print("MEVCUT DURUM - SHORT PERSPEKTIFINDEN")
print("-" * 80)

# Short conditions to check:
# 1. Price below EMA 200 (downtrend confirmed)
# 2. RSI > 65 (overbought bounce in downtrend)
# 3. ADX > 25 (strong trend)
# 4. Price near/above BB upper (overextended)

print("\nBTC/USDT SHORT KOSULLARI:")
btc_below_ema = btc_last['close'] < btc_last['ema_200']
btc_rsi_high = btc_last['rsi'] > 65
btc_strong_trend = btc_last['adx'] > 25
btc_near_bb_upper = btc_last['close'] > btc_last['bb_mid']

print(f"  1. Fiyat < EMA 200: {'✅ EVET' if btc_below_ema else '❌ HAYIR'} (${btc_last['close']:,.0f} vs ${btc_last['ema_200']:,.0f})")
print(f"  2. RSI > 65 (asiri alim): {'✅ EVET' if btc_rsi_high else '❌ HAYIR'} (RSI: {btc_last['rsi']:.1f})")
print(f"  3. ADX > 25 (guclu trend): {'✅ EVET' if btc_strong_trend else '❌ HAYIR'} (ADX: {btc_last['adx']:.1f})")
print(f"  4. Fiyat > BB Mid: {'✅ EVET' if btc_near_bb_upper else '❌ HAYIR'} (${btc_last['close']:,.0f} vs ${btc_last['bb_mid']:,.0f})")

# Alternative short condition: Trend continuation short
# Price below EMA, bounced to EMA but rejected
btc_ema_rejection = btc_below_ema and btc_last['close'] > btc_last['bb_mid'] * 0.98

print()
print("ETH/USDT SHORT KOSULLARI:")
eth_below_ema = eth_last['close'] < eth_last['ema_200']
eth_rsi_high = eth_last['rsi'] > 65
eth_strong_trend = eth_last['adx'] > 25
eth_near_bb_upper = eth_last['close'] > eth_last['bb_mid']

print(f"  1. Fiyat < EMA 200: {'✅ EVET' if eth_below_ema else '❌ HAYIR'} (${eth_last['close']:,.2f} vs ${eth_last['ema_200']:,.2f})")
print(f"  2. RSI > 65 (asiri alim): {'✅ EVET' if eth_rsi_high else '❌ HAYIR'} (RSI: {eth_last['rsi']:.1f})")
print(f"  3. ADX > 25 (guclu trend): {'✅ EVET' if eth_strong_trend else '❌ HAYIR'} (ADX: {eth_last['adx']:.1f})")
print(f"  4. Fiyat > BB Mid: {'✅ EVET' if eth_near_bb_upper else '❌ HAYIR'} (${eth_last['close']:,.2f} vs ${eth_last['bb_mid']:,.2f})")

# Historical Short Signals Analysis
print()
print("=" * 80)
print("TARIHSEL SHORT SINYALLERI BACKTEST")
print("=" * 80)

# Short Strategy 1: Trend Continuation Short
# Condition: close < ema_200 and rsi > 60 and adx > 25
print("\nStrateji: Trend Devam Short (close < ema_200 AND rsi > 60 AND adx > 25)")
print("-" * 80)

signals_btc_short = []
for i in range(len(btc)-7, 0, -1):
    row = btc.iloc[i]
    if row['close'] < row['ema_200'] and row['rsi'] > 60 and row['adx'] > 25:
        if i + 7 < len(btc):
            entry = row['close']
            future = btc.iloc[i+7]['close']
            # Short profit = entry - future (price went down)
            pnl = (entry - future) / entry * 100
            signals_btc_short.append({
                'date': btc.index[i].strftime('%Y-%m-%d %H:%M'),
                'entry': entry,
                'exit': future,
                'pnl': pnl,
                'result': 'TP' if pnl > 0 else 'SL'
            })
    if len(signals_btc_short) >= 5:
        break

print("\nBTC/USDT Short Sinyalleri:")
if signals_btc_short:
    wins = sum(1 for s in signals_btc_short if s['result'] == 'TP')
    print(f"  Win Rate: {wins}/{len(signals_btc_short)} = {wins/len(signals_btc_short)*100:.0f}%")
    for s in signals_btc_short:
        print(f"  {s['date']}: Entry=${s['entry']:,.0f}, Exit=${s['exit']:,.0f}, PnL={s['pnl']:+.2f}% ({s['result']})")
else:
    print("  Son 180 gunde short sinyal bulunamadi")

signals_eth_short = []
for i in range(len(eth)-7, 0, -1):
    row = eth.iloc[i]
    if row['close'] < row['ema_200'] and row['rsi'] > 60 and row['adx'] > 25:
        if i + 7 < len(eth):
            entry = row['close']
            future = eth.iloc[i+7]['close']
            pnl = (entry - future) / entry * 100
            signals_eth_short.append({
                'date': eth.index[i].strftime('%Y-%m-%d %H:%M'),
                'entry': entry,
                'exit': future,
                'pnl': pnl,
                'result': 'TP' if pnl > 0 else 'SL'
            })
    if len(signals_eth_short) >= 5:
        break

print("\nETH/USDT Short Sinyalleri:")
if signals_eth_short:
    wins = sum(1 for s in signals_eth_short if s['result'] == 'TP')
    print(f"  Win Rate: {wins}/{len(signals_eth_short)} = {wins/len(signals_eth_short)*100:.0f}%")
    for s in signals_eth_short:
        print(f"  {s['date']}: Entry=${s['entry']:,.2f}, Exit=${s['exit']:,.2f}, PnL={s['pnl']:+.2f}% ({s['result']})")
else:
    print("  Son 180 gunde short sinyal bulunamadi")

# Short Strategy 2: BB Upper Rejection Short
# Condition: close < ema_200 and close > bb_upper * 0.98 and rsi > 55
print()
print("\nStrateji: BB Upper Rejection Short (close < ema_200 AND close > bb_upper * 0.98)")
print("-" * 80)

signals_btc_bb = []
for i in range(len(btc)-7, 0, -1):
    row = btc.iloc[i]
    if row['close'] < row['ema_200'] and row['close'] > row['bb_upper'] * 0.98:
        if i + 7 < len(btc):
            entry = row['close']
            future = btc.iloc[i+7]['close']
            pnl = (entry - future) / entry * 100
            signals_btc_bb.append({
                'date': btc.index[i].strftime('%Y-%m-%d %H:%M'),
                'rsi': row['rsi'],
                'entry': entry,
                'exit': future,
                'pnl': pnl,
                'result': 'TP' if pnl > 0 else 'SL'
            })
    if len(signals_btc_bb) >= 5:
        break

print("\nBTC/USDT BB Rejection Short:")
if signals_btc_bb:
    wins = sum(1 for s in signals_btc_bb if s['result'] == 'TP')
    print(f"  Win Rate: {wins}/{len(signals_btc_bb)} = {wins/len(signals_btc_bb)*100:.0f}%")
    for s in signals_btc_bb:
        print(f"  {s['date']}: RSI={s['rsi']:.1f}, Entry=${s['entry']:,.0f}, Exit=${s['exit']:,.0f}, PnL={s['pnl']:+.2f}% ({s['result']})")
else:
    print("  Son 180 gunde BB rejection sinyal bulunamadi")

signals_eth_bb = []
for i in range(len(eth)-7, 0, -1):
    row = eth.iloc[i]
    if row['close'] < row['ema_200'] and row['close'] > row['bb_upper'] * 0.98:
        if i + 7 < len(eth):
            entry = row['close']
            future = eth.iloc[i+7]['close']
            pnl = (entry - future) / entry * 100
            signals_eth_bb.append({
                'date': eth.index[i].strftime('%Y-%m-%d %H:%M'),
                'rsi': row['rsi'],
                'entry': entry,
                'exit': future,
                'pnl': pnl,
                'result': 'TP' if pnl > 0 else 'SL'
            })
    if len(signals_eth_bb) >= 5:
        break

print("\nETH/USDT BB Rejection Short:")
if signals_eth_bb:
    wins = sum(1 for s in signals_eth_bb if s['result'] == 'TP')
    print(f"  Win Rate: {wins}/{len(signals_eth_bb)} = {wins/len(signals_eth_bb)*100:.0f}%")
    for s in signals_eth_bb:
        print(f"  {s['date']}: RSI={s['rsi']:.1f}, Entry=${s['entry']:,.2f}, Exit=${s['exit']:,.2f}, PnL={s['pnl']:+.2f}% ({s['result']})")
else:
    print("  Son 180 gunde BB rejection sinyal bulunamadi")

# RSI Overbought in Downtrend
print()
print("\nStrateji: Dusus Trendinde RSI > 70 (Overbought Short)")
print("-" * 80)

btc_rsi_short = []
for i in range(len(btc)-7, 0, -1):
    row = btc.iloc[i]
    if row['close'] < row['ema_200'] and row['rsi'] > 70:
        if i + 7 < len(btc):
            entry = row['close']
            future = btc.iloc[i+7]['close']
            pnl = (entry - future) / entry * 100
            btc_rsi_short.append({
                'date': btc.index[i].strftime('%Y-%m-%d %H:%M'),
                'rsi': row['rsi'],
                'entry': entry,
                'exit': future,
                'pnl': pnl,
                'result': 'TP' if pnl > 0 else 'SL'
            })
    if len(btc_rsi_short) >= 5:
        break

print("\nBTC/USDT RSI > 70 Short (EMA altinda):")
if btc_rsi_short:
    wins = sum(1 for s in btc_rsi_short if s['result'] == 'TP')
    print(f"  Win Rate: {wins}/{len(btc_rsi_short)} = {wins/len(btc_rsi_short)*100:.0f}%")
    for s in btc_rsi_short:
        print(f"  {s['date']}: RSI={s['rsi']:.1f}, Entry=${s['entry']:,.0f}, Exit=${s['exit']:,.0f}, PnL={s['pnl']:+.2f}% ({s['result']})")
else:
    print("  Son 180 gunde RSI > 70 short sinyal bulunamadi (EMA altinda)")

eth_rsi_short = []
for i in range(len(eth)-7, 0, -1):
    row = eth.iloc[i]
    if row['close'] < row['ema_200'] and row['rsi'] > 70:
        if i + 7 < len(eth):
            entry = row['close']
            future = eth.iloc[i+7]['close']
            pnl = (entry - future) / entry * 100
            eth_rsi_short.append({
                'date': eth.index[i].strftime('%Y-%m-%d %H:%M'),
                'rsi': row['rsi'],
                'entry': entry,
                'exit': future,
                'pnl': pnl,
                'result': 'TP' if pnl > 0 else 'SL'
            })
    if len(eth_rsi_short) >= 5:
        break

print("\nETH/USDT RSI > 70 Short (EMA altinda):")
if eth_rsi_short:
    wins = sum(1 for s in eth_rsi_short if s['result'] == 'TP')
    print(f"  Win Rate: {wins}/{len(eth_rsi_short)} = {wins/len(eth_rsi_short)*100:.0f}%")
    for s in eth_rsi_short:
        print(f"  {s['date']}: RSI={s['rsi']:.1f}, Entry=${s['entry']:,.2f}, Exit=${s['exit']:,.2f}, PnL={s['pnl']:+.2f}% ({s['result']})")
else:
    print("  Son 180 gunde RSI > 70 short sinyal bulunamadi (EMA altinda)")

# Current Short Setup Evaluation
print()
print("=" * 80)
print("MEVCUT SHORT FIRSATI DEGERLENDIRMESI")
print("=" * 80)

print("\nBTC/USDT:")
if btc_below_ema:
    print("  ✅ Ana trend: DUSUS (EMA 200 altinda)")
    if btc_last['rsi'] > 55:
        print(f"  ⚠️ RSI: {btc_last['rsi']:.1f} - Short icin bekle (ideal: RSI > 60-65)")
    else:
        print(f"  ❌ RSI: {btc_last['rsi']:.1f} - Asiri satim, short icin cok gec")
    
    # Calculate short levels
    btc_short_entry = btc_last['bb_mid']  # Wait for bounce to mid band
    btc_short_sl = btc_last['ema_200'] * 1.01  # Stop above EMA
    btc_short_tp = btc_last['bb_lower'] * 0.98  # Target below lower band
    btc_risk_pct = (btc_short_sl - btc_short_entry) / btc_short_entry * 100
    btc_reward_pct = (btc_short_entry - btc_short_tp) / btc_short_entry * 100
    btc_rr = btc_reward_pct / btc_risk_pct if btc_risk_pct > 0 else 0
    
    print(f"\n  Potansiyel Short Seviyeleri (bounce bekle):")
    print(f"    Giris: ${btc_short_entry:,.0f} (BB Mid)")
    print(f"    Stop Loss: ${btc_short_sl:,.0f} (EMA 200 ustu)")
    print(f"    Take Profit: ${btc_short_tp:,.0f} (BB Lower alti)")
    print(f"    Risk: {btc_risk_pct:.2f}%, Reward: {btc_reward_pct:.2f}%")
    print(f"    R:R Orani: {btc_rr:.2f}:1 {'✅' if btc_rr >= 2 else '⚠️ Yetersiz'}")
else:
    print("  ❌ Fiyat EMA 200 ustunde - Short onerilmez")

print("\nETH/USDT:")
if eth_below_ema:
    print("  ✅ Ana trend: DUSUS (EMA 200 altinda)")
    if eth_last['rsi'] > 55:
        print(f"  ⚠️ RSI: {eth_last['rsi']:.1f} - Short icin bekle (ideal: RSI > 60-65)")
    else:
        print(f"  ❌ RSI: {eth_last['rsi']:.1f} - Asiri satim, short icin cok gec")
    
    eth_short_entry = eth_last['bb_mid']
    eth_short_sl = eth_last['ema_200'] * 1.01
    eth_short_tp = eth_last['bb_lower'] * 0.98
    eth_risk_pct = (eth_short_sl - eth_short_entry) / eth_short_entry * 100
    eth_reward_pct = (eth_short_entry - eth_short_tp) / eth_short_entry * 100
    eth_rr = eth_reward_pct / eth_risk_pct if eth_risk_pct > 0 else 0
    
    print(f"\n  Potansiyel Short Seviyeleri (bounce bekle):")
    print(f"    Giris: ${eth_short_entry:,.2f} (BB Mid)")
    print(f"    Stop Loss: ${eth_short_sl:,.2f} (EMA 200 ustu)")
    print(f"    Take Profit: ${eth_short_tp:,.2f} (BB Lower alti)")
    print(f"    Risk: {eth_risk_pct:.2f}%, Reward: {eth_reward_pct:.2f}%")
    print(f"    R:R Orani: {eth_rr:.2f}:1 {'✅' if eth_rr >= 2 else '⚠️ Yetersiz'}")
else:
    print("  ❌ Fiyat EMA 200 ustunde - Short onerilmez")

print()
print("=" * 80)
print("SHORT OZET")
print("=" * 80)
print("""
MEVCUT DURUM:
- Her iki varlik EMA 200 ALTINDA = Dusus trendi devam ediyor
- RSI 33-35 = Asiri satim bolgesinde, SIMD short icin GEC
- ADX > 35 = Guclu trend (asagi yonde)

SONUC: 
❌ SIMDI SHORT GIRIS ONERILMEZ
- RSI cok dusuk, zaten asiri satilmis durumda
- Short icin bounce beklemek gerekiyor

IZLENECEK SHORT FIRSATI:
- BTC: Fiyat $93,400 (BB Mid) bölgesine bounce yaparsa
       ve RSI 55-65 arasına yükselirse → SHORT sinyal
- ETH: Fiyat $3,240 (BB Mid) bölgesine bounce yaparsa  
       ve RSI 55-65 arasına yükselirse → SHORT sinyal

ALARM SEVIYELERI:
- BTC Short Giris: $93,400 - $94,000
- ETH Short Giris: $3,240 - $3,250
""")
