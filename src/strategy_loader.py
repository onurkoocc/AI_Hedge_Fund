"""
Strategy loader module for Market Scanner Core System.

This module reads and parses trading strategies from specs/04_strategies.md.
Strategies are defined in Markdown format with structured sections.
"""

import logging
import re
from typing import List, Dict, Any
from pathlib import Path
import pandas as pd

logger = logging.getLogger(__name__)


def load_strategies(specs_dir: str = "specs") -> List[Dict[str, Any]]:
    """
    Load trading strategies from specs/04_strategies.md.
    
    Parses Markdown file to extract:
    - Strategy name
    - Type (Trend, Pair, Grid, Breakout)
    - Condition (Pandas query string)
    - Parameters (stop_loss, take_profit, position_size)
    
    Args:
        specs_dir: Directory containing strategy specifications (default: "specs")
        
    Returns:
        List of strategy dictionaries with keys:
        - name: str
        - type: str
        - condition: str (Pandas query)
        - params: dict (stop_loss_pct, take_profit_pct, position_size_pct)
    """
    try:
        # Construct path to strategies file
        strategies_file = Path(specs_dir) / "04_strategies.md"
        
        if not strategies_file.exists():
            logger.error(f"Strategies file not found: {strategies_file}")
            return []
        
        logger.info(f"Loading strategies from {strategies_file}...")
        
        # Read file content
        with open(strategies_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse strategies
        strategies = []
        
        # Extract each strategy section (starts with "### " followed by a number)
        # T016: Updated pattern - more flexible to handle different parameter formats
        # Match strategy header and entry condition, then extract parameters
        strategy_pattern = r'### \d+\.\s+(.+?)\n\n\*\*Type\*\*:\s*(.+?)\n.*?\n\n\*\*Entry Condition\*\*:\s*\n```python\n"(.+?)"\n```(.*?)\n---'
        
        matches = re.finditer(strategy_pattern, content, re.DOTALL)
        
        for match in matches:
            name = match.group(1).strip()
            strategy_type = match.group(2).strip()
            condition = match.group(3).strip()
            params_block = match.group(4)  # Everything after entry condition until ---
            
            # Extract stop loss - look for number followed by %
            stop_loss_match = re.search(r'Stop Loss[^\n]*?(\d+)%', params_block)
            stop_loss = float(stop_loss_match.group(1)) / 100 if stop_loss_match else 0.02
            
            # Extract take profit
            take_profit_match = re.search(r'Take Profit[^\n]*?(\d+\.?\d*)%', params_block)
            take_profit = float(take_profit_match.group(1)) / 100 if take_profit_match else 0.04
            
            # Extract position size
            position_size_match = re.search(r'Position Size:\s*([\d.]+)%', params_block)
            position_size = float(position_size_match.group(1)) / 100 if position_size_match else 0.02
            
            # Look for ATR Multiplier
            atr_match = re.search(r'ATR Multiplier:\s*([\d.]+)', params_block)
            atr_multiplier = float(atr_match.group(1)) if atr_match else 1.5
            
            # T017: Look for Volume Threshold
            vol_match = re.search(r'Volume Threshold:\s*([\d.]+)', params_block)
            volume_threshold = float(vol_match.group(1)) if vol_match else 0.5
            
            # Skip if position size is 0 (likely failed to parse)
            if position_size == 0:
                logger.warning(f"Skipping strategy '{name}': could not parse Position Size")
                continue
            
            # Validate condition string
            if not _validate_condition(condition):
                logger.warning(f"Invalid condition for strategy '{name}': {condition}")
                continue
            
            strategy = {
                "name": name,
                "type": strategy_type,
                "condition": condition,
                "params": {
                    "stop_loss_pct": stop_loss,
                    "take_profit_pct": take_profit,
                    "position_size_pct": position_size,
                    "atr_multiplier": atr_multiplier,  # T024: Added
                    "volume_threshold": volume_threshold  # T017: Added
                }
            }
            
            strategies.append(strategy)
            # T018: Add test logging to confirm volume_threshold parsed
            logger.info(f"  ✓ Loaded strategy: {name} ({strategy_type}) [ATR: {atr_multiplier}, Vol Threshold: {volume_threshold}]")
        
        if not strategies:
            logger.warning("No strategies parsed from file")
        else:
            logger.info(f"✓ Successfully loaded {len(strategies)} strategies")
        
        return strategies
        
    except Exception as e:
        logger.error(f"Error loading strategies: {e}")
        return []


def _validate_condition(condition_str: str) -> bool:
    """
    Validate that a condition string is valid Pandas query syntax.
    
    Args:
        condition_str: Pandas query string to validate
        
    Returns:
        True if valid, False otherwise
    """
    try:
        # Create a minimal test DataFrame
        test_df = pd.DataFrame({
            'close': [100],
            'open': [99],
            'high': [101],
            'low': [98],
            'volume': [1000],
            'rsi': [50],
            'ema_200': [95],
            'atr': [2],
            'bb_lower': [90],
            'bb_mid': [95],
            'bb_upper': [100],
            'adx': [25],
            'macd': [0.5],
            'macd_signal': [0.4],
            'macd_histogram': [0.1],
            'macd_bullish_cross': [False],
            'macd_bearish_cross': [False],
            'stoch_rsi_k': [50],
            'stoch_rsi_d': [45],
            'stoch_rsi_bullish': [False],
            'stoch_rsi_bearish': [False]
        })
        
        # Attempt to query - if it doesn't raise an exception, it's valid
        test_df.query(condition_str)
        return True
        
    except Exception as e:
        logger.debug(f"Condition validation failed: {e}")
        return False
