from resources.domain._ import _
from resources.domain.document import schema_document
from resources.domain.period import schema_period_start_date

businessFunctionType = ("chairman", "procurementOfficer", "contactPoint", "technicalEvaluator",
                        "technicalOpener", "priceOpener", "priceEvaluator", "authority")

schema_businessFunction = {
    "id": _('uuid'),
    "type": _("random.schoice", seq=businessFunctionType, end=1),
    "jobTitle": _("person.occupation"),
    "period": schema_period_start_date,
    "documents": [
        schema_document
    ]
}
