from resources.domain._ import _

relatesTo = ('lot', 'tender')
schema_amendment = {
    "id": "AMENDMENT_ID",
    "date": "2019-04-01T10:00:00Z",
    "rationale": "Some_text",
    "description": "Some_text_2",
    "status": "pending",
    "type": "cancellation",
    "relatesTo": _("random.schoice", seq=relatesTo, end=1),
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
