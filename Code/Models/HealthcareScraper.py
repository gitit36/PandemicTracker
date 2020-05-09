# Gets number of hospital beds and physicians per 1000 people from IndexMundi

from bs4 import BeautifulSoup as bs
from datetime import date
import requests
import pandas as pd


class HealthcareScraper:

	def getListEnd(
		self, soupSth
	):  # IndexMundi is nicely formatted, meaning the country list ends when the actual list does

		for i in range(1, 200):
			try:
				test = soupSth.find_all("tr")[i].find_all("td")[2].text
			except:
				listEnd = i
				break

		return listEnd

	def scrapeBeds(self):

		countries = []
		beds = []
		try: # If there is no internet access/requests fails for some reason, we just terminate
			requestsBeds = requests.get(
				"https://www.indexmundi.com/facts/indicators/SH.MED.BEDS.ZS/rankings"
			)
		except:
			return None
		if requestsBeds.status_code != 200:
			return None

		soupBeds = bs(requestsBeds.text, "html.parser")

		listEnd = self.getListEnd(soupBeds)

		for i in range(1, listEnd):

			try: # Sanity checking to make sure we're dealing with the right format (based on test case)
				countryName = soupBeds.find_all("tr")[i].find_all("td")[1].text
			except:
				return None
			countries.append(countryName)

			numBeds = float(soupBeds.find_all("tr")[i].find_all("td")[2].text)
			beds.append(numBeds)

			print(countryName, numBeds)

		dataBeds = {"countryName": countries, "numHospitalBeds": beds}
		dfBeds = pd.DataFrame(dataBeds, columns=["countryName", "numHospitalBeds"])

		return dfBeds

	def scrapeDocs(self):

		countries = []
		docs = []

		try: # If there is no internet access/requests fails for some reason, we just terminate
			requestsDocs = requests.get(
				"https://www.indexmundi.com/facts/indicators/SH.MED.PHYS.ZS/rankings"
			)
		except:
			return None
		if requestsDocs.status_code != 200:
			return None

		soupDocs = bs(requestsDocs.text, "html.parser")

		listEnd = self.getListEnd(soupDocs)

		for i in range(1, listEnd):

			try: # Sanity checking to make sure we're dealing with the right format (based on test case)
				countryName = soupDocs.find_all("tr")[i].find_all("td")[1].text
			except:
				return None
			countries.append(countryName)

			numDocs = float(soupDocs.find_all("tr")[i].find_all("td")[2].text)
			docs.append(numDocs)

			print(countryName, numDocs)

		dataDocs = {"countryName": countries, "numDoctors": docs}
		dfDocs = pd.DataFrame(dataDocs, columns=["countryName", "numDoctors"])

		return dfDocs

	def scrapeHealthcare(self):  # Calls the scrapers and merges the two dataframes

		# Country name variations between this dataset and the main database, manually checked - will be used to harmonise them
		missingHC = [
			"Czech Republic",
			"United States",
			"St. Kitts and Nevis",
			"Slovak Republic",
			"Korea",
			"The Bahamas",
			"Kyrgyz Republic",
			"Syrian Arab Republic",
			"St. Vincent and the Grenadines",
			"Lao PDR",
			"São Tomé and Principe",
			"Côte d'Ivoire",
			"Congo",
			"The Gambia",
			"St. Lucia",
			"Dem. Rep. Congo",
		]
		JHHC = [
			"Czechia",
			"US",
			"Saint Kitts and Nevis",
			"Slovakia",
			"Korea, South",
			"Bahamas",
			"Kyrgyzstan",
			"Syria",
			"Saint Vincent and the Grenadines",
			"Laos",
			"Sao Tome and Principe",
			"Cote d'Ivoire",
			"Congo (Brazzaville)",
			"Gambia",
			"Saint Lucia",
			"Congo (Kinshasa)",
		]

		dfBeds = self.scrapeBeds()
		dfDocs = self.scrapeDocs()

		print(dfBeds)
		print(dfDocs)

		dfHealthcare = pd.merge(dfDocs, dfBeds, on="countryName")
		dfHealthcare = dfHealthcare.replace(missingHC, JHHC)

		return dfHealthcare