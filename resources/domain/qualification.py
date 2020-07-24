from datetime import datetime
from resources.domain._ import _




status = ('pending', 'active', 'unsuccessful')
statusDetails=('awaiting', 'consideration')

schema_qualification = {
    "id": "QUALIFICATION_ID",
    "date": datetime.now(),
    "status": _("random.schoice", seq=status, end=1),
    "statusDetails": _("random.choice", seq=statusDetails, end=1),
    "token": "ed8e86b9-82c9-4bcc-ac40-215317afa211",
    "owner": "3fa85f64-5717-4562-b3fc-2c963f66afa6"

}
