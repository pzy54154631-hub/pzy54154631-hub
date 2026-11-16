# When is a forecast label available?

A time-series training row can start before the training cutoff and still use a future observation for its target. This small Python audit shows how to detect that problem when a series has gaps. The example uses two fictional price series, ALPHA and BRAVO, over eight synthetic sessions.

## Worked example

The forecast target is the return to the second subsequent **observed** price in the same series. The last training session is April 8, 2030. A calendar-based rule keeps starts through April 4, leaving two market sessions before the cutoff. ALPHA has a price every session. BRAVO has no observations on April 4, 5 or 8.

| BRAVO observation | Second subsequent observed price | Available by April 8? |
| --- | --- | --- |
| April 1 | April 3 | Yes |
| April 2 | April 9 | No |
| April 3 | April 10 | No |

The calendar rule admits **7** labeled rows. **2** need prices recorded after the cutoff. Checking the actual endpoint of each label leaves **5** training rows. A label ending on the cutoff is available at the close of that session.

## Reproduce

From this directory, with Python 3.10 or newer:

```sh
python audit.py
python -m unittest -v test_audit
```

To explore a different split, run `python audit.py --cutoff 2030-04-05 --horizon 1`. To try another panel, pass `--panel path/to/panel.csv`. The first column lists every session in order; each other column contains one series of positive prices. A blank cell marks a missing observation. Rows without a future endpoint have no label.

`audit.py` builds each label, compares its start and endpoint with the fold boundary, and lists the rows admitted too early. `test_audit.py` covers missing sessions, complete data, an endpoint exactly on the cutoff, and histories too short to form a label.

This is an independent synthetic demonstration of a validation method. All identifiers, dates and prices are fictional. The counts describe only the included example. No competition data, predictions or official results are used here.
