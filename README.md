# What Drives Sales and Profit in a Retail Business?
A quantitative analysis of the Sample Superstore dataset.

## Question
Which parts of a retail business make money, how do sales trend over time,
and does discounting help or hurt profit?

## Data
Sample Superstore dataset (~10,000 order lines). Numeric variables:
Sales, Profit, Quantity, Discount, Order Date. Groups: Region, Category, Segment.

## Method
Pure quantitative analysis in Python (pandas, matplotlib): totals, averages,
growth rates, a correlation coefficient, and profit-margin ratios. No machine learning.

## Findings

**Q1 — Sales over time (trend):**
Sales grew 51.4% from 2015 ($484K) to 2018 ($733K). Growth was uneven —
flat/slightly down in 2016, then accelerating in 2017–2018 — with recurring
seasonal peaks toward year-end.

**Q2 — Discount vs profit (correlation):**
Average profit falls as discount rises. Small discounts (10%) are the most
profitable, but profit turns negative at a 30% discount and worsens sharply
beyond it. Conclusion: modest discounts help; heavy discounts destroy profit.

**Q3 — Region & category (comparison):**
West is the strongest region (14.9% margin); Central is weakest (7.9%).
Furniture sells the second-most but earns only a 2.5% margin — high sales,
almost no profit — versus ~17% for Technology and Office Supplies.

## Key insight
High sales do not equal high profit. Margin, not revenue, reveals what
actually makes money — and heavy discounting is a hidden profit killer.

## Files
- `get_data.py` — downloads the dataset
- `explore.py` — headline totals and margins
- `trend.py` — sales over time (Q1)
- `correlation.py` — discount vs profit (Q2)
- `compare.py` — region & category performance (Q3)
- Charts: sales_trend.png, discount_vs_profit.png, profit_by_region.png, profit_by_category.png