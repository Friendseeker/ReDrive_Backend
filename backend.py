import dataclasses
from enum import Enum

from fastapi import FastAPI, File
from dataclasses import dataclass
from datetime import datetime

app = FastAPI()


@app.get("/getcitiesByCountry/{country_name}")
def get_cities_by_country(country_name: str):
    return HardCodedData.get_cities(country_name=country_name)


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
    US = "US"
    CA = "CA"
    CN = "CN"
    FR = "FR"
    JP = "JP"
    IT = "IT"


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


#   desc: str
#   image: File


@dataclass
class Cities:
    cityList: list[City]
    country: Country


class HardCodedData:
    # TODO: fix this bad way to do it
    jonathan = User("Jonathan", "qwertyuiop", "sksksksksksk1234")
    jerry = User("Jerry", "qwerty", "1sfhsafabfhbahfbh8833")
    apartmentList = []
    sampleCity1 = City("UC Berk", apartmentList)
    sampleCity2 = City("New York", apartmentList)
    sampleCity3 = City("France", apartmentList)
    tempCitiesCanada = [sampleCity1, sampleCity2, sampleCity3]
    canadaCities = Cities(tempCitiesCanada, Country.CA)

    no = City("New Orleans, Louisiana", apartmentList)
    sf = City("San Francisco, California", apartmentList)
    nyc = City("New York City, New York", apartmentList)
    chi = City("Chicago, Illinois", apartmentList)
    lv = City("Las Vegas, Nevada", apartmentList)
    la = City("Los Angeles, California", apartmentList)
    tempCitiesUS = [no, sf, nyc, chi, lv, la]
    usCities = Cities(tempCitiesUS, Country.US)

    ro = City("Romes", apartmentList)
    ve = City("Venice", apartmentList)
    flo = City("Florence", apartmentList)
    mi = City("Milan", apartmentList)
    na = City("Naples", apartmentList)
    am = City("Amalfi", apartmentList)
    tempCitiesItaly = [ro, ve, flo, mi, na, am]
    italyCities = Cities(tempCitiesItaly, Country.IT)

    paris = City("Paris", [])
    nice = City("Nice", [])
    bordeaux = City("Bordeaux", [])
    lyon = City("Lyon", [])
    cannes = City("Cannes", [])
    corsica = City("Corsica", [])
    tempCitiesFrance = [paris, nice, bordeaux, lyon, cannes, corsica]
    franceCities = Cities(tempCitiesFrance, Country.FR)

    tokyo = City("Tokyo", [])
    kyoto = City("Kyoto", [])
    osaka = City("Osaka", [])
    hiroshima = City("Hiroshima", [])
    sapporo = City("Sapporo", [])
    fukuoka = City("Fukuoka", [])
    tempCitiesJapan = [tokyo, kyoto, osaka, hiroshima, sapporo, fukuoka]
    japanCities = Cities(tempCitiesJapan, Country.JP)

    beijing = City("Beijing", [])
    shanghai = City("Shanghai", [])
    chengdu = City("Chengdu", [])
    xian = City("Xi'an", [])
    hangzhou = City("Hanzhou", [])
    tempCitiesChina = [beijing, shanghai, chengdu, xian, hangzhou]
    chinaCities = Cities(tempCitiesChina, Country.CN)

    negReview = Review(0, "This apartment sucks *ss I'd rather sleep in a New York dumpster", "sksksksksksk1234")
    posReview = Review(5, "This is the greatest apartment ever i'd pay my firstborn son", "1sfhsafabfhbahfbh8833")

    blueMoon = None

    start = datetime.now()
    end = datetime.now()

    timespan = Timespan(start, end)

    apartment1 = Apartment(File(default=None), 72.00, 4, "4 bedroom 2 bath", 4.5, timespan, blueMoon)
    apartmentList.append(apartment1)

    blueMoon = Host("bluemoon", "123456", "HSHDHSADASDHOAS", apartmentList)  # oh my god
    customer1 = Customer("BobtheBuilder", "sksksksksk", "SLKJFLSD1234", -10)

    @classmethod
    def get_cities(cls, country_name: str) -> Cities:
        if country_name == "US":
            return cls.usCities
        if country_name == "IT":
            return cls.italyCities
        if country_name == "JP":
            return cls.japanCities
        if country_name == "FR":
            return cls.franceCities
        if country_name == "CN":
            return cls.chinaCities
        return None
