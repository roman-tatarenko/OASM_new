from resources.domain._ import _

status = ("cancelled", "active", "complete")
statusDetails = ("empty",)

schema_lot = {
    "id": _("uuid"),
    "title": "Далеко-далеко за словесными горами в стране гласных и согласных живут рыбные тексты. "
             "Вдали от всех живут они в буквенных домах на берегу Семантика большого языкового океана. "
             "Маленький ручеек Даль журчит по всей стране и обеспечивает ее всеми необходимыми правилами. "
             "Эта парадигматическая страна, в которой жаренные члены предложения залетают прямо в рот. "
             "Даже всемогущая пунктуация не имеет власти над рыбными текстами, ведущими безорфографичный образ жизни.",
    "description": "looot",
    "status": _("random.schoice", seq=status, end=1),
    "statusDetails": _("random.schoice", seq=statusDetails, end=1),
    "value": {
        "amount": 10.00,
        "currency": "EUR"
    },
    "internalId": "Lot1",
    "options": [{
        "hasOptions": False
    }],
    "variants": [{
        "hasVariants": False
    }],
    "renewals": [{
        "hasRenewals": False
    }],
    "recurrentProcurement": [{
        "isRecurrent": False
    }],
    "contractPeriod": {
        "startDate": "2020-04-28T14:45:00Z",
        "endDate": "2020-04-30T14:45:00Z"
    },
    "placeOfPerformance": {
        "address": {
            "streetAddress": "6666",
            "postalCode": "666",
            "addressDetails": {
                "country": {
                    "scheme": "iso-alpha2",
                    "id": "MD",
                    "description": "Moldova, Republica",
                    "uri": "https://www.iso.org"
                },
                "region": {
                    "scheme": "CUATM",
                    "id": "0101000",
                    "description": "mun.Chişinău",
                    "uri": "http://statistica.md"
                },
                "locality": {
                    "description": "mun.Chişinău",
                    "id": "002125",
                    "scheme": "other"

                }
            }
        },
        "description": "description of lot"
    }
}


