"""Test strategy loader with volume threshold - detailed"""
from src.strategy_loader import load_strategies

strategies = load_strategies()
print(f"\nFound {len(strategies)} strategies:\n")
for s in strategies:
    name = s['name']
    vol_threshold = s['params'].get('volume_threshold', 'N/A')
    atr = s['params'].get('atr_multiplier', 'N/A')
    print(f"  {name}: volume_threshold={vol_threshold}, atr={atr}")
