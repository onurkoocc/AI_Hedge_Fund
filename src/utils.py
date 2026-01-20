"""
Utility functions for the Market Scanner Core System.

This module provides helper functions for:
- Column name standardization (lowercase snake_case)
- Logging setup
- Timestamp generation
"""

import logging
from datetime import datetime
import pandas as pd


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert all DataFrame column names to lowercase snake_case format.
    
    Examples:
        'Close' -> 'close'
        'EMA_200' -> 'ema_200'
        'BB Upper' -> 'bb_upper'
    
    Args:
        df: Input DataFrame with any column naming convention
        
    Returns:
        DataFrame with standardized column names
    """
    df = df.copy()
    df.columns = [col.lower().replace(' ', '_').replace('-', '_') for col in df.columns]
    return df


def setup_logging(level: int = logging.INFO) -> None:
    """
    Configure logging with consistent format for the application.
    
    Args:
        level: Logging level (default: INFO)
    """
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Suppress verbose logs from third-party libraries
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('ccxt').setLevel(logging.WARNING)


def get_timestamp() -> str:
    """
    Get current timestamp in ISO-8601 format.
    
    Returns:
        Timestamp string (e.g., '2026-01-19T15:30:00')
    """
    return datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
