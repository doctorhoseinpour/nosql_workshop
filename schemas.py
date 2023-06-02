from typing import List, Optional

from pydantic import BaseModel

class AssetMetaDataResponseModel(BaseModel):
    file_hash: str
    name: str
    date_created: datetime
    content_type: Optional[str]

