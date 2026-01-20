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
        strategy_pattern = r'### \d+\.\s+(.+?)\n\n\*\*Type\*\*:\s*(.+?)\n.*?\n\n\*\*Entry Condition\*\*:\s*\n```python\n"(.+?)"\n```.*?\n\*\*Parameters\*\*:\s*\n-\s+Stop Loss:\s*(\d+)%.*?\n-\s+Take Profit:\s*(\d+\.?\d*)%.*?\n-\s+Position Size:\s*([\d.]+)%'
        
        matches = re.finditer(strategy_pattern, content, re.DOTALL)
        
        for match in matches:
            name = match.group(1).strip()
            strategy_type = match.group(2).strip()
            condition = match.group(3).strip()
            stop_loss = float(match.group(4)) / 100  # Convert to decimal
            take_profit = float(match.group(5)) / 100
            position_size = float(match.group(6)) / 100
            
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
                    "position_size_pct": position_size
                }
            }
            
            strategies.append(strategy)
            logger.info(f"  ✓ Loaded strategy: {name} ({strategy_type})")
        
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
