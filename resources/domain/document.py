from resources.domain._ import _

documentType = ("regulatoryDocument",)
schema_document = {
    "documentType": _("random.schoice", seq=documentType, end=1),
    "id": _("uuid"),
    "title": _("text.title"),
    "description": _("text.text", quantity=1)
}
