from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class Resolution(BaseModel):
    width: int
    height: int

class FileMeta(BaseModel):
    resolution: Optional[Resolution] = None
    tokenLength: int
    duration: int

class UploadFileResponse(BaseModel):
    url: str
    object_name: str
    uid: str
    meta: Optional[FileMeta] = None

class UploadRawDataResponse(BaseModel):
    raw_data_id: str

class UploadFileWithInfoResponse(BaseModel):
    url: str
    object_name: str
    uid: str
    raw_data_id: str
    meta: Optional[FileMeta] = None

class UploadAnnotationDataResponse(BaseModel):
    annotation_data_id: str
