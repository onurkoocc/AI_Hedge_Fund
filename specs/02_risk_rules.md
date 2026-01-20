# Risk Management Rules

## Critical Rule: 1:2 Risk/Reward Ratio

**Formula**: `(Target - Entry) / (Entry - Stop) >= 2.0`

Every trade setup MUST satisfy this minimum ratio. If a setup doesn't meet 1:2 R:R, it must be rejected.

### Example Calculation
- Entry: $100
- Stop Loss: $98 (Risk: $2)
- Take Profit: $104 (Reward: $4)
- R:R Ratio: 4 / 2 = **2:1** ✅ VALID

## Mini-Backtest Validation (Proof Engine)

Before any trade is proposed:

1. **Identify Last 3 Signals**: Find the most recent 3 occurrences where the strategy condition was true
2. **Simulate Each Trade**: For each historical signal, simulate the trade outcome:
   - Did it hit Take Profit?
   - Did it hit Stop Loss?
   - What was the P&L percentage?
3. **Report Results**: Present all 3 trade results to the user

### Acceptance Criteria
- At least 2 out of 3 historical signals should be profitable
- If 2 or more failed, flag the setup as "High Risk"
- Always show the user the proof - transparency is mandatory

## Trade Specification Requirements

Every trade proposal must include:

1. **Entry Price**: Specific price level (Limit or Market)
2. **Stop Loss**: Exact price where position closes if wrong
3. **Take Profit**: Target price for profit-taking
4. **Position Size**: Calculated based on risk per trade (typically 1-2% of capital)
5. **Risk/Reward Ratio**: Explicitly stated (must be >= 2.0)

## Position Sizing Formula

```
Risk Per Trade = 1% of Total Capital
Position Size = (Risk Amount) / (Entry - Stop Loss)
```

### Example
- Capital: $10,000
- Risk: 1% = $100
- Entry: $50
- Stop: $48
- Position Size: $100 / ($50 - $48) = 50 units

## Emergency Exit Rules

1. If market sentiment shifts dramatically (Fear & Greed Index moves > 20 points in a day), re-evaluate all open positions
2. If macro correlation breaks (e.g., Gold diverges from expected behavior), consider hedging
3. Never hold through major news events without stops in place
