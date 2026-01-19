"""
Technical analysis module for Market Scanner Core System.

This module calculates technical indicators using pandas-ta and merges
macro data for correlation analysis.
"""

import logging
import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator, ADXIndicator
from ta.volatility import AverageTrueRange, BollingerBands
from typing import Dict
from .utils import standardize_columns

logger = logging.getLogger(__name__)


def calculate_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate all technical indicators on OHLCV data.
    
    Adds columns: rsi, ema_200, atr, bb_lower, bb_mid, bb_upper, adx
    
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
