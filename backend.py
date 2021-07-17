import dataclasses
from enum import Enum

import uvicorn as uvicorn
from fastapi import FastAPI, File
from dataclasses import dataclass
from datetime import datetime

app = FastAPI()


@app.get("/getLocationsByCountry/{country_name}")
def get_locations_by_country(country_name: str):
    return HardCodedData.tempLocations


@app.get("/getApartementsByLocation/{location_name}")
def get_apartments_by_location(location_name: str):
    return HardCodedData.apartmentList


@app.get("/getApartementsBySearch/{searchbar}")
def get_apartments_by_search(searchbar: str):
    return HardCodedData.apartmentList


@app.get("/getUserByUserID/{userID}")
def get_users_by_userID(userID: str):
    return HardCodedData.jerry


@dataclass
class User:
    username: str
    password: str  # todo: add salt + hash when we have time
    userID: str


@dataclass
class Review:
    Rating: int
    review: str
    userID: str


@dataclass
class Timespan:
    startTime: datetime
    endTime: datetime


class Country(Enum):
    US = "United States"
    CA = "Canada"


# ugly workaround for circular reference
class Apartment:
    pass


@dataclass
class Host(User):
    apartments: list[Apartment]


@dataclass
class Apartment:
    image: File
    price: float
    occupancy: int
    description: str
    averageRating: float
    timespan: Timespan
    owner: Host


@dataclass
class Location:
    locationName: str
    apartmentList: list[Apartment]


@dataclass
class Locations:
    locationList: list[Location]
    country: Country


class HardCodedData:
    # TODO: fix this bad way to do it
    jonathan = User("Jonathan", "qwertyuiop", "sksksksksksk1234")
    jerry = User("Jerry", "qwerty", "1sfhsafabfhbahfbh8833")
    apartmentList = []
    sampleLocation1 = Location("UC", apartmentList)
    sampleLocation2 = Location("Trump hotels", apartmentList)
    sampleLocation3 = Location("de hideup", apartmentList)
    tempLocations = [sampleLocation1, sampleLocation2, sampleLocation3]
    sampleLocations = Locations(tempLocations, "Canada")

    negReview = Review(0, "This apartment sucks *ss I'd rather sleep in a New York dumpster", "sksksksksksk1234")
    posReview = Review(5, "This is the greatest apartment ever i'd pay my firstborn son", "1sfhsafabfhbahfbh8833")

    blueMoon = None

    start = datetime.now()
    end = datetime.now()

    timespan = Timespan(start, end)

    apartment1 = Apartment(File(default=None), 72.00, 4, "4 bedroom 2 bath", 4.5, timespan, blueMoon)
    apartmentList.append(apartment1)

    blueMoon = Host("bluemoon", "123456", "HSHDHSADASDHOAS", apartmentList)  # oh my god


## TODO: change host="0,0,0,0"
if __name__ == "__main__":
    uvicorn.run(app, port=8000)
