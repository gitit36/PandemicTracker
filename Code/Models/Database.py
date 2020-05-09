import pymysql.cursors
from Models.CountryList import CountryList
from Models.StatsScraper import StatsScraper
from Models.TravelScraper import TravelScraper
from Models.HealthcareScraper import HealthcareScraper


class Database:
    def __init__(self):
        # Configure MySQL
        self.conn = pymysql.connect(
            host="localhost",
            port=8889,
            user="root",
            password="root",
            db="PandemicTracker",
            charset="utf8",
            cursorclass=pymysql.cursors.DictCursor,
        )
        self.CountryList = CountryList()
        self.StatsScraper = StatsScraper()
        self.TravelScraper = TravelScraper()
        self.Healthcare = HealthcareScraper()

    def searchCountry(self, country):
        print(country)
        cursor = self.conn.cursor()
        query = "SELECT * FROM Country WHERE countryName = %s"
        cursor.execute(query, country)
        data = cursor.fetchall()
        cursor.close()
        return data

    ## displays all countries
    def viewCountry(self):
        cursor = self.conn.cursor()
        query = "SELECT countryName, numCases, numDeaths, numRecovered, numTests, numHospitalBeds, latestTravelRestriction FROM Country"
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        return data

    def addCountries(self):
        cursor = self.conn.cursor()
        query = "INSERT INTO Country (countryName, numCases, numDeaths, numRecovered, numDoctors, numHospitalBeds, latestTravelRestriction) VALUES (%s, 0, 0, 0, 0, 0, NULL)"
        for country in self.CountryList.countryList:
            cursor.execute(query, country)
            self.conn.commit()
        cursor.close()
        print("success")

    def updateCountryHealthcare(self, country, numDoctors, numHospitalBeds):
        cursor = self.conn.cursor()
        query = "UPDATE Country SET numDoctors = %d, numHospitalBeds = %d WHERE countryName = %s)"
        cursor.execute(
            query, (numDoctors, numHospitalBeds, country),
        )
        self.conn.commit()
        cursor.close()

    def updateCountryStats(self, country, numCases, numDeaths, numRecovered):
        cursor = self.conn.cursor()
        query = "UPDATE Country SET numCases = %d, numDeaths = %d, numRecovered = %d WHERE countryName = %s)"
        cursor.execute(
            query, (numCases, numDeaths, numRecovered, country),
        )
        self.conn.commit()
        cursor.close()

    def updateCountryTravelRestrictions(self, country, latestTravelRestriction):
        cursor = self.conn.cursor()
        query = (
            "UPDATE Country SET latestTravelRestriction = %s WHERE countryName = %s)"
        )
        cursor.execute(query, (latestTravelRestriction, country))
        self.conn.commit()
        cursor.close()

    def updateCountryHospitalBeds(self, country):
        health = self.Healthcare.scrapeHealthcare()
        if health:
            for index, row in health.iterrows():
                countryName = row["countryName"]
                numDoctors = row["numDoctors"]
                numHospitalBeds = row["numHospitalBeds"]
                self.updateCountryHealthcare(countryName, numDoctors, numHospitalBeds)

        pass

    def updateWHO(self):
        pass

    def updateCDC(self):
        pass

    def updateWorldStats(self):
        pass

    # <<<<<<< HEAD

    def updateAllCoutriesHealthcare(self):
        # how do we  time this?
        allCases = self.StatsScraper.scrapeCases()
        if allCases:
            df = allCases[0]
            for index, row in df.iterrows():
                countryName = row["countryName"]
                numCases = row["numCases"]
                numDeaths = row["numDeaths"]
                numRecovered = row["numRecovered"]
                self.updateCountryStats(countryName, numCases, numDeaths, numRecovered)
            print("updated all countries")

    def updateAllCountriesTravel(self):
        travel = self.TravelScraper.scrapeTravel()
        for index, row in travel.iterrows():
            countryName = row["countryName"]
            latestTravelRestriction = row["travelAdv"]
            self.updateCountryTravelRestrictions(countryName, latestTravelRestriction)


# =======
# >>>>>>> 15caf204401816919fbd989800776cdc644c5c1a
