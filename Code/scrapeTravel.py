# Gets travel restrictions from Wikipedia

from bs4 import BeautifulSoup as bs
import requests
import pandas as pd

travelWiki = requests.get("https://en.wikipedia.org/wiki/Travel_restrictions_related_to_the_2019%E2%80%9320_coronavirus_pandemic")
soupWiki = bs(travelWiki.text,"html.parser")

travelAdv = ""
countries = []
travelAdvs = []

for countryNum in range(96, 227): # Country entries are between li tags of these numbers--manually checked
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
    
    #print(travelAdv, "\n")
    travelAdv = ""
    
dataTravel = {'countryName': countries, 'travelAdv': travelAdvs}
dfTravel = pd.DataFrame(dataTravel, columns=['countryName', 'travelAdv'])
print(dfTravel.to_string())