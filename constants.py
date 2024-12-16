from enum import Enum

class Gender(str, Enum):
    HOME = 'Home'
    DONA = 'Dona'
    ALTRES = 'Altres'

class Age(str, Enum):
    JOVE = 'Jove'
    MITJA = 'Mitjana edat'
    GRAN = 'Gran'

class Profile(str, Enum):
    EXPERT = 'Expert'
    CURIOS = 'Curiós'
    PRAGMATIC = 'Pragmàtic'
    OCASIONAL = 'Ocasional'

class Category(str, Enum):
    NEGRE = 'Negre'
    BLANC = 'Blanc'
    ROSAT = 'Rosat'
    ESPUMOS = 'Espumós'

class Aroma(str, Enum):
    AFRUITAT = 'Afruitat'
    ESPECIAT = 'Especiat'

class Ripening(str, Enum):
    JOVE = 'Jove'
    BARRIL = 'Barril'

class Body(str, Enum):
    LLEUGER = 'Lleuger'
    AMB_COS = 'Amb cos'

# Category
RED = 'Red'
WHITE = 'White'
ROSE = 'Rose'
SPARKLING = 'Sparkling'

# Categoria
NEGRE = 'Negre'
BLANC = 'Blanc'
ROSAT = 'Rosat'
ESPUMOS = 'Espumós'

# Food
APPETIZERS = "Appetizers"
CHEESE = "Cheese"
CHICKEN = "Chicken"
DESSERTS = "Desserts"
FISH = "Fish"
MEAT = "Meat"
PASTA = "Pasta"
RED_MEAT = "Red Meat"
SALAD = "Salad"
SEAFOOD = "Seafood"
VEGETABLES = "Vegetables"
WHITE_MEAT = "White Meat"

# Menjar
APERITIUS = "Aperitius"
FORMATGE = "Formatge"
POLLASTRE = "Pollastre"
POSTRES = "Postres"
PEIX = "Peix"
CARN = "Carn"
PASTA_CATALAN = "Pasta"
CARN_VERMELLA = "Carn Vermella"
AMANIDA = "Amanida"
MARISC = "Marisc"
VERDURES = "Verdures"
CARN_BLANCA = "Carn Blanca"


# Countries
SPAIN = "Spain"
FRANCE = "France"
PORTUGAL = "Portugal"
GERMANY = "Germany"
ITALY = "Italy"
USA = "USA"
SOUTH_AFRICA = "South Africa"
CHILE = "Chile"
ARGENTINA = "Argentina"
NEW_ZEALAND = "New Zealand"
JAPAN = "Japan"
BRAZIL = "Brazil"
MOROCCO = "Morocco"
URUGUAY = "Uruguay"
ROMANIA = "Romania"

# Països
ESPANYA = "Espanya"
FRANÇA = "França"
PORTUGAL_CATALAN = "Portugal"
ALEMANYA = "Alemanya"
ITALIA = "Itàlia"
EUA = "EUA"
SUD_AFRICA = "Sud-àfrica"
XILE = "Xile"
ARGENTINA_CATALAN = "Argentina"
NOVA_ZELANDA = "Nova Zelanda"
JAPO = "Japó"
BRASIL = "Brasil"
MARROC = "Marroc"
URUGUAI = "Uruguai"
ROMANIA_CATALAN = "Romania"
MEXIC = "Mèxic"
XINA = "Xina"
INDIA = 'Índia'
ANGLATERRA = 'Anglaterra'
GRECIA = 'Grècia'
GEORGIA = 'Geòrgia'
LIBAN = 'Líban'

# Tastes
BRUT = "Brut"
BRUT_NATURE = "Brut Nature"
BRUT_ORGANIC = "Brut Organic"
DRY = "Dry"
EXTRA_BRUT = "Extra Brut"
EXTRA_DRY = "Extra Dry"
FORTIFIED_WINE = "Fortified Wine"
SEMI_DRY = "Semi Dry"
SEMI_SWEET = "Semi Sweet"
SWEET = "Sweet"

# Gustos
BRUT_CATALAN = "Brut"
BRUT_NATURE_CATALAN = "Brut Nature"
BRUT_ORGANIC_CATALAN = "Brut Orgànic"
SEC = "Sec"
EXTRA_BRUT_CATALAN = "Extra Brut"
EXTRA_SEC = "Extra Sec"
VI_FORTIFICAT = "Vi Fortificat"
SEMI_SEC = "Semi Sec"
SEMI_DOLÇ = "Semi Dolç"
DOLÇ = "Dolç"


translation_dict = {
    # Categories
    RED: NEGRE,
    WHITE: BLANC,
    ROSE: ROSAT,
    SPARKLING: ESPUMOS,
    
    # Food
    APPETIZERS: APERITIUS,
    CHEESE: FORMATGE,
    CHICKEN: POLLASTRE,
    DESSERTS: POSTRES,
    FISH: PEIX,
    MEAT: CARN,
    PASTA: PASTA_CATALAN,
    RED_MEAT: CARN_VERMELLA,
    SALAD: AMANIDA,
    SEAFOOD: MARISC,
    VEGETABLES: VERDURES,
    WHITE_MEAT: CARN_BLANCA,

    # Countries
    SPAIN: ESPANYA,
    FRANCE: FRANÇA,
    PORTUGAL: PORTUGAL_CATALAN,
    GERMANY: ALEMANYA,
    ITALY: ITALIA,
    USA: EUA,
    SOUTH_AFRICA: SUD_AFRICA,
    CHILE: XILE,
    ARGENTINA: ARGENTINA_CATALAN,
    NEW_ZEALAND: NOVA_ZELANDA,
    JAPAN: JAPO,
    BRAZIL: BRASIL,
    MOROCCO: MARROC,
    URUGUAY: URUGUAI,
    ROMANIA: ROMANIA_CATALAN,

    # Tastes
    BRUT: BRUT_CATALAN,
    BRUT_NATURE: BRUT_NATURE_CATALAN,
    BRUT_ORGANIC: BRUT_ORGANIC_CATALAN,
    DRY: SEC,
    EXTRA_BRUT: EXTRA_BRUT_CATALAN,
    EXTRA_DRY: EXTRA_SEC,
    FORTIFIED_WINE: VI_FORTIFICAT,
    SEMI_DRY: SEMI_SEC,
    SEMI_SWEET: SEMI_DOLÇ,
    SWEET: DOLÇ,
}


ranges_alcohol = [
    (0, 5),
    (5, 10),
    (10, 15),
    (15, 21)
]

ranges_price = [
    (7, 15),
    (15, 25),
    (25, 50),
    (50, 100),
    (100, 160)
]

# Coneixemet expert
exotic_varieties = [
    'Assyrtiko',
    'Xinomavro',
    'Torrontés',
    'Saperavi',
    'Aglianico',
    'Grüner Veltliner',
    'Carmenère',
    'Verdicchio',
    'Picpoul',
    'Blaufränkisch',
    'Furmint',
    'Mencia',
    'Touriga Nacional',
    'Schiava',
    'Bobal',
]

noble_varieties = [
    'Cabernet Sauvignon',
    'Merlot',
    'Pinot Noir',
    'Syrah',
    'Chardonnay',
    'Sauvignon Blanc',
    'Riesling',
    'Tempranillo',
    'Nebbiolo',
    'Sangiovese',
]

recognized_countries = [
    ESPANYA,
    FRANÇA,
    ALEMANYA,
    ITALIA,
    EUA,
    SUD_AFRICA,
    XILE,
    ARGENTINA_CATALAN,
    NOVA_ZELANDA,
]

emerging_countries = [
    URUGUAI,
    BRASIL,
    MEXIC,
    XINA,
    INDIA,
    ANGLATERRA,
    GRECIA,
    GEORGIA,
    LIBAN,
    SUD_AFRICA,
]

varieties_young_men = [
    'Pinot Noir',
    'Chardonnay',
    'Syrah',
    'Riesling',
    'Malbec',
]

varieties_mid_men = [
    'Tempranillo',
    'Sauvignon Blanc',
    'Cabernet Sauvignon',
    'Gewürztraminer',
    'Merlot',
]

varieties_old_men = [
    'Chardonnay',
    'Pinot Noir',
    'Syrah',
    'Riesling',
    'Malbec',
]

varieties_young_women = [
    'Moscatel',
    'Garnacha',
    'Sauvignon Blanc',
    'Pinot Noir',
]

varieties_mid_women = [
    'Tempranillo',
    'Chardonnay',
    'Syrah',
    'Riesling',
]

varieties_old_women = [
    'Cabernet Sauvignon',
    'Sauvignon Blanc',
    'Merlot',
    'Gewürztraminer',
    'Tempranillo',
]