"""
Daily Range - ICT Concept
"""

CONCEPT_DATA = {
    'title': 'Daily Range',
    'short_name': 'DAILY_RANGE',
    'summary': 'The high and low of the current or previous trading day. Essential for understanding daily structure and setting profit targets.',
    'key_points': [
        'Previous Day High (PDH) and Low (PDL) are critical levels',
        'Current day often seeks to take out PDH or PDL',
        'Used to calculate average true range for position sizing',
        'Daily 50% level often acts as support/resistance',
        'Range expansion days follow range contraction',
        'Track relationship between daily ranges for context'
    ],
    'definition': """
**Daily Range Components:**

**Key Levels:**
• **Daily High (DH):** Highest point of current day
• **Daily Low (DL):** Lowest point of current day
• **Previous Day High (PDH):** Yesterday's high - key resistance
• **Previous Day Low (PDL):** Yesterday's low - key support
• **Daily Midpoint:** 50% of current daily range
• **Daily Open:** Where price opened at midnight EST

**Using Daily Range:**

1. **Previous Day Levels (Most Important):**
   
   **PDH (Previous Day High):**
   • Acts as resistance on bullish days
   • Breaking PDH = very bullish signal
   • Often swept before reversal
   • Target when in bullish trend
   
   **PDL (Previous Day Low):**
   • Acts as support on bearish days
   • Breaking PDL = very bearish signal
   • Often swept before reversal
   • Target when in bearish trend

2. **Daily Range Analysis:**
   
   **Range Expansion:**
   • Today's range > Yesterday's range
   • Indicates strong directional move
   • Often follows multiple small range days
   • High probability of trend continuation
   
   **Range Contraction:**
   • Today's range < Yesterday's range
   • Market consolidating
   • Precedes big moves
   • Reduce position size

3. **Trading Strategies:**
   
   **Breakout Trades:**
   • Wait for break of PDH (bullish) or PDL (bearish)
   • Confirm with structure shift
   • Enter on retest of broken level
   • Target: Previous week high/low
   
   **Range Bound Trades:**
   • Fade extremes when range is established
   • Buy at daily low, sell at daily high
   • Only in clear ranging markets
   • Use tight stops

4. **Daily 50% Rule:**
   • Calculate: (DH + DL) / 2
   • Above 50% = bullish bias
   • Below 50% = bearish bias
   • Price often returns to 50% (mean reversion)

**Practical Example:**

Yesterday (Previous Day):
• PDH: 4600
• PDL: 4550
• Range: 50 points

Today (Current Day):
• Price opens at 4575
• Morning low: 4565
• Current price: 4585

**Analysis:**
• Price held above PDL (4550) - bullish sign
• If break above PDH (4600), go long
• Target next resistance level
• Stop below daily low (4565) or PDL (4550)

**Daily Range Tips:**
• Track daily ranges in a journal
• Average daily range helps with targets
• Expanding ranges = trending market
• Contracting ranges = prepare for breakout
• PDH/PDL are magnets for price
""",
    'category': 'ICT Concepts'
}
