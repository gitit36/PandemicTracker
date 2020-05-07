# Driver and aggregator for the four web scrapers

from datetime import date
import requests
import pandas as pd

import StatsScraper, TravelScraper, GuidelineScraper, HealthcareScraper

# Country name variations among the three datasets, manually checked - will be used to harmonise them later
missingHC = ["Czech Republic", "United States", "St. Kitts and Nevis", "Slovak Republic", "Korea", "The Bahamas", "Kyrgyz Republic", "Syrian Arab Republic", "St. Vincent and the Grenadines", "Lao PDR", "São Tomé and Principe", "Côte d'Ivoire", "Congo", "The Gambia", "St. Lucia", "Dem. Rep. Congo"]
missingTravel = ["Taiwan", "UAE", "Democratic Republic of the Congo", "The Gambia", "Czech Republic", "South Korea", "United States"]
JHHC = ["Czechia", "US", "Saint Kitts and Nevis", "Slovakia", "Korea, South", "Bahamas", "Kyrgyzstan", "Syria", "Saint Vincent and the Grenadines", "Laos", "Sao Tome and Principe", "Cote d'Ivoire", "Congo (Brazzaville)", "Gambia", "Saint Lucia", "Congo (Kinshasa)"]
JHTravel = ["Taiwan*", "United Arab Emirates", "Congo (Kinshasa)", "Gambia", "Czechia", "Korea, South", "US"]

# Initialising the scrapers
StatsScraper = StatsScraper.StatsScraper()
TravelScraper = TravelScraper.TravelScraper()
GuidelineScraper = GuidelineScraper.GuidelineScraper()
HealthcareScraper = HealthcareScraper.HealthcareScraper()

# Getting their results
dfStats, globalConfirmed, globalDeaths, globalRecovered = StatsScraper.scrapeCases() # Special case as it also returns global case totals
dfStats.to_csv('cases.csv', header=True)
dfTravel = TravelScraper.scrapeTravel()
dfTravel.to_csv('travel.csv', header=True)
dfHealthcare = HealthcareScraper.scrapeHealthcare()
dfHealthcare.to_csv('healthcare.csv', header=True)
dfGuidelines = GuidelineScraper.scrapeWHO() # Only one not part of the country database
dfGuidelines.to_csv('guidelines.csv', header=True)

# Replacing country name variations so we can merge smoothly - country list based on the Johns Hopkins case dataset
dfTravel = dfTravel.replace(missingTravel, JHTravel)
dfHealthcare = dfHealthcare.replace(missingHC, JHHC)

# Finally putting it all together
dfMerged1 = pd.merge(dfStats,dfHealthcare, on="countryName")
dfMerged = pd.merge(dfMerged1,dfTravel, on="countryName")

print(dfMerged.to_string)
dfMerged.to_csv('scrapedData.csv', header=True)