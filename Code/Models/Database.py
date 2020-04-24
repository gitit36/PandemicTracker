import pymysql.cursors


class Database:
    def __init__(self):
        # Configure MySQL
        self.conn = pymysql.connect(
            host="localhost",
            port=8889,
            user="root",
            password="root",
            db="PandemicTracker",
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
        )

    def searchCountry(self, country):
        print(country)
        cursor = self.conn.cursor()
        query = "SELECT * FROM Country WHERE countryName = %s"
        cursor.execute(query, country)
        data = cursor.fetchall()
        cursor.close()
        return data

    def updateCountryHealthcare(self, country, numCases, numDeaths, numRecovered, numTests, numHospitalBeds):
        cursor = self.conn.cursor()
        query = "UPDATE Country SET numCases = %d, numDeaths = %d, numRecovered = %d, numTests = %d, numTests = %s, numHospitalBeds = %d WHERE countryName = %s)
        cursor.execute(query, (numCases, numDeaths, numRecovered, numTests, numHospitalBeds, country))
        conn.commit()
        cursor.close()

    def updateCountryTravelRestrictions(self, country, latestTravelRestriction):
        cursor = self.conn.cursor()
        query = "UPDATE Country SET latestTravelRestriction = %s WHERE countryName = %s)
        cursor.execute(query, (latestTravelRestriction, country))
        conn.commit()
        cursor.close()

    def updateCountryHospitalBeds(self, country):
        pass

    def updateWHO(self):
        pass

    def updateCDC(self):
        pass

    def updateWorldStats(self):
        pass

