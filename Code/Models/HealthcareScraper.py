# Gets number of hospital beds and physicians per 1000 people from IndexMundi

from bs4 import BeautifulSoup as bs
from datetime import date
import requests
import pandas as pd

class HealthcareScraper:
	lastScraped = 0

	def checkVersion(self):  # Since this is general data, it only needs to be updated yearly
		if self.lastScraped != date.today().year:
			return True
		else:
			return False

	def getListEnd(self, soupSth): # IndexMundi is nicely formatted, meaning the country list ends when the actual list does

		for i in range(1,200):
			try:
				test = soupSth.find_all("tr")[i].find_all("td")[2].text
			except:
				listEnd = i
				break

		return listEnd

	def scrapeBeds(self):

		if self.checkVersion() == False:
			return "Beds database already up to date."

		countries = []
		beds = []

		requestsBeds = requests.get("https://www.indexmundi.com/facts/indicators/SH.MED.BEDS.ZS/rankings")
		if (requestsBeds.status_code != 200):
			return "Error: could not access IndexMundi dataset."

		soupBeds = bs(requestsBeds.text,"html.parser")

		listEnd = self.getListEnd(soupBeds)

		for i in range(1,listEnd):
			
			countryName = soupBeds.find_all("tr")[i].find_all("td")[1].text
			countries.append(countryName)
			
			numBeds = float(soupBeds.find_all("tr")[i].find_all("td")[2].text)
			beds.append(numBeds)
			
			print(countryName, numBeds)

		dataBeds = {'countryName': countries, 'numHospitalBeds': beds}
		dfBeds = pd.DataFrame(dataBeds, columns=['countryName', 'numHospitalBeds'])

		return dfBeds

	def scrapeDocs(self):

		if self.checkVersion() == False:
			return "Doctors database already up to date."

		countries = []
		docs = []

		requestsDocs = requests.get("https://www.indexmundi.com/facts/indicators/SH.MED.PHYS.ZS/rankings")
		if (requestsDocs.status_code != 200):
			return "Error: could not access IndexMundi dataset."

		soupDocs = bs(requestsDocs.text,"html.parser")

		listEnd = self.getListEnd(soupDocs)

		for i in range(1,listEnd):
			
			countryName = soupDocs.find_all("tr")[i].find_all("td")[1].text
			countries.append(countryName)
			
			numDocs = float(soupDocs.find_all("tr")[i].find_all("td")[2].text)
			docs.append(numDocs)
			
			print(countryName, numDocs)

		dataDocs = {'countryName': countries, 'numDoctors': docs}
		dfDocs = pd.DataFrame(dataDocs, columns=['countryName', 'numDoctors'])

		self.lastScraped = date.today().year # Update dataset version

		return dfDocs