"""
Technical analysis module for Market Scanner Core System.

This module calculates technical indicators using pandas-ta and merges
macro data for correlation analysis.
"""

import logging
import pandas as pd
from ta.momentum import RSIIndicator, StochRSIIndicator
from ta.trend import EMAIndicator, ADXIndicator, MACD
from ta.volatility import AverageTrueRange, BollingerBands
from typing import Dict, Any
from .utils import standardize_columns

logger = logging.getLogger(__name__)


def calculate_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate all technical indicators on OHLCV data.
    
    Adds columns: rsi, ema_200, atr, bb_lower, bb_mid, bb_upper, adx,
                  macd, macd_signal, macd_histogram, macd_bullish_cross, macd_bearish_cross,
                  stoch_rsi_k, stoch_rsi_d, stoch_rsi_bullish, stoch_rsi_bearish
    
    Args:
        df: DataFrame with standardized OHLCV columns (open, high, low, close, volume)
        
    Returns:
        DataFrame with added indicator columns. Returns original DataFrame 
        with warning if insufficient data.
    """
    try:
        df = df.copy()
        
        # Check if we have enough data for EMA200
        if len(df) < 200:
            logger.warning(f"Insufficient data for EMA200: {len(df)} rows (need 200+)")
            return df
        
        logger.info("Calculating technical indicators...")
        
        # RSI (14-period)
        rsi_indicator = RSIIndicator(close=df['close'], window=14)
        df['rsi'] = rsi_indicator.rsi()
        
        # EMA 200
        ema_indicator = EMAIndicator(close=df['close'], window=200)
        df['ema_200'] = ema_indicator.ema_indicator()
        
        # ATR (14-period)
        atr_indicator = AverageTrueRange(high=df['high'], low=df['low'], close=df['close'], window=14)
        df['atr'] = atr_indicator.average_true_range()
        
        # Bollinger Bands (20-period, 2 std dev)
        bb_indicator = BollingerBands(close=df['close'], window=20, window_dev=2)
        df['bb_lower'] = bb_indicator.bollinger_lband()
        df['bb_mid'] = bb_indicator.bollinger_mavg()
        df['bb_upper'] = bb_indicator.bollinger_hband()
        
        # ADX (14-period)
        adx_indicator = ADXIndicator(high=df['high'], low=df['low'], close=df['close'], window=14)
        df['adx'] = adx_indicator.adx()
        
        # MACD (12, 26, 9)
        if len(df) < 35:
            logger.warning(f"Insufficient data for MACD calculation: {len(df)} rows (need 35+)")
        else:
            macd_indicator = MACD(close=df['close'], window_fast=12, window_slow=26, window_sign=9)
            df['macd'] = macd_indicator.macd()
            df['macd_signal'] = macd_indicator.macd_signal()
            df['macd_histogram'] = macd_indicator.macd_diff()
            
            # Detect MACD crossovers
            df['macd_bullish_cross'] = (df['macd_histogram'] > 0) & (df['macd_histogram'].shift(1) <= 0)
            df['macd_bearish_cross'] = (df['macd_histogram'] < 0) & (df['macd_histogram'].shift(1) >= 0)
            
            # Log crossover events
            bullish_crosses = df[df['macd_bullish_cross'] == True]
            bearish_crosses = df[df['macd_bearish_cross'] == True]
            
            for idx in bullish_crosses.index:
                macd_val = df.loc[idx, 'macd']
                signal_val = df.loc[idx, 'macd_signal']
                logger.info(f"MACD bullish crossover detected (MACD: {macd_val:.4f}, Signal: {signal_val:.4f})")
            
            for idx in bearish_crosses.index:
                macd_val = df.loc[idx, 'macd']
                signal_val = df.loc[idx, 'macd_signal']
                logger.info(f"MACD bearish crossover detected (MACD: {macd_val:.4f}, Signal: {signal_val:.4f})")
        
        # Stochastic RSI (14, 3, 3)
        if len(df) < 28:
            logger.warning(f"Insufficient data for StochRSI calculation: {len(df)} rows (need 28+)")
        else:
            stoch_rsi_indicator = StochRSIIndicator(close=df['close'], window=14, smooth1=3, smooth2=3)
            # Scale from 0-1 to 0-100
            df['stoch_rsi_k'] = stoch_rsi_indicator.stochrsi_k() * 100
            df['stoch_rsi_d'] = stoch_rsi_indicator.stochrsi_d() * 100
            
            # Detect StochRSI crossovers in oversold/overbought zones
            # Bullish: K crosses above D in oversold zone (<20)
            k_crosses_above_d = (df['stoch_rsi_k'] > df['stoch_rsi_d']) & (df['stoch_rsi_k'].shift(1) <= df['stoch_rsi_d'].shift(1))
            df['stoch_rsi_bullish'] = k_crosses_above_d & (df['stoch_rsi_k'] < 20)
            
            # Bearish: K crosses below D in overbought zone (>80)
            k_crosses_below_d = (df['stoch_rsi_k'] < df['stoch_rsi_d']) & (df['stoch_rsi_k'].shift(1) >= df['stoch_rsi_d'].shift(1))
            df['stoch_rsi_bearish'] = k_crosses_below_d & (df['stoch_rsi_k'] > 80)
            
            # Log crossover events
            bullish_stoch = df[df['stoch_rsi_bullish'] == True]
            bearish_stoch = df[df['stoch_rsi_bearish'] == True]
            
            for idx in bullish_stoch.index:
                k_val = df.loc[idx, 'stoch_rsi_k']
                d_val = df.loc[idx, 'stoch_rsi_d']
                logger.info(f"Bullish StochRSI crossover in oversold (K: {k_val:.4f}, D: {d_val:.4f})")
            
            for idx in bearish_stoch.index:
                k_val = df.loc[idx, 'stoch_rsi_k']
                d_val = df.loc[idx, 'stoch_rsi_d']
                logger.info(f"Bearish StochRSI crossover in overbought (K: {k_val:.4f}, D: {d_val:.4f})")
        
        # Volume SMA (20-period) for volume filter feature
        # T003: Calculate 20-period simple moving average of volume
        if 'volume' in df.columns:
            df['volume_sma_20'] = df['volume'].rolling(20).mean()
            
            # T004: Handle edge cases - count non-NaN values
            valid_volume_bars = df['volume'].notna().sum()
            if valid_volume_bars < 20:
                if valid_volume_bars >= 5:
                    logger.warning(f"Insufficient data for full volume SMA: {valid_volume_bars} bars (need 20+). Using available data.")
                else:
                    logger.warning(f"Critical: Only {valid_volume_bars} volume bars available (need minimum 5). Volume filter may be unreliable.")
            
            # T005: Log volume calculation completion
            non_nan_sma = df['volume_sma_20'].notna().sum()
            logger.info(f"Volume SMA-20 calculated: {non_nan_sma} valid data points")
        else:
            logger.warning("Volume column not found - volume filter will be unavailable")
        
        # Standardize all column names again (in case pandas-ta added non-standard names)
        df = standardize_columns(df)
        
        logger.info(f"✓ Calculated indicators. Columns: {df.columns.tolist()}")
        return df
        
    except Exception as e:
        logger.error(f"Error calculating indicators: {e}")
        return df


def merge_macro_data(crypto_df: pd.DataFrame, macro_dfs: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Merge macro indicator data into crypto DataFrame with proper time alignment.
    
    Crypto trades 24/7, macro markets trade M-F. This function uses forward fill
    to extend macro values through weekends.
    
    Args:
        crypto_df: Main crypto DataFrame with datetime index
        macro_dfs: Dictionary of {asset_name: DataFrame} for macro data
                   e.g., {'gold': gold_df, 'dxy': dxy_df, 'sp500': sp500_df}
    
    Returns:
        DataFrame with added columns like 'gold_close', 'dxy_close', 'sp500_close'
    """
    try:
        result = crypto_df.copy()
        
        for asset_name, macro_df in macro_dfs.items():
            if macro_df.empty:
                logger.warning(f"Skipping empty macro data for {asset_name}")
                continue
            
            logger.info(f"Merging {asset_name} data...")
            
            # Ensure macro_df has datetime index
            if not isinstance(macro_df.index, pd.DatetimeIndex):
                logger.warning(f"{asset_name} does not have datetime index, skipping")
                continue
            
            # Select only the close price for macro data
            if 'close' not in macro_df.columns:
                logger.warning(f"{asset_name} does not have 'close' column, skipping")
                continue
            
            macro_close = macro_df[['close']].copy()
            
            # Rename column to include asset prefix
            macro_close.columns = [f'{asset_name}_close']
            
            # Use merge_asof for time-based alignment (forward fill)
            # This aligns crypto timestamps with the nearest prior macro timestamp
            result = pd.merge_asof(
                result.sort_index(),
                macro_close.sort_index(),
                left_index=True,
                right_index=True,
                direction='backward'  # Use the most recent macro value
            )
            
            # Forward fill any remaining NaN values (weekends)
            result[f'{asset_name}_close'] = result[f'{asset_name}_close'].ffill()
            
            logger.info(f"✓ Merged {asset_name} data (column: {asset_name}_close)")
        
        return result
        
    except Exception as e:
        logger.error(f"Error merging macro data: {e}")
        return crypto_df


def calculate_risk_levels(
    entry_price: float,
    atr: float,
    side: str,
    atr_multiplier: float = 1.5,
    min_rr: float = 2.0
) -> Dict[str, Any]:
    """
    Calculate dynamic stop-loss and take-profit levels based on ATR.
    
    Implements FR-001 through FR-006 from specs/003-atr-dynamic-stoploss/spec.md
    
    Args:
        entry_price: Price at signal generation (must be > 0)
        atr: ATR value at signal time (must be >= 0)
        side: Trade direction - 'long' or 'short'
        atr_multiplier: Multiplier for ATR (default: 1.5)
        min_rr: Minimum Risk/Reward ratio (default: 2.0)
        
    Returns:
        Dictionary with keys:
        - stop_loss: Absolute price for stop loss
        - take_profit: Absolute price for take profit
        - stop_distance: Absolute price distance from entry to stop
        - stop_pct: Stop distance as percentage (0.01 = 1%)
        - rr_ratio: Risk/Reward ratio
        - status: 'OK', 'LOW_RR', 'VOLATILITY_TOO_HIGH', or 'VOLATILITY_UNDEFINED'
    """
    try:
        # T003: Input validation
        if entry_price <= 0:
            logger.error(f"Invalid entry_price: {entry_price} (must be > 0)")
            return {
                'stop_loss': entry_price,
                'take_profit': entry_price,
                'stop_distance': 0,
                'stop_pct': 0,
                'rr_ratio': 0,
                'status': 'VOLATILITY_UNDEFINED'
            }
        
        if atr < 0:
            logger.error(f"Invalid ATR: {atr} (must be >= 0)")
            return {
                'stop_loss': entry_price,
                'take_profit': entry_price,
                'stop_distance': 0,
                'stop_pct': 0,
                'rr_ratio': 0,
                'status': 'VOLATILITY_UNDEFINED'
            }
        
        if side not in ['long', 'short']:
            logger.error(f"Invalid side: {side} (must be 'long' or 'short')")
            return {
                'stop_loss': entry_price,
                'take_profit': entry_price,
                'stop_distance': 0,
                'stop_pct': 0,
                'rr_ratio': 0,
                'status': 'VOLATILITY_UNDEFINED'
            }
        
        # T004: Handle ATR = 0 or very small (edge case)
        if atr == 0:
            logger.warning("ATR is zero, using minimum stop-loss of 1%")
            stop_distance = entry_price * 0.01  # Minimum 1%
            status = 'VOLATILITY_UNDEFINED'
        else:
            # FR-002: Calculate stop distance using ATR
            stop_distance = atr * atr_multiplier
            status = 'OK'
        
        # Calculate stop loss percentage
        stop_pct = stop_distance / entry_price
        
        # T005: FR-004 - Enforce minimum 1% stop-loss
        if stop_pct < 0.01:
            logger.info(f"Stop distance {stop_pct:.4%} < 1%, adjusting to 1%")
            stop_pct = 0.01
            stop_distance = entry_price * 0.01
        
        # T006: FR-004 - Enforce maximum 5% stop-loss
        if stop_pct > 0.05:
            logger.warning(f"Stop distance {stop_pct:.4%} > 5%, marking as VOLATILITY_TOO_HIGH")
            return {
                'stop_loss': entry_price * (0.95 if side == 'long' else 1.05),
                'take_profit': entry_price * (1.10 if side == 'long' else 0.90),
                'stop_distance': entry_price * 0.05,
                'stop_pct': 0.05,
                'rr_ratio': 2.0,
                'status': 'VOLATILITY_TOO_HIGH'
            }
        
        # FR-002: Calculate stop loss price (long: subtract, short: add)
        if side == 'long':
            stop_loss = entry_price - stop_distance
            # FR-006: Take profit is stop_distance * min_rr above entry
            take_profit = entry_price + (stop_distance * min_rr)
        else:  # short
            stop_loss = entry_price + stop_distance
            take_profit = entry_price - (stop_distance * min_rr)
        
        # Calculate take profit distance
        tp_distance = abs(take_profit - entry_price)
        
        # T007: FR-005 - Calculate R:R ratio
        rr_ratio = tp_distance / stop_distance if stop_distance > 0 else 0
        
        # T008: FR-005 - Check if R:R is below minimum
        if rr_ratio < min_rr:
            logger.warning(f"R:R ratio {rr_ratio:.2f} < {min_rr}, marking as LOW_RR")
            status = 'LOW_RR'
        
        # T009: Log edge cases
        if status != 'OK':
            logger.info(f"Risk calculation: Entry=${entry_price:.2f}, ATR={atr:.2f}, "
                       f"Stop%={stop_pct:.2%}, R:R={rr_ratio:.2f}, Status={status}")
        
        return {
            'stop_loss': stop_loss,
            'take_profit': take_profit,
            'stop_distance': stop_distance,
            'stop_pct': stop_pct,
            'rr_ratio': rr_ratio,
            'status': status
        }
        
    except Exception as e:
        logger.error(f"Error calculating risk levels: {e}")
        return {
            'stop_loss': entry_price,
            'take_profit': entry_price,
            'stop_distance': 0,
            'stop_pct': 0,
            'rr_ratio': 0,
            'status': 'VOLATILITY_UNDEFINED'
        }
