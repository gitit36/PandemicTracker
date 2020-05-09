# Gets case data on a country level from Johns Hopkins

from bs4 import BeautifulSoup as bs
from datetime import date
import requests
import pandas as pd

class StatsScraper:
	globalConfirmed = 0  # Global case data, stored as class variables for easy access
	globalDeaths = 0
	globalRecovered = 0

	def getTodaysIndex(self):
		startDate = date(2020, 4, 24)  # Arbitrary date (the day this parser was first written!), used to calculate the list index
		today = date.today()
		todaysIndex = (today - startDate).days + 97  # This will give the index used for the most recent entry the BeautifulSoup scrapes

		return todaysIndex

	def scrapeCases(self):  # Scrapes the most recent case data

		# Accessing the github pages
		try: # If there is no internet access/requests fails for some reason, we just terminate
			responseConfirmed = requests.get("https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")
			responseDeaths = requests.get("https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv")
			responseRecovered = requests.get("https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv")
		except:
			return None

		if (responseConfirmed.status_code != 200 or responseDeaths.status_code != 200 or responseRecovered.status_code != 200):
			return None

		soupConfirmed = bs(responseConfirmed.text, "html.parser")
		soupDeaths = bs(responseDeaths.text, "html.parser")
		soupRecovered = bs(responseRecovered.text, "html.parser")

		# Getting the index to be used
		todaysIndex = self.getTodaysIndex()

		# Scraping the data and creating Pandas dataframe - total cases and deaths
		countries = []
		confirmed = []
		deaths = []

		for i in range(2, 266):  # There are 266 rows in the dataset
			row = "LC" + str(i)
			countryConfirmed = soupConfirmed.find("tr", id=row)  # Scoping onto one row
			countryDeaths = soupDeaths.find("tr", id=row)

			if countryConfirmed is None or countryDeaths is None: # If we're not finding anything in this format, we're on the wrong page - terminate (based on test case)
				return None

			countryName = countryConfirmed.find_all("td")[2].get_text()  # Getting the name
			countries.append(countryName)

			# Making it smart about updates, based on a test case failure - if there is no data for the current day, it'll try the day before
			try:
				currentConfirmed = countryConfirmed.find_all("td")[todaysIndex].get_text()
			except:
				todaysIndex -= 1
				try: # If the day before works, keep going like nothing happened with that date
					currentConfirmed = countryConfirmed.find_all("td")[todaysIndex].get_text()
				except: # Else, just return gracefully
					return None

			confirmed.append(int(currentConfirmed))
			self.globalConfirmed += int(currentConfirmed)

			currentDeaths = countryDeaths.find_all("td")[todaysIndex].get_text()
			deaths.append(int(currentDeaths))
			self.globalDeaths += int(currentDeaths)

			print(countryName, "total cases and deaths scraped.")

		data1 = {"countryName": countries, "numCases": confirmed, "numDeaths": deaths}
		dfConfD = pd.DataFrame(data1, columns=["countryName", "numCases", "numDeaths"])

		# Scraping recovered data - has different size than the other two and thus has to be scraped with a different loop
		countries = []
		recovered = []

		for i in range(2, 252):
			row = "LC" + str(i)
			countryRecovered = soupRecovered.find("tr", id=row)

			countryName = countryRecovered.find_all("td")[2].get_text()
			countries.append(countryName)

			currentRecovered = countryRecovered.find_all("td")[todaysIndex].get_text()
			recovered.append(int(currentRecovered))
			self.globalRecovered += int(currentRecovered)

			print(countryName, "recovered cases scraped.")

		data2 = {"countryName": countries, "numRecovered": recovered}
		dfRec = pd.DataFrame(data2, columns=["countryName", "numRecovered"])

		dfAll = self.mergeDataFrames(dfConfD, dfRec)
		print(dfAll.to_string())

		return dfAll, self.globalConfirmed, self.globalDeaths, self.globalRecovered

	def mergeDataFrames(self, dfConfD, dfRec):

		# Some countries in the JH dataset are listed multiple times, on a state/county level - here we sum up their numbers separately
		dfConf = dfConfD[["countryName", "numCases"]]
		dfConf = dfConf.groupby(["countryName"], as_index=False).sum()

		dfD = dfConfD[["countryName", "numDeaths"]]
		dfD = dfD.groupby(["countryName"], as_index=False).sum()

		dfRec = dfRec.groupby(["countryName"], as_index=False).sum()

		# And finally merge the three dataframes together to get the combined, summed up database for the day
		dfAll = pd.merge(dfConf, dfD, on="countryName")
		dfAll = pd.merge(dfAll, dfRec, on="countryName")

		return dfAll