import os
import uuid
import pandas as pd
import polars as pl
from typing import Tuple, Dict, Any, List
from backend.app.schemas.dataset import DatasetMetadata, DatasetColumnSchema

class DataIntakeAgent:
    """
    Data Intake Agent: Validates file type, detects delimiter & encoding,
    infers basic column schemas, detects empty/duplicate columns, and generates metadata.
    """
    
    SUPPORTED_EXTENSIONS = {".csv", ".xlsx", ".xls"}
    
    @staticmethod
    def detect_encoding(file_path: str) -> str:
        # Try common encodings
        encodings = ["utf-8", "utf-8-sig", "latin-1", "cp1252", "iso-8859-1"]
        for enc in encodings:
            try:
                with open(file_path, "r", encoding=enc) as f:
                    f.read(4096)
                return enc
            except UnicodeDecodeError:
                continue
        return "utf-8"

    @staticmethod
    def detect_delimiter(file_path: str, encoding: str) -> str:
        delimiters = [",", ";", "\t", "|"]
        try:
            with open(file_path, "r", encoding=encoding) as f:
                first_line = f.readline()
            counts = {d: first_line.count(d) for d in delimiters}
            best_delim = max(counts, key=counts.get)
            return best_delim if counts[best_delim] > 0 else ","
        except Exception:
            return ","

    def process_file(self, file_path: str, original_filename: str) -> Tuple[DatasetMetadata, pl.DataFrame]:
        ext = os.path.splitext(original_filename)[1].lower()
        if ext not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(f"Unsupported file format: {ext}. Supported formats: {self.SUPPORTED_EXTENSIONS}")
            
        file_size = os.path.getsize(file_path)
        warnings = []
        
        if ext == ".csv":
            encoding = self.detect_encoding(file_path)
            delimiter = self.detect_delimiter(file_path, encoding)
            try:
                df = pl.read_csv(file_path, encoding=encoding, separator=delimiter, ignore_errors=True)
            except Exception as e:
                # Fallback to pandas
                pdf = pd.read_csv(file_path, encoding=encoding, sep=delimiter, on_bad_lines='skip')
                df = pl.from_pandas(pdf)
                warnings.append(f"Used fallback parser due to formatting issues: {str(e)}")
        else: # Excel
            encoding = "utf-8"
            delimiter = "N/A"
            pdf = pd.read_excel(file_path)
            df = pl.from_pandas(pdf)
            
        dataset_id = f"ds_{uuid.uuid4().hex[:12]}"
        rows, cols = df.shape
        
        # Check duplicate column names
        col_names = df.columns
        duplicate_cols = [c for c in set(col_names) if col_names.count(c) > 1]
        if duplicate_cols:
            warnings.append(f"Duplicate column names detected: {duplicate_cols}")
            
        # Analyze schema info
        schema_info: List[DatasetColumnSchema] = []
        empty_cols = []
        
        for col_name in col_names:
            dtype_str = str(df[col_name].dtype)
            null_count = df[col_name].null_count()
            is_empty = null_count == rows
            if is_empty:
                empty_cols.append(col_name)
                
            inferred = "categorical"
            if "Int" in dtype_str or "Float" in dtype_str:
                inferred = "numeric"
            elif "Date" in dtype_str or "Time" in dtype_str:
                inferred = "datetime"
            elif "Boolean" in dtype_str:
                inferred = "boolean"
                
            schema_info.append(DatasetColumnSchema(
                name=col_name,
                inferred_type=inferred,
                original_type=dtype_str,
                is_empty=is_empty,
                is_duplicate_name=col_name in duplicate_cols
            ))
            
        metadata = DatasetMetadata(
            dataset_id=dataset_id,
            filename=original_filename,
            file_size_bytes=file_size,
            file_format=ext[1:],
            encoding=encoding if ext == ".csv" else "binary",
            delimiter=delimiter,
            has_headers=True,
            rows=rows,
            columns=cols,
            schema_info=schema_info,
            duplicate_columns=duplicate_cols,
            empty_columns=empty_cols,
            warnings=warnings
        )
        
        return metadata, df
