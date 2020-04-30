from collections import defaultdict


class Country:
    def __init__(self, countryName):
        self.countryName = countryName
        # each country will have a dictionary with the healthcare, stats, and latest  travel updates

        # stats dict
        self.stats = defaultdict(int)
        self.stats["totalCases"] = 0
        self.stats["totalRecovered"] = 0

        # healthcare
        self.totalBeds = 0

        # travel updates
        self.travelUpdates = list()

    def displayHealthcare(self):
        print(self.countryName + "\n")
        print("The country has ", self.totalBeds, " beds.\n")

    def displayStats(self):
        print(self.countryName + "\n")
        for key, value in self.stats:
            print(key, ": ", value)

    def displayTravel(self):
        print(self.countryName + "\n")
        print(self.travelUpdates)

    def displayInfo(self):
        self.displayHealthcare()
        self.displayStats()
        self.displayTravel()

