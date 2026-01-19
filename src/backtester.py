"""
Backtest proof engine for Market Scanner Core System.

This is NOT a full backtesting framework. It's a "signal validator" that verifies
trading signals by simulating the last 3 historical occurrences.

Key Concept: Before proposing a trade, show proof that this signal has worked 
in the past by backtesting the last 3 times it occurred.
"""

import logging
import argparse
import json
from typing import List, Dict, Any
import pandas as pd

logger = logging.getLogger(__name__)


def find_signal_dates(df: pd.DataFrame, condition_str: str) -> List[int]:
    """
    Find dates where a strategy condition was True.
    
    Args:
        df: DataFrame with technical indicators
        condition_str: Pandas query string (e.g., "rsi < 30 and close > ema_200")
        
    Returns:
        List of integer indices where condition was True (last 3 occurrences)
        Returns empty list if no signals found or invalid condition
    """
    try:
        # Validate condition by attempting query
        mask = df.query(condition_str).index
        
        if len(mask) == 0:
            logger.warning(f"No signals found for condition: {condition_str}")
            return []
        
        # Get the indices (positions) of True values
        signal_indices = df.index.get_indexer(mask)
        
        # Return last 3 signals
        last_3 = signal_indices[-3:].tolist() if len(signal_indices) >= 3 else signal_indices.tolist()
        
        if len(last_3) < 3:
            logger.warning(f"Only found {len(last_3)} signals (expected 3)")
        
        return last_3
        
    except Exception as e:
        logger.error(f"Error finding signal dates: {e}")
        return []


def simulate_trade(
    df: pd.DataFrame, 
    entry_idx: int, 
    stop_loss_pct: float = 0.02, 
    take_profit_pct: float = 0.04
) -> Dict[str, Any]:
    """
    Simulate a single trade from entry to exit (TP or SL).
    
    This implements the 1:2 Risk/Reward rule from specs/02_risk_rules.md
    
    Args:
        df: DataFrame with OHLCV data
        entry_idx: Index position where trade entry occurs
        stop_loss_pct: Stop loss as percentage below entry (e.g., 0.02 = 2%)
        take_profit_pct: Take profit as percentage above entry (e.g., 0.04 = 4%)
        
    Returns:
        Dictionary with keys:
        - result: "TP" (take profit), "SL" (stop loss), or "Open" (insufficient data)
        - pnl_percent: P&L as decimal (e.g., 0.04 = 4% profit)
        - duration_bars: Number of candles until exit
    """
    try:
        # Validate index
        if entry_idx >= len(df):
            logger.error(f"Invalid entry index: {entry_idx} >= {len(df)}")
            return {"result": "Open", "pnl_percent": 0.0, "duration_bars": 0}
        
        # Get entry price
        entry_price = df.iloc[entry_idx]['close']
        
        # Calculate stop loss and take profit levels
        stop_loss_price = entry_price * (1 - stop_loss_pct)
        take_profit_price = entry_price * (1 + take_profit_pct)
        
        logger.debug(f"Entry: ${entry_price:.2f}, SL: ${stop_loss_price:.2f}, TP: ${take_profit_price:.2f}")
        
        # Scan forward bars to see which level is hit first
        for i in range(entry_idx + 1, len(df)):
            bar = df.iloc[i]
            
            # Check if stop loss hit (price went below SL)
            if bar['low'] <= stop_loss_price:
                duration = i - entry_idx
                pnl = -stop_loss_pct  # Negative return
                logger.debug(f"SL hit at bar {i}, duration: {duration}, PnL: {pnl:.2%}")
                return {
                    "result": "SL",
                    "pnl_percent": pnl,
                    "duration_bars": duration
                }
            
            # Check if take profit hit (price went above TP)
            if bar['high'] >= take_profit_price:
                duration = i - entry_idx
                pnl = take_profit_pct  # Positive return
                logger.debug(f"TP hit at bar {i}, duration: {duration}, PnL: {pnl:.2%}")
                return {
                    "result": "TP",
                    "pnl_percent": pnl,
                    "duration_bars": duration
                }
        
        # If we get here, neither SL nor TP was hit (insufficient future data)
        logger.warning(f"Trade still open at end of data (entry_idx: {entry_idx})")
        return {
            "result": "Open",
            "pnl_percent": 0.0,
            "duration_bars": len(df) - entry_idx - 1
        }
        
    except Exception as e:
        logger.error(f"Error simulating trade: {e}")
        return {"result": "Open", "pnl_percent": 0.0, "duration_bars": 0}


def backtest_strategy(
    df: pd.DataFrame, 
    condition_str: str, 
    stop_loss_pct: float = 0.02, 
    take_profit_pct: float = 0.04
) -> List[Dict[str, Any]]:
    """
    Backtest a strategy by finding last 3 signals and simulating each trade.
    
    This is the main "proof engine" function.
    
    Args:
        df: DataFrame with OHLCV and indicators
        condition_str: Strategy condition (Pandas query string)
        stop_loss_pct: Stop loss percentage (default: 2%)
        take_profit_pct: Take profit percentage (default: 4%, giving 2:1 R:R)
        
    Returns:
        List of backtest results matching backtest-schema.json format
    """
    try:
        # Validate inputs
        if df.empty:
            logger.error("Cannot backtest on empty DataFrame")
            return []
        
        # Find signal dates
        signal_indices = find_signal_dates(df, condition_str)
        
        if not signal_indices:
            logger.info("No signals found to backtest")
            return []
        
        logger.info(f"Found {len(signal_indices)} signals, simulating trades...")
        
        # Simulate each signal
        results = []
        for idx in signal_indices:
            # Get signal date
            signal_date = df.index[idx]
            
            # Simulate trade
            trade_result = simulate_trade(df, idx, stop_loss_pct, take_profit_pct)
            
            # Build result dict
            result = {
                "signal_date": signal_date.strftime('%Y-%m-%d %H:%M:%S'),
                "result": trade_result["result"],
                "pnl_percent": round(trade_result["pnl_percent"] * 100, 2),  # Convert to percentage
                "duration_bars": trade_result["duration_bars"]
            }
            
            results.append(result)
            
            logger.info(f"  {result['signal_date']}: {result['result']} ({result['pnl_percent']:+.2f}%)")
        
        return results
        
    except Exception as e:
        logger.error(f"Error in backtest_strategy: {e}")
        return []


def main():
    """
    Standalone test mode for backtester.
    
    Usage:
        python src/backtester.py --symbol BTC/USDT --condition "rsi < 30" --days 90
    """
    parser = argparse.ArgumentParser(description='Backtest a trading strategy')
    parser.add_argument('--symbol', type=str, default='BTC/USDT', help='Trading symbol')
    parser.add_argument('--condition', type=str, required=True, help='Strategy condition (Pandas query)')
    parser.add_argument('--days', type=int, default=90, help='Days of historical data')
    parser.add_argument('--stop-loss', type=float, default=0.02, help='Stop loss percentage (e.g., 0.02 = 2%)')
    parser.add_argument('--take-profit', type=float, default=0.04, help='Take profit percentage (e.g., 0.04 = 4%)')
    
    args = parser.parse_args()
    
    # Setup logging
    from .utils import setup_logging
    setup_logging()
    
    logger.info("=" * 60)
    logger.info("BACKTEST PROOF ENGINE - Standalone Test Mode")
    logger.info("=" * 60)
    
    # Import data fetching functions
    from .data_loader import fetch_crypto_data
    from .analysis import calculate_indicators
    
    # Fetch data
    logger.info(f"Fetching {args.symbol} data for {args.days} days...")
    df = fetch_crypto_data(args.symbol, days=args.days)
    
    if df.empty:
        logger.error("Failed to fetch data")
        return
    
    # Calculate indicators
    logger.info("Calculating technical indicators...")
    df = calculate_indicators(df)
    
    # Run backtest
    logger.info(f"Running backtest for condition: {args.condition}")
    results = backtest_strategy(df, args.condition, args.stop_loss, args.take_profit)
    
    # Print results as JSON
    print("\n" + "=" * 60)
    print("BACKTEST RESULTS:")
    print("=" * 60)
    print(json.dumps(results, indent=2))
    
    # Calculate summary stats
    if results:
        wins = sum(1 for r in results if r['result'] == 'TP')
        losses = sum(1 for r in results if r['result'] == 'SL')
        win_rate = (wins / len(results) * 100) if results else 0
        
        print("\n" + "=" * 60)
        print("SUMMARY:")
        print("=" * 60)
        print(f"Total Signals: {len(results)}")
        print(f"Wins: {wins} ({win_rate:.1f}%)")
        print(f"Losses: {losses}")
        print("=" * 60)


if __name__ == '__main__':
    main()
