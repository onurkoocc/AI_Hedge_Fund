"""
BTC/USDT ve ETH/USDT Kombine Analiz Scripti
"""
import ccxt
import pandas as pd
import numpy as np
from datetime import datetime

def get_data(exchange, symbol, days=180):
    """Fetch OHLCV data and calculate indicators"""
    ohlcv = exchange.fetch_ohlcv(symbol, '1d', limit=days)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    
    # EMA 200
    df['ema_200'] = df['close'].ewm(span=200, adjust=False).mean()
    
    # RSI
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / loss
    df['rsi'] = 100 - (100 / (1 + rs))
    
    # ADX
    high = df['high']
    low = df['low']
    close = df['close']
    plus_dm = high.diff()
    minus_dm = low.diff().abs() * -1
    plus_dm = plus_dm.where((plus_dm > minus_dm.abs()) & (plus_dm > 0), 0)
    minus_dm = minus_dm.abs().where((minus_dm.abs() > plus_dm) & (minus_dm < 0), 0)
    tr = pd.concat([high - low, (high - close.shift()).abs(), (low - close.shift()).abs()], axis=1).max(axis=1)
    atr = tr.rolling(14).mean()
    plus_di = 100 * (plus_dm.rolling(14).mean() / atr)
    minus_di = 100 * (minus_dm.rolling(14).mean() / atr)
    dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di)
    df['adx'] = dx.rolling(14).mean()
    
    # Bollinger Bands
    df['bb_mid'] = df['close'].rolling(20).mean()
    std = df['close'].rolling(20).std()
    df['bb_upper'] = df['bb_mid'] + 2 * std
    df['bb_lower'] = df['bb_mid'] - 2 * std
    
    # ATR
    df['atr'] = atr
    
    # Volume SMA
    df['volume_sma'] = df['volume'].rolling(20).mean()
    
    return df

def analyze():
    exchange = ccxt.binance({'enableRateLimit': True})
    
    print('=' * 70)
    print('BTC/USDT ve ETH/USDT GUNCEL TEKNIK GOSTERGELER')
    print('Tarih:', datetime.now().strftime('%Y-%m-%d %H:%M'))
    print('=' * 70)
    
    results = {}
    
    for symbol in ['BTC/USDT', 'ETH/USDT']:
        df = get_data(exchange, symbol, 180)
        latest = df.iloc[-1]
        
        # 7 ve 30 gunluk degisim
        change_7d = ((latest['close'] - df.iloc[-8]['close']) / df.iloc[-8]['close']) * 100
        change_30d = ((latest['close'] - df.iloc[-31]['close']) / df.iloc[-31]['close']) * 100
        
        # Bollinger pozisyonu
        bb_range = latest['bb_upper'] - latest['bb_lower']
        bb_position = ((latest['close'] - latest['bb_lower']) / bb_range) * 100
        
        results[symbol] = {
            'price': latest['close'],
            'ema_200': latest['ema_200'],
            'rsi': latest['rsi'],
            'adx': latest['adx'],
            'bb_lower': latest['bb_lower'],
            'bb_mid': latest['bb_mid'],
            'bb_upper': latest['bb_upper'],
            'atr': latest['atr'],
            'change_7d': change_7d,
            'change_30d': change_30d,
            'bb_position': bb_position,
            'volume_ratio': latest['volume'] / latest['volume_sma'] if latest['volume_sma'] > 0 else 1,
            'above_ema': latest['close'] > latest['ema_200']
        }
        
        print(f'\n{symbol}')
        print('-' * 40)
        print(f"Fiyat: ${latest['close']:,.2f}")
        above_below = 'USTUNDE' if latest['close'] > latest['ema_200'] else 'ALTINDA'
        ema_diff = ((latest['close'] - latest['ema_200']) / latest['ema_200']) * 100
        print(f"EMA 200: ${latest['ema_200']:,.2f} ({above_below}, {ema_diff:+.2f}%)")
        print(f"RSI (14): {latest['rsi']:.1f}")
        print(f"ADX: {latest['adx']:.1f}")
        print(f"BB Lower: ${latest['bb_lower']:,.2f}")
        print(f"BB Mid: ${latest['bb_mid']:,.2f}")
        print(f"BB Upper: ${latest['bb_upper']:,.2f}")
        print(f"BB Pozisyon: %{bb_position:.1f}")
        print(f"ATR: ${latest['atr']:,.2f}")
        print(f"Volume/Avg: {results[symbol]['volume_ratio']:.2f}x")
        print(f"7 Gun Degisim: {change_7d:+.2f}%")
        print(f"30 Gun Degisim: {change_30d:+.2f}%")
        
        # LONG Kosullari
        long_ema = latest['close'] > latest['ema_200']
        long_rsi = latest['rsi'] < 35
        long_adx = latest['adx'] > 25
        
        print(f'\n  LONG Kosullari (Trend Pullback):')
        print(f"    - Fiyat > EMA 200: {'✅' if long_ema else '❌'}")
        print(f"    - RSI < 35: {'✅' if long_rsi else '❌'} (mevcut: {latest['rsi']:.1f})")
        print(f"    - ADX > 25: {'✅' if long_adx else '❌'} (mevcut: {latest['adx']:.1f})")
        long_ready = long_ema and long_rsi and long_adx
        print(f"    >>> LONG SINYAL: {'✅ AKTIF' if long_ready else '❌ BEKLE'}")
        
        # SHORT Kosullari
        short_ema = latest['close'] < latest['ema_200']
        short_rsi = latest['rsi'] > 60
        short_adx = latest['adx'] > 25
        
        print(f'\n  SHORT Kosullari (Trend Continuation):')
        print(f"    - Fiyat < EMA 200: {'✅' if short_ema else '❌'}")
        print(f"    - RSI > 60: {'✅' if short_rsi else '❌'} (mevcut: {latest['rsi']:.1f})")
        print(f"    - ADX > 25: {'✅' if short_adx else '❌'} (mevcut: {latest['adx']:.1f})")
        short_ready = short_ema and short_rsi and short_adx
        print(f"    >>> SHORT SINYAL: {'✅ AKTIF' if short_ready else '❌ BEKLE'}")
        
        results[symbol]['long_ready'] = long_ready
        results[symbol]['short_ready'] = short_ready
        results[symbol]['long_conditions'] = (long_ema, long_rsi, long_adx)
        results[symbol]['short_conditions'] = (short_ema, short_rsi, short_adx)
    
    # BTC/ETH orani
    btc = results['BTC/USDT']
    eth = results['ETH/USDT']
    
    ratio = btc['price'] / eth['price']
    
    print(f'\n' + '=' * 70)
    print('BTC/ETH ORANI ANALIZI')
    print('=' * 70)
    print(f"Mevcut BTC/ETH: {ratio:.2f}")
    
    # 30 gunluk performans karsilastirmasi
    print(f'\n30 GUNLUK PERFORMANS:')
    print(f"  BTC: {btc['change_30d']:+.2f}%")
    print(f"  ETH: {eth['change_30d']:+.2f}%")
    diff = abs(btc['change_30d'] - eth['change_30d'])
    print(f"  Performans Farki: {diff:.2f}%")
    stronger = 'BTC' if btc['change_30d'] > eth['change_30d'] else 'ETH'
    print(f"  Guclu Olan: {stronger}")
    
    # Pair Trading degerlendirmesi
    print(f'\n  PAIR TRADING DEGERLENDIRMESI:')
    if diff > 5:
        print(f"    Yeterli fark (>{5}%): ✅ EVET")
        print(f"    Oneri: LONG {stronger} / SHORT {'ETH' if stronger == 'BTC' else 'BTC'}")
    else:
        print(f"    Yeterli fark (>{5}%): ❌ HAYIR")
        print(f"    Oneri: Pair trading icin uygun degil")
    
    # Ozet tablo
    print(f'\n' + '=' * 70)
    print('OZET TAVSIYE')
    print('=' * 70)
    print(f"\n{'Varlik':<12} {'LONG':<15} {'SHORT':<15} {'Aktif Sinyal':<15}")
    print('-' * 60)
    
    for symbol in ['BTC/USDT', 'ETH/USDT']:
        r = results[symbol]
        long_status = 'Uygun' if r['long_ready'] else 'Bekle'
        short_status = 'Uygun' if r['short_ready'] else 'Bekle'
        active = 'LONG' if r['long_ready'] else ('SHORT' if r['short_ready'] else 'YOK')
        print(f"{symbol:<12} {long_status:<15} {short_status:<15} {active:<15}")
    
    # Pozisyon onerileri
    print(f'\n' + '=' * 70)
    print('POZISYON ONERILERI')
    print('=' * 70)
    
    for symbol in ['BTC/USDT', 'ETH/USDT']:
        r = results[symbol]
        print(f"\n{symbol}:")
        
        if r['long_ready']:
            entry = r['price']
            stop = entry * 0.98  # 2% stop
            target = entry * 1.05  # 5% target
            rr = (target - entry) / (entry - stop)
            print(f"  LONG POZISYON ONERISI:")
            print(f"    Giris: ${entry:,.2f}")
            print(f"    Stop Loss: ${stop:,.2f} (-2%)")
            print(f"    Take Profit: ${target:,.2f} (+5%)")
            print(f"    R:R Orani: {rr:.1f}:1")
        elif r['short_ready']:
            entry = r['price']
            stop = entry * 1.02  # 2% stop
            target = entry * 0.95  # 5% target
            rr = (entry - target) / (stop - entry)
            print(f"  SHORT POZISYON ONERISI:")
            print(f"    Giris: ${entry:,.2f}")
            print(f"    Stop Loss: ${stop:,.2f} (+2%)")
            print(f"    Take Profit: ${target:,.2f} (-5%)")
            print(f"    R:R Orani: {rr:.1f}:1")
        else:
            # Potansiyel alarm seviyeleri
            print(f"  AKTIF SINYAL YOK - ALARM SEVIYELERI:")
            if r['above_ema']:
                # LONG icin RSI dusmesi bekle
                print(f"    LONG icin izle: RSI {r['rsi']:.1f} -> 35 altina dusmeli")
                print(f"    Potansiyel entry: BB Lower ${r['bb_lower']:,.2f}")
            else:
                # SHORT icin RSI yukselisi bekle
                print(f"    SHORT icin izle: RSI {r['rsi']:.1f} -> 60 ustune cikmali")
                print(f"    Potansiyel entry: BB Mid ${r['bb_mid']:,.2f} - BB Upper ${r['bb_upper']:,.2f}")
    
    print(f'\n' + '=' * 70)
    print('RISK UYARISI')
    print('=' * 70)
    print("Bu analiz yatirim tavsiyesi degildir.")
    print("1:2 R:R kurali saglanmadan islem yapilmamalidir.")
    print("Aylik maksimum 5 Sniper islem limiti uygulanmaktadir.")

if __name__ == '__main__':
    analyze()
