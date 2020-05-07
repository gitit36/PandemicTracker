# Gets latest news from the WHO

from bs4 import BeautifulSoup as bs
from datetime import date
import requests
import pandas as pd

class GuidelineScraper:
	lastScraped = date(2020, 4, 24)

	def checkVersion(self): # Checks for last scraping time--scraping is only done if the current version is outdated
		if self.lastScraped != date.today():
			return True
		else:
			return False

	def getListStart(self, soupWHO): # Finds the start of the article list within the page
		for i in range(0,20):
			if soupWHO.find_all(class_="sf-content-block")[i].contents[1].h2 is not None:
				listStart = i+1
				break

		return listStart

	def scrapeWHO(self):
		article = ""
		titles = []
		dates = []
		contents = []
		articleCounter = 0 # How many articles have been parsed/do we want

		requestsWHO = requests.get("https://www.who.int/emergencies/diseases/novel-coronavirus-2019/events-as-they-happen")
		if (requestsWHO.status_code != 200):
			return "Error: could not access WHO website."

		soupWHO = bs(requestsWHO.text,"html.parser")

		listStart = self.getListStart(soupWHO)

		for i in range(listStart, listStart+10): # Some extra leeway so that we get our five articles for sure
			if(articleCounter < 5):
				for j in range(0, len(soupWHO.find_all(class_="sf-content-block")[i].contents[1].find_all("p"))):
					if("\xa0" == str(soupWHO.find_all(class_="sf-content-block")[i].contents[1].find_all("p")[j])): # Filtering out garbage and unnecessary content
						continue
					elif("twitter" in str(soupWHO.find_all(class_="sf-content-block")[i].contents[1].find_all("p")[j]) or "<a href" in str(soupWHO.find_all(class_="sf-content-block")[i].contents[1].find_all("p")[j]) or "strong" in str(soupWHO.find_all(class_="sf-content-block")[i].contents[1].find_all("p")[j])):
						continue
					else:
						article += " "+str(soupWHO.find_all(class_="sf-content-block")[i].contents[1].find_all("p")[j].text)
						
				# Separating date from content
				artDate = article[0:article.find("2020")+4]
				article = article[article.find(artDate)+len(artDate)+1:]

				try: # If there is no title, we're not in an article block--reset and skip over it
					title = soupWHO.find_all(class_="sf-content-block")[i].contents[1].h2.text
				except:
					article = ""
					continue

				# Title always has an h2 tag; the article content has already been constructed
				titles.append(title)
				dates.append(artDate)
				contents.append(article)

				print(title + "\n" + artDate + "\n" + article + "\n")
				
				article = ""
				articleCounter += 1
			else:
				break
			
		dataWHO = {'title': titles, 'date': dates, 'content': contents}
		dfWHO = pd.DataFrame(dataWHO, columns=['title', 'date', 'content'])

		print(dfWHO.to_string)

		self.lastScraped = date.today() # Update dataset version

		return dfWHO