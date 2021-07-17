import dataclasses
from enum import Enum

from fastapi import FastAPI, File
from dataclasses import dataclass
from datetime import datetime

app = FastAPI()


@app.get("/getcitiesByCountry/{country_name}")
def get_cities_by_country(country_name: str):
    return HardCodedData.tempcities


@app.get("/getApartementsBycity/{city_name}")
def get_apartments_by_city(city_name: str):
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
class Customer(User):
    trustRating: int


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
class City:
    cityName: str
    apartmentList: list[Apartment]


@dataclass
class cities:
    cityList: list[City]
    country: Country


class HardCodedData:
    # TODO: fix this bad way to do it
    jonathan = User("Jonathan", "qwertyuiop", "sksksksksksk1234")
    jerry = User("Jerry", "qwerty", "1sfhsafabfhbahfbh8833")
    apartmentList = []
    sampleCity1 = City("UC Berk", apartmentList)
    sampleCity2 = City("Trump hotels", apartmentList)
    sampleCity3 = City("de hideup", apartmentList)
    tempCities = [sampleCity1, sampleCity2, sampleCity3]
    sampleCities = cities(tempCities, "Canada")

    negReview = Review(0, "This apartment sucks *ss I'd rather sleep in a New York dumpster", "sksksksksksk1234")
    posReview = Review(5, "This is the greatest apartment ever i'd pay my firstborn son", "1sfhsafabfhbahfbh8833")

    blueMoon = None

    start = datetime.now()
    end = datetime.now()

    timespan = Timespan(start, end)

    apartment1 = Apartment(File(default=None), 72.00, 4, "4 bedroom 2 bath", 4.5, timespan, blueMoon)
    apartmentList.append(apartment1)

    blueMoon = Host("bluemoon", "123456", "HSHDHSADASDHOAS", apartmentList)  # oh my god
