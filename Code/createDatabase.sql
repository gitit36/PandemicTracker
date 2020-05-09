CREATE TABLE Country(
    countryName VARCHAR(50),
    numCases int,
    numDeaths int,
    numRecovered int,
    numDoctors float(5),
    numHospitalBeds float(5),
    latestTravelRestriction VARCHAR(2000),
    PRIMARY KEY (countryName)
);
