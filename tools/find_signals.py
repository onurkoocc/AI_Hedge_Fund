"""Find historical signals for backtest"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data_loader import fetch_crypto_data
from src.analysis import calculate_indicators

df = fetch_crypto_data('BTC/USDT', days=180)
df = calculate_indicators(df)

# Condition: RSI < 35 and ADX > 25 (trend pullback without EMA filter)
print("RSI < 35 VE ADX > 25 OLAN SON DURUMLAR:")
print("="*70)

signals = df[(df['rsi'] < 35) & (df['adx'] > 25)]
print(f"Toplam {len(signals)} sinyal bulundu (4h candle)")
print()

if len(signals) > 0:
    for idx, row in signals.tail(15).iterrows():
        entry = row['close']
        atr = row['atr']
        sl = entry - (atr * 2)  # 2 ATR stop
        tp = entry + (atr * 4)  # 4 ATR target (2:1 R:R)
        
        # Check next candles for outcome
        future_df = df[df.index > idx].head(20)  # Next 20 candles (80 hours)
        
        hit_tp = False
        hit_sl = False
        result = "AÇIK"
        pnl = 0
        
        for f_idx, f_row in future_df.iterrows():
            if f_row['low'] <= sl:
                hit_sl = True
                result = "SL ❌"
                pnl = ((sl - entry) / entry) * 100
                break
            if f_row['high'] >= tp:
                hit_tp = True
                result = "TP ✅"
                pnl = ((tp - entry) / entry) * 100
                break
        
        if not hit_tp and not hit_sl:
            # Still open or no clear outcome
            if len(future_df) > 0:
                last_close = future_df['close'].iloc[-1]
                pnl = ((last_close - entry) / entry) * 100
                result = f"BEKLEMEDE ({pnl:+.2f}%)"
        
        print(f"{idx.strftime('%Y-%m-%d %H:%M')}: Entry=${entry:,.0f}, SL=${sl:,.0f}, TP=${tp:,.0f} -> {result}")

print()
print("="*70)
print("EMA200 DURUMU:")
# Check how many of these signals were above/below EMA200
above_ema = signals[signals['close'] > signals['ema_200']]
below_ema = signals[signals['close'] < signals['ema_200']]
print(f"  EMA200 üzerinde: {len(above_ema)}")
print(f"  EMA200 altında: {len(below_ema)}")
