"""
Fair Value Gap (FVG) - ICT Concept
COMPREHENSIVE GUIDE - Maximum Detail
"""

CONCEPT_DATA = {
    'title': 'Fair Value Gap (FVG)',
    'short_name': 'FVG',
    'category': 'ICT Core Concepts - Price Action',
    
    'summary': '''A Fair Value Gap is a three-candle price imbalance that occurs when the market moves so rapidly that 
it leaves an unfilled gap between candle wicks. This gap represents an area where price moved too quickly for 
efficient price discovery, creating an imbalance that the market often returns to "fill" or "rebalance." FVGs are 
considered institutional footprints and high-probability reversal or continuation zones.''',
    
    'key_points': [
        'FVGs form when there is NO overlap between candle 1 wick and candle 3 wick',
        'The middle candle (candle 2) creates the gap through its impulsive move',
        'Consequent Encroachment (50% of gap) is the most powerful reaction zone',
        'FVGs work best during killzone times (2AM-5AM, 8AM-11AM, 1PM-4PM EST)',
        'Higher timeframe FVGs (4H, Daily) are more significant than lower timeframes',
        'FVGs can invert (IFVG) when price completely breaks through without filling',
        'Combine with market structure, order blocks, and liquidity for highest probability',
        'Not every FVG gets filled - context determines which ones are tradeable',
        'FVGs act as support in uptrends and resistance in downtrends',
        'Multiple FVGs stacked together create stronger confluence zones'
    ],
    
    'definition': '''
═══════════════════════════════════════════════════════════════════
WHAT IS A FAIR VALUE GAP?
═══════════════════════════════════════════════════════════════════

A Fair Value Gap (FVG) is a specific three-candle price pattern that reveals where 
institutional algorithms moved price so aggressively that inefficient pricing occurred.

The Pattern Formation:
---------------------
Candle 1: Sets up the move (has a wick - high or low)
Candle 2: The impulsive candle (moves aggressively)
Candle 3: Continuation or reversal (has opposite wick)

The Gap: Area between Candle 1 wick and Candle 3 wick with NO overlap


═══════════════════════════════════════════════════════════════════
BULLISH FVG (Acts as Support)
═══════════════════════════════════════════════════════════════════

Formation:
• Candle 1: Bearish or neutral - note its HIGH
• Candle 2: Bullish impulsive move upward
• Candle 3: Bullish or neutral - note its LOW

The Gap = Space between Candle 1 HIGH and Candle 3 LOW

Rules for Bullish FVG:
1. Candle 1 high must NOT touch Candle 3 low
2. Gap must be clearly visible on chart
3. Minimum gap size varies by timeframe (4H = larger gaps)
4. Forms during bullish market structure

What It Means:
• Institutions accumulated (bought) aggressively
• Created inefficiency as price jumped higher
• Market will likely return to "fill the gap"
• Acts as SUPPORT when price returns

Trading Bullish FVG:
• Wait for price to return to gap
• Enter LONG positions within the gap
• Best entry: 50% of gap (Consequent Encroachment)
• Stop loss: Just below the gap
• Target: Previous high or next resistance level


═══════════════════════════════════════════════════════════════════
BEARISH FVG (Acts as Resistance)
═══════════════════════════════════════════════════════════════════

Formation:
• Candle 1: Bullish or neutral - note its LOW
• Candle 2: Bearish impulsive move downward
• Candle 3: Bearish or neutral - note its HIGH

The Gap = Space between Candle 1 LOW and Candle 3 HIGH

Rules for Bearish FVG:
1. Candle 1 low must NOT touch Candle 3 high
2. Gap must be clearly visible on chart
3. Minimum gap size varies by timeframe
4. Forms during bearish market structure

What It Means:
• Institutions distributed (sold) aggressively
• Created inefficiency as price dropped lower
• Market will likely return to "fill the gap"
• Acts as RESISTANCE when price returns

Trading Bearish FVG:
• Wait for price to return to gap
• Enter SHORT positions within the gap
• Best entry: 50% of gap (Consequent Encroachment)
• Stop loss: Just above the gap
• Target: Previous low or next support level


═══════════════════════════════════════════════════════════════════
CONSEQUENT ENCROACHMENT - THE 50% SWEET SPOT
═══════════════════════════════════════════════════════════════════

The 50% level of any FVG is called the Consequent Encroachment (CE).
This is THE most powerful reaction point within the gap.

Why 50% Works:
• Perfect balance point of the imbalance
• Institutional algorithms target this level
• Highest probability of reversal/continuation
• Often wicks into CE and immediately reverses

How to Calculate:
1. Identify FVG boundaries (top and bottom)
2. Calculate midpoint: (Top + Bottom) / 2
3. Mark this level on your chart
4. Wait for price to approach

Example:
Bullish FVG: Top = 1.1050, Bottom = 1.1000
Consequent Encroachment = (1.1050 + 1.1000) / 2 = 1.1025

Trading the CE:
• Set alert at 50% level
• Watch for price reaction as it approaches
• Enter on confirmation (wick rejection, engulfing candle)
• Tighter stop loss possible (just below/above CE)
• Higher win rate than entering at gap edges


═══════════════════════════════════════════════════════════════════
TIMEFRAME SIGNIFICANCE
═══════════════════════════════════════════════════════════════════

NOT all FVGs are created equal. Timeframe matters significantly:

Daily & Weekly FVGs:
• Most powerful and most respected
• Can control price for weeks or months
• Rarely fail to get filled
• Priority #1 for long-term positioning

4-Hour FVGs:
• Very strong for swing trading
• Control price for days to weeks
• High probability of being filled
• Excellent for multi-day holds

1-Hour FVGs:
• Good for day trading
• Last for hours to days
• Must align with higher timeframes
• Best during killzones

15-Minute FVGs:
• Intraday scalping only
• Last for 1-4 hours typically
• Weakest FVGs
• Only trade if confirmed by higher TF

5-Minute & Lower:
• Very noisy and unreliable
• Many false FVGs
• Only for experienced scalpers
• Must have multiple confluence factors

Multi-Timeframe Analysis:
1. Start with Daily/4H FVGs
2. Use these as your "zones of interest"
3. Drop to 1H for refined entries
4. Use 15M for precise execution
5. Never trade against higher TF FVGs


═══════════════════════════════════════════════════════════════════
FVG TYPES & VARIATIONS
═══════════════════════════════════════════════════════════════════

1. Standard FVG
   • Classic 3-candle pattern
   • Most common type
   • Straightforward to identify

2. Inverted Fair Value Gap (IFVG)
   • Occurs when FVG is completely broken through
   • Polarity change: Support becomes Resistance (or vice versa)
   • Price trades through gap without filling
   • Gap now acts as OPPOSITE zone
   • Example: Bullish FVG broken down = now resistance

3. Nested FVGs
   • FVG within a larger FVG
   • Creates multiple reaction points
   • Higher probability zone
   • Trade the inner FVG first

4. Stacked FVGs
   • Multiple FVGs at same price level
   • Extremely high probability
   • Often marks major turning points
   • Don't miss these setups!

5. Rejected FVG
   • Price approaches but doesn't enter
   • Shows strength in current direction
   • Opposite bias confirmed
   • Adjust trading plan accordingly


═══════════════════════════════════════════════════════════════════
CONFLUENCE FACTORS - When FVGs Are Most Powerful
═══════════════════════════════════════════════════════════════════

FVGs work BEST when combined with other ICT concepts:

✓ FVG + Order Block
  • OB and FVG at same level = high probability
  • Enter at the overlap zone
  • Strongest setups in ICT methodology

✓ FVG + Liquidity Sweep
  • Stops taken above/below key level
  • Price returns into FVG
  • Classic manipulation then distribution

✓ FVG + Market Structure Shift (MSS)
  • Structure breaks, creating FVG
  • FVG acts as retest of broken structure
  • High probability trend reversal

✓ FVG + Daily/Weekly Bias
  • FVG in direction of higher TF trend
  • Increases probability significantly
  • Never fade higher timeframe bias

✓ FVG + Fibonacci Levels
  • FVG at 0.618, 0.705, or 0.79 retracement
  • Optimal Trade Entry (OTE) zone
  • Institutions love these levels

✓ FVG + Killzone Timing
  • London Open (2AM-5AM EST)
  • New York AM (8AM-11AM EST)
  • New York PM (1PM-4PM EST)
  • Higher volume = more respected FVGs

✓ FVG + Premium/Discount Pricing
  • Bullish FVG in discount = buy setup
  • Bearish FVG in premium = sell setup
  • Avoid FVGs in wrong pricing zone


═══════════════════════════════════════════════════════════════════
COMMON MISTAKES & HOW TO AVOID THEM
═══════════════════════════════════════════════════════════════════

❌ Mistake #1: Trading Every FVG You See
   → Solution: Only trade FVGs with 3+ confluence factors

❌ Mistake #2: Wrong Timeframe
   → Solution: Daily/4H for structure, 1H for entries

❌ Mistake #3: Ignoring Market Context
   → Solution: Check daily bias, trend, and market structure first

❌ Mistake #4: Entering at Wrong Part of Gap
   → Solution: Wait for 50% (Consequent Encroachment)

❌ Mistake #5: No Stop Loss
   → Solution: Always place stop just outside the FVG

❌ Mistake #6: Trading Against Higher Timeframe
   → Solution: Never trade against Daily/Weekly structure

❌ Mistake #7: Impatience
   → Solution: Wait for price to RETURN to FVG before entering

❌ Mistake #8: Ignoring Killzone Times
   → Solution: Best FVGs form during institutional trading hours

❌ Mistake #9: Overleveraging
   → Solution: Risk 1-2% per trade maximum

❌ Mistake #10: Not Journaling Results
   → Solution: Track every FVG trade to learn what works
''',
    
    'how_to_identify': '''
═══════════════════════════════════════════════════════════════════
STEP-BY-STEP: HOW TO IDENTIFY FVGs ON YOUR CHART
═══════════════════════════════════════════════════════════════════

Visual Checklist:
----------------
□ Look for aggressive price movement (big candle)
□ Examine the three candles involved
□ Check if there's a visible gap between wicks
□ Verify no overlap between candle 1 and candle 3

For BULLISH FVG:
1. Find a strong bullish (green/white) candle
2. Look at the candle BEFORE it (candle 1)
3. Look at the candle AFTER it (candle 3)
4. Check: Does candle 1 HIGH overlap with candle 3 LOW?
   • If NO overlap = You have a Bullish FVG! ✓
   • If overlap = Not a valid FVG ✗
5. Mark the gap on your chart
6. Calculate and mark 50% level

For BEARISH FVG:
1. Find a strong bearish (red/black) candle
2. Look at the candle BEFORE it (candle 1)
3. Look at the candle AFTER it (candle 3)
4. Check: Does candle 1 LOW overlap with candle 3 HIGH?
   • If NO overlap = You have a Bearish FVG! ✓
   • If overlap = Not a valid FVG ✗
5. Mark the gap on your chart
6. Calculate and mark 50% level

Pro Tips for Spotting FVGs:
• Use line drawing tool to mark gap boundaries
• Set different colors for bullish (blue) vs bearish (red) FVGs
• Only mark FVGs that matter (align with bias)
• Review higher timeframes first (Daily → 4H → 1H)
• Look for FVGs that haven't been filled yet
''',
    
    'trading_rules': '''
═══════════════════════════════════════════════════════════════════
PROFESSIONAL FVG TRADING RULES
═══════════════════════════════════════════════════════════════════

Entry Rules:
-----------
1. Only trade FVGs in direction of daily bias
2. Wait for price to RETURN to the FVG
3. Enter at 50% (Consequent Encroachment) for best odds
4. Use limit orders at CE level
5. Confirm with lower timeframe price action

Stop Loss Rules:
---------------
• Bullish FVG: Stop 10-20 pips below gap low
• Bearish FVG: Stop 10-20 pips above gap high
• Give room for wick hunts
• Never move stop closer (widen OK if needed)
• If stopped out, don't re-enter same FVG

Take Profit Rules:
-----------------
• First target: Previous swing high/low
• Second target: Next FVG or Order Block
• Third target: Daily/Weekly high/low
• Scale out: 50% at target 1, 25% at target 2, 25% at target 3
• Move stop to breakeven after target 1 hit

Position Sizing:
--------------
• Risk 1-2% of account per trade
• Never more than 5% total exposure
• Reduce size if win rate drops below 50%
• Increase size only after 10+ consecutive profitable trades

Time-Based Rules:
----------------
• Best results during killzones
• Avoid trading 30 min before/after major news
• Friday afternoon FVGs less reliable
• Monday morning FVGs can be traps
• Best: Tuesday-Thursday during NY session

Invalidation Rules:
------------------
• FVG is invalidated if price closes completely through it
• Once invalidated, it may become an IFVG
• Don't trade "old" FVGs (>3 days on 1H chart)
• If FVG overlaps with equal highs/lows, use caution

Risk Management:
---------------
• Max 3 FVG trades open simultaneously
• If 2 losses in a row, stop trading FVGs for the day
• Journal every trade with screenshot
• Review weekly performance
• Adjust rules based on data

Advanced Rules:
--------------
• Partial fills (price only enters 25% of gap) = weak FVG
• Full fills (price enters 75%+ of gap) = strong FVG
• Overnight holds: Only with 4H+ FVGs
• News days: Reduce position size by 50%
• High impact news: Don't trade FVGs
''',
    
    'examples': '''
═══════════════════════════════════════════════════════════════════
REAL-WORLD TRADING EXAMPLES
═══════════════════════════════════════════════════════════════════

Example 1: Perfect Bullish FVG Trade (EUR/USD, 1H Chart)
--------------------------------------------------------
Setup:
• Daily bias: Bullish
• Price in discount of daily range
• 1H Bullish FVG formed at 1.0850-1.0870

Execution:
• Entry: Limit order at 1.0860 (50% of gap)
• Stop: 1.0840 (10 pips below gap)
• Target 1: 1.0900 (previous swing high)
• Target 2: 1.0950 (daily resistance)

Result:
• Filled at 1.0860
• Price wicked to 1.0858, held
• Reached target 1 in 4 hours
• Reached target 2 next day
• Profit: +90 pips, Risk/Reward: 1:4.5


Example 2: Failed FVG (Learning Experience)
-------------------------------------------
Setup:
• Daily bias: Mixed (ranging)
• 15M Bearish FVG formed at 1.1020-1.1030
• No higher timeframe confirmation

Execution:
• Entry: 1.1025 (50% of gap)
• Stop: 1.1035 (above gap)
• Target: 1.0990

Result:
• Price blew through FVG without reacting
• Stopped out at 1.1035
• Loss: -10 pips

Lesson:
• Don't trade 15M FVGs without 4H confirmation
• Ranging markets make FVGs unreliable
• Always respect daily bias


Example 3: FVG + Order Block Confluence (Gold, 4H Chart)
--------------------------------------------------------
Setup:
• Weekly bias: Bullish
• Daily pullback to discount zone
• 4H Bullish FVG at $2020-$2025
• Order Block at same level
• Liquidity sweep below $2020

Execution:
• Entry: $2022.50 (50% of FVG, middle of OB)
• Stop: $2015 (below liquidity sweep)
• Target 1: $2040 (previous high)
• Target 2: $2055 (weekly resistance)

Result:
• Perfect setup with 3 confluences
• Filled and immediate reaction
• Target 1 hit in 8 hours
• Target 2 hit in 2 days
• Profit: $32.50 per ounce, Risk/Reward: 1:4.3


Example 4: Inverted FVG (IFVG) Resistance
-----------------------------------------
Setup:
• Previous Bullish FVG at 1.2150-1.2170 (was support)
• Price broke down through it
• Now approaching from below

Execution:
• Previous FVG now acts as resistance (IFVG)
• Entry: Short at 1.2160 (middle of old FVG)
• Stop: 1.2175 (above IFVG)
• Target: 1.2100 (next support)

Result:
• Price rejected perfectly at old FVG
• Dropped to target in 6 hours
• Profit: +60 pips
• IFVG concept validated


Example 5: FVG During Killzone (NAS100, 1H Chart)
-------------------------------------------------
Setup:
• New York AM session (9:30AM EST)
• Daily bias: Bullish
• Bearish FVG formed at 15,800-15,820
• BUT: Against daily bias

Decision:
• Skip this trade
• FVG against bias = low probability
• Wait for bullish FVG instead

Result:
• FVG filled but then price reversed up
• Would have been stopped out
• Discipline saved account from loss

Lesson:
• Never trade against daily bias
• Patience prevents bad trades
''',
    
    'related_concepts': [
        'Order Blocks',
        'Liquidity Sweeps',
        'Market Structure Shift (MSS)',
        'Break of Structure (BOS)',
        'Optimal Trade Entry (OTE)',
        'Premium and Discount Pricing',
        'Killzones',
        'Breaker Blocks',
        'Mitigation Blocks',
        'Consequent Encroachment'
    ],
    
    'resources': [
        'ICT YouTube Channel - FVG Mentorship Videos',
        'The Inner Circle Trader - 2022 Mentorship (Free)',
        'Trading View - Use rectangle tool to mark FVGs',
        'ICT Discord Communities - Share FVG setups',
        'Practice on Demo Account - Mark 100+ FVGs before trading live'
    ]
}
