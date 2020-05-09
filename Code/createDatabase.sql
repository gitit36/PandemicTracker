CREATE TABLE Country(
    countryName VARCHAR(50), 
    numCases int, 
    numDeaths int,
    numRecovered int,
    numDoctors int,
    numHospitalBeds int,
    latestTravelRestriction VARCHAR(1000),
    PRIMARY KEY (countryName)
);
