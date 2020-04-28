from resources.domain._ import _

from resources.domain.businessFunction import schema_businessFunction
from resources.domain.identifier import schema_identifier

schema_person = {
    "title": _("person.title"),
    "name": _("person.name"),
    "identifier": schema_identifier,
    "businessFunctions": [
        schema_businessFunction
    ]
}
