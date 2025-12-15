"""
Opening Range - ICT Concept
"""

CONCEPT_DATA = {
    'title': 'Opening Range',
    'short_name': 'OPENING_RANGE',
    'summary': 'The high and low established during the first 30-60 minutes of the trading session. Often determines the day\'s directional bias.',
    'key_points': [
        'Measured from 9:30 AM to 10:00 AM EST (30 min) or 10:30 AM (60 min)',
        'Often sees manipulation before true directional move',
        'Breaking above opening range high = bullish signal',
        'Breaking below opening range low = bearish signal',
        'Institutional orders often triggered at these levels',
        'Can be used as stop loss reference points'
    ],
    'definition': """
**Opening Range Mechanics:**

**Time Frames:**
• **30-Minute OR:** 9:30 AM - 10:00 AM EST
• **60-Minute OR:** 9:30 AM - 10:30 AM EST

**Components:**
• OR High: Highest price during opening period
• OR Low: Lowest price during opening period
• OR Midpoint: 50% level between high and low

**Trading the Opening Range:**

1. **Initial Formation (9:30-10:00 AM):**
   • Market opens with volatility
   • Often sees stop hunts in both directions
   • Wait for range to establish
   • Don't trade during formation

2. **Post-Range Strategy (After 10:00 AM):**
   
   **Bullish Scenario:**
   • Price breaks above OR High
   • Retest of OR High as support
   • Entry: On retest with confirmation
   • Stop: Below OR Low
   • Target: Previous day high or beyond
   
   **Bearish Scenario:**
   • Price breaks below OR Low
   • Retest of OR Low as resistance
   • Entry: On retest with confirmation
   • Stop: Above OR High
   • Target: Previous day low or beyond

3. **Advanced Concepts:**
   • **Judas Swing:** False break one way, then reversal
     - Example: Break OR High, fail, then crash through OR Low
   • **True Day:** Respects OR and continues in one direction
   • **Turtle Soup:** Fake-out of OR high/low, then reversal

**Opening Range Rules:**
• Never chase the initial break - wait for retest
• OR levels often magnetize price throughout the day
• 50% of OR is key intraday level
• Best in trending markets, less reliable in ranges
• Combine with daily bias for best results

**Example:**
OR High: 4580 (10:00 AM)
OR Low: 4560 (10:00 AM)
OR Midpoint: 4570

Bullish Setup: Price breaks 4580 at 10:15 AM, retests 4580 at 10:45 AM, enters long with stop at 4560.
""",
    'category': 'ICT Concepts'
}
