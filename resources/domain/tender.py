from resources.domain.person import schema_person

schema_tender={
	"ocid": "CPID",
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
				"id": "ocds-t1s2t3-MD-1585831995355-FS-1585832229215",
				"description": "description",
				"amount": {
					"amount": 15.00,
					"currency": "EUR"
				},
				"period": {
					"startDate": "2020-04-01T11:07:00Z",
					"endDate": "2020-10-01T00:00:00Z"
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
		"id": "5e8b7aea-5656-4621-b308-2cf77bbff071",
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
			"startDate": "2020-04-08T16:35:29Z",
			"endDate": "2020-04-08T16:45:29Z"
		},
		"enquiryPeriod": {
			"startDate": "2020-04-08T13:15:29Z",
			"endDate": "2020-04-08T16:35:29Z"
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
		"procurementMethodAdditionalInfo": "tenderprocurementMethodAdditionalInfo",
		"mainProcurementCategory": "goods",
		"eligibilityCriteria": "Regulile generale privind naționalitatea și originea, precum și alte criterii de eligibilitate sunt enumerate în Ghidul practic privind procedurile de contractare a acțiunilor externe ale UE (PRAG)",
		"contractPeriod": {
			"startDate": "2020-04-28T14:45:00Z",
			"endDate": "2020-04-30T14:45:00Z"
		},
		"procurementMethodModalities": ["electronicAuction"],
		"procuringEntity": {
			"id": "MD-IDNO-1",
			"name": "name of procuringEntity",
			"identifier": {
				"scheme": "MD-IDNO",
				"id": "1",
				"legalName": "identifier/legal name",
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
			"persones": [schema_person]
		},
		"value": {
			"amount": 10.00,
			"currency": "EUR"
		},
		"lotGroups": [{
			"optionToCombine": False
		}],
		"criteria": [{
			"id": "1",
			"title": "criteriatitle",
			"description": "criteria description",
			"requirementGroups": [{
				"id": "1",
				"requirements": [{
					"id": "1",
					"title": "Your age???",
					"dataType": "integer",
					"period": {
						"startDate": "2019-12-26T14:45:00Z",
						"endDate": "2019-12-30T14:45:00Z"
					},
					"minValue": -5,
					"maxValue": 18
				}]
			}],
			"relatesTo": "lot",
			"relatedItem": "8fb60930-6947-4d1c-9512-f6a7dea12d97"
		}],
		"conversions": [{
			"id": "1",
			"relatesTo": "requirement",
			"relatedItem": "1",
			"rationale": "Number of years/conversions rationale",
			"description": "conversions description",
			"coefficients": [{
				"id": "111",
				"value": 6,
				"coefficient": 0.6
			}, {
				"id": "112",
				"value": 7,
				"coefficient": 0.7
			}]
		}],
		"lots": [{
			"id": "8fb60930-6947-4d1c-9512-f6a7dea12d97",
			"title": "Далеко-далеко за словесными горами в стране гласных и согласных живут рыбные тексты. Вдали от всех живут они в буквенных домах на берегу Семантика большого языкового океана. Маленький ручеек Даль журчит по всей стране и обеспечивает ее всеми необходимыми правилами. Эта парадигматическая страна, в которой жаренные члены предложения залетают прямо в рот. Даже всемогущая пунктуация не имеет власти над рыбными текстами, ведущими безорфографичный образ жизни.",
			"description": "looot",
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
							"scheme": "666",
							"id": "666",
							"description": "666"
						}
					}
				},
				"description": ""
			}
		}],
		"items": [{
			"id": "400fc08d-9a1a-4129-ad16-0e7f2967e5eb",
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
				"id": "120",
				"name": "Milion decalitri"
			},
			"description": "Душа моя озарена неземной радостью, как эти чудесные весенние утра, которыми я наслаждаюсь от всего сердца. Я совсем один и блаженствую в здешнем краю, словно созданном для таких, как я.",
			"relatedLot": "8fb60930-6947-4d1c-9512-f6a7dea12d97"
		}],
		"awardCriteria": "qualityOnly",
		"awardCriteriaDetails": "automated",
		"requiresElectronicCatalogue": False,
		"submissionMethod": ["electronicSubmission"],
		"submissionMethodRationale": ["Ofertele vor fi primite prin intermediul unei platforme electronice de achiziții publice"],
		"submissionMethodDetails": "Lista platformelor: achizitii, ebs, licitatie, yptender",
		"documents": [{
			"id": "9dc2023f-bfbb-42aa-b1e8-48fe7da7a92c-1573734632179",
			"documentType": "billOfQuantity",
			"title": "doc1т"
		}]
	}
}