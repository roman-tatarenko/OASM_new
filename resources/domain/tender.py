from resources.domain.lot import schema_lot
from resources.domain.person import schema_person, schema_person_GPA
from resources.domain._ import _

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
			"relatedItem": schema_lot['id']
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
		"lots": [schema_lot],
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
			"relatedLot": schema_lot['id']
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
statusDetails = ["qualification", "qualificationStandstill", ]
schema_tender_GPA={
	"ocid": "CPID",
	"planning": {
		"budget": {
			"amount": {
				"amount": 2000.00,
				"currency": "EUR"
			},
			"isEuropeanUnionFunded": True,
			"budgetBreakdown": [{
				"id": "ocds-t1s2t3-MD-1594025658436-FS-1594025662851",
				"description": "description",
				"amount": {
					"amount": 2000.00,
					"currency": "EUR"
				},
				"period": {
					"startDate": "2020-02-20T00:00:00Z",
					"endDate": "2020-12-31T00:00:00Z"
				},
				"sourceParty": {
					"id": "MD-IDNO-123654789000",
					"name": "buyer's name"
				},
				"europeanUnionFunding": {
					"projectIdentifier": "projectIdentifier",
					"projectName": "Name of this project",
					"uri": "http://uriuri.th"
				}
			}]
		},
		"rationale": "reason for budget"
	},
	"tender": {
		"id": "2dbd9295-cef8-4c13-9942-459a3cafddff",
		"title": "title of tender",
		"description": "desription of tender",
		"status": "active",
		"statusDetails": _("random.schoice", seq=statusDetails, end=1),
		"classification": {
			"scheme": "CPV",
			"id": "50100000-6",
			"description": "Servicii de reparare şi de întreţinere a vehiculelor şi a echipamentelor aferente şi "
						   "servicii conexe"
		},
		"mainProcurementCategory": "services",
		"procurementMethod": "selective",
		"procurementMethodDetails": "testGpaProcedure",
		"procurementMethodRationale": "procurementMethodRationale",
		"procurementMethodAdditionalInfo": "tender.procurementMethodAdditionalInfo",
		"submissionMethod": ["electronicSubmission"],
		"submissionMethodDetails": "Lista platformelor: achizitii, ebs, licitatie, yptender",
		"submissionMethodRationale": ["Ofertele vor fi primite prin intermediul unei platforme electronice de "
									  "achiziții publice"],
		"eligibilityCriteria": "Regulile generale privind naționalitatea și originea, precum și alte criterii de "
							   "eligibilitate sunt enumerate în Ghidul practic privind procedurile de contractare "
							   "a acțiunilor externe ale UE (PRAG)",
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
		"procuringEntity": {
			"id": "MD-IDNO-123654789000",
			"name": "name of PE",
			"identifier": {
				"id": "123654789000",
				"scheme": "MD-IDNO",
				"legalName": "legal name",
				"uri": "uri"
			},
			"address": {
				"streetAddress": "street address",
				"postalCode": "123",
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
						"scheme": "other",
						"id": "locality",
						"description": "4596"
					}
				}
			},
			"additionalIdentifiers": [{
				"id": "445521",
				"scheme": "md-idno",
				"legalName": "legalName",
				"uri": "uri"
			}],
			"contactPoint": {
				"name": "name",
				"email": "email",
				"telephone": "456-95-96",
				"faxNumber": "fax-number",
				"url": "url"
			},
			"persones": [schema_person_GPA]
		},
		"awardCriteria": "qualityOnly",
		"awardCriteriaDetails": "automated",
		"criteria": [{
			"id": "1",
			"title": "test title mdm",
			"source": "procuringEntity",
			"description": "test description",
			"requirementGroups": [{
				"id": "1-1",
				"description": "test description",
				"requirements": [{
					"id": "1-1-1",
					"title": "test title",
					"dataType": "boolean",
					"description": "test description"
				}]
			}],
			"relatesTo": "award"
		}],
		"conversions": [{
			"id": "566e2ad5-8c6a-4f4b-99f0-184f516505d9",
			"relatesTo": "requirement",
			"relatedItem": "4d67c9c2-ac3b-437f-89e0-6251f15b9109",
			"rationale": "Number of years/conversions rationale",
			"description": "conversions description",
			"coefficients": [{
				"id": "a5231f33-d3d8-4052-acce-e79563824bc7",
				"value": False,
				"coefficient": 0.6
			}]
		}],
		"requiresElectronicCatalogue": False,
		"contractPeriod": {
			"startDate": "2020-07-15T00:00:00Z",
			"endDate": "2020-07-31T00:20:00Z"
		},
		"value": {
			"amount": 2000.00,
			"currency": "EUR"
		},
		"lotGroups": [{
			"optionToCombine": False
		}],
		"lots": [schema_lot],
		"items": [{
			"id": "033193af-b876-47b0-a6f3-3ce67285d60d",
			"internalId": "item 1",
			"description": "description",
			"classification": {
				"scheme": "CPV",
				"id": "50100000-6",
				"description": "Servicii de reparare şi de întreţinere a vehiculelor şi a echipamentelor aferente "
							   "şi servicii conexe"
			},
			"additionalClassifications": [{
				"scheme": "CPVS",
				"id": "AA12-4",
				"description": "Oţel carbon"
			}],
			"quantity": 0.010,
			"unit": {
				"id": "10",
				"name": "Parsec"
			},
			"relatedLot": schema_lot['id']
		}],
		"documents": [{
			"id": "af8a1ede-226e-4edf-a273-d9c3ba217be2-1591026439835",
			"documentType": "assetAndLiabilityAssessment",
			"title": "doc1т"
		}],
		"procurementMethodModalities": ["electronicAuction"],
		"electronicAuctions": {
			"details": [{
				"id": "1",
				"relatedLot": schema_lot['id'],
				"electronicAuctionModalities": [{
					"eligibleMinimumDifference": {
						"amount": 10.00,
						"currency": "EUR"
					}
				}]
			}]
		},
		"otherCriteria": {
			"reductionCriteria": "none",
			"qualificationSystemMethods": ["manual"]
		}
	}
}
