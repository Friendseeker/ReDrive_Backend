from enum import Enum
from typing import Optional

from fastapi import FastAPI, File, HTTPException, Depends
from dataclasses import dataclass
from datetime import datetime

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from starlette import status
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


#  ----- user auth

fake_users_db = {
    "Jonathan": {
        "username": "Jonathan",
        "full_name": "Jonathan Cheng",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedqwertyuiop",
        "disabled": False,
        "userID": "sksksksksksk1234"
    },
    "Jerry": {
        "username": "Jerry",
        "full_name": "Jiahui Tan",
        "email": "realjerrytan@gmail.com",
        "hashed_password": "fakehashedqwerty",
        "disabled": False,
        "userID": "1sfhsafabfhbahfbh8833"
    },
}


def fake_hash_password(password: str):
    return "fakehashed" + password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@app.post("/signup")
async def signup(form_data: OAuth2PasswordRequestForm = Depends()):
    fake_users_db[form_data.username] = {
        "username": form_data.username,
        "full_name": form_data.username,
        "email": form_data.username + "@gmail.com",
        "hashed_password": "hashed" + form_data.password,
        "disabled": False,
        "userID": "sdjnasjfnajfj2323"
    }

    return {"access_token": form_data.username, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


#  ----- data definitions

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
                     + " plan to spend a fair amount of time in Grant Park. This area is home to such notable " \
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

    roDesc = "Rome was called the “Eternal City” by the ancient Romans because they believed that no matter" \
             + " what happened in the rest of the world, the city of Rome would always remain standing. Exploring" \
             + " the city centre by foot surrounded by glorious monuments and colossal remains takes you back" \
             + " in time to the “glory that was Rome”"
    veDesc = "Venice is unique environmentally, architecturally, and historically, and in its days as a republic" \
             + " the city was styled la serenissima (“the most serene” or “sublime”). It remains a major Italian" \
             + " port in the northern Adriatic Sea and is one of the world's oldest tourist and cultural centres"
    floDesc = "Florence (Firenze in Italian) is a small cultural metropolis that offers visitors some of the" \
              + " world's top museums and art galleries. The city is a real open-air museum and is the" \
              + " birthplace of the Renaissance."
    miDesc = "Milan offers all the advantages of a large city, but it is relatively small, thus making it perfect" \
             + " to visit, as tourists can get to most of the city’s attractions and museums by foot." \
             + " Additionaly, Milan is internationally recognised as one of the world’s most important fashion" \
             + " capitals, but it also has a wealth of interesting museums and things to see and do."
    naDesc = "Naples, Napoli in Italian, is the third-largest city in Italy, located in the Campania region in" \
             + " the southern part of the country.  Its close proximity to many interesting sites, such as " \
             + "Pompeii and the Bay of Naples, makes it a good base for exploring the area. Naples is a vibrant" \
             + " and chaotic city, full of wonderful historical and artistic treasures and narrow," \
             + " winding streets with small shops."
    amDesc = "The Amalfi coast is one of the most renowned tourist destinations in the whole of Italy and " \
             + "draws thousands of tourists annually. This stretch of mountainous coast sits in-between Naples " \
             + "and Salerno and encompasses the arm of the Sorrento Peninsula. The coastline includes some absolutely" \
             + " gorgeous towns that hug the mountains, some sublime beaches and jaw-dropping scenery."

    ro = City("Romes", apartmentList, roDesc, parse_url("https://tinyurl.com/3kunj28y").url)
    ve = City("Venice", apartmentList, veDesc, parse_url("https://tinyurl.com/5wavafev").url)
    flo = City("Florence", apartmentList, floDesc, parse_url("https://tinyurl.com/zrarspdc").url)
    mi = City("Milan", apartmentList, miDesc, parse_url("https://tinyurl.com/rztp6mbm").url)
    na = City("Naples", apartmentList, naDesc, parse_url("https://tinyurl.com/yuwurmjy").url)
    am = City("Amalfi", apartmentList, amDesc, parse_url("https://tinyurl.com/yfmx9vch").url)
    tempCitiesItaly = [ro, ve, flo, mi, na, am]
    italyCities = Cities(tempCitiesItaly, Country.IT)

    parisDesc = "Paris, capital of France, is one of the most important and influential cities in the world." \
                + " Some of the most memorable things to do in Paris include visiting the Eiffel Tower," \
                + " the Arc de Triomphe and Notre-Dame Cathedral. During the evening, experiencing one of the" \
                + " legendary Moulin Rouge cabaret shows, strolling through some of the most picturesque" \
                + " neighborhoods, like Montmartre, or climbing the Montparnasse Tower are a must."
    niceDesc = "Nice is a place to enjoy life, to take in the beauty of the gardens and the sea, and to soak" \
               + " up the vibrant Mediterranean energy. From wandering the quaint cobblestone streets to strolling" \
               + " the famous Promenade des Anglais, the joys of spending time in this beautiful city are endless."
    bordeauxDesc = "Bordeaux is called the 'Port of the Moon' because of its romantic location on a crescent-shaped" \
                   + " bend of the Garonne River. In this splendid setting that allowed trade to flourish, the city" \
                   + " has a rich cultural heritage dating back to antiquity."
    lyonDesc = "Lyon is France's second city, one of France's oldest cities, and is reputed as the gourmet capital" \
               + " of France. It's large historic centre, Le Vieux Lyon, is a UNESCO World Heritage site," \
               + " and is the largest ensemble of Renaissance buildings in Europe."
    cannesDesc = "In an enchanting setting on Golfe de la Napoule bay, Cannes is blessed with a balmy" \
                 + " Mediterranean climate. The weather is mild year-round and perfect for sunbathing by the " \
                 + "beach from May through October. Leafy palm trees grace the streets of Cannes, and subtropical" \
                 + " flowers flourish throughout the city, giving visitors the impression of being in paradise."
    corsicaDesc = "Corsica is an island of superlatives,a mountain jewel set in the middle of the" \
                  + " Mediterranean. Our many museums are home to remarkable exhibits which bear witness " \
                  + "to the passing of time and the island's history. Corsica is an island of superlatives,a " \
                  + "mountain jewel set in the middle of the Mediterranean."

    paris = City("Paris", [], parisDesc, parse_url("https://tinyurl.com/rc4cd4fe").url)
    nice = City("Nice", [], niceDesc, parse_url("https://tinyurl.com/55498jwc").url)
    bordeaux = City("Bordeaux", [], bordeauxDesc, parse_url("https://tinyurl.com/2sa7xzcc").url)
    lyon = City("Lyon", [], lyonDesc, parse_url("https://tinyurl.com/dv9wtxas").url)
    cannes = City("Cannes", [], cannesDesc, parse_url("https://tinyurl.com/2u6krn7v").url)
    corsica = City("Corsica", [], corsicaDesc, parse_url("https://tinyurl.com/njz58nwc").url)
    tempCitiesFrance = [paris, nice, bordeaux, lyon, cannes, corsica]
    franceCities = Cities(tempCitiesFrance, Country.FR)

    tokyoDESC = "Tokyo offers a seemingly unlimited choice of shopping, entertainment, culture " \
                "and dining to its visitors. The city's history can be appreciated in districts " \
                "such as Asakusa and in many excellent museums, historic temples and gardens. In " \
                "addition to the city, Tokyo also offers a number of attractive green spaces in " \
                "the city center and within relatively short train rides at its outskirts."
    kyotoDESC = "The streets of Kyoto, which are deeply influenced by traditional Japanese culture. " \
                "The seas, in which Japan's oldest legends are still alive, and the mountains that are" \
                " the origins of the Japanese people. Beyond the city, Kyoto Prefecture stretches north" \
                " through the forest to the sea."
    osakaDESC = "Hop off the bullet train into an area of exciting nightlife, delicious food and" \
                " straight-talking, friendly locals. Along with plenty of shopping and modern " \
                "attractions, Osaka also has a historical side, the highlight of which is Osaka " \
                "Castle. The castle is a great place to discover more about Japanese history and " \
                "to wander the beautiful grounds, especially during cherry blossom season in April " \
                "when the sakura blooms and the weather is often at its best."
    hiroshimaDESC = "Hiroshima Prefecture is located in the southwestern part of the Japanese islands. " \
                    "It is rich in the natural beauty of the Inland Sea and the Chugoku Mountains, with " \
                    "mountains, sea, rivers, valleys, plains, basins that characterize Japan's landscape."
    sapporoDESC = "Sapporo (札幌, \"important river flowing through a plain\" in Ainu language) is the capital " \
                  "of Hokkaido and Japan's fifth largest city. Sapporo is also one of the nation's youngest " \
                  "major cities. Sapporo became world famous in 1972 when the Olympic Winter Games were held " \
                  "there. Today, the city is well known for its ramen, beer, and the annual snow festival held " \
                  "in February."
    fukuokaDESC = "Fukuoka is the administrative, economic, and cultural center of the southernmost island of " \
                  "Kyushu and is one of the country's most progressive cities. Located in Hakata Bay, Fukuoka " \
                  "is divided in two by the River Naka, with Hakata, the older eastern part of the city, serving " \
                  "as an important port and commercial center. Fukuoka is also a tourism hot spot that's home to " \
                  "numerous fine museums, art galleries, and theaters, as well as great places to eat. The city " \
                  "also hosts many professional sporting events and festivals."

    tokyo = City("Tokyo", [], tokyoDESC, parse_url("https://tinyurl.com/3v4e8atv").url)
    kyoto = City("Kyoto", [], kyotoDESC, parse_url("https://tinyurl.com/ynynermf").url)
    osaka = City("Osaka", [], osakaDESC, parse_url("https://tinyurl.com/85t9d34z").url)
    hiroshima = City("Hiroshima", [], hiroshimaDESC, parse_url("https://tinyurl.com/hesjnytw").url)
    sapporo = City("Sapporo", [], sapporoDESC, parse_url("https://tinyurl.com/dy5jze3p").url)
    fukuoka = City("Fukuoka", [], fukuokaDESC, parse_url("https://tinyurl.com/263u9ntt").url)
    tempCitiesJapan = [tokyo, kyoto, osaka, hiroshima, sapporo, fukuoka]
    japanCities = Cities(tempCitiesJapan, Country.JP)

    beijingDESC = " Beijing is the nation's political, economic, and cultural center. Located in north China, close to " \
                  "the port city of Tianjin and partially surrounded by Hebei Province, it also serves as the most " \
                  "important transportation hub and port of entry."
    shanghaiDESC = "Shanghai, Hu for short, is a renowned international metropolis drawing more and more attention" \
                   " from all over the world. Situated on the estuary of Yangtze River, it serves as the most" \
                   " influential economic, financial, international trade, and cultural center in East China. " \
                   "Here, one finds the perfect blend of cultures, the modern and the traditional , " \
                   "and the western and the oriental."
    chengduDESC = "Chengdu is now one of the most popular travel destinations in China mostly owning to its everlasting" \
                  " history, well-preserved tradition, unique local folks and arts, pleasant weather, developed tourism " \
                  "industry. Among all these features, Giant Panda is the most attractive treasure for all visitors to " \
                  "Chengdu, and world-famous Sichuan Cuisine and Chengdu’s local leisure lifestyle also appeal to " \
                  "worldwide curiosity."
    xianDESC = "Xi'an, located in central-northwest China, records the great changes of the country just like a living " \
               "history book. Called Chang'an (meaning the eternal city) in ancient times, it is one of the birthplaces " \
               "of the ancient Chinese civilization in the Yellow River Basin area."
    hangzhouDESC = "Considered more tranquil than many of China's other big cities, the downtown core is built up around" \
                   " the beautiful West Lake with its many old shrines and temples, romantic bridges, and pagodas, all " \
                   "of them popular to see at night when they're lit up. Hangzhou was famously described by Marco Polo " \
                   "as the most beautiful city in the world. Hangzhou is also known as the Silk City for its long " \
                   "tradition of manufacturing the material, a tradition that lives on in its many silk mills and markets."

    beijing = City("Beijing", [], beijingDESC, parse_url("https://tinyurl.com/yfypw5uj").url)
    shanghai = City("Shanghai", [], shanghaiDESC, parse_url("https://tinyurl.com/xe7k7sem").url)
    chengdu = City("Chengdu", [], chengduDESC, parse_url("https://tinyurl.com/v6nw25f").url)
    xian = City("Xi'an", [], xianDESC, parse_url("https://tinyurl.com/s9243y3v").url)
    hangzhou = City("Hanzhou", [], hangzhouDESC, parse_url("https://tinyurl.com/jeaaej4p").url)
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
