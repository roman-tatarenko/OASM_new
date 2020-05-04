from resources.domain.businessFunction import schema_businessFunction
from resources.domain.identifier import schema_identifier

schema_responder = {
    "title": "title",
    "name": "name",
    "identifier": schema_identifier,
    "businessFunctions": [schema_businessFunction]
}
