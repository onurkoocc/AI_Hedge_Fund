"""
Market Scanner - Main CLI Tool

This orchestrates the entire market scanning workflow:
1. Fetch data (crypto, macro, sentiment)
2. Calculate technical indicators
3. Scan for strategy signals
4. Backtest signal verification (proof engine)
5. Generate Markdown report

Usage:
    python tools/market_scanner.py
    python tools/market_scanner.py --symbols BTC/USDT ETH/USDT --output custom_report.md
"""

import logging
import argparse
import time
from pathlib import Path
from typing import List, Dict, Any
import sys

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils import setup_logging, get_timestamp
from src.data_loader import fetch_crypto_data, fetch_macro_data, fetch_rss_headlines, calculate_sentiment
from src.analysis import calculate_indicators, merge_macro_data
from src.backtester import backtest_strategy
from src.strategy_loader import load_strategies

logger = logging.getLogger(__name__)


def main():
    """
    Main market scanning workflow.
    
    Steps:
    1. Data Collection: Fetch crypto, macro, and sentiment data
    2. Analysis: Calculate indicators and merge macro data
    3. Signal Scanning: Apply strategies to find trading signals
    4. Backtest Verification: Validate signals with historical proof
    5. Report Generation: Create Markdown report with all findings
    """
    
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Market Scanner - AI Hedge Fund Core System')
    parser.add_argument('--symbols', nargs='+', default=['BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'BNB/USDT', 'XRP/USDT'],
                        help='Crypto symbols to scan')
    parser.add_argument('--days', type=int, default=180, help='Days of historical data')
    parser.add_argument('--output-path', type=str, default='output/market_snapshot.md',
                        help='Output report file path')
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging()
    
    # Track execution time
    start_time = time.time()
    
    try:
        logger.info("=" * 70)
        logger.info("MARKET SCANNER - AI HEDGE FUND")
        logger.info("=" * 70)
        logger.info(f"Scanning {len(args.symbols)} assets with {args.days} days of history")
        logger.info("")
        
        # ==================================================================
        # STEP 1: DATA COLLECTION
        # ==================================================================
        logger.info("STEP 1: DATA COLLECTION")
        logger.info("-" * 70)
        
        # Fetch crypto data
        crypto_data = {}
        for symbol in args.symbols:
            try:
                df = fetch_crypto_data(symbol, days=args.days)
                if not df.empty:
                    crypto_data[symbol] = df
                else:
                    logger.warning(f"⚠ Skipping {symbol} (no data)")
            except Exception as e:
                logger.error(f"✗ Error fetching {symbol}: {e}")
                continue  # Continue with other symbols
        
        if not crypto_data:
            logger.error("No crypto data fetched. Aborting.")
            return
        
        # Fetch macro data
        macro_symbols = {
            'gold': 'GC=F',
            'dxy': 'DX-Y.NYB',
            'sp500': '^GSPC'
        }
        
        macro_data = {}
        for name, symbol in macro_symbols.items():
            try:
                df = fetch_macro_data(symbol, days=args.days)
                if not df.empty:
                    macro_data[name] = df
            except Exception as e:
                logger.error(f"✗ Error fetching {name}: {e}")
                continue
        
        # Fetch sentiment data
        rss_feeds = [
            'https://cointelegraph.com/rss',
            'https://www.coindesk.com/arc/outboundfeeds/rss/',
        ]
        
        sentiment_score = 0.0
        try:
            headlines = fetch_rss_headlines(rss_feeds)
            sentiment_score = calculate_sentiment(headlines)
        except Exception as e:
            logger.error(f"✗ Error fetching sentiment: {e}")
        
        logger.info("")
        
        # ==================================================================
        # STEP 2: TECHNICAL ANALYSIS
        # ==================================================================
        logger.info("STEP 2: TECHNICAL ANALYSIS")
        logger.info("-" * 70)
        
        # Calculate indicators for each crypto asset
        for symbol, df in crypto_data.items():
            try:
                logger.info(f"Analyzing {symbol}...")
                
                # Calculate indicators
                df = calculate_indicators(df)
                
                # Merge macro data
                if macro_data:
                    df = merge_macro_data(df, macro_data)
                
                # Update in dictionary
                crypto_data[symbol] = df
                
                # Validate critical columns
                critical_cols = ['rsi', 'ema_200', 'close']
                missing = [col for col in critical_cols if col not in df.columns]
                if missing:
                    logger.warning(f"⚠ {symbol} missing columns: {missing}")
                else:
                    logger.info(f"✓ {symbol} analysis complete")
                
            except Exception as e:
                logger.error(f"✗ Error analyzing {symbol}: {e}")
                continue
        
        logger.info("")
        
        # ==================================================================
        # STEP 3: SIGNAL SCANNING
        # ==================================================================
        logger.info("STEP 3: SIGNAL SCANNING")
        logger.info("-" * 70)
        
        # Load strategies
        strategies = load_strategies()
        
        if not strategies:
            logger.error("No strategies loaded. Aborting.")
            return
        
        # Scan for signals
        found_signals = []
        
        for symbol, df in crypto_data.items():
            for strategy in strategies:
                try:
                    logger.info(f"↻ Scanning {strategy['name']} on {symbol}...")
                    
                    # Check if current (last) candle matches strategy condition
                    # Use last 1 row to check current signal
                    current_row = df.tail(1)
                    
                    # Check condition
                    matches = current_row.query(strategy['condition'])
                    
                    if not matches.empty:
                        # Signal found!
                        signal = {
                            "asset": symbol,
                            "strategy": strategy['name'],
                            "strategy_type": strategy['type'],
                            "timestamp": df.index[-1].strftime('%Y-%m-%d %H:%M:%S'),
                            "entry_price": float(df['close'].iloc[-1]),
                            "condition": strategy['condition'],
                            "params": strategy['params']
                        }
                        
                        found_signals.append(signal)
                        logger.info(f"  ✓ SIGNAL FOUND: {symbol} @ ${signal['entry_price']:.2f}")
                
                except Exception as e:
                    logger.error(f"  ✗ Error scanning {strategy['name']} on {symbol}: {e}")
                    continue
        
        logger.info(f"\nTotal signals found: {len(found_signals)}")
        logger.info("")
        
        # ==================================================================
        # STEP 4: BACKTEST VERIFICATION (PROOF ENGINE)
        # ==================================================================
        logger.info("STEP 4: BACKTEST VERIFICATION")
        logger.info("-" * 70)
        
        for signal in found_signals:
            try:
                symbol = signal['asset']
                df = crypto_data[symbol]
                
                logger.info(f"Verifying {symbol} {signal['strategy']}...")
                
                # Run backtest for this strategy
                backtest_results = backtest_strategy(
                    df,
                    signal['condition'],
                    stop_loss_pct=signal['params']['stop_loss_pct'],
                    take_profit_pct=signal['params']['take_profit_pct']
                )
                
                # Attach proof to signal
                signal['proof'] = backtest_results
                
                # Calculate win rate
                if backtest_results:
                    wins = sum(1 for r in backtest_results if r['result'] == 'TP')
                    total = len(backtest_results)
                    win_rate = (wins / total * 100) if total > 0 else 0
                    signal['win_rate'] = win_rate
                    
                    logger.info(f"  ✓ Proof: {wins}/{total} wins ({win_rate:.0f}%)")
                else:
                    signal['proof'] = []
                    signal['win_rate'] = 0
                    logger.warning(f"  ⚠ No backtest proof available")
                
            except Exception as e:
                logger.error(f"  ✗ Error verifying {signal['asset']}: {e}")
                signal['proof'] = []
                signal['win_rate'] = 0
        
        logger.info("")
        
        # ==================================================================
        # STEP 5: REPORT GENERATION
        # ==================================================================
        logger.info("STEP 5: REPORT GENERATION")
        logger.info("-" * 70)
        
        report_content = generate_markdown_report(
            found_signals,
            sentiment_score,
            get_timestamp(),
            args.symbols
        )
        
        # Write report to file
        output_path = Path(args.output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        logger.info(f"✓ Report saved to: {output_path}")
        logger.info("")
        
        # ==================================================================
        # COMPLETION
        # ==================================================================
        elapsed_time = time.time() - start_time
        
        logger.info("=" * 70)
        logger.info(f"✓ Market scan complete in {elapsed_time:.1f}s")
        logger.info(f"✓ Report: {output_path}")
        logger.info(f"✓ Signals Found: {len(found_signals)}")
        logger.info("=" * 70)
        
    except Exception as e:
        logger.error(f"✗ Fatal error in market scanner: {e}", exc_info=True)
        sys.exit(1)


def generate_markdown_report(
    signals: List[Dict[str, Any]],
    sentiment_score: float,
    timestamp: str,
    scanned_symbols: List[str]
) -> str:
    """
    Generate a Markdown report for LLM consumption.
    
    Args:
        signals: List of signal dictionaries with backtest proof
        sentiment_score: Sentiment score from -1 to +1
        timestamp: Generation timestamp
        scanned_symbols: List of symbols that were scanned
        
    Returns:
        Markdown-formatted report string
    """
    
    # Start report
    report = f"""# Market Snapshot Report

**Generated**: {timestamp}  
**Sentiment Score**: {sentiment_score:+.3f} {'📈 Bullish' if sentiment_score > 0.2 else '📉 Bearish' if sentiment_score < -0.2 else '😐 Neutral'}  
**Assets Scanned**: {', '.join(scanned_symbols)}

---

"""
    
    # Add signals section
    if signals:
        report += f"## 🎯 Trading Signals ({len(signals)} Found)\n\n"
        
        for i, signal in enumerate(signals, 1):
            # Check if signal meets 1:2 R:R ratio
            rr_ratio = signal['params']['take_profit_pct'] / signal['params']['stop_loss_pct']
            rr_check = "✅" if rr_ratio >= 2.0 else "⚠️"
            
            report += f"### Signal {i}: {signal['asset']} - {signal['strategy']}\n\n"
            report += f"- **Type**: {signal['strategy_type']}\n"
            report += f"- **Entry Price**: ${signal['entry_price']:.2f}\n"
            report += f"- **Timestamp**: {signal['timestamp']}\n"
            report += f"- **Stop Loss**: {signal['params']['stop_loss_pct'] * 100:.1f}%\n"
            report += f"- **Take Profit**: {signal['params']['take_profit_pct'] * 100:.1f}%\n"
            report += f"- **R:R Ratio**: {rr_check} {rr_ratio:.1f}:1\n"
            report += f"- **Win Rate (Last 3)**: {signal['win_rate']:.0f}%\n\n"
            
            # Add backtest proof table
            if signal['proof']:
                report += "**Backtest Proof (Last 3 Signals)**:\n\n"
                report += "| Signal Date | Result | P&L | Duration |\n"
                report += "|-------------|--------|-----|----------|\n"
                
                for proof in signal['proof']:
                    result_emoji = "✅" if proof['result'] == 'TP' else "❌" if proof['result'] == 'SL' else "⏸️"
                    report += f"| {proof['signal_date']} | {result_emoji} {proof['result']} | {proof['pnl_percent']:+.2f}% | {proof['duration_bars']} bars |\n"
                
                report += "\n"
            else:
                report += "⚠️ **No backtest proof available** (insufficient historical signals)\n\n"
            
            report += "---\n\n"
    
    else:
        report += "## 😴 No Trading Signals Found\n\n"
        report += "No strategy conditions were met in the current market scan.\n\n"
        report += "**Possible Reasons**:\n"
        report += "- Market is not in a favorable condition for defined strategies\n"
        report += "- All assets are outside strategy entry criteria\n"
        report += "- This is normal - quality over quantity (max 5 trades/month)\n\n"
    
    # Add footer
    report += "---\n\n"
    report += "## 📋 Next Steps\n\n"
    report += "1. Review signals against specs/02_risk_rules.md (1:2 R:R minimum)\n"
    report += "2. Check backtest proof - prefer signals with 2/3+ wins\n"
    report += "3. Consider macro context and sentiment before entry\n"
    report += "4. Remember: Maximum 5 trades per month (Sniper approach)\n\n"
    report += "*This report is for analysis purposes. Always validate before live trading.*\n"
    
    return report


if __name__ == '__main__':
    main()
