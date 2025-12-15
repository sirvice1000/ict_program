"""
Order Blocks (OB) - ICT Concept
"""

CONCEPT_DATA = {
    'title': 'Order Blocks (OB)',
    'short_name': 'OB',
    'summary': 'Zones where institutional traders placed large orders, creating areas that act as support or resistance when price returns.',
    'key_points': [
        'The last opposite candle before an impulsive move is the OB',
        'Works best when aligned with higher timeframe trend',
        'OBs get weaker with multiple tests - first test is strongest',
        'Failed Order Blocks become Breaker Blocks (polarity change)',
        'Best during killzone times when institutions are active',
        'Use 50% of OB (Mean Threshold) for better entry'
    ],
    'definition': """
**Bullish Order Block:**
• Last BEARISH candle before strong bullish move
• Represents where institutions placed BUY orders
• Acts as SUPPORT when price returns

**Bearish Order Block:**
• Last BULLISH candle before strong bearish move
• Represents where institutions placed SELL orders
• Acts as RESISTANCE when price returns

**Entry Methods:**
1. Aggressive: Buy/Sell stop above/below key candles
2. Conservative: Wait for price to return to OB zone
3. High Probability: Combine with FVG + liquidity sweep

**Stop Loss:**
• Bullish OB: 10-20 pips below the low
• Bearish OB: 10-20 pips above the high

**Invalidation:**
• Price closes completely through without reaction
""",
    'category': 'ICT Concepts'
}
