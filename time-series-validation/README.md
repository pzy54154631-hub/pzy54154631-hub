# When is a forecast label available?

A time-series training row can start before the training cutoff and still use a future observation for its target. This small Python audit shows how to detect that problem when a series has gaps. The example uses two fictional price series, ALPHA and BRAVO, over eight synthetic sessions.

## Worked example

The last training session is April 8, 2030. The horizon is two. ALPHA has a price every session. BRAVO has no price on April 4, 5 or 8. The audit compares two target definitions on the same panel.

| BRAVO start | Second subsequent observation | Second subsequent session on the shared calendar |
| --- | --- | --- |
| April 1 | April 3, usable | April 3, usable |
| April 2 | April 9, beyond cutoff | April 4, price missing |
| April 3 | April 10, beyond cutoff | April 5, price missing |

**Observed-price horizon.** Count two later prices for each series, skipping gaps. A rule that simply trims two sessions off the training calendar admits **7** labeled rows. Checking the dates when those prices occurred reveals that **2** labels cross the cutoff, leaving **5** eligible for training.

**Fixed-session horizon.** Count two sessions on the shared calendar, including sessions when the series has no quote. Compute the return only when the start and scheduled endpoint both have prices. Of the **7** observed starts with a scheduled endpoint by the cutoff, **2** yield a null target and **5** have a usable return. Missing intermediate prices are allowed when both endpoint prices exist. The code never substitutes a later quote for a missing endpoint price.

Both definitions yield five training rows at this cutoff and horizon. On the same panel, set the cutoff to April 9 and the horizon to four. Starting on April 3, BRAVO has a quoted price of 51 and a price of 54 on its fourth scheduled session, April 9. Its fixed-session return is **5.88%**. There are only two later observed quotes in the entire fixture, so a four-observation return cannot be formed. The cutoff is inclusive of the close of the named session.

## Reproduce

From this directory, with Python 3.10 or newer:

```sh
python audit.py
python -m unittest -v test_audit
```

To explore a different split, run `python audit.py --cutoff 2030-04-05 --horizon 1`. To try another panel, pass `--panel path/to/panel.csv`. The first column lists every session in order; each other column contains one series of positive prices. A blank cell marks a missing observation. Rows without a future endpoint have no label.

`audit.py` prints both audits, including the actual dates for crossing observed-price labels and the scheduled dates for missing fixed-session targets. `test_audit.py` also checks gaps between valid endpoints, an endpoint exactly on the cutoff, a horizon longer than the training history, and invariance of fixed-session training targets when all post-cutoff quotes are removed.

This is an independent synthetic demonstration of a validation method. All identifiers, dates and prices are fictional. The counts describe only the included example. No competition data, predictions or official results are used here.
