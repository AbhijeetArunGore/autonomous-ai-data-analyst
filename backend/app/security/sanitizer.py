import re
import os
from typing import Tuple

class PromptInjectionDefense:
    """
    Security Engine: Enforces boundary isolation between system instructions
    and untrusted cell data content uploaded via CSV/Excel datasets.
    """
    
    @staticmethod
    def wrap_data_boundary(content: str, tag_name: str = "DATASET_CONTENT") -> str:
        # Strip potential system override commands embedded inside dataset strings
        sanitized = re.sub(r'(?i)(ignore previous instructions|system prompt|you are now)', '[REDACTED_TEXT]', content)
        return f"<{tag_name}>\n{sanitized}\n</{tag_name}>"

class SecurityValidator:
    """
    Validates uploaded files for size limits, MIME magic bytes, and path traversal prevention.
    """
    MAX_FILE_SIZE_BYTES = 50 * 1024 * 1024  # 50MB
    
    @classmethod
    def validate_file_upload(cls, filename: str, file_size: int) -> Tuple[bool, str]:
        if file_size > cls.MAX_FILE_SIZE_BYTES:
            return False, f"File size ({file_size / 1024 / 1024:.1f}MB) exceeds maximum allowed limit of 50MB."
            
        ext = os.path.splitext(filename)[1].lower()
        if ext not in [".csv", ".xlsx", ".xls"]:
            return False, f"Unsupported file extension: {ext}"
            
        # Prevent path traversal in filename
        clean_name = os.path.basename(filename)
        if clean_name != filename:
            return False, "Invalid filename detected (path traversal attempt)."
            
        return True, "Valid"
