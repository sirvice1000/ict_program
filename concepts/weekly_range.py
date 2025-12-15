"""
Weekly Range - ICT Concept
"""

CONCEPT_DATA = {
    'title': 'Weekly Range',
    'short_name': 'WEEKLY_RANGE',
    'summary': 'The high and low established during the trading week. Used to determine if price is in premium (expensive) or discount (cheap) areas.',
    'key_points': [
        'Formed from Sunday open to Friday close',
        'Divide range into thirds: discount (lower), equilibrium (middle), premium (upper)',
        '50% of weekly range is key equilibrium level',
        'Price typically seeks to fill imbalances within the range',
        'Weekly high/low often act as magnets for price',
        'Monday often sets up the week\'s direction'
    ],
    'definition': """
**Weekly Range Structure:**

**Components:**
• Weekly High (WH): Highest point reached during the week
• Weekly Low (WL): Lowest point reached during the week
• Weekly 50%: Midpoint - key equilibrium level
• Premium Zone: Upper third of range (expensive area)
• Discount Zone: Lower third of range (cheap area)

**Using Weekly Range for Trading:**

1. **Determine Position:**
   • Calculate: (Weekly High - Weekly Low) = Range
   • If price > 50%: We're in premium
   • If price < 50%: We're in discount

2. **Trading Strategy:**
   • **In Discount (lower 1/3):**
     - Look for longs
     - Price is "cheap" - institutions accumulate
     - Target: Weekly 50% or premium zone
   
   • **At Equilibrium (middle 1/3):**
     - Wait for clearer direction
     - Can be choppy - use caution
     - Look for deviation from 50%
   
   • **In Premium (upper 1/3):**
     - Look for shorts
     - Price is "expensive" - institutions distribute
     - Target: Weekly 50% or discount zone

3. **Weekly Range Rules:**
   • Don't buy in premium (expensive)
   • Don't sell in discount (cheap)
   • Best setups occur at extremes of range
   • Weekly high/low often get swept before reversal

**Example Calculation:**
Weekly High: 2000
Weekly Low: 1900
Range: 100 points

• Premium: 1967 - 2000 (upper third)
• Equilibrium: 1933 - 1967 (middle third)  
• Discount: 1900 - 1933 (lower third)
• 50% Level: 1950
""",
    'category': 'ICT Concepts'
}
