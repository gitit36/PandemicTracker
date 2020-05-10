CREATE TABLE Country(
    countryName VARCHAR(50),
    numCases int,
    numDeaths int,
    numRecovered int,
    numDoctors float(20),
    numHospitalBeds float(20),
    latestTravelRestriction VARCHAR(2000),
    PRIMARY KEY (countryName)
);
