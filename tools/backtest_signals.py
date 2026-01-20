"""Backtest historical signals for BTC and ETH"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data_loader import fetch_crypto_data
from src.analysis import calculate_indicators

# BTC historical signals
print("Fetching BTC data for backtest...")
btc = fetch_crypto_data('BTC/USDT', days=180)
btc = calculate_indicators(btc)

# Find last 3 trend pullback signals for BTC
# Condition: close > ema_200 and rsi < 35 and adx > 25
signals_btc = []
for i in range(len(btc)-7, 0, -1):
    row = btc.iloc[i]
    if row['close'] > row['ema_200'] and row['rsi'] < 35 and row['adx'] > 25:
        # Check outcome after 7 days
        if i + 7 < len(btc):
            entry = row['close']
            future = btc.iloc[i+7]['close']
            pnl = (future - entry) / entry * 100
            signals_btc.append({
                'date': btc.index[i].strftime('%Y-%m-%d'),
                'entry': entry,
                'exit': future,
                'pnl': pnl,
                'result': 'TP' if pnl > 0 else 'SL'
            })
    if len(signals_btc) >= 3:
        break

print()
print('BTC/USDT Son Trend Pullback Sinyalleri (close > ema_200 AND rsi < 35 AND adx > 25):')
print('-' * 60)
if signals_btc:
    for s in signals_btc:
        print(f"  {s['date']}: Entry=${s['entry']:,.0f}, Exit=${s['exit']:,.0f}, PnL={s['pnl']:+.2f}% ({s['result']})")
else:
    print('  Son 180 gunde sinyal bulunamadi')

# ETH historical signals
print()
print("Fetching ETH data for backtest...")
eth = fetch_crypto_data('ETH/USDT', days=180)
eth = calculate_indicators(eth)

signals_eth = []
for i in range(len(eth)-7, 0, -1):
    row = eth.iloc[i]
    if row['close'] > row['ema_200'] and row['rsi'] < 35 and row['adx'] > 25:
        if i + 7 < len(eth):
            entry = row['close']
            future = eth.iloc[i+7]['close']
            pnl = (future - entry) / entry * 100
            signals_eth.append({
                'date': eth.index[i].strftime('%Y-%m-%d'),
                'entry': entry,
                'exit': future,
                'pnl': pnl,
                'result': 'TP' if pnl > 0 else 'SL'
            })
    if len(signals_eth) >= 3:
        break

print()
print('ETH/USDT Son Trend Pullback Sinyalleri (close > ema_200 AND rsi < 35 AND adx > 25):')
print('-' * 60)
if signals_eth:
    for s in signals_eth:
        print(f"  {s['date']}: Entry=${s['entry']:,.2f}, Exit=${s['exit']:,.2f}, PnL={s['pnl']:+.2f}% ({s['result']})")
else:
    print('  Son 180 gunde sinyal bulunamadi')

# Also check for any RSI < 30 oversold signals
print()
print('='*60)
print('RSI < 30 ASIRI SATIM SINYALLERI (Son 30 gun)')
print('='*60)

btc_oversold = []
for i in range(len(btc)-7, max(0, len(btc)-30), -1):
    row = btc.iloc[i]
    if row['rsi'] < 30:
        if i + 7 < len(btc):
            entry = row['close']
            future = btc.iloc[i+7]['close']
            pnl = (future - entry) / entry * 100
            btc_oversold.append({
                'date': btc.index[i].strftime('%Y-%m-%d %H:%M'),
                'rsi': row['rsi'],
                'entry': entry,
                'exit': future,
                'pnl': pnl,
            })
    if len(btc_oversold) >= 5:
        break

print()
print('BTC/USDT RSI < 30 Sinyalleri:')
if btc_oversold:
    for s in btc_oversold:
        print(f"  {s['date']}: RSI={s['rsi']:.1f}, Entry=${s['entry']:,.0f}, 7-gun sonra=${s['exit']:,.0f}, PnL={s['pnl']:+.2f}%")
else:
    print('  Son 30 gunde RSI < 30 sinyal yok')

eth_oversold = []
for i in range(len(eth)-7, max(0, len(eth)-30), -1):
    row = eth.iloc[i]
    if row['rsi'] < 30:
        if i + 7 < len(eth):
            entry = row['close']
            future = eth.iloc[i+7]['close']
            pnl = (future - entry) / entry * 100
            eth_oversold.append({
                'date': eth.index[i].strftime('%Y-%m-%d %H:%M'),
                'rsi': row['rsi'],
                'entry': entry,
                'exit': future,
                'pnl': pnl,
            })
    if len(eth_oversold) >= 5:
        break

print()
print('ETH/USDT RSI < 30 Sinyalleri:')
if eth_oversold:
    for s in eth_oversold:
        print(f"  {s['date']}: RSI={s['rsi']:.1f}, Entry=${s['entry']:,.2f}, 7-gun sonra=${s['exit']:,.2f}, PnL={s['pnl']:+.2f}%")
else:
    print('  Son 30 gunde RSI < 30 sinyal yok')
