"""
CME Data - Next Day High/Low Projection - ICT Concept
"""

CONCEPT_DATA = {
    'title': 'CME Data - Next Day High/Low',
    'short_name': 'CME_NEXTDAY',
    'summary': 'Using CME settlement prices and ranges to project the next trading day\'s potential high and low. A powerful forecasting tool for intraday traders.',
    'key_points': [
        'CME settlement = official closing price for futures contracts',
        'Used by institutions to calculate next day parameters',
        'Combines previous day range with settlement price',
        'Most accurate for index futures (ES, NQ, YM)',
        'Helps identify key levels before market opens',
        'Not exact predictions - but high probability zones'
    ],
    'definition': """
**Understanding CME Data:**

**What is CME Settlement?**
• Official closing price determined by CME Group
• Published around 4:00 PM EST for equity index futures
• Different from where cash market closes
• Institutions use this for next day calculations
• Found on CME website or trading platforms

**Key CME Contracts:**
• **ES** - E-mini S&P 500
• **NQ** - E-mini NASDAQ-100
• **YM** - E-mini Dow Jones

**Method 1: Basic Range Projection**

Formula:
1. Calculate Previous Day Range:
   Range = Previous Day High - Previous Day Low

2. Project Next Day High:
   Settlement Price + Range = Next Day High (projected)

3. Project Next Day Low:
   Settlement Price - Range = Next Day Low (projected)

**Example:**
Previous Day:
• High: 4600
• Low: 4550
• Range: 50 points
• CME Settlement: 4580

Next Day Projection:
• Projected High: 4580 + 50 = 4630
• Projected Low: 4580 - 50 = 4530

**Method 2: Fibonacci Extension**

Instead of using full range, use Fibonacci ratios:

Next Day High: Settlement + (Range × 0.618)
Next Day Low: Settlement - (Range × 0.618)

**Example:**
• Settlement: 4580
• Range: 50
• 61.8% of Range: 50 × 0.618 = 30.9

Next Day Projection:
• Projected High: 4580 + 31 = 4611
• Projected Low: 4580 - 31 = 4549

**Method 3: Using Opening Reference Price**

Some traders use CME opening price instead:

1. Get CME Opening Price (usually 6:00 PM EST)
2. Calculate range from settlement to opening
3. Project from opening price

**How to Use These Projections:**

1. **Before Market Opens:**
   • Calculate projected high/low
   • Mark levels on your chart
   • Plan potential entries

2. **During Trading Day:**
   • Watch for price approaching levels
   • Use as profit targets
   • Look for reversals at extremes
   • Combine with other ICT concepts

3. **Trade Examples:**
   
   **Scenario A - Buying Discount:**
   • Next Day Low projected: 4530
   • Price drops to 4535 in morning
   • Enter long with stop at 4525
   • Target: Settlement (4580) or Next Day High (4630)
   
   **Scenario B - Selling Premium:**
   • Next Day High projected: 4630
   • Price rallies to 4625 in afternoon
   • Enter short with stop at 4635
   • Target: Settlement (4580) or Next Day Low (4530)

**Advanced Tips:**

1. **Accuracy Improves When:**
   • Market is trending
   • Clear daily bias exists
   • Previous day had normal range
   • No major news events scheduled

2. **Less Accurate When:**
   • Major news pending (Fed, NFP, etc.)
   • Previous day had unusual range
   • Market gapping significantly
   • Low volume holidays

3. **Refinements:**
   • Track actual vs projected daily
   • Calculate average error margin
   • Adjust for market conditions
   • Use multiple projection methods

**Where to Find CME Data:**

• CME Group website: www.cmegroup.com
• Trading platforms (Think or Swim, TradingView, etc.)
• Financial news sites (Bloomberg, CNBC)
• Your broker's platform

**Integration with Market Tab:**

Your Market Tab has:
• CME settlement input fields
• Automatic calculations
• Clear visual display
• Save daily data for tracking

**Practical Workflow:**

Evening (after market close):
1. Get CME settlement from official source
2. Enter in Market Tab
3. Note projected high/low
4. Review with weekly/daily structure

Next Morning:
1. Mark levels on chart
2. Set alerts at projected zones
3. Wait for price to approach
4. Execute with ICT setups (FVG, OB, etc.)

**Remember:**
• These are probability zones, not guarantees
• Always use with proper risk management
• Combine with other ICT concepts
• Price doesn't always reach both levels
• Some days exceed projections
""",
    'category': 'ICT Concepts'
}
