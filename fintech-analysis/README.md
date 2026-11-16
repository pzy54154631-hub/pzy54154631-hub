# How much liquidity does the portfolio need?

Two recorded cases from Corridor Wealth, a financial advisory prototype for the Shenzhen FinTechathon International AI Track, use the same CNY 10,000 principal. One case adds a requirement to make CNY 5,000 available by day three. The inputs, allocations and projected proceeds are synthetic.

| Scenario | Simulated allocation | Projected net proceeds above principal | Proceeds / principal |
| --- | --- | ---: | ---: |
| Default | CNY 5,000 each in P_A and P_C | CNY 350 | 3.5% |
| Day-three liquidity requirement | CNY 5,000 each in P_A and P_D | CNY 300 | 3.0% |

Meeting the liquidity requirement replaces P_C with P_D. In this pair of cases, earlier access to cash costs CNY 50 in projected proceeds, or 0.5 percentage points of the original principal.

The policy also illustrates a reporting pitfall. It defines five customer risk labels, but only two distinct sets of target weights. C1 puts its entire target in risk sleeve R1. C2 through C5 each split their targets equally between R1 and R2. Counting labels alone would overstate the number of allocation strategies in this dataset.

## Reproduce the comparison

Run `python analyze.py` from this folder with Python 3. It reads the three JSON files alongside it, checks the recorded assertions, groups policy weights with SQLite and calculates projected proceeds as a percentage of principal. The comparison uses model projections from two fixed scenarios.

## Original competition materials

The JSON files are byte-for-byte copies of the public [allocation policy](https://github.com/pzy54154631-hub/Shenzhen-Fintech-international-Project/blob/1f3cb3684ad490985d2826cba403b62a1e0e15fb/data/wealth/allocation-policy-v1.json), [default case](https://github.com/pzy54154631-hub/Shenzhen-Fintech-international-Project/blob/1f3cb3684ad490985d2826cba403b62a1e0e15fb/evidence/final-f5/main/gpt-6.1-sol/live-recorded/gpt-6.1-sol/W04/scripted/default_hand_calculation/assertions.json) and [liquidity case](https://github.com/pzy54154631-hub/Shenzhen-Fintech-international-Project/blob/1f3cb3684ad490985d2826cba403b62a1e0e15fb/evidence/final-f5/main/gpt-6.1-sol/live-recorded/gpt-6.1-sol/W05/scripted/liquidity_first/assertions.json). The [worked examples](https://github.com/pzy54154631-hub/Shenzhen-Fintech-international-Project/blob/1f3cb3684ad490985d2826cba403b62a1e0e15fb/docs/wealth-contracts.md#L226-L245) describe the scenario assumptions.
