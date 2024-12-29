"""
DoubaoTranslator
===============

A professional translation toolkit based on Doubao API.

Basic usage:
-----------

    from doubaotrans import DoubaoTranslator
    
    translator = DoubaoTranslator(api_key='your_api_key')
    result = translator.doubao_translate('Hello, world!', dest='zh')
    print(result.text)
"""

from .doubaotrans import (
    DoubaoTranslator,
    DoubaoTranslated,
    DoubaoDetected,
    DoubaoTranslationError,
    DoubaoAPIError,
    DoubaoAuthenticationError,
    DoubaoConnectionError,
)

__version__ = '1.2.0'
__author__ = 'kilolonion'
__email__ = 'kilolonion@gmail.com'

__all__ = [
    'DoubaoTranslator',
    'DoubaoTranslated',
    'DoubaoDetected',
    'DoubaoTranslationError',
    'DoubaoAPIError',
    'DoubaoAuthenticationError',
    'DoubaoConnectionError',
]
