# AI Log

Tool used: Claude (Anthropic), via the Claude desktop app.

| Date | What we asked AI for | What we did with it | How we checked it |
|---|---|---|---|
| 30 Sep | Brainstorm ideas from the brief; build a throwaway prototype with fake data | Used only for ideas. Not submitted. We rebuilt the app from scratch and changed the design (live Today page, interactive season boxes, season wheel) | Ran the prototype to see how it worked |
| 5 Oct | How to download BOM daily data; a script to explore and clean it | Used `explore_data.py` and `clean_data.py`; decided to keep unchecked (Quality N) data and start analysis at 1945 | Checked row counts, date ranges, missing values and min > max checks in the output |
| 6 Oct | Help with Git/GitHub setup and fixing a "divergent branches" sync error | Followed the steps | Checked commits appeared on GitHub |
| 6 Oct | Code for live weather (`weather.py`), season lookup and averages (`seasons.py`), and the four pages | Used with changes (e.g. our own season spellings, removed a "six vs four" statistic we didn't want) | Ran each part on its own (`python seasons.py`), checked results made sense (Mookaroo wettest, Boonaroo hottest), tested with Wi-Fi off |
| 6 Oct | Reformat our flora/fauna spreadsheet into a clean CSV | AI fixed formatting, spelling and season names only. All cultural content was found and written by us from published sources | Compared the cleaned file against our original |
| 6 Oct | Automated tests | Used, and ran them | All 20 pass; checked each test matches a real edge case |
| 6 Oct | Help deploying to Streamlit Community Cloud | Followed the steps | Opened the live link in a private window |

## What we rejected or changed
- AI was **not** used to write any cultural, language or historical content (season descriptions,
  flora/fauna information). This was sourced by us from published sources.
- ADD your own examples of things you changed, fixed or chose not to use.

## What we learned
- ADD (each team member, in your own words)