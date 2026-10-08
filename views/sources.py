import streamlit as st

st.title("Sources & About")

st.header("Acknowledgement")
st.write("The University of Western Australia (UWA) formally acknowledges the traditional custodians "
         "of the lands on which its operations and campuses stand, recognizing the Whadjuk Noongar "
         "people in Perth (Boorloo) and the Menang Noongar people in Albany (Kinjarling).")
st.caption("Acknowledgement of Country from The University of Western Australia.")

st.header("Seasonal knowledge")
st.markdown("""
- **Season descriptions:** Bureau of Meteorology, *Indigenous Weather Knowledge – Nyoongar calendar*,
  https://www.bom.gov.au/resources/indigenous-weather-knowledge/indigenous-seasonal-calendars/nyoongar-calendar
- **Flora and fauna seasonal signs:**
    - City of Stirling, *Native Plants and Habitats*,
      https://www.stirling.wa.gov.au/waste-and-environment/natural-environment-and-conservation/native-plants-and-habitats
    - Marine Waters (DPIRD), *Fact Sheet: The Noongar Six Seasons*,
      https://marinewaters.fish.wa.gov.au/resource/fact-sheet-the-noongar-six-seasons/
    - Noongar Boodjar Language Cultural Aboriginal Corporation, *Noongar Boodjar Plants and Animals*,
      https://profiles.ala.org.au/opus/noongar
- **Season names and months:** Bureau of Meteorology, *Indigenous Weather Knowledge – Nyoongar calendar* (link above).

Season names have more than one spelling (e.g. Bunuru/Boonaroo). We use one main spelling
and show the alternative in each season's details.

Indigenous Weather Knowledge belongs to the Noongar communities who shared it, the Bureau of Meteorology
and Monash University. It is used here for study purposes only, as permitted by the Bureau's copyright terms
(https://www.bom.gov.au/copyright). No restricted cultural knowledge is included.
""")

st.header("Weather data")
st.markdown("""
- **Historical weather:** Bureau of Meteorology, Climate Data Online – daily maximum temperature,
  minimum temperature and rainfall, Perth Airport (station 009021), 1944–2026.
  https://www.bom.gov.au/climate/data/ · © Commonwealth of Australia, Bureau of Meteorology.
- **Live weather and forecast:** Weather data by [Open-Meteo.com](https://open-meteo.com/),
  licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
""")

st.header("How we prepared the data")
st.markdown("""
- Merged the three BOM files by date and removed 121 days with no measurements.
- Checked for multi-day readings (none found) and days where min > max (none found).
- Analysis starts in 1945, the first full year with all three measurements.
- About 3,900 temperature values from 2016 onwards are not yet quality-checked by BOM.
  We kept them so recent years are included, and note this as a limitation.
- Incomplete seasons at the start and end of the record are left out of averages and trends.
""")

st.header("Privacy")
st.write("This app does not collect, store or ask for any personal information. "
         "It has no logins and uses no API keys.")

st.header("Team")
st.write("Sam Day + Sol Manners · CITS1501, University of Western Australia, 2026 · "
         "https://github.com/samnday-debug/six-seasons-app")