"""
DoubaoTranslator - A professional translation toolkit based on Doubao API
"""

from doubaotrans.doubaotrans import (
    DoubaoTranslator,
    DoubaoTranslated,
    DoubaoDetected,
    DoubaoError,
    DoubaoAuthenticationError,
    DoubaoConnectionError,
    DoubaoAPIError,
    DoubaoConfigError,
    DoubaoValidationError,
)

__version__ = "1.2.2.1"
__author__ = "kilon"
__email__ = "a15607467772@163.com"

__all__ = [
    "DoubaoTranslator",
    "DoubaoTranslated",
    "DoubaoDetected",
    "DoubaoError",
    "DoubaoAuthenticationError",
    "DoubaoConnectionError",
    "DoubaoAPIError",
    "DoubaoConfigError",
    "DoubaoValidationError",
]