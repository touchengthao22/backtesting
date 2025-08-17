# Code Explanation: Trading Day Condition Check

This code is designed to decide whether to **BUY** or **SELL** based on
stock price trends, using the last trading day and a trading day from 5
days earlier.

------------------------------------------------------------------------

## Key Variables

-   **`group`** → A pandas DataFrame that contains stock data indexed by
    trading dates.
-   **`yesterday`** → The most recent trading day before the current day
    being checked.
-   **`prev_5`** → The trading day from 5 days earlier than `yesterday`.
-   **`is_uptrend_conditions`** → A list of boolean conditions that must
    all be true to confirm an uptrend.
-   **`is_downtrend_conditions`** → A list of boolean conditions that
    must all be true to confirm a downtrend.
-   **`count`** → A counter to track how many times a trade signal (BUY
    or SELL) is triggered.

------------------------------------------------------------------------

## Code Logic Breakdown - WORK IN PROGRESS!

``` python
if yesterday in group.index and prev_5 in group.index:
    if group.loc[yesterday, "close_spy"] > group.loc[prev_5, "close_spy"]:
        if all(is_uptrend_conditions):
            count += 1
            print(f"{group.index[i]}, low: {low}, close: {close} - BUY")

    elif group.loc[yesterday, "close_spy"] < group.loc[prev_5, "close_spy"]:
        if all(is_downtrend_conditions):
            count += 1
            print(f"{group.index[i]}, low: {low}, close: {close} - SELL")
```

### Step 1: Check if both `yesterday` and `prev_5` exist in the DataFrame index

This ensures you are comparing **valid trading days**, not weekends or
holidays when markets are closed.

### Step 2: Compare prices

-   If **yesterday's closing price \> closing price from 5 days ago**,
    it suggests an **uptrend** → check conditions, then issue a **BUY**
    signal.
-   If **yesterday's closing price \< closing price from 5 days ago**,
    it suggests a **downtrend** → check conditions, then issue a
    **SELL** signal.

------------------------------------------------------------------------

## Handling Missing Data

``` python
else:
    if all(is_uptrend_conditions):
        count += 1
        print(f"{group.index[i]}, low: {low}, close: {close} - BUY")
    
    if all(is_downtrend_conditions):
        count += 1
        print(f"{group.index[i]}, low: {low}, close: {close} - SELL")
```

If either `yesterday` or `prev_5` is **missing** (e.g., due to weekends,
holidays, or not enough history): - The decision falls back to trend
conditions (`is_uptrend_conditions` or `is_downtrend_conditions`)
**without comparing prices**.

------------------------------------------------------------------------

## Summary

✅ If both yesterday and prev_5 are trading days → compare prices and
confirm uptrend/downtrend.\
✅ If data is missing → rely only on uptrend/downtrend conditions.\
✅ Only SELL if conditions confirm a downtrend.