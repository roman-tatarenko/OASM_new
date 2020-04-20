import pytest


@pytest.fixture(scope='function')
def prepared_ac_for_registration(prepared_cpid, prepared_ac_ocid, prepared_ac_id, prepared_ev_ocid):
    return {
        "ocid": f"{prepared_ac_ocid}",
        "id": f"{prepared_ac_id}",
        "date": "2020-02-14T13:26:22Z",
        "tag": [
            "contractUpdate"
        ],
        "initiationType": "tender",
        "planning": {
            "implementation": {
                "transactions": [
                    {
                        "id": "274271d1-4f2d-11ea-9b59-d33f3073f231",
                        "type": "advance",
                        "value": {
                            "amount": 10,
                            "currency": "EUR"
                        },
                        "executionPeriod": {
                            "durationInDays": 100
                        },
                        "relatedContractMilestone": "55"
                    }
                ]
            },
            "budget": {
                "description": "описание",
                "budgetAllocation": [
                    {
                        "budgetBreakdownID": "ocds-t1s2t3-MD-1581430419141-FS-1581430428418",
                        "amount": 15,
                        "period": {
                            "startDate": "2020-02-02T00:00:00Z",
                            "endDate": "2020-03-01T00:00:00Z"
                        },
                        "relatedItem": "d3b39b04-1f12-48af-974d-e4f4e16a4d42"
                    }
                ],
                "budgetSource": [
                    {
                        "budgetBreakdownID": "ocds-t1s2t3-MD-1581430419141-FS-1581430428418",
                        "amount": 15,
                        "currency": "EUR"
                    }
                ]
            }
        },
        "tender": {
            "id": "ocds-t1s2t3-MD-1581683206878",
            "lots": [
                {
                    "id": "954de98b-5034-493d-af48-651f562b1510",
                    "title": "lots title",
                    "description": "lots description",
                    "placeOfPerformance": {
                        "address": {
                            "streetAddress": "placeOfPerformance streetAddress",
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
                                    "scheme": "locality scheme",
                                    "id": "locality id",
                                    "description": "locality description"
                                }
                            }
                        }
                    }
                }
            ],
            "classification": {
                "scheme": "CPV",
                "id": "15500000-3",
                "description": "Produse lactate"
            },
            "mainProcurementCategory": "goods",
            "procurementMethod": "open",
            "procurementMethodDetails": "TEST_microValue"
        },
        "awards": [
            {
                "id": "award",
                "description": "description of award",
                "date": "2020-02-14T12:54:26Z",
                "value": {
                    "amount": 20,
                    "currency": "EUR",
                    "amountNet": 10,
                    "valueAddedTaxIncluded": True
                },
                "suppliers": [
                    {
                        "id": "MD-IDNO-tenderers id5",
                        "name": "nam2"
                    }
                ],
                "items": [
                    {
                        "id": "d3b39b04-1f12-48af-974d-e4f4e16a4d42",
                        "description": "items description",
                        "classification": {
                            "scheme": "CPV",
                            "id": "15500000-3",
                            "description": "Produse lactate"
                        },
                        "additionalClassifications": [
                            {
                                "scheme": "CPVS",
                                "id": "AB06-7",
                                "description": "Plastic"
                            }
                        ],
                        "quantity": 10,
                        "unit": {
                            "name": "Metru cub consistent",
                            "value": {
                                "amount": 15,
                                "currency": "EUR",
                                "amountNet": 10,
                                "valueAddedTaxIncluded": True
                            },
                            "id": "121"
                        },
                        "deliveryAddress": {
                            "streetAddress": "street",
                            "postalCode": "45900",
                            "addressDetails": {
                                "country": {
                                    "scheme": "iso-alpha2",
                                    "id": "MD",
                                    "description": "MOLDOVA",
                                    "uri": "http://reference.iatistandard.org"
                                },
                                "region": {
                                    "scheme": "CUATM",
                                    "id": "0301000",
                                    "description": "mun.Bălţi",
                                    "uri": "http://statistica.md"
                                },
                                "locality": {
                                    "scheme": "other",
                                    "id": "450020",
                                    "description": "Khrystynivka"
                                }
                            }
                        },
                        "relatedLot": "954de98b-5034-493d-af48-651f562b1510"
                    }
                ],
                "documents": [
                    {
                        "id": "9004ab09-ca9b-4cb7-95f4-525a3bf64734-1574862409148",
                        "documentType": "contractSchedule",
                        "title": "title of doc",
                        "description": "description of doc",
                        "url": "http://dev.bpe.eprocurement.systems/api/v1/storage/get/9004ab09-ca9b-4cb7-95f4-525a3bf64734-1574862409148",
                        "datePublished": "2019-11-27T13:48:23Z",
                        "relatedLots": [
                            "954de98b-5034-493d-af48-651f562b1510"
                        ]
                    }
                ],
                "relatedLots": [
                    "954de98b-5034-493d-af48-651f562b1510"
                ]
            }
        ],
        "contracts": [
            {
                "id": f"{prepared_ac_ocid}",
                "date": "2020-02-14T13:23:56Z",
                "awardId": "909f7a8c-d487-45fc-a169-0d4ce3bb306c",
                "title": "title of contract",
                "description": "description of contract",
                "status": "pending",
                "statusDetails": "signed",
                "documents": [
                    {
                        "id": "9004ab09-ca9b-4cb7-95f4-525a3bf64734-1574862409148",
                        "documentType": "contractSigned",
                        "url": "http://dev.bpe.eprocurement.systems/api/v1/storage/get/9004ab09-ca9b-4cb7-95f4-525a3bf64734-1574862409148",
                        "datePublished": "2019-11-27T13:48:23Z",
                        "relatedConfirmations": [
                            "cs-tenderer-confirmation-on-9004ab09-ca9b-4cb7-95f4-525a3bf64734-1574862409148-4569123"
                        ]
                    },
                    {
                        "id": "9004ab09-ca9b-4cb7-95f4-525a3bf64734-1574862409148",
                        "documentType": "contractSigned",
                        "url": "http://dev.bpe.eprocurement.systems/api/v1/storage/get/9004ab09-ca9b-4cb7-95f4-525a3bf64734-1574862409148",
                        "datePublished": "2019-11-27T13:48:23Z",
                        "relatedConfirmations": [
                            "cs-buyer-confirmation-on-9004ab09-ca9b-4cb7-95f4-525a3bf64734-1574862409148-4569123"
                        ]
                    },
                    {
                        "id": "9004ab09-ca9b-4cb7-95f4-525a3bf64734-1574862409148",
                        "documentType": "contractNotice",
                        "title": "title of doc",
                        "description": "description of doc",
                        "url": "http://dev.bpe.eprocurement.systems/api/v1/storage/get/9004ab09-ca9b-4cb7-95f4-525a3bf64734-1574862409148",
                        "datePublished": "2019-11-27T13:48:23Z",
                        "relatedLots": [
                            "954de98b-5034-493d-af48-651f562b1510"
                        ]
                    },
                    {
                        "id": "3cef0168-3a87-4f83-8373-c8aa8105ee7d-1581686636286",
                        "documentType": "contractSigned",
                        "url": "http://dev.bpe.eprocurement.systems/api/v1/storage/get/3cef0168-3a87-4f83-8373-c8aa8105ee7d-1581686636286",
                        "datePublished": "2020-02-14T13:23:56Z"
                    }
                ],
                "period": {
                    "startDate": "2020-02-26T20:48:20Z",
                    "endDate": "2020-02-29T00:00:00Z"
                },
                "value": {
                    "amount": 20,
                    "currency": "EUR",
                    "amountNet": 10,
                    "valueAddedTaxIncluded": True
                },
                "agreedMetrics": [
                    {
                        "id": "cc-general",
                        "title": "Responsabilități generale",
                        "description": "Condiții contractuale care reglementează responsabilitățile generale legate de ambele părți",
                        "observations": [
                            {
                                "id": "cc-general-1-1",
                                "notes": "Nr. max. de zile pentru informarea prinvind invocarea forței majore",
                                "measure": "142",
                                "unit": {
                                    "id": "359",
                                    "name": "ziua",
                                    "scheme": "MD-CUMC"
                                }
                            },
                            {
                                "id": "cc-general-1-2",
                                "notes": "Nr. max. de pentru notificarea despre intenția de reziliere",
                                "measure": "15",
                                "unit": {
                                    "id": "359",
                                    "name": "ziua",
                                    "scheme": "MD-CUMC"
                                }
                            },
                            {
                                "id": "cc-general-1-3",
                                "notes": "Nr. max. de zile pentru răspunsul la notificarea despre intenția de reziliere",
                                "measure": "10",
                                "unit": {
                                    "id": "359",
                                    "name": "ziua",
                                    "scheme": "MD-CUMC"
                                }
                            }
                        ]
                    },
                    {
                        "id": "cc-tenderer-1",
                        "title": "Garanție de executare",
                        "description": "Condiții contractuale care reglementează responsabilitățile generale legate de operatorul economic în ceea ce privește garanția",
                        "observations": [
                            {
                                "id": "cc-tenderer-1-1",
                                "notes": "Cuantumul garanției",
                                "measure": "15",
                                "unit": {
                                    "id": "744",
                                    "name": "procent",
                                    "scheme": "MD-CUMC"
                                }
                            },
                            {
                                "id": "cc-tenderer-1-2",
                                "notes": "Forma de garanţie de bună executare a contractului",
                                "measure": "10000"
                            }
                        ]
                    },
                    {
                        "id": "cc-tenderer-2",
                        "title": "Termeni",
                        "description": "Condiții contractuale care reglementează responsabilitățile generale legate de EO în ceea ce privește calendarul",
                        "observations": [
                            {
                                "id": "cc-tenderer-2-1",
                                "notes": "Nr. max. de zile de la semnarea contractului pentru anunțarea Cumpărătorului despre disponibilitatea livrării Bunurilor şi/sau prestării Serviciilor",
                                "measure": "10000",
                                "unit": {
                                    "id": "359",
                                    "name": "ziua",
                                    "scheme": "MD-CUMC"
                                }
                            },
                            {
                                "id": "cc-tenderer-2-2",
                                "notes": "Nr. max. de zile pentru examinarea pretenţiilor înaintate privind calitatea bunurilor şi/sau serviciilor livrate",
                                "measure": "10000",
                                "unit": {
                                    "id": "359",
                                    "name": "ziua",
                                    "scheme": "MD-CUMC"
                                }
                            },
                            {
                                "id": "cc-tenderer-2-3",
                                "notes": "Nr. max. de zile pentru livrarea suplimentară în baza pretențiilor privind calitatea",
                                "measure": "10000",
                                "unit": {
                                    "id": "359",
                                    "name": "ziua",
                                    "scheme": "MD-CUMC"
                                }
                            },
                            {
                                "id": "cc-tenderer-2-4",
                                "notes": "Nr. de zile după care se consideră refuz de a vinde Bunurile/Serviciile/Lucrările contractate",
                                "measure": "10000",
                                "unit": {
                                    "id": "359",
                                    "name": "ziua",
                                    "scheme": "MD-CUMC"
                                }
                            }
                        ]
                    },
                    {
                        "id": "cc-tenderer-3",
                        "title": "Răspundere",
                        "description": "Condiții contractuale care reglementează responsabilitățile generale legate de furnizor în ceea ce privește răspunderea",
                        "observations": [
                            {
                                "id": "cc-tenderer-3-1",
                                "notes": "% de răspundere materială pentru livrarea cu întărziere",
                                "measure": "1000000",
                                "unit": {
                                    "id": "744",
                                    "name": "procent",
                                    "scheme": "MD-CUMC"
                                }
                            },
                            {
                                "id": "cc-tenderer-3-2",
                                "notes": "% maxim de răspundere materială a Vânzătorului în cazul livrării cu întârziere",
                                "measure": "1000000",
                                "unit": {
                                    "id": "744",
                                    "name": "procent",
                                    "scheme": "MD-CUMC"
                                }
                            },
                            {
                                "id": "cc-tenderer-3-3",
                                "notes": "% max. a penalității pentru refuzul executării contractului",
                                "measure": "1000000",
                                "unit": {
                                    "id": "744",
                                    "name": "procent",
                                    "scheme": "MD-CUMC"
                                }
                            }
                        ]
                    },
                    {
                        "id": "cc-buyer-1",
                        "title": "Termeni",
                        "description": "Condiții contractuale care reglementează responsabilitățile generale legate de entitatea contractantă în ceea ce privește calendarul",
                        "observations": [
                            {
                                "id": "cc-buyer-1-1",
                                "notes": "Nr. max. de zile pentru depunerea pretențiilor privind calitatea bunurilor şi/sau serviciilor livrate",
                                "measure": "1000000",
                                "unit": {
                                    "id": "359",
                                    "name": "ziua",
                                    "scheme": "MD-CUMC"
                                }
                            }
                        ]
                    },
                    {
                        "id": "cc-buyer-2",
                        "title": "Răspundere",
                        "description": "Condiții contractuale care reglementează responsabilitățile generale legate de entitatea contractantă privind răspunderea",
                        "observations": [
                            {
                                "id": "cc-buyer-2-1",
                                "notes": "% de răspundere materială a Beneficiarului in caz de achitare cu întârziere",
                                "measure": "1000000",
                                "unit": {
                                    "id": "744",
                                    "name": "procent",
                                    "scheme": "MD-CUMC"
                                }
                            },
                            {
                                "id": "cc-buyer-2-2",
                                "notes": "% răspundere materială maximă a Beneficiarului in caz de achitare cu întârziere",
                                "measure": "1000000",
                                "unit": {
                                    "id": "744",
                                    "name": "procent",
                                    "scheme": "MD-CUMC"
                                }
                            }
                        ]
                    },
                    {
                        "id": "cc-subject-909f7a8c-d487-45fc-a169-0d4ce3bb306c-d3b39b04-1f12-48af-974d-e4f4e16a4d42",
                        "title": "Specificație pentru items description",
                        "description": "Informații detaliate privind obiectul achiziției",
                        "observations": [
                            {
                                "id": "cc-subject-1",
                                "notes": "Modelul articolului",
                                "measure": "1000000"
                            },
                            {
                                "id": "cc-subject-2",
                                "notes": "Tara de origine",
                                "measure": "1000000"
                            },
                            {
                                "id": "cc-subject-3",
                                "notes": "Producător",
                                "measure": "1000000"
                            },
                            {
                                "id": "cc-subject-4",
                                "notes": "Specificația tehnică propusă de Furnizor",
                                "measure": "1000000"
                            },
                            {
                                "id": "cc-subject-5",
                                "notes": "Standarde de referință",
                                "measure": "1000000"
                            }
                        ]
                    }
                ],
                "milestones": [
                    {
                        "id": "delivery-MD-IDNO-tenderers id5-274271d0-4f2d-11ea-9b59-d33f3073f231",
                        "title": "title_000",
                        "description": "description_000",
                        "type": "delivery",
                        "status": "scheduled",
                        "relatedItems": [
                            "d3b39b04-1f12-48af-974d-e4f4e16a4d42"
                        ],
                        "additionalInformation": "дополнительная ифнормация должнаа изменяться",
                        "dueDate": "2020-10-28T00:00:00Z",
                        "relatedParties": [
                            {
                                "id": "MD-IDNO-tenderers id5",
                                "name": "nam2"
                            }
                        ]
                    },
                    {
                        "id": "approval-MD-IDNO-140aa80e0-4f2d-11ea-9b59-d33f3073f231",
                        "title": "Signature by the Buyer",
                        "description": "Buyer has to sign the contract",
                        "type": "approval",
                        "status": "met",
                        "relatedParties": [
                            {
                                "id": "MD-IDNO-1",
                                "name": "name of buyerei"
                            }
                        ],
                        "dateModified": "2020-02-14T13:25:08Z",
                        "dateMet": "2018-12-04T12:50:49Z"
                    },
                    {
                        "id": "approval-MD-IDNO-tenderers id540aaa7f0-4f2d-11ea-9b59-d33f3073f231",
                        "title": "Signature by the Supplier",
                        "description": "Supplier has to sign the contract",
                        "type": "approval",
                        "status": "met",
                        "relatedParties": [
                            {
                                "id": "MD-IDNO-tenderers id5",
                                "name": "nam2"
                            }
                        ],
                        "dateModified": "2020-02-14T13:26:22Z",
                        "dateMet": "2018-12-04T12:50:49Z"
                    },
                    {
                        "id": "approval-MD-IDNO-140aacf00-4f2d-11ea-9b59-d33f3073f231",
                        "title": "Contract activation",
                        "description": "Buyer has to activate the contract",
                        "type": "approval",
                        "status": "scheduled",
                        "relatedParties": [
                            {
                                "id": "MD-IDNO-1",
                                "name": "name of buyerei"
                            }
                        ]
                    },
                    {
                        "id": "approval-approveBodyId40aaf610-4f2d-11ea-9b59-d33f3073f231",
                        "title": "Contract validation",
                        "description": "Treasury has to approve the contract",
                        "type": "approval",
                        "status": "scheduled",
                        "relatedParties": [
                            {
                                "id": "approveBodyId",
                                "name": "approveBodyName"
                            }
                        ]
                    }
                ],
                "confirmationRequests": [
                    {
                        "id": "cs-buyer-confirmation-on-3cef0168-3a87-4f83-8373-c8aa8105ee7d-1581686636286",
                        "type": "digitalSignature",
                        "title": "Document signing",
                        "description": "Buyer has to sign the transferred document",
                        "relatesTo": "document",
                        "relatedItem": "3cef0168-3a87-4f83-8373-c8aa8105ee7d-1581686636286",
                        "source": "buyer",
                        "requestGroups": [
                            {
                                "id": "cs-buyer-confirmation-on-3cef0168-3a87-4f83-8373-c8aa8105ee7d-1581686636286-1",
                                "requests": [
                                    {
                                        "id": "cs-buyer-confirmation-on-3cef0168-3a87-4f83-8373-c8aa8105ee7d-1581686636286-4569123",
                                        "title": "parties[role:buyer].persones[role:authority].name",
                                        "description": "Defined person has to sign the transferred document",
                                        "relatedPerson": {
                                            "id": "4569123",
                                            "name": "name"
                                        }
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "id": "cs-tenderer-confirmation-on-9004ab09-ca9b-4cb7-95f4-525a3bf64734-1574862409148",
                        "type": "digitalSignature",
                        "title": "Document signing",
                        "description": "Supplier has to sign the transferred document",
                        "relatesTo": "document",
                        "relatedItem": "9004ab09-ca9b-4cb7-95f4-525a3bf64734-1574862409148",
                        "source": "tenderer",
                        "requestGroups": [
                            {
                                "id": "cs-tenderer-confirmation-on-9004ab09-ca9b-4cb7-95f4-525a3bf64734-1574862409148-tenderers id5",
                                "requests": [
                                    {
                                        "id": "cs-tenderer-confirmation-on-9004ab09-ca9b-4cb7-95f4-525a3bf64734-1574862409148-4569123",
                                        "title": "parties[role:supplier].persones[role:authority].name",
                                        "description": "Supplier has to sign the transferred document",
                                        "relatedPerson": {
                                            "id": "4569123",
                                            "name": "name"
                                        }
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "id": "cs-approveBody-confirmation-on-9004ab09-ca9b-4cb7-95f4-525a3bf64734-1574862409148",
                        "type": "outsideAction",
                        "title": "Document approving",
                        "description": "TEST",
                        "relatesTo": "document",
                        "relatedItem": "9004ab09-ca9b-4cb7-95f4-525a3bf64734-1574862409148",
                        "source": "approveBody",
                        "requestGroups": [
                            {
                                "id": "TEST",
                                "requests": [
                                    {
                                        "id": "cs-approveBody-confirmation-on-9004ab09-ca9b-4cb7-95f4-525a3bf64734-1574862409148-approveBodyID",
                                        "title": "TEST",
                                        "description": "TEST"
                                    }
                                ]
                            }
                        ]
                    }
                ],
                "confirmationResponses": [
                    {
                        "id": "cs-tenderer-confirmation-on-9004ab09-ca9b-4cb7-95f4-525a3bf64734-1574862409148-4569123",
                        "value": {
                            "name": "nam2",
                            "id": "MD-IDNO-tenderers id5",
                            "date": "2018-12-04T12:50:49Z",
                            "relatedPerson": {
                                "id": "4569123",
                                "name": "name"
                            },
                            "verification": [
                                {
                                    "type": "document",
                                    "value": "9004ab09-ca9b-4cb7-95f4-525a3bf64734-1574862409148",
                                    "rationale": "Acest document se semnează electronic în conformitate cu Legea nr. 91 din 29.05.2014. Verificarea semnăturii poate fi realizată la adresa https://msign.gov.md"
                                }
                            ]
                        },
                        "request": "cs-tenderer-confirmation-on-9004ab09-ca9b-4cb7-95f4-525a3bf64734-1574862409148-4569123"
                    },
                    {
                        "id": "cs-buyer-confirmation-on-9004ab09-ca9b-4cb7-95f4-525a3bf64734-1574862409148-4569123",
                        "value": {
                            "name": "name of buyerei",
                            "id": "MD-IDNO-1",
                            "date": "2018-12-04T12:50:49Z",
                            "relatedPerson": {
                                "id": "4569123",
                                "name": "name"
                            },
                            "verification": [
                                {
                                    "type": "document",
                                    "value": "9004ab09-ca9b-4cb7-95f4-525a3bf64734-1574862409148",
                                    "rationale": "Acest document se semnează electronic în conformitate cu Legea nr. 91 din 29.05.2014. Verificarea semnăturii poate fi realizată la adresa https://msign.gov.md"
                                }
                            ]
                        },
                        "request": "cs-buyer-confirmation-on-3cef0168-3a87-4f83-8373-c8aa8105ee7d-1581686636286-4569123"
                    }
                ]
            }
        ],
        "parties": [
            {
                "id": "MD-IDNO-1",
                "name": "name of buyerei",
                "identifier": {
                    "scheme": "MD-IDNO",
                    "id": "1",
                    "legalName": "identifier/legal name",
                    "uri": "uri"
                },
                "address": {
                    "streetAddress": "street address",
                    "addressDetails": {
                        "country": {
                            "scheme": "iso-alpha2",
                            "id": "MD",
                            "description": "MOLDOVA",
                            "uri": "http://reference.iatistandard.org"
                        },
                        "region": {
                            "scheme": "CUATM",
                            "id": "0101000",
                            "description": "mun.Chişinău",
                            "uri": "http://statistica.md"
                        },
                        "locality": {
                            "scheme": "other",
                            "id": "localityid",
                            "description": "locality/description"
                        }
                    }
                },
                "additionalIdentifiers": [
                    {
                        "scheme": "MD-IDNO",
                        "id": "123650008",
                        "legalName": "LN",
                        "uri": "http://hrystynivka.miskrada.org.ua/"
                    },
                    {
                        "scheme": "MD-BRANCHES",
                        "id": "8888",
                        "legalName": "Legal Name666",
                        "uri": "http://hrystynivka.miskrada.org.ua/"
                    }
                ],
                "contactPoint": {
                    "name": "contactPoint/name",
                    "email": "contactPoint/email",
                    "telephone": "contactPoint/456-95-96",
                    "faxNumber": "fax-number",
                    "url": "url"
                },
                "details": {
                    "typeOfBuyer": "NATIONAL_AGENCY",
                    "mainGeneralActivity": "GENERAL_PUBLIC_SERVICES",
                    "mainSectoralActivity": "WATER",
                    "permits": [
                        {
                            "id": "id546",
                            "scheme": "SRLE",
                            "url": "url",
                            "permitDetails": {
                                "issuedBy": {
                                    "id": "id",
                                    "name": "name"
                                },
                                "issuedThought": {
                                    "id": "1",
                                    "name": "name"
                                },
                                "validityPeriod": {
                                    "startDate": "2019-10-10T00:00:00Z",
                                    "endDate": "2019-11-10T00:00:00Z"
                                }
                            }
                        }
                    ],
                    "bankAccounts": [
                        {
                            "description": "description",
                            "bankName": "MBank",
                            "address": {
                                "streetAddress": "address of pe",
                                "postalCode": "10205",
                                "addressDetails": {
                                    "country": {
                                        "scheme": "iso-alpha2",
                                        "id": "MD",
                                        "description": "republic of Moldova",
                                        "uri": "http://hrystynivka.miskrada.org.ua/"
                                    },
                                    "region": {
                                        "scheme": "CUATM",
                                        "id": "1000000",
                                        "description": "Anenii Noi",
                                        "uri": "http://hrystynivka.miskrada.org.ua/"
                                    },
                                    "locality": {
                                        "scheme": "666",
                                        "id": "666",
                                        "description": "666",
                                        "uri": "http://hrystynivka.miskrada.org.ua/"
                                    }
                                }
                            },
                            "identifier": {
                                "id": "300711",
                                "scheme": "MD-BANKS"
                            },
                            "accountIdentification": {
                                "id": "2600000625637",
                                "scheme": "MD-IBAN"
                            },
                            "additionalAccountIdentifiers": [
                                {
                                    "id": "456654",
                                    "scheme": "MD-SETTLEMENT"
                                }
                            ]
                        }
                    ],
                    "legalForm": {
                        "id": "654",
                        "scheme": "MD-IDNO",
                        "description": "desc",
                        "uri": "http://hrystynivka.miskrada.org.ua/"
                    }
                },
                "persones": [
                    {
                        "title": "title",
                        "name": "name",
                        "identifier": {
                            "scheme": "MD-IDNO",
                            "id": "4569123",
                            "uri": "http://hrystynivka.miskrada.org.ua/"
                        },
                        "businessFunctions": [
                            {
                                "id": "456921",
                                "type": "authority",
                                "jobTitle": "Chief Executive Officer",
                                "period": {
                                    "startDate": "2018-11-20T00:00:00Z"
                                },
                                "documents": [
                                    {
                                        "id": "9004ab09-ca9b-4cb7-95f4-525a3bf64734-1574862409148",
                                        "documentType": "regulatoryDocument",
                                        "title": "title of doc",
                                        "description": "description of doc",
                                        "url": "http://dev.bpe.eprocurement.systems/api/v1/storage/get/9004ab09-ca9b-4cb7-95f4-525a3bf64734-1574862409148",
                                        "datePublished": "2019-11-27T13:48:23Z"
                                    }
                                ]
                            }
                        ]
                    }
                ],
                "roles": [
                    "buyer"
                ]
            },
            {
                "id": "MD-IDNO-tenderersid",
                "name": "nam2",
                "identifier": {
                    "scheme": "MD-IDNO",
                    "id": "tenderers id5",
                    "legalName": "tenderers legalname",
                    "uri": "http://tenderers.com"
                },
                "address": {
                    "streetAddress": "tenderers adress",
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
                "additionalIdentifiers": [
                    {
                        "scheme": "MD-IDNO",
                        "id": "555555",
                        "legalName": "Legal Name",
                        "uri": "http://hrystynivka.miskrada.org.ua/"
                    },
                    {
                        "scheme": "MD-BRANCHES",
                        "id": "6666",
                        "legalName": "Legal Name1",
                        "uri": "http://hrystynivka.miskrada.org.ua/"
                    }
                ],
                "contactPoint": {
                    "name": "Illia Petrusenko",
                    "email": "illya.petrusenko@gmail.com",
                    "telephone": "+380632074071",
                    "faxNumber": "+380445450099",
                    "url": "http://petrusenko.com/illia"
                },
                "details": {
                    "typeOfSupplier": "type of Supplier",
                    "mainEconomicActivities": [
                        "456-00-777"
                    ],
                    "permits": [
                        {
                            "id": "1234",
                            "scheme": "MD-IDNO",
                            "url": "4",
                            "permitDetails": {
                                "issuedBy": {
                                    "id": "125-MD-IDDNO",
                                    "name": "vasia pupkin"
                                },
                                "issuedThought": {
                                    "id": "id123",
                                    "name": "sasha tsytrus"
                                },
                                "validityPeriod": {
                                    "startDate": "2018-12-05T00:00:00Z",
                                    "endDate": "2018-12-15T00:00:00Z"
                                }
                            }
                        }
                    ],
                    "bankAccounts": [
                        {
                            "description": "description",
                            "bankName": "bankName",
                            "address": {
                                "streetAddress": "Chornovola",
                                "postalCode": "20000",
                                "addressDetails": {
                                    "country": {
                                        "scheme": "iso-alpha2",
                                        "id": "MD",
                                        "description": "Khrystynivka",
                                        "uri": "http://hrystynivka.miskrada.org.ua/*"
                                    },
                                    "region": {
                                        "scheme": "CUATM",
                                        "id": "0301000",
                                        "description": "Khrystynivka",
                                        "uri": "http://hrystynivka.miskrada.org.ua/*"
                                    },
                                    "locality": {
                                        "scheme": "CUATM",
                                        "id": "0301000",
                                        "description": "Khrystynivka",
                                        "uri": "http://hrystynivka.miskrada.org.ua/"
                                    }
                                }
                            },
                            "identifier": {
                                "id": "300711",
                                "scheme": "MD-MFO"
                            },
                            "accountIdentification": {
                                "id": "2600000625637",
                                "scheme": "IBAN"
                            },
                            "additionalAccountIdentifiers": [
                                {
                                    "id": "458-9652",
                                    "scheme": "settlement"
                                }
                            ]
                        }
                    ],
                    "legalForm": {
                        "id": "4592",
                        "scheme": "MD-IDNO",
                        "description": "description",
                        "uri": "http://hrystynivka.miskrada.org.ua/"
                    },
                    "scale": "large"
                },
                "persones": [
                    {
                        "title": "title",
                        "name": "name",
                        "identifier": {
                            "scheme": "MD-IDNO",
                            "id": "4569123",
                            "uri": "http://hrystynivka.miskrada.org.ua/"
                        },
                        "businessFunctions": [
                            {
                                "id": "1234",
                                "type": "authority",
                                "jobTitle": "Chief Executive Officer",
                                "period": {
                                    "startDate": "2018-11-20T00:00:00Z"
                                },
                                "documents": [
                                    {
                                        "id": "9004ab09-ca9b-4cb7-95f4-525a3bf64734-1574862409148",
                                        "documentType": "regulatoryDocument",
                                        "title": "title of doc",
                                        "description": "description",
                                        "url": "http://dev.bpe.eprocurement.systems/api/v1/storage/get/9004ab09-ca9b-4cb7-95f4-525a3bf64734-1574862409148",
                                        "datePublished": "2019-11-27T13:48:23Z"
                                    }
                                ]
                            }
                        ]
                    }
                ],
                "roles": [
                    "supplier",
                    "payee"
                ]
            },
            {
                "id": "MD-IDNO-123456789000",
                "name": "Payer's Name",
                "identifier": {
                    "scheme": "MD-IDNO",
                    "id": "123456789000",
                    "legalName": "Legal Name",
                    "uri": "http://454.to"
                },
                "address": {
                    "streetAddress": "street",
                    "postalCode": "785412",
                    "addressDetails": {
                        "country": {
                            "scheme": "iso-alpha2",
                            "id": "MD",
                            "description": "MOLDOVA",
                            "uri": "http://reference.iatistandard.org"
                        },
                        "region": {
                            "scheme": "CUATM",
                            "id": "3400000",
                            "description": "Donduşeni",
                            "uri": "http://statistica.md"
                        },
                        "locality": {
                            "scheme": "CUATM",
                            "id": "3401000",
                            "description": "or.Donduşeni (r-l Donduşeni)",
                            "uri": "http://statistica.md"
                        }
                    }
                },
                "additionalIdentifiers": [
                    {
                        "scheme": "MD-K",
                        "id": "additional identifier",
                        "legalName": "legalname",
                        "uri": "http://k.to"
                    }
                ],
                "contactPoint": {
                    "name": "contact person",
                    "email": "string@mail.ccc",
                    "telephone": "98-79-87",
                    "faxNumber": "78-56-55",
                    "url": "http://url.com"
                },
                "roles": [
                    "payer"
                ]
            }
        ],
        "relatedProcesses": [
            {
                "id": "21f095d2-4f29-11ea-85b3-f5103b0c4234",
                "relationship": [
                    "x_evaluation"
                ],
                "scheme": "ocid",
                "identifier": f"{prepared_ev_ocid}",
                "uri": f"http://dev.public.eprocurement.systems/tenders/{prepared_cpid}/{prepared_ev_ocid}"
            },
            {
                "id": "21f095d0-4f29-11ea-85b3-f5103b0c4234",
                "relationship": [
                    "parent"
                ],
                "scheme": "ocid",
                "identifier": "ocds-t1s2t3-MD-1581683206878",
                "uri": "http://dev.public.eprocurement.systems/tenders/ocds-t1s2t3-MD-1581683206878/ocds-t1s2t3-MD-1581683206878"
            },
            {
                "id": "274c0ec0-4f2d-11ea-85b3-f5103b0c4234",
                "relationship": [
                    "x_fundingSource"
                ],
                "scheme": "ocid",
                "identifier": "ocds-t1s2t3-MD-1581683158951-FS-1581683184113",
                "uri": "http://dev.public.eprocurement.systems/budgets/ocds-t1s2t3-MD-1581683158951/ocds-t1s2t3-MD-1581683158951-FS-1581683184113"
            },
            {
                "id": "274cd210-4f2d-11ea-85b3-f5103b0c4234",
                "relationship": [
                    "x_expenditureItem"
                ],
                "scheme": "ocid",
                "identifier": "ocds-t1s2t3-MD-1581683158951",
                "uri": "http://dev.public.eprocurement.systems/budgets/ocds-t1s2t3-MD-1581683158951/ocds-t1s2t3-MD-1581683158951"
            }
        ]
    }


@pytest.fixture(scope='function')
def prepared_ev_for_registration(prepared_cpid, prepared_ev_id, prepared_ac_id, prepared_ev_ocid):
    return {
        "ocid": f"{prepared_ev_ocid}",
        "id": f"{prepared_ev_id}",
        "date": "2020-02-07T10:22:27Z",
        "tag": [
            "awardUpdate"
        ],
        "initiationType": "tender",
        "parties": [
            {
                "id": "MD-IDNO-tenderers id5",
                "name": "nam2",
                "identifier": {
                    "scheme": "MD-IDNO",
                    "id": "tenderers id5",
                    "legalName": "tenderers legalname",
                    "uri": "http://tenderers.com"
                },
                "address": {
                    "streetAddress": "tenderers adress",
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
                "additionalIdentifiers": [
                    {
                        "scheme": "MD-IDNO",
                        "id": "additionalIdentifiers id",
                        "legalName": "additionalIdentifiers legalName",
                        "uri": "http://additionalIdentifier.com"
                    }
                ],
                "contactPoint": {
                    "name": "Illia Petrusenko",
                    "email": "illya.petrusenko@gmail.com",
                    "telephone": "+380632074071",
                    "faxNumber": "+380445450099",
                    "url": "http://petrusenko.com/illia"
                },
                "details": {
                    "typeOfSupplier": "company",
                    "mainEconomicActivities": [
                        "456-00"
                    ],
                    "permits": [
                        {
                            "id": "2",
                            "scheme": "SRLE",
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
                                    "startDate": "2019-10-29T16:35:00Z",
                                    "endDate": "2019-10-29T16:36:00Z"
                                }
                            }
                        }
                    ],
                    "bankAccounts": [
                        {
                            "description": "description",
                            "bankName": "bankName",
                            "address": {
                                "streetAddress": "Steet",
                                "postalCode": "5",
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
                                        "description": "descr",
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
                                "id": "300711",
                                "scheme": "UA-MFO"
                            },
                            "accountIdentification": {
                                "id": "2600000625637",
                                "scheme": "IBAN"
                            },
                            "additionalAccountIdentifiers": [
                                {
                                    "id": "458-9652",
                                    "scheme": "settlement"
                                }
                            ]
                        }
                    ],
                    "legalForm": {
                        "id": "260000",
                        "scheme": "MD-IDNO",
                        "description": "description",
                        "uri": "uri"
                    },
                    "scale": "sme"
                },
                "persones": [
                    {
                        "title": "persones.title",
                        "name": "persones.name",
                        "identifier": {
                            "scheme": "MD-IDNO",
                            "id": "88888000",
                            "uri": "http://petrusenko.com/illia"
                        },
                        "businessFunctions": [
                            {
                                "id": "businessFunctions id",
                                "type": "authority",
                                "jobTitle": "Chief Executive Officer",
                                "period": {
                                    "startDate": "2019-10-30T00:00:35Z"
                                },
                                "documents": [
                                    {
                                        "id": "9004ab09-ca9b-4cb7-95f4-525a3bf64734-1574862409148",
                                        "documentType": "regulatoryDocument",
                                        "title": "doc title",
                                        "description": "doc description",
                                        "url": "http://dev.bpe.eprocurement.systems/api/v1/storage/get/9004ab09-ca9b-4cb7-95f4-525a3bf64734-1574862409148",
                                        "datePublished": "2019-11-27T13:48:23Z"
                                    }
                                ]
                            }
                        ]
                    }
                ],
                "roles": [
                    "tenderer",
                    "supplier"
                ]
            }
        ],
        "tender": {
            "id": "ocds-t1s2t3-MD-1581070591188",
            "title": "Evaluation",
            "description": "Evaluation stage of contracting process",
            "status": "active",
            "statusDetails": "awarding",
            "criteria": [
                {
                    "id": "852d3adc-a245-4b86-9e43-e694e1bf2740",
                    "title": "",
                    "source": "procuringEntity",
                    "description": "",
                    "requirementGroups": [
                        {
                            "id": "68f8a408-e15f-4271-83c4-58d20d57dfe5",
                            "requirements": [
                                {
                                    "id": "004e1ed2-2d7c-4ed7-b671-d324f41cca03",
                                    "title": "",
                                    "dataType": "boolean"
                                }
                            ]
                        }
                    ],
                    "relatesTo": "award"
                }
            ],
            "items": [
                {
                    "id": "6733055d-9a88-4b90-8eee-c99a03ce3acd",
                    "description": "items description",
                    "classification": {
                        "scheme": "CPV",
                        "id": "15500000-3",
                        "description": "Produse lactate"
                    },
                    "additionalClassifications": [
                        {
                            "scheme": "CPVS",
                            "id": "AB06-7",
                            "description": "Plastic"
                        }
                    ],
                    "quantity": 1,
                    "unit": {
                        "name": "Metru cub consistent",
                        "id": "121"
                    },
                    "relatedLot": "36133175-8f63-4763-a1dd-b1d16b551453"
                }
            ],
            "lots": [
                {
                    "id": "36133175-8f63-4763-a1dd-b1d16b551453",
                    "title": "lots title",
                    "description": "lots description",
                    "status": "active",
                    "statusDetails": "awarded",
                    "value": {
                        "amount": 10,
                        "currency": "EUR"
                    },
                    "options": [
                        {
                            "hasOptions": False
                        }
                    ],
                    "recurrentProcurement": [
                        {
                            "isRecurrent": False
                        }
                    ],
                    "renewals": [
                        {
                            "hasRenewals": False
                        }
                    ],
                    "variants": [
                        {
                            "hasVariants": False
                        }
                    ],
                    "contractPeriod": {
                        "startDate": "2020-02-10T10:30:40Z",
                        "endDate": "2020-03-30T10:30:40Z"
                    },
                    "placeOfPerformance": {
                        "address": {
                            "streetAddress": "placeOfPerformance streetAddress",
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
                                    "scheme": "locality scheme",
                                    "id": "locality id",
                                    "description": "locality description"
                                }
                            }
                        }
                    }
                }
            ],
            "lotGroups": [
                {
                    "optionToCombine": False
                }
            ],
            "tenderPeriod": {
                "startDate": "2020-02-07T10:19:23Z",
                "endDate": "2020-02-07T10:20:23Z"
            },
            "enquiryPeriod": {
                "startDate": "2020-02-07T10:17:23Z",
                "endDate": "2020-02-07T10:19:23Z"
            },
            "awardPeriod": {
                "startDate": "2020-02-07T10:20:23Z"
            },
            "hasEnquiries": False,
            "documents": [
                {
                    "id": "9004ab09-ca9b-4cb7-95f4-525a3bf64734-1574862409148",
                    "documentType": "billOfQuantity",
                    "title": "doc1т",
                    "url": "http://dev.bpe.eprocurement.systems/api/v1/storage/get/9004ab09-ca9b-4cb7-95f4-525a3bf64734-1574862409148",
                    "datePublished": "2019-11-27T13:48:23Z"
                }
            ],
            "awardCriteria": "priceOnly",
            "awardCriteriaDetails": "automated",
            "submissionMethod": [
                "electronicSubmission"
            ],
            "submissionMethodDetails": "Lista platformelor: achizitii, ebs, licitatie, yptender",
            "submissionMethodRationale": [
                "Ofertele vor fi primite prin intermediul unei platforme electronice de achiziții publice"
            ],
            "requiresElectronicCatalogue": False
        },
        "awards": [
            {
                "id": "3c7faff8-6123-4862-a7ff-04875ca4b767",
                "description": "description",
                "status": "pending",
                "statusDetails": "active",
                "date": "2020-02-07T10:21:04Z",
                "value": {
                    "amount": 0.65,
                    "currency": "EUR"
                },
                "suppliers": [
                    {
                        "id": "MD-IDNO-tenderers id5",
                        "name": "nam2"
                    }
                ],
                "documents": [
                    {
                        "id": "9004ab09-ca9b-4cb7-95f4-525a3bf64734-1574862409148",
                        "documentType": "evaluationReports",
                        "title": "doctitle",
                        "description": "description",
                        "url": "http://dev.bpe.eprocurement.systems/api/v1/storage/get/9004ab09-ca9b-4cb7-95f4-525a3bf64734-1574862409148",
                        "datePublished": "2019-11-27T13:48:23Z"
                    }
                ],
                "relatedLots": [
                    "36133175-8f63-4763-a1dd-b1d16b551453"
                ],
                "relatedBid": "40d2b509-bff5-4d54-a98e-1c952d5adecd"
            }
        ],
        "bids": {
            "details": [
                {
                    "id": "40d2b509-bff5-4d54-a98e-1c952d5adecd",
                    "date": "2020-02-07T10:19:26Z",
                    "status": "pending",
                    "statusDetails": "valid",
                    "tenderers": [
                        {
                            "id": "MD-IDNO-tenderers id5",
                            "name": "nam2"
                        }
                    ],
                    "value": {
                        "amount": 0.65,
                        "currency": "EUR"
                    },
                    "documents": [
                        {
                            "id": "b5494aa9-578a-4f3b-a21d-cf4546374cef-1578921285987",
                            "documentType": "submissionDocuments",
                            "title": "doc title",
                            "description": "doc description",
                            "url": "http://dev.bpe.eprocurement.systems/api/v1/storage/get/b5494aa9-578a-4f3b-a21d-cf4546374cef-1578921285987",
                            "datePublished": "2020-01-13T13:51:49Z"
                        }
                    ],
                    "relatedLots": [
                        "36133175-8f63-4763-a1dd-b1d16b551453"
                    ]
                }
            ]
        },
        "contracts": [
            {
                "id": "848a5f27-2159-46af-aff1-82728af1ced4",
                "date": "2020-02-07T10:21:50Z",
                "awardId": "3c7faff8-6123-4862-a7ff-04875ca4b767",
                "relatedLots": [
                    "36133175-8f63-4763-a1dd-b1d16b551453"
                ],
                "status": "pending",
                "statusDetails": "active",
                "relatedProcesses": [
                    {
                        "id": "bd45f483-4993-11ea-85b3-f5103b0c4234",
                        "relationship": [
                            "x_contracting"
                        ],
                        "scheme": "ocid",
                        "identifier": "ocds-t1s2t3-MD-1581070591188-AC-1581816477249",
                        "uri": "http://dev.public.eprocurement.systems/tenders/ocds-t1s2t3-MD-1581070591188/ocds-t1s2t3-MD-1581070591188-AC-1581816477249"
                    }
                ]
            }
        ],
        "hasPreviousNotice": True,
        "purposeOfNotice": {
            "isACallForCompetition": True
        },
        "relatedProcesses": [
            {
                "id": "08af2e61-4993-11ea-85b3-f5103b0c4234",
                "relationship": [
                    "planning"
                ],
                "scheme": "ocid",
                "identifier": "ocds-t1s2t3-MD-1581070591188-PN-1581070591216",
                "uri": "http://dev.public.eprocurement.systems/tenders/ocds-t1s2t3-MD-1581070591188/ocds-t1s2t3-MD-1581070591188-PN-1581070591216"
            },
            {
                "id": "e90c1f03-4992-11ea-85b3-f5103b0c4234",
                "relationship": [
                    "parent"
                ],
                "scheme": "ocid",
                "identifier": "ocds-t1s2t3-MD-1581070591188",
                "uri": "http://dev.public.eprocurement.systems/tenders/ocds-t1s2t3-MD-1581070591188/ocds-t1s2t3-MD-1581070591188"
            }
        ]
    }


@pytest.fixture(scope='function')
def prepared_record(prepared_cpid, prepared_ac_ocid, prepared_request_id):
    from uuid import uuid4
    return {
        "id": f"{uuid4()}",
        "command": "sendAcForVerification",
        "context": {
            "operationId": f"{uuid4()}",
            "requestId": f"{prepared_request_id}",
            "cpid": f"{prepared_cpid}",
            "ocid": f"{prepared_ac_ocid}",
            "stage": "AC",
            "prevStage": "AC",
            "processType": "supplierSigningAC",
            "operationType": "supplierSigningAC",
            "phase": "signed",
            "owner": "445f6851-c908-407d-9b45-14b92f3e964b",
            "country": "RU",
            "language": "ro",
            "pmd": "pmd",
            "token": "b31d35ed-1412-4a3d-a1ed-a3983031f23a",
            "startDate": "2020-02-11T14:18:26Z",
            "id": "cs-tenderer-confirmation-on--888-999-000",
            "timeStamp": 1581430706042,
            "isAuction": False
        },
        "data": {
            "ocid": f"{prepared_ac_ocid}",
            "cpid": f"{prepared_cpid}",
            "treasuryBudgetSources": [{
                "budgetBreakdownID": "ocds-t1s2t3-MD-1581430419141-FS-1581430428418",
                "budgetIBAN": "000000001",
                "amount": 100000.00
            }
            ]},
        "version": "0.0.1"
    }


@pytest.fixture(scope='function')
def prepared_create_amendment():
    return {
        "id": "AMENDMENT_ID",
        "date": "2019-04-01T10:00:00Z",
        "rationale": "Some_text",
        "description": "Some_text_2",
        "status": "pending",
        "type": "cancellation",
        "relatesTo": "RELATES_TO",
        "relatedItem": "RELATED_ITEM",
        "documents": [{
            "documentType": "cancellationDetails",
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "title": "string",
            "description": "string"
        }],
        "token": "ed8e86b9-82c9-4bcc-ac40-215317afa211",
        "owner": "3fa85f64-5717-4562-b3fc-2c963f66afa6"

    }


@pytest.fixture(scope='function')
def data_tender():
    return {
        "ocid": "OCID",
        "planning": {
            "rationale": "reason for budget",
            "budget": {
                "description": "budgetBreakdown/description",
                "amount": {
                    "amount": 15.00,
                    "currency": "EUR"
                },
                "isEuropeanUnionFunded": True,
                "budgetBreakdown": [{
                    "id": "ocds-t1s2t3-MD-1580832122842-FS-1581070108536",
                    "description": "description",
                    "amount": {
                        "amount": 15.00,
                        "currency": "EUR"
                    },
                    "period": {
                        "startDate": "2020-02-01T11:07:00Z",
                        "endDate": "2020-12-01T00:00:00Z"
                    },
                    "sourceParty": {
                        "id": "MD-IDNO-1",
                        "name": "name of buyerei"
                    },
                    "europeanUnionFunding": {
                        "projectIdentifier": "projectIdentifier",
                        "projectName": "Name of this project",
                        "uri": "http://uriuri.th"
                    }
                }]
            }
        },
        "tender": {
            "id": "84bbb5ad-2da9-43d5-a0a3-9635c48c1bbc",
            "status": "active",
            "statusDetails": "clarification",
            "title": "title of tender",
            "description": "desription of tender",
            "classification": {
                "scheme": "CPV",
                "description": "Produse lactate",
                "id": "15500000-3"
            },
            "tenderPeriod": {
                "startDate": "2020-02-20T13:45:07Z",
                "endDate": "2020-02-20T13:50:07Z"
            },
            "enquiryPeriod": {
                "startDate": "2020-02-20T13:40:07Z",
                "endDate": "2020-02-20T13:45:07Z"
            },
            "acceleratedProcedure": {
                "isAcceleratedProcedure": False
            },
            "designContest": {
                "serviceContractAward": False
            },
            "electronicWorkflows": {
                "useOrdering": False,
                "usePayment": False,
                "acceptInvoicing": False
            },
            "jointProcurement": {
                "isJointProcurement": False
            },
            "procedureOutsourcing": {
                "procedureOutsourced": False
            },
            "framework": {
                "isAFramework": False
            },
            "dynamicPurchasingSystem": {
                "hasDynamicPurchasingSystem": False
            },
            "legalBasis": "REGULATION_966_2012",
            "procurementMethod": "open",
            "procurementMethodDetails": "TEST_microValue",
            "mainProcurementCategory": "goods",
            "eligibilityCriteria": "Regulile generale privind naționalitatea și originea, precum și alte criterii de eligibilitate sunt enumerate în Ghidul practic privind procedurile de contractare a acțiunilor externe ale UE (PRAG)",
            "contractPeriod": {
                "startDate": "2020-02-29T10:30:40Z",
                "endDate": "2020-03-30T10:30:40Z"
            },
            "procuringEntity": {
                "id": "MD-IDNO-12",
                "name": "name of procuringEntity",
                "identifier": {
                    "scheme": "MD-IDNO",
                    "id": "12",
                    "legalName": "identifier/legal name2",
                    "uri": "uri"
                },
                "additionalIdentifiers": [{
                    "scheme": "md-idno",
                    "id": "445521",
                    "legalName": "legalName",
                    "uri": "uri"
                }],
                "address": {
                    "streetAddress": "street address",
                    "addressDetails": {
                        "country": {
                            "scheme": "iso-alpha2",
                            "id": "MD",
                            "description": "MOLDOVA",
                            "uri": "http://reference.iatistandard.org"
                        },
                        "region": {
                            "scheme": "CUATM",
                            "id": "0101000",
                            "description": "mun.Chişinău",
                            "uri": "http://statistica.md"
                        },
                        "locality": {
                            "scheme": "other",
                            "id": "localityid",
                            "description": "locality/description"
                        }
                    }
                },
                "contactPoint": {
                    "name": "contactPoint/name",
                    "email": "contactPoint/email",
                    "telephone": "contactPoint/456-95-96",
                    "faxNumber": "fax-number",
                    "url": "url"
                },
                "persones": [{
                    "title": "persones.title",
                    "name": "persones.name",
                    "identifier": {
                        "scheme": "MD-IDNO",
                        "id": "88888000",
                        "uri": "http://petrusenko.com/illia"
                    },
                    "businessFunctions": [{
                        "id": "businessFunctions id",
                        "type": "chairman",
                        "jobTitle": "Chief Executive Officer",
                        "period": {
                            "startDate": "2019-10-30T00:00:35Z"
                        }
                    }]
                }]
            },
            "value": {
                "amount": 10.00,
                "currency": "EUR"
            },
            "lotGroups": [{
                "optionToCombine": False
            }],
            "lots": [{
                "id": "3ce7a92d-d504-4529-89c0-abab2e30bd6b",
                "title": "lots title",
                "description": "lots description",
                "status": "active",
                "statusDetails": "empty",
                "value": {
                    "amount": 10.00,
                    "currency": "EUR"
                },
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
                    "startDate": "2020-02-29T10:30:40Z",
                    "endDate": "2020-03-30T10:30:40Z"
                },
                "placeOfPerformance": {
                    "address": {
                        "streetAddress": "placeOfPerformance streetAddress",
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
                                "scheme": "locality scheme",
                                "id": "locality id",
                                "description": "locality description"
                            }
                        }
                    }
                }
            }],
            "items": [{
                "id": "700b19b0-5756-4b25-b0c4-9e4522d1e12f",
                "classification": {
                    "scheme": "CPV",
                    "description": "Produse lactate",
                    "id": "15500000-3"
                },
                "additionalClassifications": [{
                    "scheme": "CPVS",
                    "description": "Plastic",
                    "id": "AB06-7"
                }],
                "quantity": 1.000,
                "unit": {
                    "id": "121",
                    "name": "Metru cub consistent"
                },
                "description": "items description",
                "relatedLot": "3ce7a92d-d504-4529-89c0-abab2e30bd6b"
            }],
            "awardCriteria": "priceOnly",
            "awardCriteriaDetails": "automated",
            "requiresElectronicCatalogue": False,
            "submissionMethod": ["electronicSubmission"],
            "submissionMethodRationale": [
                "Ofertele vor fi primite prin intermediul unei platforme electronice de achiziții publice"],
            "submissionMethodDetails": "Lista platformelor: achizitii, ebs, licitatie, yptender",
            "documents": [{
                "id": "9004ab09-ca9b-4cb7-95f4-525a3bf64734-1574862409148",
                "documentType": "billOfQuantity",
                "title": "doc1т"
            }]
        }
    }


@pytest.fixture(scope='function')
def data_two_lots_and_items():
    return {
        "lots": [
            {
                "id": "3ce7a92d-d504-4529-89c0-abab2e30bd6b",
                "title": "lots title",
                "description": "lots description",
                "status": "STATUS",
                "statusDetails": "STATUS_DETAILS",
                "value": {
                    "amount": 10.00,
                    "currency": "EUR"
                },
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
                    "startDate": "2020-02-29T10:30:40Z",
                    "endDate": "2020-03-30T10:30:40Z"
                },
                "placeOfPerformance": {
                    "address": {
                        "streetAddress": "placeOfPerformance streetAddress",
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
                                "scheme": "locality scheme",
                                "id": "locality id",
                                "description": "locality description"
                            }
                        }
                    }
                }
            },
            {
                "id": "1ce7a82d-d504-4529-89c0-abab2e30bd6b",
                "title": "lots title",
                "description": "lots description",
                "status": "STATUS",
                "statusDetails": "STATUS_DETAILS",
                "value": {
                    "amount": 1.00,
                    "currency": "EUR"
                },
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
                    "startDate": "2020-02-29T10:30:40Z",
                    "endDate": "2020-03-30T10:30:40Z"
                },
                "placeOfPerformance": {
                    "address": {
                        "streetAddress": "placeOfPerformance streetAddress",
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
                                "scheme": "locality scheme",
                                "id": "locality id",
                                "description": "locality description"
                            }
                        }
                    }
                }
            }
        ],
        "items": [
            {
                "id": "700b19b0-5756-4b25-b0c4-9e4522d1e12f",
                "classification": {
                    "scheme": "CPV",
                    "description": "Produse lactate",
                    "id": "15500000-3"
                },
                "additionalClassifications": [{
                    "scheme": "CPVS",
                    "description": "Plastic",
                    "id": "AB06-7"
                }],
                "quantity": 1.000,
                "unit": {
                    "id": "121",
                    "name": "Metru cub consistent"
                },
                "description": "items description",
                "relatedLot": "3ce7a92d-d504-4529-89c0-abab2e30bd6b"
            },
            {
                "id": "2ce7a82d-d504-4529-89c0-abab2e30bd6b",
                "classification": {
                    "scheme": "CPV",
                    "description": "Produse lactate",
                    "id": "15500000-3"
                },
                "additionalClassifications": [{
                    "scheme": "CPVS",
                    "description": "Plastic",
                    "id": "AB06-7"
                }],
                "quantity": 1.000,
                "unit": {
                    "id": "121",
                    "name": "Metru cub consistent"
                },
                "description": "items description",
                "relatedLot": "1ce7a82d-d504-4529-89c0-abab2e30bd6b"
            }
        ]
    }


@pytest.fixture(scope='function')
def prepared_data_add_EV_before_SendAcForVerification(prepared_cpid, prepared_ev_ocid):
    return {
        "ocid": prepared_ev_ocid,
        "id": prepared_cpid,
        "date": "2020-02-07T10:22:27Z",
        "tag": [
            "awardUpdate"
        ],
        "initiationType": "tender",
        "parties": [
            {
                "id": "MD-IDNO-tenderers id5",
                "name": "nam2",
                "identifier": {
                    "scheme": "MD-IDNO",
                    "id": "tenderers id5",
                    "legalName": "tenderers legalname",
                    "uri": "http://tenderers.com"
                },
                "address": {
                    "streetAddress": "tenderers adress",
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
                "additionalIdentifiers": [
                    {
                        "scheme": "MD-IDNO",
                        "id": "additionalIdentifiers id",
                        "legalName": "additionalIdentifiers legalName",
                        "uri": "http://additionalIdentifier.com"
                    }
                ],
                "contactPoint": {
                    "name": "Illia Petrusenko",
                    "email": "illya.petrusenko@gmail.com",
                    "telephone": "+380632074071",
                    "faxNumber": "+380445450099",
                    "url": "http://petrusenko.com/illia"
                },
                "details": {
                    "typeOfSupplier": "company",
                    "mainEconomicActivities": [
                        "456-00"
                    ],
                    "permits": [
                        {
                            "id": "2",
                            "scheme": "SRLE",
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
                                    "startDate": "2019-10-29T16:35:00Z",
                                    "endDate": "2019-10-29T16:36:00Z"
                                }
                            }
                        }
                    ],
                    "bankAccounts": [
                        {
                            "description": "description",
                            "bankName": "bankName",
                            "address": {
                                "streetAddress": "Steet",
                                "postalCode": "5",
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
                                        "description": "descr",
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
                                "id": "300711",
                                "scheme": "UA-MFO"
                            },
                            "accountIdentification": {
                                "id": "2600000625637",
                                "scheme": "IBAN"
                            },
                            "additionalAccountIdentifiers": [
                                {
                                    "id": "458-9652",
                                    "scheme": "settlement"
                                }
                            ]
                        }
                    ],
                    "legalForm": {
                        "id": "260000",
                        "scheme": "MD-IDNO",
                        "description": "description",
                        "uri": "uri"
                    },
                    "scale": "sme"
                },
                "persones": [
                    {
                        "title": "persones.title",
                        "name": "persones.name",
                        "identifier": {
                            "scheme": "MD-IDNO",
                            "id": "88888000",
                            "uri": "http://petrusenko.com/illia"
                        },
                        "businessFunctions": [
                            {
                                "id": "businessFunctions id",
                                "type": "authority",
                                "jobTitle": "Chief Executive Officer",
                                "period": {
                                    "startDate": "2019-10-30T00:00:35Z"
                                },
                                "documents": [
                                    {
                                        "id": "9004ab09-ca9b-4cb7-95f4-525a3bf64734-1574862409148",
                                        "documentType": "regulatoryDocument",
                                        "title": "doc title",
                                        "description": "doc description",
                                        "url": "http://dev.bpe.eprocurement.systems/api/v1/storage/get/9004ab09-ca9b-4cb7-95f4-525a3bf64734-1574862409148",
                                        "datePublished": "2019-11-27T13:48:23Z"
                                    }
                                ]
                            }
                        ]
                    }
                ],
                "roles": [
                    "tenderer",
                    "supplier"
                ]
            }
        ],
        "tender": {
            "id": "ocds-t1s2t3-MD-1581070591188",
            "title": "Evaluation",
            "description": "Evaluation stage of contracting process",
            "status": "active",
            "statusDetails": "awarding",
            "criteria": [
                {
                    "id": "852d3adc-a245-4b86-9e43-e694e1bf2740",
                    "title": "",
                    "source": "procuringEntity",
                    "description": "",
                    "requirementGroups": [
                        {
                            "id": "68f8a408-e15f-4271-83c4-58d20d57dfe5",
                            "requirements": [
                                {
                                    "id": "004e1ed2-2d7c-4ed7-b671-d324f41cca03",
                                    "title": "",
                                    "dataType": "boolean"
                                }
                            ]
                        }
                    ],
                    "relatesTo": "award"
                }
            ],
            "items": [
                {
                    "id": "6733055d-9a88-4b90-8eee-c99a03ce3acd",
                    "description": "items description",
                    "classification": {
                        "scheme": "CPV",
                        "id": "15500000-3",
                        "description": "Produse lactate"
                    },
                    "additionalClassifications": [
                        {
                            "scheme": "CPVS",
                            "id": "AB06-7",
                            "description": "Plastic"
                        }
                    ],
                    "quantity": 1,
                    "unit": {
                        "name": "Metru cub consistent",
                        "id": "121"
                    },
                    "relatedLot": "36133175-8f63-4763-a1dd-b1d16b551453"
                }
            ],
            "lots": [
                {
                    "id": "36133175-8f63-4763-a1dd-b1d16b551453",
                    "title": "lots title",
                    "description": "lots description",
                    "status": "active",
                    "statusDetails": "awarded",
                    "value": {
                        "amount": 10,
                        "currency": "EUR"
                    },
                    "options": [
                        {
                            "hasOptions": False
                        }
                    ],
                    "recurrentProcurement": [
                        {
                            "isRecurrent": False
                        }
                    ],
                    "renewals": [
                        {
                            "hasRenewals": False
                        }
                    ],
                    "variants": [
                        {
                            "hasVariants": False
                        }
                    ],
                    "contractPeriod": {
                        "startDate": "2020-02-10T10:30:40Z",
                        "endDate": "2020-03-30T10:30:40Z"
                    },
                    "placeOfPerformance": {
                        "address": {
                            "streetAddress": "placeOfPerformance streetAddress",
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
                                    "scheme": "locality scheme",
                                    "id": "locality id",
                                    "description": "locality description"
                                }
                            }
                        }
                    }
                }
            ],
            "lotGroups": [
                {
                    "optionToCombine": False
                }
            ],
            "tenderPeriod": {
                "startDate": "2020-02-07T10:19:23Z",
                "endDate": "2020-02-07T10:20:23Z"
            },
            "enquiryPeriod": {
                "startDate": "2020-02-07T10:17:23Z",
                "endDate": "2020-02-07T10:19:23Z"
            },
            "awardPeriod": {
                "startDate": "2020-02-07T10:20:23Z"
            },
            "hasEnquiries": False,
            "documents": [
                {
                    "id": "9004ab09-ca9b-4cb7-95f4-525a3bf64734-1574862409148",
                    "documentType": "billOfQuantity",
                    "title": "doc1т",
                    "url": "http://dev.bpe.eprocurement.systems/api/v1/storage/get/9004ab09-ca9b-4cb7-95f4-525a3bf64734-1574862409148",
                    "datePublished": "2019-11-27T13:48:23Z"
                }
            ],
            "awardCriteria": "priceOnly",
            "awardCriteriaDetails": "automated",
            "submissionMethod": [
                "electronicSubmission"
            ],
            "submissionMethodDetails": "Lista platformelor: achizitii, ebs, licitatie, yptender",
            "submissionMethodRationale": [
                "Ofertele vor fi primite prin intermediul unei platforme electronice de achiziții publice"
            ],
            "requiresElectronicCatalogue": False
        },
        "awards": [
            {
                "id": "3c7faff8-6123-4862-a7ff-04875ca4b767",
                "description": "description",
                "status": "pending",
                "statusDetails": "active",
                "date": "2020-02-07T10:21:04Z",
                "value": {
                    "amount": 0.65,
                    "currency": "EUR"
                },
                "suppliers": [
                    {
                        "id": "MD-IDNO-tenderers id5",
                        "name": "nam2"
                    }
                ],
                "documents": [
                    {
                        "id": "9004ab09-ca9b-4cb7-95f4-525a3bf64734-1574862409148",
                        "documentType": "evaluationReports",
                        "title": "doctitle",
                        "description": "description",
                        "url": "http://dev.bpe.eprocurement.systems/api/v1/storage/get/9004ab09-ca9b-4cb7-95f4-525a3bf64734-1574862409148",
                        "datePublished": "2019-11-27T13:48:23Z"
                    }
                ],
                "relatedLots": [
                    "36133175-8f63-4763-a1dd-b1d16b551453"
                ],
                "relatedBid": "40d2b509-bff5-4d54-a98e-1c952d5adecd"
            }
        ],
        "bids": {
            "details": [
                {
                    "id": "40d2b509-bff5-4d54-a98e-1c952d5adecd",
                    "date": "2020-02-07T10:19:26Z",
                    "status": "pending",
                    "statusDetails": "valid",
                    "tenderers": [
                        {
                            "id": "MD-IDNO-tenderers id5",
                            "name": "nam2"
                        }
                    ],
                    "value": {
                        "amount": 0.65,
                        "currency": "EUR"
                    },
                    "documents": [
                        {
                            "id": "b5494aa9-578a-4f3b-a21d-cf4546374cef-1578921285987",
                            "documentType": "submissionDocuments",
                            "title": "doc title",
                            "description": "doc description",
                            "url": "http://dev.bpe.eprocurement.systems/api/v1/storage/get/b5494aa9-578a-4f3b-a21d-cf4546374cef-1578921285987",
                            "datePublished": "2020-01-13T13:51:49Z"
                        }
                    ],
                    "relatedLots": [
                        "36133175-8f63-4763-a1dd-b1d16b551453"
                    ]
                }
            ]
        },
        "contracts": [
            {
                "id": "848a5f27-2159-46af-aff1-82728af1ced4",
                "date": "2020-02-07T10:21:50Z",
                "awardId": "3c7faff8-6123-4862-a7ff-04875ca4b767",
                "relatedLots": [
                    "36133175-8f63-4763-a1dd-b1d16b551453"
                ],
                "status": "pending",
                "statusDetails": "active",
                "relatedProcesses": [
                    {
                        "id": "bd45f483-4993-11ea-85b3-f5103b0c4234",
                        "relationship": [
                            "x_contracting"
                        ],
                        "scheme": "ocid",
                        "identifier": "ocds-t1s2t3-MD-1581070591188-AC-1581816477249",
                        "uri": "http://dev.public.eprocurement.systems/tenders/ocds-t1s2t3-MD-1581070591188/ocds-t1s2t3-MD-1581070591188-AC-1581816477249"
                    }
                ]
            }
        ],
        "hasPreviousNotice": True,
        "purposeOfNotice": {
            "isACallForCompetition": True
        },
        "relatedProcesses": [
            {
                "id": "08af2e61-4993-11ea-85b3-f5103b0c4234",
                "relationship": [
                    "planning"
                ],
                "scheme": "ocid",
                "identifier": "ocds-t1s2t3-MD-1581070591188-PN-1581070591216",
                "uri": "http://dev.public.eprocurement.systems/tenders/ocds-t1s2t3-MD-1581070591188/ocds-t1s2t3-MD-1581070591188-PN-1581070591216"
            },
            {
                "id": "e90c1f03-4992-11ea-85b3-f5103b0c4234",
                "relationship": [
                    "parent"
                ],
                "scheme": "ocid",
                "identifier": "ocds-t1s2t3-MD-1581070591188",
                "uri": "http://dev.public.eprocurement.systems/tenders/ocds-t1s2t3-MD-1581070591188/ocds-t1s2t3-MD-1581070591188"
            }
        ]
    }


@pytest.fixture(scope='function')
def data_for_test_notice_compiled_release(prepared_cpid, prepared_ev_ocid):
    return {"cpid": prepared_cpid, "ocid": prepared_ev_ocid,
            "tender": {"token": "85baeb0a-5cc5-42bc-9516-45e341f666d0", "owner": "445f6851-c908-407d-9b45-14b92f3e964b",
                       "lots": [{"id": "a681ce60-0f95-4bc1-987c-96b7e1bdd5d1", "status": "active",
                                 "statusDetails": "empty"}], "hasEnquiries": False, "amendments": [
                    {"id": "561d0928-bd54-4255-bf42-5f33d3a044a0", "token": "e07aa4b3-d806-4f09-9daf-bf5c03955b27",
                     "type": "cancellation", "status": "pending", "relatesTo": "lot",
                     "relatedItem": "a681ce60-0f95-4bc1-987c-96b7e1bdd5d1", "date": "2020-04-02T09:14:25Z",
                     "description": "amendment.description", "rationale": "amendment.rationale", "documents": [
                        {"id": "835b8d03-80dc-4d1b-8b1c-fe2b1a23366c-1573211196021",
                         "documentType": "cancellationDetails", "title": "doc.title", "description": "12",
                         "url": "http://dev.bpe.eprocurement.systems/api/v1/storage/get/835b8d03-80dc-4d1b-8b1c-fe2b1a23366c-1573211196021",
                         "datePublished": "2019-11-08T11:31:51Z"}]}]}}


@pytest.fixture(scope='function')
def data_ev_with_amendment(prepared_ev_ocid, prepared_ev_id):
    return {
        "ocid": prepared_ev_ocid,
        "id": prepared_ev_id,
        "date": "2020-02-07T10:22:27Z",
        "tag": [
            "awardUpdate"
        ],
        "initiationType": "tender",
        "parties": [
            {
                "id": "MD-IDNO-tenderers id5",
                "name": "nam2",
                "identifier": {
                    "scheme": "MD-IDNO",
                    "id": "tenderers id5",
                    "legalName": "tenderers legalname",
                    "uri": "http://tenderers.com"
                },
                "address": {
                    "streetAddress": "tenderers adress",
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
                "additionalIdentifiers": [
                    {
                        "scheme": "MD-IDNO",
                        "id": "additionalIdentifiers id",
                        "legalName": "additionalIdentifiers legalName",
                        "uri": "http://additionalIdentifier.com"
                    }
                ],
                "contactPoint": {
                    "name": "Illia Petrusenko",
                    "email": "illya.petrusenko@gmail.com",
                    "telephone": "+380632074071",
                    "faxNumber": "+380445450099",
                    "url": "http://petrusenko.com/illia"
                },
                "details": {
                    "typeOfSupplier": "company",
                    "mainEconomicActivities": [
                        "456-00"
                    ],
                    "permits": [
                        {
                            "id": "2",
                            "scheme": "SRLE",
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
                                    "startDate": "2019-10-29T16:35:00Z",
                                    "endDate": "2019-10-29T16:36:00Z"
                                }
                            }
                        }
                    ],
                    "bankAccounts": [
                        {
                            "description": "description",
                            "bankName": "bankName",
                            "address": {
                                "streetAddress": "Steet",
                                "postalCode": "5",
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
                                        "description": "descr",
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
                                "id": "300711",
                                "scheme": "UA-MFO"
                            },
                            "accountIdentification": {
                                "id": "2600000625637",
                                "scheme": "IBAN"
                            },
                            "additionalAccountIdentifiers": [
                                {
                                    "id": "458-9652",
                                    "scheme": "settlement"
                                }
                            ]
                        }
                    ],
                    "legalForm": {
                        "id": "260000",
                        "scheme": "MD-IDNO",
                        "description": "description",
                        "uri": "uri"
                    },
                    "scale": "sme"
                },
                "persones": [
                    {
                        "title": "persones.title",
                        "name": "persones.name",
                        "identifier": {
                            "scheme": "MD-IDNO",
                            "id": "88888000",
                            "uri": "http://petrusenko.com/illia"
                        },
                        "businessFunctions": [
                            {
                                "id": "businessFunctions id",
                                "type": "authority",
                                "jobTitle": "Chief Executive Officer",
                                "period": {
                                    "startDate": "2019-10-30T00:00:35Z"
                                },
                                "documents": [
                                    {
                                        "id": "9004ab09-ca9b-4cb7-95f4-525a3bf64734-1574862409148",
                                        "documentType": "regulatoryDocument",
                                        "title": "doc title",
                                        "description": "doc description",
                                        "url": "http://dev.bpe.eprocurement.systems/api/v1/storage/get/9004ab09-ca9b-4cb7-95f4-525a3bf64734-1574862409148",
                                        "datePublished": "2019-11-27T13:48:23Z"
                                    }
                                ]
                            }
                        ]
                    }
                ],
                "roles": [
                    "tenderer",
                    "supplier"
                ]
            }
        ],
        "tender": {
            "id": "ocds-t1s2t3-MD-1581070591188",
            "title": "Evaluation",
            "description": "Evaluation stage of contracting process",
            "status": "active",
            "statusDetails": "awarding",
            "amendments":
                [
                    {
                        "rationale": "string",
                        "description": "string",
                        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "date": "2020-02-22T11:25:44Z",
                        "status": "pending",
                        "type": "cancellation",
                        "relatesTo": "lot",
                        "relatedItem": "36133175-8f63-4763-a1dd-b1d16b551453"

                    }],
            "criteria": [
                {
                    "id": "852d3adc-a245-4b86-9e43-e694e1bf2740",
                    "title": "",
                    "source": "procuringEntity",
                    "description": "",
                    "requirementGroups": [
                        {
                            "id": "68f8a408-e15f-4271-83c4-58d20d57dfe5",
                            "requirements": [
                                {
                                    "id": "004e1ed2-2d7c-4ed7-b671-d324f41cca03",
                                    "title": "",
                                    "dataType": "boolean"
                                }
                            ]
                        }
                    ],
                    "relatesTo": "award"
                }
            ],
            "items": [
                {
                    "id": "6733055d-9a88-4b90-8eee-c99a03ce3acd",
                    "description": "items description",
                    "classification": {
                        "scheme": "CPV",
                        "id": "15500000-3",
                        "description": "Produse lactate"
                    },
                    "additionalClassifications": [
                        {
                            "scheme": "CPVS",
                            "id": "AB06-7",
                            "description": "Plastic"
                        }
                    ],
                    "quantity": 1,
                    "unit": {
                        "name": "Metru cub consistent",
                        "id": "121"
                    },
                    "relatedLot": "36133175-8f63-4763-a1dd-b1d16b551453"
                },
                {
                    "id": "6733055d-9a88-4b90-8eee-c99a03ce4acd",
                    "description": "items description",
                    "classification": {
                        "scheme": "CPV",
                        "id": "15500000-3",
                        "description": "Produse lactate"
                    },
                    "additionalClassifications": [
                        {
                            "scheme": "CPVS",
                            "id": "AB06-7",
                            "description": "Plastic"
                        }
                    ],
                    "quantity": 1,
                    "unit": {
                        "name": "Metru cub consistent",
                        "id": "121"
                    },
                    "relatedLot": "36133175-8f63-4763-a1dd-b1d16b551454"
                }
            ],
            "lots": [
                {
                    "id": "36133175-8f63-4763-a1dd-b1d16b551453",
                    "title": "lots title",
                    "description": "lots description",
                    "status": "active",
                    "statusDetails": "awarded",
                    "value": {
                        "amount": 10,
                        "currency": "EUR"
                    },
                    "options": [
                        {
                            "hasOptions": False
                        }
                    ],
                    "recurrentProcurement": [
                        {
                            "isRecurrent": False
                        }
                    ],
                    "renewals": [
                        {
                            "hasRenewals": False
                        }
                    ],
                    "variants": [
                        {
                            "hasVariants": False
                        }
                    ],
                    "contractPeriod": {
                        "startDate": "2020-02-10T10:30:40Z",
                        "endDate": "2020-03-30T10:30:40Z"
                    },
                    "placeOfPerformance": {
                        "address": {
                            "streetAddress": "placeOfPerformance streetAddress",
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
                                    "scheme": "locality scheme",
                                    "id": "locality id",
                                    "description": "locality description"
                                }
                            }
                        }
                    }
                },
                {
                    "id": "36133175-8f63-4763-a1dd-b1d16b551454",
                    "title": "lots title",
                    "description": "lots description",
                    "status": "active",
                    "statusDetails": "awarded",
                    "value": {
                        "amount": 10,
                        "currency": "EUR"
                    },
                    "options": [
                        {
                            "hasOptions": False
                        }
                    ],
                    "recurrentProcurement": [
                        {
                            "isRecurrent": False
                        }
                    ],
                    "renewals": [
                        {
                            "hasRenewals": False
                        }
                    ],
                    "variants": [
                        {
                            "hasVariants": False
                        }
                    ],
                    "contractPeriod": {
                        "startDate": "2020-02-10T10:30:40Z",
                        "endDate": "2020-03-30T10:30:40Z"
                    },
                    "placeOfPerformance": {
                        "address": {
                            "streetAddress": "placeOfPerformance streetAddress",
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
                                    "scheme": "locality scheme",
                                    "id": "locality id",
                                    "description": "locality description"
                                }
                            }
                        }
                    }
                }
            ],
            "lotGroups": [
                {
                    "optionToCombine": False
                }
            ],
            "tenderPeriod": {
                "startDate": "2020-02-07T10:19:23Z",
                "endDate": "2020-02-07T10:20:23Z"
            },
            "enquiryPeriod": {
                "startDate": "2020-02-07T10:17:23Z",
                "endDate": "2020-02-07T10:19:23Z"
            },
            "awardPeriod": {
                "startDate": "2020-02-07T10:20:23Z"
            },
            "hasEnquiries": False,
            "documents": [
                {
                    "id": "9004ab09-ca9b-4cb7-95f4-525a3bf64734-1574862409148",
                    "documentType": "billOfQuantity",
                    "title": "doc1т",
                    "url": "http://dev.bpe.eprocurement.systems/api/v1/storage/get/9004ab09-ca9b-4cb7-95f4-525a3bf64734-1574862409148",
                    "datePublished": "2019-11-27T13:48:23Z"
                }
            ],
            "awardCriteria": "priceOnly",
            "awardCriteriaDetails": "automated",
            "submissionMethod": [
                "electronicSubmission"
            ],
            "submissionMethodDetails": "Lista platformelor: achizitii, ebs, licitatie, yptender",
            "submissionMethodRationale": [
                "Ofertele vor fi primite prin intermediul unei platforme electronice de achiziții publice"
            ],
            "requiresElectronicCatalogue": False
        },
        "awards": [
            {
                "id": "3c7faff8-6123-4862-a7ff-04875ca4b767",
                "description": "description",
                "status": "pending",
                "statusDetails": "active",
                "date": "2020-02-07T10:21:04Z",
                "value": {
                    "amount": 0.65,
                    "currency": "EUR"
                },
                "suppliers": [
                    {
                        "id": "MD-IDNO-tenderers id5",
                        "name": "nam2"
                    }
                ],
                "documents": [
                    {
                        "id": "9004ab09-ca9b-4cb7-95f4-525a3bf64734-1574862409148",
                        "documentType": "evaluationReports",
                        "title": "doctitle",
                        "description": "description",
                        "url": "http://dev.bpe.eprocurement.systems/api/v1/storage/get/9004ab09-ca9b-4cb7-95f4-525a3bf64734-1574862409148",
                        "datePublished": "2019-11-27T13:48:23Z"
                    }
                ],
                "relatedLots": [
                    "36133175-8f63-4763-a1dd-b1d16b551453"
                ],
                "relatedBid": "40d2b509-bff5-4d54-a98e-1c952d5adecd"
            }
        ],
        "bids": {
            "details": [
                {
                    "id": "40d2b509-bff5-4d54-a98e-1c952d5adecd",
                    "date": "2020-02-07T10:19:26Z",
                    "status": "pending",
                    "statusDetails": "valid",
                    "tenderers": [
                        {
                            "id": "MD-IDNO-tenderers id5",
                            "name": "nam2"
                        }
                    ],
                    "value": {
                        "amount": 0.65,
                        "currency": "EUR"
                    },
                    "documents": [
                        {
                            "id": "b5494aa9-578a-4f3b-a21d-cf4546374cef-1578921285987",
                            "documentType": "submissionDocuments",
                            "title": "doc title",
                            "description": "doc description",
                            "url": "http://dev.bpe.eprocurement.systems/api/v1/storage/get/b5494aa9-578a-4f3b-a21d-cf4546374cef-1578921285987",
                            "datePublished": "2020-01-13T13:51:49Z"
                        }
                    ],
                    "relatedLots": [
                        "36133175-8f63-4763-a1dd-b1d16b551453"
                    ]
                }
            ]
        },
        "contracts": [
            {
                "id": "848a5f27-2159-46af-aff1-82728af1ced4",
                "date": "2020-02-07T10:21:50Z",
                "awardId": "3c7faff8-6123-4862-a7ff-04875ca4b767",
                "relatedLots": [
                    "36133175-8f63-4763-a1dd-b1d16b551453"
                ],
                "status": "pending",
                "statusDetails": "active",
                "relatedProcesses": [
                    {
                        "id": "bd45f483-4993-11ea-85b3-f5103b0c4234",
                        "relationship": [
                            "x_contracting"
                        ],
                        "scheme": "ocid",
                        "identifier": "ocds-t1s2t3-MD-1581070591188-AC-1581816477249",
                        "uri": "http://dev.public.eprocurement.systems/tenders/ocds-t1s2t3-MD-1581070591188/ocds-t1s2t3-MD-1581070591188-AC-1581816477249"
                    }
                ]
            }
        ],
        "hasPreviousNotice": True,
        "purposeOfNotice": {
            "isACallForCompetition": True
        },
        "relatedProcesses": [
            {
                "id": "08af2e61-4993-11ea-85b3-f5103b0c4234",
                "relationship": [
                    "planning"
                ],
                "scheme": "ocid",
                "identifier": "ocds-t1s2t3-MD-1581070591188-PN-1581070591216",
                "uri": "http://dev.public.eprocurement.systems/tenders/ocds-t1s2t3-MD-1581070591188/ocds-t1s2t3-MD-1581070591188-PN-1581070591216"
            },
            {
                "id": "e90c1f03-4992-11ea-85b3-f5103b0c4234",
                "relationship": [
                    "parent"
                ],
                "scheme": "ocid",
                "identifier": "ocds-t1s2t3-MD-1581070591188",
                "uri": "http://dev.public.eprocurement.systems/tenders/ocds-t1s2t3-MD-1581070591188/ocds-t1s2t3-MD-1581070591188"
            }
        ]
    }


@pytest.fixture(scope='function')
def data_award():
    return {
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
        "suppliers": [{
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
            "persones": [{
                "title": "persones.title",
                "name": "persones.name",
                "identifier": {
                    "scheme": "persones MD-IDNO",
                    "id": "88888000",
                    "uri": "http://petrusenko.com/illia"
                },
                "businessFunctions": [{
                    "id": "businessFunctions id",
                    "type": "authority",
                    "jobTitle": "Chief Executive Officer",
                    "period": {
                        "startDate": "2019-10-30T00:00:35Z"
                    },
                    "documents": [{
                        "id": "e6886bf2-6911-4d11-ac38-62b943d73bb5-1572864287975",
                        "documentType": "regulatoryDocument",
                        "title": "doc title",
                        "description": "doc description"
                    }]
                }]
            }]
        }]
    }


@pytest.fixture(scope='function')
def data_person():
    return {
        "title": "string",
        "name": "string",
        "identifier": {
            "scheme": "string",
            "id": "UUID_1",
            "uri": "string"
        },
        "businessFunctions": [
            {
                "id": "string",
                "type": "priceEvaluator",
                "jobTitle": "string",
                "period": {
                    "startDate": "2020-02-12T12:14:12Z"
                },
                "documents": [
                    {
                        "documentType": "regulatoryDocument",
                        "id": "UUID_2",
                        "title": "string",
                        "description": "string"
                    }
                ]
            }
        ]
    }


@pytest.fixture(scope='function')
def data_businessFunction():
    return {
        "id": "string",
        "type": "priceEvaluator",
        "jobTitle": "string",
        "period": {
            "startDate": "2020-02-12T12:14:12Z"
        },
        "documents": [
            {
                "documentType": "regulatoryDocument",
                "id": "UUID_2",
                "title": "string",
                "description": "string"
            }
        ]
    }


@pytest.fixture(scope='function')
def data_document():
    return {
        "documentType": "regulatoryDocument",
        "id": "UUID_2",
        "title": "string",
        "description": "string"
    }


@pytest.fixture(scope='function')
def data_requirementResponse():
    return {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "value": "true",
        "relatedTenderer": {
            "id": "MD-IDNO-4214231235"
        },
        "requirement": {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        },
        "responder": {
            "name": "IMSP SCM nr.1",
            "identifier": {
                "sheme": "string",
                "id": "string"
            }
        }
    }


@pytest.fixture(scope='function')
def data_businessFunction():
    return {
        "id": "string",
        "type": "priceEvaluator",
        "jobTitle": "string",
        "period": {
            "startDate": "2020-02-12T12:14:12Z"
        },
        "documents": [
            {
                "documentType": "regulatoryDocument",
                "id": "UUID_2",
                "title": "string",
                "description": "string"
            }
        ]
    }


@pytest.fixture(scope='function')
def data_document():
    return {
        "documentType": "regulatoryDocument",
        "id": "UUID_2",
        "title": "string",
        "description": "string"
    }
