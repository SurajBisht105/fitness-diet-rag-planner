# frontend/utils/validators.py
"""Frontend form validation utilities."""

import re
from typing import Optional, Tuple


class FormValidator:
    """Form validation utilities."""
    
    @staticmethod
    def validate_email(email: str) -> Tuple[bool, Optional[str]]:
        """Validate email format."""
        if not email:
            return False, "Email is required"
        
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(pattern, email):
            return False, "Invalid email format"
        
        return True, None
    
    @staticmethod
    def validate_name(name: str) -> Tuple[bool, Optional[str]]:
        """Validate name."""
        if not name:
            return False, "Name is required"
        
        if len(name) < 2:
            return False, "Name must be at least 2 characters"
        
        if len(name) > 100:
            return False, "Name must be less than 100 characters"
        
        return True, None
    
    @staticmethod
    def validate_age(age: int) -> Tuple[bool, Optional[str]]:
        """Validate age."""
        if age < 16:
            return False, "Must be at least 16 years old"
        
        if age > 80:
            return False, "Age must be less than 80"
        
        return True, None
    
    @staticmethod
    def validate_weight(weight: float) -> Tuple[bool, Optional[str]]:
        """Validate weight."""
        if weight < 30:
            return False, "Weight must be at least 30 kg"
        
        if weight > 300:
            return False, "Weight must be less than 300 kg"
        
        return True, None
    
    @staticmethod
    def validate_height(height: float) -> Tuple[bool, Optional[str]]:
        """Validate height."""
        if height < 100:
            return False, "Height must be at least 100 cm"
        
        if height > 250:
            return False, "Height must be less than 250 cm"
        
        return True, None
    
    @staticmethod
    def validate_profile_form(data: dict) -> Tuple[bool, list]:
        """Validate entire profile form."""
        errors = []
        
        # Validate name
        valid, error = FormValidator.validate_name(data.get("name", ""))
        if not valid:
            errors.append(error)
        
        # Validate email
        valid, error = FormValidator.validate_email(data.get("email", ""))
        if not valid:
            errors.append(error)
        
        # Validate age
        valid, error = FormValidator.validate_age(data.get("age", 0))
        if not valid:
            errors.append(error)
        
        # Validate weight
        valid, error = FormValidator.validate_weight(data.get("weight_kg", 0))
        if not valid:
            errors.append(error)
        
        # Validate height
        valid, error = FormValidator.validate_height(data.get("height_cm", 0))
        if not valid:
            errors.append(error)
        
        return len(errors) == 0, errors