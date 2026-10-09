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
| 8 Oct | 7-day forecast, chart label fix, page styling (ui.py) and weather icons/hourly forecast | Used; first axis fix didn't work so we tried a second approach; updated tests when weather.py changed | Ran the app locally and live, all 22 tests pass |

## What we rejected or changed
- AI was **not** used to write any cultural, language or historical content (season descriptions,
  flora/fauna information). This was sourced by us from published sources.
- The first prototype AI built used made-up weather data. We only used it for ideas and rebuilt the
  app from scratch with real BOM data.
- We changed the design from the prototype: a live Today page instead of a date picker, interactive
  season boxes with popups, a season wheel, and a 7-day forecast.
- AI added a statistic comparing how well six vs four seasons fit Perth's weather. We removed it and
  kept only the season wheel, because we wanted a simpler, visual comparison.
- We removed the "plants and animals recorded per season" bar chart from the Explorer page.
- AI's first fix for the forecast chart's °C label (rotating the axis title) didn't work in our app.
  We tried a second approach (°C on each axis label) and checked it locally before pushing.
 - When we replaced weather.py with a new version (icons, hourly and 7-day forecast), two tests
  failed. We rewrote those tests to match the new code rather than keeping outdated ones.
- AI's Git instructions didn't cover every situation (divergent branches, a Word temp file and a
  deleted report causing merge conflicts), so we had to understand what Git was doing to fix them.
- We removed duplicate files and Word documents that were uploaded to the repo by mistake. 

## What we learned
Sam: I learned how to structure an app so the logic is separate from the interface, which made it much easier to test. I got much more comfortable with Git, especially pulling before pushing and fixing conflicts. Using AI sped things up a lot, but I learned I still had to run and check everything. A few suggestions didn’t work first time, and I had to understand the code to fix them. I also learned why timezones matter when an app runs on a server in another country.

Sol: I learned how to correctly prompt a question when using AI, i also gained a lot of experience using GitHub and interacting with its different features. Using AI helped with organisation of the season information and formatting a spread sheet that would be easily integrated into the app.  
