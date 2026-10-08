from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
import uuid

class DatasetColumnSchema(BaseModel):
    name: str
    inferred_type: str  # numeric, categorical, datetime, boolean, text, unknown
    original_type: str
    is_empty: bool = False
    is_duplicate_name: bool = False

class DatasetMetadata(BaseModel):
    dataset_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    filename: str
    file_size_bytes: int
    file_format: str  # csv, xlsx, xls
    encoding: str
    delimiter: str
    has_headers: bool
    rows: int
    columns: int
    schema_info: List[DatasetColumnSchema]
    malformed_rows_count: int = 0
    duplicate_columns: List[str] = []
    empty_columns: List[str] = []
    warnings: List[str] = []
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class DatasetUploadResponse(BaseModel):
    dataset_id: str
    metadata: DatasetMetadata
    message: str = "Dataset successfully ingested and validated"
