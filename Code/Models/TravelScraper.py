# Gets travel restrictions from Wikipedia

from bs4 import BeautifulSoup as bs
from datetime import date
import requests
import pandas as pd

class TravelScraper:
	lastScraped = date(2020, 4, 24)

	def checkVersion(self): # Checks for last scraping time--scraping is only done if the current version is outdated
		if self.lastScraped != date.today():
			return True
		else:
			return False

	def getListBoundaries(self, soupWiki): # Finds the specific start and end of the country list within the article
		listStart = 0
		listEnd = 0

		for i in range(90,110): # Some initial angling is done to speed up the search
			if("flagicon" in str(soupWiki.find_all("li")[i].contents[0])): # Every country entry contains a flag icon
				listStart = i
				break

		for j in range(listStart,250):
			if("flagicon" not in str(soupWiki.find_all("li")[j].contents[0])):
				listEnd = j
				break

		return listStart, listEnd

	def scrapeTravel(self):

		if self.checkVersion() == False:
			return "Travel database already up to date."

		travelWiki = requests.get("https://en.wikipedia.org/w/index.php?title=Travel_restrictions_related_to_the_COVID-19_pandemic&oldid=954913741")
		soupWiki = bs(travelWiki.text,"html.parser")

		listStart, listEnd = self.getListBoundaries(soupWiki)
		print(listStart, listEnd)

		travelAdv = ""
		countries = []
		travelAdvs = []

		for countryNum in range(listStart, listEnd): # Country entries are between li tags of these numbers--manually checked
			for i in range(0,len(soupWiki.find_all("li")[countryNum].contents)): # Each entry has multiple elements
				if "<span" in str(soupWiki.find_all("li")[countryNum].contents[i]) or "<sup" in str(soupWiki.find_all("li")[countryNum].contents[i]): # If it's something beside a text (a reference or a redirect), ignore
					continue
				elif "<a" in str(soupWiki.find_all("li")[countryNum].contents[i]): # If it's a link, just get the text
					travelAdv += str(soupWiki.find_all("li")[countryNum].contents[i].text)
				else: # Else it's plain text and is good to add
					travelAdv += str(soupWiki.find_all("li")[countryNum].contents[i])

			# Split the created clean advisory into country and info
			countries.append(travelAdv.split(": ")[0])
			travelAdvs.append(travelAdv.split(": ")[1])
			
			print(travelAdv, "\n")
			travelAdv = ""
		
		# Create dataframe
		dataTravel = {'countryName': countries, 'travelAdv': travelAdvs}
		dfTravel = pd.DataFrame(dataTravel, columns=['countryName', 'travelAdv'])

		self.lastScraped = date.today() # Update dataset version

		return dfTravel

TravelScraper = TravelScraper()
print(TravelScraper.scrapeTravel().to_string())
#print(TravelScraper.scrapeTravel())