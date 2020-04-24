CREATE TABLE Country(
    countryName VARCHAR(20), 
    numCases int, 
    numDeaths int,
    numRecovered int,
    numTests int,
    numHospitalBeds int,
    latestTravelRestriction VARCHAR(1000),
    PRIMARY KEY (countryName)
);


CREATE TABLE Healthcare(
    date datetime,
    latestWHO TEXT, 
    latestCDC TEXT,
    PRIMARY KEY (date)
);
