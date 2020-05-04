from resources.domain._ import _
from resources.domain.document import schema_document

amendmentDocumentType = ('cancellationDetails',)
schema_document['documentType'] = _("random.schoice",
                                    seq=amendmentDocumentType,
                                    end=1)
relatesTo = ('lot', 'tender')
status = ('pending', 'active')

schema_amendment = {
    "id": "AMENDMENT_ID",
    "date": "2019-04-01T10:00:00Z",
    "rationale": "Some_text",
    "description": "Some_text_2",
    "status": _("random.schoice", seq=status, end=1),
    "type": "cancellation",
    "relatesTo": _("random.schoice", seq=relatesTo, end=1),
    "relatedItem": "RELATED_ITEM",
    "documents": [schema_document],
    "token": "ed8e86b9-82c9-4bcc-ac40-215317afa211",
    "owner": "3fa85f64-5717-4562-b3fc-2c963f66afa6"

}
