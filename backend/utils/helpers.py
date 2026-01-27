# backend/utils/helpers.py
"""Helper utility functions."""

import uuid
import re
from datetime import datetime, date
from typing import Optional


def generate_id() -> str:
    """Generate a unique ID."""
    return str(uuid.uuid4())


def format_date(dt: datetime, format_str: str = "%Y-%m-%d") -> str:
    """Format a datetime object to string."""
    return dt.strftime(format_str)


def parse_date(date_str: str, format_str: str = "%Y-%m-%d") -> Optional[datetime]:
    """Parse a date string to datetime object."""
    try:
        return datetime.strptime(date_str, format_str)
    except ValueError:
        return None


def sanitize_string(text: str) -> str:
    """Sanitize a string by removing special characters."""
    # Remove any potentially harmful characters
    sanitized = re.sub(r'[<>"\';]', '', text)
    # Trim whitespace
    sanitized = sanitized.strip()
    return sanitized


def calculate_age(birth_date: date) -> int:
    """Calculate age from birth date."""
    today = date.today()
    age = today.year - birth_date.year
    
    # Adjust if birthday hasn't occurred this year
    if (today.month, today.day) < (birth_date.month, birth_date.day):
        age -= 1
    
    return age


def format_weight(weight_kg: float) -> str:
    """Format weight with unit."""
    return f"{weight_kg:.1f} kg"


def format_height(height_cm: float) -> str:
    """Format height with unit."""
    return f"{height_cm:.0f} cm"


def format_calories(calories: int) -> str:
    """Format calories with unit."""
    return f"{calories} kcal"


def format_macros(protein: int, carbs: int, fats: int) -> str:
    """Format macros as string."""
    return f"P: {protein}g | C: {carbs}g | F: {fats}g"


def calculate_water_intake(weight_kg: float) -> float:
    """Calculate recommended water intake in liters."""
    # 35ml per kg body weight
    return round((weight_kg * 35) / 1000, 1)


def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email))


def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to max length with ellipsis."""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."