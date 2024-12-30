from enum import Enum
from pydantic import BaseModel, Field, HttpUrl, field_validator, model_validator
from typing import Optional

class ChartType(str, Enum):
    BAR = "bar"
    COUNTER = "counter"
    LINE = "line"
    MAP = "map"
    SCATTERPLOT = "scatter"
    TABLE = "table"

    def __str__(self):
        return self.value

    def __repr__(self):
        return f"ChartType.{self.name}"

    def __json__(self):
        return self.value

import unicodedata

def validate_text(input_text: str, max_length: int, field_name: str) -> str:
    """
    Validates text input for chart fields with reasonable Unicode support while maintaining security.
    
    Allows:
    - Common Unicode letters and numbers
    - Common punctuation and symbols
    - Mathematical symbols
    - Currency symbols
    - Diacritical marks
    - Common CJK characters
    
    Blocks:
    - Control characters
    - Private Use Areas
    - Unassigned code points
    - Potentially dangerous Unicode categories
    """
    if len(input_text) > max_length:
        raise ValueError(f"{field_name} exceeds the maximum allowed length of {max_length} characters.")
    
    if len(input_text.strip()) == 0:
        raise ValueError(f"{field_name} cannot be empty or just whitespace")
    
    # Block certain Unicode categories that could be used maliciously
    blocked_categories = {
        'Cc',  # Control
        'Cf',  # Format
        'Cs',  # Surrogate
        'Co',  # Private Use
        'Cn',  # Unassigned
    }
    
    # Additional blocked ranges (hex)
    blocked_ranges = [
        (0x2028, 0x2029),    # Line/paragraph separators
        (0x202A, 0x202E),    # Bidirectional formatting
        (0xFFF0, 0xFFFF),    # Specials
        (0xFFF9, 0xFFFB),    # Interlinear annotations
        (0xFEFF, 0xFEFF),    # Zero width no-break space
        (0x200B, 0x200F),    # Zero width spaces and direction marks
        (0x2060, 0x2064),    # Word joiner and invisible operators
    ]
    
    # Explicitly allow certain Unicode blocks that are useful for charts
    allowed_ranges = [
        (0x0020, 0x007E),    # Basic Latin
        (0x00A0, 0x00FF),    # Latin-1 Supplement (includes common symbols and diacritics)
        (0x0100, 0x017F),    # Latin Extended-A
        (0x0180, 0x024F),    # Latin Extended-B
        (0x0250, 0x02AF),    # IPA Extensions
        (0x02B0, 0x02FF),    # Spacing Modifier Letters (including ʻokina)
        (0x0300, 0x036F),    # Combining Diacritical Marks
        (0x0370, 0x03FF),    # Greek and Coptic
        (0x0400, 0x04FF),    # Cyrillic
        (0x0500, 0x052F),    # Cyrillic Supplement
        (0x0600, 0x06FF),    # Arabic
        (0x0900, 0x097F),    # Devanagari
        (0x0E00, 0x0E7F),    # Thai
        (0x1E00, 0x1EFF),    # Latin Extended Additional
        (0x2000, 0x206F),    # General Punctuation (excluding blocked items above)
        (0x2070, 0x209F),    # Superscripts and Subscripts
        (0x20A0, 0x20CF),    # Currency Symbols
        (0x2100, 0x214F),    # Letterlike Symbols
        (0x2150, 0x218F),    # Number Forms
        (0x2190, 0x21FF),    # Arrows
        (0x2200, 0x22FF),    # Mathematical Operators
        (0x2460, 0x24FF),    # Enclosed Alphanumerics
        (0x3000, 0x303F),    # CJK Symbols and Punctuation
        (0x3040, 0x309F),    # Hiragana
        (0x30A0, 0x30FF),    # Katakana
        (0x4E00, 0x9FFF),    # CJK Unified Ideographs (Common)
    ]
    
    for char in input_text:
        char_ord = ord(char)
        char_category = unicodedata.category(char)
        
        # Check if character is in blocked category
        if char_category in blocked_categories:
            raise ValueError(f"{field_name} contains invalid character: {char} (category {char_category})")
        
        # Check if character is in blocked range
        if any(start <= char_ord <= end for start, end in blocked_ranges):
            raise ValueError(f"{field_name} contains invalid character: {char}")
        
        # Check if character is in allowed range
        if not any(start <= char_ord <= end for start, end in allowed_ranges):
            raise ValueError(f"{field_name} contains invalid character: {char}")
            
    return input_text


class BaseChart(BaseModel):
    model_config = {
        'extra': 'forbid'  
    }

    type: ChartType
    source_id: Optional[str] = None
    title: str = Field(..., min_length=8, max_length=140)
    subtitle: Optional[str] = Field(None, min_length=3, max_length=140)
    description: Optional[str] = Field(None, min_length=8, max_length=2000)
    icon: Optional[HttpUrl] = None

    @model_validator(mode='before')
    def validate_fields(cls, values):
        for field, max_length in [('title', 140), ('description', 2000)]:
            if field in values and values[field] is not None:
                values[field] = validate_text(values[field], max_length, field)
        return values
