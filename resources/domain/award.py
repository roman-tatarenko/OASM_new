from resources.domain.person import schema_person

schema_award = {
    "token": "TOKEN",
    "id": "AWARD_ID",
    "date": "2020-04-02T13:07:00Z",
    "status": "pending",
    "statusDetails": "awaiting",
    "description": "",
    "value": {
        "amount": 3.00,
        "currency": "EUR"
    },
    "weightedValue": {
        "amount": 3.00,
        "currency": "EUR"
    },
    "relatedLots": ["c0b4b878-d32a-4878-a9cc-9b66e23f5931"],
    "relatedBid": "76887269-a195-4aa2-9e23-afa72214a2b9",
    "bidDate": "2020-04-02T13:01:42Z",
    "suppliers": [
        {

            "id": "MD-IDNO-tenderers id",
            "name": "name",
            "identifier": {
                "id": "tenderers id",
                "scheme": "MD-IDNO",
                "legalName": "tenderers legalname",
                "uri": "http://tenderers.com"
            },
            "address": {
                "streetAddress": "tenderers street adress",
                "postalCode": "tenderers postalcode",
                "addressDetails": {
                    "country": {
                        "scheme": "iso-alpha2",
                        "id": "MD",
                        "description": "MOLDOVA",
                        "uri": "http://reference.iatistandard.org"
                    },
                    "region": {
                        "scheme": "CUATM",
                        "id": "1000000",
                        "description": "Anenii Noi",
                        "uri": "http://statistica.md"
                    },
                    "locality": {
                        "scheme": "CUATM",
                        "id": "1001000",
                        "description": "or.Anenii Noi",
                        "uri": "http://statistica.md"
                    }
                }
            },
            "contactPoint": {
                "name": "Illia Petrusenko",
                "email": "illya.petrusenko@gmail.com",
                "telephone": "+380632074071",
                "faxNumber": "+380445450099",
                "url": "http://petrusenko.com/illia"
            },
            "additionalIdentifiers": [{
                "id": "additionalIdentifiers id",
                "scheme": "MD-IDNO",
                "legalName": "additionalIdentifiers legalName",
                "uri": "http://additionalIdentifier.com"
            }],
            "details": {
                "typeOfSupplier": "company",
                "mainEconomicActivities": ["456-00"],
                "scale": "sme",
                "permits": [{
                    "scheme": "SRLE",
                    "id": "2",
                    "url": "5",
                    "permitDetails": {
                        "issuedBy": {
                            "id": "changed",
                            "name": "changed1"
                        },
                        "issuedThought": {
                            "id": "kjhgh",
                            "name": "rey"
                        },
                        "validityPeriod": {
                            "startDate": "2019-10-29T16:35",
                            "endDate": "2019-10-29T16:36"
                        }
                    }
                }],
                "bankAccounts": [{
                    "description": "description",
                    "bankName": "bankName",
                    "address": {
                        "streetAddress": "streetAddress",
                        "postalCode": "postalCode",
                        "addressDetails": {
                            "country": {
                                "scheme": "iso-alpha2",
                                "id": "MD",
                                "description": "description of country",
                                "uri": "URI*"
                            },
                            "region": {
                                "scheme": "CUATM",
                                "id": "0301000",
                                "description": "description",
                                "uri": "URI*"
                            },
                            "locality": {
                                "scheme": "CUATM",
                                "id": "0301000",
                                "description": ""
                            }
                        }
                    },
                    "identifier": {
                        "scheme": "UA-MFO",
                        "id": "300711"
                    },
                    "accountIdentification": {
                        "scheme": "IBAN",
                        "id": "2600000625637"
                    },
                    "additionalAccountIdentifiers": [{
                        "scheme": "settlement",
                        "id": "458-9652"
                    }]
                }],
                "legalForm": {
                    "scheme": "MD-IDNO",
                    "id": "260000",
                    "description": "description",
                    "uri": "uri"
                }
            },
            "persones": [schema_person]
        }
    ]
}
