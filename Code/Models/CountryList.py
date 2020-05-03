import pycountry
from Models.Country import Country

# must only be initialized once


class CountryList:
    def __init__(self):
        self.countryList = list()

        ## append all the countries to the list
        for country in pycountry.countries:
            self.countryList.append(Country(country.name))

