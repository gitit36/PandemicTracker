# Driver and aggregator for the four web scrapers

from datetime import date
import requests
import pandas as pd

import StatsScraper, TravelScraper, GuidelineScraper, HealthcareScraper

StatsScraper = StatsScraper.StatsScraper()
TravelScraper = TravelScraper.TravelScraper()
GuidelineScraper = GuidelineScraper.GuidelineScraper()
HealthcareScraper = HealthcareScraper.HealthcareScraper()

dfStats, globalConfirmed, globalDeaths, globalRecovered = StatsScraper.scrapeCases() # Special case as it also returns global case totals
dfTravel = TravelScraper.scrapeTravel()
dfHealthcare = HealthcareScraper.scrapeHealthcare()
dfGuidelines = GuidelineScraper.scrapeWHO() # Only one not part of the country database

dfMerged1 = pd.merge(dfStats,dfHealthcare, on="countryName")
dfMerged2 = pd.merge(dfMerged1,dfTravel, on="countryName")

print(dfMerged2.to_string)

#dfMerged2.to_csv('scrapedData.csv', header=True)