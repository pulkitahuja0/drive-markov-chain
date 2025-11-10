# NFL Drive Markov Chain

Uses play by play data from the NFL to model how field positions change. Modelling/computation is done in ``modelling`` with Python and the frontend is in ``frontend`` using SvelteKit.

## Modelling

Only drives that end in a **punt**, **turnover**, **touchdown**, **successful or unsuccessful field goal attempt**, or **safety** are counted. Drives that end otherwise might end for example without getting to one of those end states before the half ends, which muddies the data and makes it harder to analyze properly, so they are not included.

Every state outside of those end states is stored as a combination of the down, the yards to first down (or to endzone if in a goaline situation), and the yards to the endzone. Scraping the play by play data, we can store how a drive may transition from one state to another. 

`scrape_pbp.py` will scrape the play-by-play data for each season from 2015 to the most recent **fully complete** NFL season.

`merge_years.py` merges the seasons together and normalizes it to relative frequencies.

`compute_end_states.py` creates a table of end states of a drive for each seen field position - ie will a drive currently at 2nd and 6 65 yards from the end zone end up scoring?

## Frontend

This is a basic one page static frontend made with SvelteKit. It fetches the JSON data and uses it to display next play and end of drive states from a user-inputed state.

For a state that is not present in the data, it will find and use a state present in the data with the same down, and closest geometrically in terms of yards to first down and yards to the end zone.