from enum import Enum

from fastapi import FastAPI, File
from dataclasses import dataclass
from datetime import datetime

from urllib3.util import url, parse_url

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
    image: url
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
    desc: str
    image: url


@dataclass
class Cities:
    cityList: list[City]
    country: Country


class HardCodedData:
    # TODO: fix this bad way to do it
    jonathan = User("Jonathan", "qwertyuiop", "sksksksksksk1234")
    jerry = User("Jerry", "qwerty", "1sfhsafabfhbahfbh8833")
    apartmentList = []
    trumpImage = parse_url(r"https://i.imgur.com/cHKbKQT.jpeg").url
    sampleCity1 = City("UC Berk", apartmentList, "desc", trumpImage)
    sampleCity2 = City("New York", apartmentList, "desc", trumpImage)
    sampleCity3 = City("Dublin", apartmentList, "desc", trumpImage)
    tempCitiesCanada = [sampleCity1, sampleCity2, sampleCity3]
    canadaCities = Cities(tempCitiesCanada, Country.CA)

    no = City("New Orleans, Louisiana", apartmentList, "description", trumpImage)
    sf = City("San Francisco, California", apartmentList, "description", trumpImage)
    nyc = City("New York City, New York", apartmentList, "description", trumpImage)
    chi = City("Chicago, Illinois", apartmentList, "description", trumpImage)
    lv = City("Las Vegas, Nevada", apartmentList, "description", trumpImage)
    la = City("Los Angeles, California", apartmentList, "description", trumpImage)
    tempCitiesUS = [no, sf, nyc, chi, lv, la]
    usCities = Cities(tempCitiesUS, Country.US)

    ro = City("Romes", apartmentList, "description", trumpImage)
    ve = City("Venice", apartmentList, "description", trumpImage)
    flo = City("Florence", apartmentList, "description", trumpImage)
    mi = City("Milan", apartmentList, "description", trumpImage)
    na = City("Naples", apartmentList, "description", trumpImage)
    am = City("Amalfi", apartmentList, "description", trumpImage)
    tempCitiesItaly = [ro, ve, flo, mi, na, am]
    italyCities = Cities(tempCitiesItaly, Country.IT)

    paris = City("Paris", [], "description", trumpImage)
    nice = City("Nice", [], "description", trumpImage)
    bordeaux = City("Bordeaux", [], "description", trumpImage)
    lyon = City("Lyon", [], "description", trumpImage)
    cannes = City("Cannes", [], "description", trumpImage)
    corsica = City("Corsica", [], "description", trumpImage)
    tempCitiesFrance = [paris, nice, bordeaux, lyon, cannes, corsica]
    franceCities = Cities(tempCitiesFrance, Country.FR)

    tokyo = City("Tokyo", [], "description", trumpImage)
    kyoto = City("Kyoto", [], "description", trumpImage)
    osaka = City("Osaka", [], "description", trumpImage)
    hiroshima = City("Hiroshima", [], "description", trumpImage)
    sapporo = City("Sapporo", [], "description", trumpImage)
    fukuoka = City("Fukuoka", [], "description", trumpImage)
    tempCitiesJapan = [tokyo, kyoto, osaka, hiroshima, sapporo, fukuoka]
    japanCities = Cities(tempCitiesJapan, Country.JP)

    beijing = City("Beijing", [], "description", trumpImage)
    shanghai = City("Shanghai", [], "description", trumpImage)
    chengdu = City("Chengdu", [], "description", trumpImage)
    xian = City("Xi'an", [], "description", trumpImage)
    hangzhou = City("Hanzhou", [], "description", trumpImage)
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
        if country_name == "CA":
            return cls.canadaCities
        return None
