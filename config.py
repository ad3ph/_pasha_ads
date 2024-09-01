from configparser import ConfigParser
config = ConfigParser(interpolation=None)

config.read('config.ini')

# Accessing the configurations
urls = {
    "TORGI_1_INVESTMOSCOW": {
        "url": config['TORGI_1_INVESTMOSCOW']['url'],
        "paginator": config['TORGI_1_INVESTMOSCOW']['paginator'],
        "max_pages": int(config['TORGI_1_INVESTMOSCOW']['max_pages'])
    },
    "TORGI_2_INVESTMOSCOW": {
        "url": config['TORGI_2_INVESTMOSCOW']['url'],
        "paginator": config['TORGI_2_INVESTMOSCOW']['paginator'],
        "max_pages": int(config['TORGI_2_INVESTMOSCOW']['max_pages'])
    },
    "TORGI_GOV_RU": config['TORGI_GOV_RU']['url'],
    "AVITO": {
        "url": config['AVITO']['url'],
        "paginator": config['AVITO']['paginator'],
        "max_pages": int(config['AVITO']['max_pages'])
        },
    "TORGI_ROSSII": {
        "url": config['TORGI_ROSSII']['url'],
        "date_parametrized": config['TORGI_ROSSII']['date_parametrized'],
        "date_format": config['TORGI_ROSSII']['date_format'],
        "date_offset": int(config['TORGI_ROSSII']['date_offset'])
    },
    "TBANKROT": {
        "url": config['TBANKROT']['url'],
        "date_parametrized": config['TBANKROT']['date_parametrized'],
        "date_format": config['TBANKROT']['date_format'],
        "date_offset": int(config['TBANKROT']['date_offset'])
    }
}

class ExcelSettings:
    safety_save = config.getboolean('ExcelSettings', 'safety_save')
    remove_duplicates = config.getboolean('ExcelSettings', 'remove_duplicates')
    checklist = config.get('ExcelSettings', '').split(',')
    default_cols = config['ExcelSettings']['default_cols'].split(', ')

class WebSettings:
    timeout = config.getint('WebSettings', 'timeout')
    additional_wait = config.getint('WebSettings', 'additional_wait')
    input_wait = config.getint('WebSettings', 'input_wait')
    avito_random_time_min = config.getint('WebSettings', 'avito_random_time_min')
    avito_random_time_max = config.getint('WebSettings', 'avito_random_time_max')
    do_scroll = config.getboolean('WebSettings', 'do_scroll')

run_every = config.getint('General', 'run_every')
KLATR_TOKEN = config['General']['KLATR_TOKEN']

# Unpacking purpose_keywords into a dictionary
purpose_keywords = {}
for key in config['purpose_keywords']:
    purpose_keywords[key] = config['purpose_keywords'][key].split(', ')

class TBANKROTcredentials:
    login = config['TBANKROTcredentials']['login']
    password = config['TBANKROTcredentials']['password']

# Example usage
from json import dumps
print(dumps(urls, indent=4))
print("______________________________________________")
print(ExcelSettings.__dict__)
print("______________________________________________")

print(WebSettings.__dict__)
print("______________________________________________")

print(TBANKROTcredentials.__dict__)
print("______________________________________________")

print(run_every)
print("______________________________________________")

print(KLATR_TOKEN)

########
'''urls = {
    "TORGI_1_INVESTMOSCOW": {
        "url": """https://investmoscow.ru/tenders?pageNumber=1&pageSize=50&orderBy=RequestEndDate&orderAsc=false&objectTypes=nsi:41:30011569,nsi:41:817,nsi:41:30020049&objectKinds=nsi:tender_type_portal:13&price.min=35000000&price.max=429079002&area.min=200&area.max=9097.4&tenderStatus=nsi:tender_status_tender_filter:2&timeToPublicTransportStop.max=0&timeToPublicTransportStop.foot=false&timeToPublicTransportStop.publicTransport=false&timeToPublicTransportStop.noMatter=true&areaNoLiving.min=200&areaBuilding.min=200&entranceTypes=nsi:1032:103201&noLivingRoomFloors=nsi:1071:30021071""",
        "paginator": """https://investmoscow.ru/tenders?pageNumber={}&pageSize=50&orderBy=RequestEndDate&orderAsc=false&objectTypes=nsi:41:30011569,nsi:41:817,nsi:41:30020049&objectKinds=nsi:tender_type_portal:13&price.min=35000000&price.max=429079002&area.min=200&area.max=9097.4&tenderStatus=nsi:tender_status_tender_filter:2&timeToPublicTransportStop.max=0&timeToPublicTransportStop.foot=false&timeToPublicTransportStop.publicTransport=false&timeToPublicTransportStop.noMatter=true&areaNoLiving.min=200&areaBuilding.min=200&entranceTypes=nsi:1032:103201&noLivingRoomFloors=nsi:1071:30021071""",
        "max_pages": 4
    },
    "TORGI_2_INVESTMOSCOW": {
        "url": """https://investmoscow.ru/tenders?pageNumber=1&pageSize=50&orderBy=RequestEndDate&orderAsc=false&objectTypes=nsi:41:30011568,nsi:41:30011578,nsi:41:30011569,nsi:41:818,nsi:41:99021071,nsi:41:817,nsi:41:30011570,nsi:41:30011571,nsi:41:30011572,nsi:41:30011573,nsi:41:30011574,nsi:41:30011575,nsi:41:30011576,nsi:41:30011616,nsi:41:30011617,nsi:41:30021081,nsi:41:30021085,nsi:41:105001,nsi:41:30011566,nsi:41:30020001,nsi:41:105002,nsi:41:30016285,nsi:41:30020000,nsi:41:30011567,nsi:41:30011577,nsi:41:30011580,nsi:41:30020049,nsi:41:30011579,nsi:41:30021099,nsi:41:30021098,nsi:41:30021068,nsi:41:30021069&objectKinds=nsi:tender_type_portal:15,nsi:tender_type_portal:16,nsi:tender_type_portal:19&price.min=35000000&price.max=7451881550.05&area.min=200&area.max=9097.4&tenderStatus=nsi:tender_status_tender_filter:2&timeToPublicTransportStop.max=0&timeToPublicTransportStop.foot=false&timeToPublicTransportStop.publicTransport=false&timeToPublicTransportStop.noMatter=true&areaNoLiving.min=200&areaBuilding.min=200&entranceTypes=nsi:1032:103201&noLivingRoomFloors=nsi:1071:30021071""",
        "paginator": """https://investmoscow.ru/tenders?pageNumber={}&pageSize=50&orderBy=RequestEndDate&orderAsc=false&objectTypes=nsi:41:30011568,nsi:41:30011578,nsi:41:30011569,nsi:41:818,nsi:41:99021071,nsi:41:817,nsi:41:30011570,nsi:41:30011571,nsi:41:30011572,nsi:41:30011573,nsi:41:30011574,nsi:41:30011575,nsi:41:30011576,nsi:41:30011616,nsi:41:30011617,nsi:41:30021081,nsi:41:30021085,nsi:41:105001,nsi:41:30011566,nsi:41:30020001,nsi:41:105002,nsi:41:30016285,nsi:41:30020000,nsi:41:30011567,nsi:41:30011577,nsi:41:30011580,nsi:41:30020049,nsi:41:30011579,nsi:41:30021099,nsi:41:30021098,nsi:41:30021068,nsi:41:30021069&objectKinds=nsi:tender_type_portal:15,nsi:tender_type_portal:16,nsi:tender_type_portal:19&price.min=35000000&price.max=7451881550.05&area.min=200&area.max=9097.4&tenderStatus=nsi:tender_status_tender_filter:2&timeToPublicTransportStop.max=0&timeToPublicTransportStop.foot=false&timeToPublicTransportStop.publicTransport=false&timeToPublicTransportStop.noMatter=true&areaNoLiving.min=200&areaBuilding.min=200&entranceTypes=nsi:1032:103201&noLivingRoomFloors=nsi:1071:30021071""",
        "max_pages": 4
    },
    "TORGI_GOV_RU": """https://torgi.gov.ru/new/api/public/lotcards/export/excel?biddType=178FZ,229FZ&chars=&chars=dec-totalAreaRealty:200~&biddEndFrom=&biddEndTo=&pubFrom=&pubTo=&aucStartFrom=&aucStartTo=&catCode=11&text=&matchPhrase=false&amoOrgCode=&npa=&typeTransaction=sale&byFirstVersion=true&sort=firstVersionPublicationDate,desc""",
    "AVITO": {
        "url": """https://www.avito.ru/moskva/kommercheskaya_nedvizhimost/prodam-ASgBAgICAUSwCNJW?cd=1&f=ASgBAQECAkSwCNJW8hKg2gECQJ7DDSSI2TmG2TmI9BE0zIGLA8qBiwPIgYsDAUXGmgwXeyJmcm9tIjo1MDAwMDAwLCJ0byI6MH0&p=1""",
        "paginator": """https://www.avito.ru/moskva/kommercheskaya_nedvizhimost/prodam-ASgBAgICAUSwCNJW?cd=1&f=ASgBAQECAkSwCNJW8hKg2gECQJ7DDSSI2TmG2TmI9BE0zIGLA8qBiwPIgYsDAUXGmgwXeyJmcm9tIjo1MDAwMDAwLCJ0byI6MH0&p={}""",
        "max_pages": 4
        },
    "TORGI_ROSSII": {
        "url": """https://xn----etbpba5admdlad.xn--p1ai/search?search=&categorie_childs%5B%5D=8&trades-section=&trades-type=&begin-price-from=35000000&begin-price-to=&current-price-from=&current-price-to=&begin_bid_from=&begin_bid_to=&end_bid_from=01.01.2024&end_bid_to=30.06.2024&debtor_type=&debtor_name=&debtor_inn=&group_org=&organizer_name=&arbitr_inn=""",
        "date_parametrized": """https://xn----etbpba5admdlad.xn--p1ai/search?search=&categorie_childs%5B%5D=8&trades-section=&trades-type=&begin-price-from=35000000&begin-price-to=&current-price-from=&current-price-to=&begin_bid_from=&begin_bid_to=&end_bid_from={}&end_bid_to={}&debtor_type=&debtor_name=&debtor_inn=&group_org=&organizer_name=&arbitr_inn=""",
        "date_format": "dd.mm.yyyy",
        "date_offset": 14 #days
    },
    "TBANKROT": {
        "url": """https://tbankrot.ru/?start_p1=&start_p2=&p1=35000000&p2=&min_p1=&min_p2=&sort=created&sort_order=desc&swp=&search=&num=&debtor_cat=0&debtor=&au=&org=&stop=&pp_1=&pp_2=&st_1=&st_2=&sz_1=&sz_2=&ez_1=2024-08-15&ez_2=2024-09-13&et_1=&et_2=&parent_cat=2&sub_cat=3%2C5&spec_search=1&spec_type=&show_period=all&mark=&pattern_name=""",
        "date_parametrized": """https://tbankrot.ru/?start_p1=&start_p2=&p1=35000000&p2=&min_p1=&min_p2=&sort=created&sort_order=desc&swp=&search=&num=&debtor_cat=0&debtor=&au=&org=&stop=&pp_1=&pp_2=&st_1=&st_2=&sz_1=&sz_2=&ez_1={}&ez_2={}&et_1=&et_2=&parent_cat=2&sub_cat=3%2C5&spec_search=1&spec_type=&show_period=all&mark=&pattern_name=""",
        "date_format": "yyyy-mm-dd",
        "date_offset": 14 #days
    }
}
class ExcelSettings:
    safety_save = False # True - save the excel every time something is being added to the table

    remove_duplicates = True # True - check for duplicates upon addition of new entries into the tables
    checklist = [] # Переписать сюда пути к экселькам, по которым надо проверить дубликаты

    default_cols = ['Площадь', 'Стоимость', 'Адрес', 'Назначение', 'Ссылка', 'Описание', 'Дата окончания торгов', 'Дубликат']

class WebSettings:
    timeout = 15 #s for reaching the site
    additional_wait = 5 #s
    input_wait = 1 #s

    avito_random_time_min = 1
    avito_random_time_max = 5
    do_scroll = True

run_every = -1 #seconds. Можно писать 24*3600. Поставить -1, чтобы запустить только один раз

purpose_keywords = {
    "Свободное": ["свободного назначения", "свободное назначение", "псн"],
    "ГАБ": ["гaб"],
    "Торговое помещение": ["торгового помещения", "торговое помещение", "ритейл", "retail", "торговая площадь", "торговой площади"],
    "Офисное помещение": ["офис", "офисное помещение", "офисная площадь"],
    "Складское помещение": ["склад", "складское помещение"],
    "Жилое помещение": ["жилой", "жилое помещение", "квартира"],
    "Производственное помещение": ["производственное", "производственное помещение"]
}

class TBANKROTcredentials:
    login = "averageemailenjoyer@proton.me"
    password = "memes_temes"


KLATR_TOKEN = "QYDhnhTzyn7aHnYEs9b4znAT2EfEQtHS"

'''
############