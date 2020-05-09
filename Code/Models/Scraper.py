# Driver and aggregator for the four web scrapers

from datetime import date
import requests
import pandas as pd

import StatsScraper, TravelScraper, GuidelineScraper, HealthcareScraper

# Initialising the scrapers
StatsScraper = StatsScraper.StatsScraper()
TravelScraper = TravelScraper.TravelScraper()
GuidelineScraper = GuidelineScraper.GuidelineScraper()
HealthcareScraper = HealthcareScraper.HealthcareScraper()

# Getting their results
dfStats, globalConfirmed, globalDeaths, globalRecovered = StatsScraper.scrapeCases() # Special case as it also returns global case totals
#dfStats.to_csv('cases.csv', header=True)
dfTravel = TravelScraper.scrapeTravel()
#dfTravel.to_csv('travel.csv', header=True)
dfHealthcare = HealthcareScraper.scrapeHealthcare()
#dfHealthcare.to_csv('healthcare.csv', header=True)
dfGuidelines = GuidelineScraper.scrapeWHO() # Only one not part of the country database
#dfGuidelines.to_csv('guidelines.csv', header=True)