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

    noDescription = "Anytime of year find live music, amazing Creole and Cajun cuisine, fresh seafood, farmers," \
                    + "markets shopping, nightlife and more.  During Mardi Gras season, the city becomes the " \
                      + "world’s center. No matter the time of year, New Orleans' calendar overflows in celebration."
    sfDescription = "San Francisco is home to revelatory architecture, the first established LGBTQ+ neighborhood " \
            + "in the country, and Michelin-starred dining. When in San Francisco dress in layers because the weather" \
                    + " is constantly changing, and the fog often rolls in with little warning. Spend an afternoon" \
                    + " lounging in a public park, taking advantage of San Francisco's seemingly endless green space." \
                    + " Take the BART—i.e., the Metro—to dinner in the Mission. Hike along the Pacific Ocean, or at" \
                    + " least stroll on Ocean Beach at sunset."
    nycDescription = "One of the most popular tourist destinations in the world, NYC is the mecca of business in the " \
                     + "United States, and a melting pot of American culture. NYC has something for every style," \
                     + "taste and budget, and with so many hidden gems around every corner."
    chiDescription = "Chicago has all the offerings you'd expect from a major city: world-class museums, vibrant " \
                    + "shopping districts and ample nightlife venues, just to name a few. If you're here to learn," \
                    +  " plan to spend a fair amount of time in Grant Park. This area is home to such notable " \
                    + "institutions as the Art Institute of Chicago and The Field Museum. For a more Windy " \
                    + "City-centric education, start your vacation with an architecture river cruise – which can" \
                    + " provide background on Chicago's famous skyscrapers like the Willis Tower and Tribune Tower."
    lvDescription = "Las Vegas is a city that was made for entertainment, carved out of the Mojave Desert with escape" \
                    + "in mind. Millions of people visit Las Vegas annually to relax, dine, shop, " \
                    + "see performers, and experience the nightlife."
    laDescription = "L.A. is the entertainment capital of the world, a cultural mecca boasting more than 100 museums," \
                    + " many of them world-class, and a paradise of idyllic weather. It is the only city in North " \
                    + "America to have hosted the Summer Olympics twice - and by 2028 the third time. " \
                    + "Downtown L.A. is the largest government center outside of Washington, D.C. Additionally, " \
                    + "Los Angeles has the only remaining wooden lighthouse in the state (located in San " \
                    + "Pedro’s Fermin Park) and the largest historical theater district on the National" \
                    " Register of Historic Places (located Downtown on Broadway)."

    no = City("New Orleans, Louisiana", apartmentList, noDescription, parse_url("https://tinyurl.com/9hz9neyn").url)
    sf = City("San Francisco, California", apartmentList, sfDescription, parse_url("https://tinyurl.com/4uh8b8z4").url)
    nyc = City("New York City, New York", apartmentList, nycDescription, parse_url("https://tinyurl.com/2ekk6ud3").url)
    chi = City("Chicago, Illinois", apartmentList, chiDescription, parse_url("https://tinyurl.com/54fchxsc").url)
    lv = City("Las Vegas, Nevada", apartmentList, lvDescription, parse_url("https://tinyurl.com/brusdza7").url)
    la = City("Los Angeles, California", apartmentList, laDescription, parse_url("https://tinyurl.com/az45dsah").url)
    tempCitiesUS = [no, sf, nyc, chi, lv, la]
    usCities = Cities(tempCitiesUS, Country.US)

    ro = City("Romes", apartmentList, "description", parse_url("https://tinyurl.com/3kunj28y").url)
    ve = City("Venice", apartmentList, "description", parse_url("https://tinyurl.com/5wavafev").url)
    flo = City("Florence", apartmentList, "description", parse_url("https://tinyurl.com/zrarspdc").url)
    mi = City("Milan", apartmentList, "description", parse_url("https://tinyurl.com/rztp6mbm").url)
    na = City("Naples", apartmentList, "description", parse_url("https://tinyurl.com/yuwurmjy").url)
    am = City("Amalfi", apartmentList, "description", parse_url("https://tinyurl.com/yfmx9vch").url)
    tempCitiesItaly = [ro, ve, flo, mi, na, am]
    italyCities = Cities(tempCitiesItaly, Country.IT)

    paris = City("Paris", [], "description", parse_url("https://tinyurl.com/rc4cd4fe").url)
    nice = City("Nice", [], "description", parse_url("https://tinyurl.com/55498jwc").url)
    bordeaux = City("Bordeaux", [], "description", parse_url("https://tinyurl.com/2sa7xzcc").url)
    lyon = City("Lyon", [], "description", parse_url("https://tinyurl.com/dv9wtxas").url)
    cannes = City("Cannes", [], "description", parse_url("https://tinyurl.com/2u6krn7v").url)
    corsica = City("Corsica", [], "description", parse_url("https://tinyurl.com/njz58nwc").url)
    tempCitiesFrance = [paris, nice, bordeaux, lyon, cannes, corsica]
    franceCities = Cities(tempCitiesFrance, Country.FR)

    tokyo = City("Tokyo", [], "description", parse_url("https://tinyurl.com/3v4e8atv").url)
    kyoto = City("Kyoto", [], "description", parse_url("https://tinyurl.com/ynynermf").url)
    osaka = City("Osaka", [], "description", parse_url("https://tinyurl.com/85t9d34z").url)
    hiroshima = City("Hiroshima", [], "description", parse_url("https://tinyurl.com/hesjnytw").url)
    sapporo = City("Sapporo", [], "description", parse_url("https://tinyurl.com/dy5jze3p").url)
    fukuoka = City("Fukuoka", [], "description", parse_url("https://tinyurl.com/263u9ntt").url)
    tempCitiesJapan = [tokyo, kyoto, osaka, hiroshima, sapporo, fukuoka]
    japanCities = Cities(tempCitiesJapan, Country.JP)

    beijing = City("Beijing", [], "description", parse_url("https://tinyurl.com/yfypw5uj").url)
    shanghai = City("Shanghai", [], "description", parse_url("https://tinyurl.com/xe7k7sem").url)
    chengdu = City("Chengdu", [], "description", parse_url("https://tinyurl.com/v6nw25f").url)
    xian = City("Xi'an", [], "description", parse_url("https://tinyurl.com/s9243y3v").url)
    hangzhou = City("Hanzhou", [], "description", parse_url("https://tinyurl.com/jeaaej4p").url)
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
