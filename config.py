urls = {
    "TORGI_1_INVESTMOSCOW": {
        "url": """https://investmoscow.ru/tenders?pageNumber=1&pageSize=10&orderBy=RequestEndDate&orderAsc=false&objectTypes=nsi:41:30011569,nsi:41:817,nsi:41:30020049&objectKinds=nsi:tender_type_portal:13&price.min=35000000&price.max=429079002&area.min=200&area.max=9097.4&tenderStatus=nsi:tender_status_tender_filter:2&timeToPublicTransportStop.max=0&timeToPublicTransportStop.foot=false&timeToPublicTransportStop.publicTransport=false&timeToPublicTransportStop.noMatter=true&areaNoLiving.min=200&areaBuilding.min=200&entranceTypes=nsi:1032:103201&noLivingRoomFloors=nsi:1071:30021071""",
        "paginator": """https://investmoscow.ru/tenders?pageNumber={}&pageSize=10&orderBy=RequestEndDate&orderAsc=false&objectTypes=nsi:41:30011569,nsi:41:817,nsi:41:30020049&objectKinds=nsi:tender_type_portal:13&price.min=35000000&price.max=429079002&area.min=200&area.max=9097.4&tenderStatus=nsi:tender_status_tender_filter:2&timeToPublicTransportStop.max=0&timeToPublicTransportStop.foot=false&timeToPublicTransportStop.publicTransport=false&timeToPublicTransportStop.noMatter=true&areaNoLiving.min=200&areaBuilding.min=200&entranceTypes=nsi:1032:103201&noLivingRoomFloors=nsi:1071:30021071"""
    },
    "TORGI_2_INVESTMOSCOW": {
        "url": """https://investmoscow.ru/tenders?pageNumber=1&pageSize=10&orderBy=RequestEndDate&orderAsc=false&objectTypes=nsi:41:30011568,nsi:41:30011578,nsi:41:30011569,nsi:41:818,nsi:41:99021071,nsi:41:817,nsi:41:30011570,nsi:41:30011571,nsi:41:30011572,nsi:41:30011573,nsi:41:30011574,nsi:41:30011575,nsi:41:30011576,nsi:41:30011616,nsi:41:30011617,nsi:41:30021081,nsi:41:30021085,nsi:41:105001,nsi:41:30011566,nsi:41:30020001,nsi:41:105002,nsi:41:30016285,nsi:41:30020000,nsi:41:30011567,nsi:41:30011577,nsi:41:30011580,nsi:41:30020049,nsi:41:30011579,nsi:41:30021099,nsi:41:30021098,nsi:41:30021068,nsi:41:30021069&objectKinds=nsi:tender_type_portal:15,nsi:tender_type_portal:16,nsi:tender_type_portal:19&price.min=35000000&price.max=7451881550.05&area.min=200&area.max=9097.4&tenderStatus=nsi:tender_status_tender_filter:2&timeToPublicTransportStop.max=0&timeToPublicTransportStop.foot=false&timeToPublicTransportStop.publicTransport=false&timeToPublicTransportStop.noMatter=true&areaNoLiving.min=200&areaBuilding.min=200&entranceTypes=nsi:1032:103201&noLivingRoomFloors=nsi:1071:30021071""",
        "paginator": """https://investmoscow.ru/tenders?pageNumber={}&pageSize=10&orderBy=RequestEndDate&orderAsc=false&objectTypes=nsi:41:30011568,nsi:41:30011578,nsi:41:30011569,nsi:41:818,nsi:41:99021071,nsi:41:817,nsi:41:30011570,nsi:41:30011571,nsi:41:30011572,nsi:41:30011573,nsi:41:30011574,nsi:41:30011575,nsi:41:30011576,nsi:41:30011616,nsi:41:30011617,nsi:41:30021081,nsi:41:30021085,nsi:41:105001,nsi:41:30011566,nsi:41:30020001,nsi:41:105002,nsi:41:30016285,nsi:41:30020000,nsi:41:30011567,nsi:41:30011577,nsi:41:30011580,nsi:41:30020049,nsi:41:30011579,nsi:41:30021099,nsi:41:30021098,nsi:41:30021068,nsi:41:30021069&objectKinds=nsi:tender_type_portal:15,nsi:tender_type_portal:16,nsi:tender_type_portal:19&price.min=35000000&price.max=7451881550.05&area.min=200&area.max=9097.4&tenderStatus=nsi:tender_status_tender_filter:2&timeToPublicTransportStop.max=0&timeToPublicTransportStop.foot=false&timeToPublicTransportStop.publicTransport=false&timeToPublicTransportStop.noMatter=true&areaNoLiving.min=200&areaBuilding.min=200&entranceTypes=nsi:1032:103201&noLivingRoomFloors=nsi:1071:30021071"""
    },
    "TORGI_GOV_RU": """https://torgi.gov.ru/new/api/public/lotcards/export/excel?biddType=178FZ,229FZ&chars=&chars=dec-totalAreaRealty:200~&biddEndFrom=&biddEndTo=&pubFrom=&pubTo=&aucStartFrom=&aucStartTo=&catCode=11&text=&matchPhrase=false&amoOrgCode=&npa=&typeTransaction=sale&byFirstVersion=true&sort=firstVersionPublicationDate,desc""",
    "AVITO": {
        "url": """https://www.avito.ru/moskva/kommercheskaya_nedvizhimost/prodam-ASgBAgICAUSwCNJW?cd=1&f=ASgBAQECAkSwCNJW8hKg2gECQJ7DDSSI2TmG2TmI9BE0zIGLA8qBiwPIgYsDAUXGmgwXeyJmcm9tIjo1MDAwMDAwLCJ0byI6MH0&p=1""",
        "paginator": """https://www.avito.ru/moskva/kommercheskaya_nedvizhimost/prodam-ASgBAgICAUSwCNJW?cd=1&f=ASgBAQECAkSwCNJW8hKg2gECQJ7DDSSI2TmG2TmI9BE0zIGLA8qBiwPIgYsDAUXGmgwXeyJmcm9tIjo1MDAwMDAwLCJ0byI6MH0&p={}""",
        "max_pages": 4
        }
    }
class ExcelSettings:
    safety_save = False # True - save the excel every time something is being added to the table
    remove_duplicates = False # True - check for duplicates upon addition of new entries into the tables

    default_cols = ['Площадь', 'Стоимость', 'Адрес', 'Назначение', 'Ссылка', 'Описание', 'Дата окончания торгов']

class WebSettings:
    timeout = 15 #s for reaching the site
    additional_wait = 5 #s

    avito_random_time_min = 1
    avito_random_time_max = 5

run_every = 3600*24 #s