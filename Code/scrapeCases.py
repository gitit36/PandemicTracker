# Gets case data on a country level from Johns Hopkins

from bs4 import BeautifulSoup as bs
import requests
import pandas as pd

# Accessing the github pages
responseConfirmed = requests.get("https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")
responseDeaths = requests.get("https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv")
responseRecovered = requests.get("https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv")

soupConfirmed = bs(responseConfirmed.text,"html.parser")
soupDeaths = bs(responseDeaths.text,"html.parser")
soupRecovered = bs(responseRecovered.text,"html.parser")

# Scraping the data and creating Pandas dataframe - total cases and deaths
countries = []
confirmed = []
deaths = []

for i in range(2,266): # There are 266 rows in the dataset
    row = "LC"+str(i)
    countryConfirmed = soupConfirmed.find("tr", id=row) # Scoping onto one row
    countryDeaths = soupDeaths.find("tr", id=row)
    
    countryName = countryConfirmed.find_all("td")[2].get_text() # Getting the name
    countries.append(countryName)
    
    currentConfirmed = countryConfirmed.find_all("td")[98].get_text() # 98 is the entry for April 24--will have to make it update daily
    confirmed.append(int(currentConfirmed))
    
    currentDeaths = countryDeaths.find_all("td")[98].get_text()
    deaths.append(int(currentDeaths))

    #print(countryName, "total cases and deaths scraped.")
    
data1 = {'countryName': countries, 'numCases': confirmed, 'numDeaths': deaths}
dfConfD = pd.DataFrame(data1, columns=['countryName', 'numCases', 'numDeaths'])

# Scraping recovered data - has different size than the other two and thus has to be scraped with a different loop
countries = []
recovered = []

for i in range(2, 252):
    row = "LC"+str(i)
    countryRecovered = soupRecovered.find("tr", id=row)

    countryName = countryRecovered.find_all("td")[2].get_text()
    countries.append(countryName)

    currentRecovered = countryRecovered.find_all("td")[98].get_text()
    recovered.append(int(currentRecovered))

    #print(countryName, "recovered cases scraped.")
    
data2 = {'countryName': countries, 'numRecovered': recovered}
dfRec = pd.DataFrame(data2, columns=['countryName', 'numRecovered'])

# Some countries in the JH dataset are listed multiple times, on a state/county level - here we sum up their numbers separately
dfConf = dfConfD[['countryName', 'numCases']]
dfConf = dfConf.groupby(['countryName'], as_index=False).sum()

dfD = dfConfD[['countryName', 'numDeaths']]
dfD = dfD.groupby(['countryName'], as_index=False).sum()

dfRec = dfRec.groupby(['countryName'], as_index=False).sum()

# And finally merge the three dataframes together to get the combined, summed up database for the day
dfAll = pd.merge(dfConf, dfD, on='countryName')
dfAll = pd.merge(dfAll, dfRec, on='countryName')
print(dfAll.to_string())