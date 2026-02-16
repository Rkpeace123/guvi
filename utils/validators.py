"""
Input validation utilities
"""

import re
from typing import Optional, Tuple


def validate_phone(phone: str) -> Tuple[bool, Optional[str]]:
    """
    Validate Indian phone number
    
    Args:
        phone: Phone number string
    
    Returns:
        (is_valid, cleaned_number)
    """
    # Remove all non-digits
    cleaned = re.sub(r'\D', '', phone)
    
    # Check length and format
    if len(cleaned) == 10:
        # Must start with 6-9
        if cleaned[0] in '6789':
            return True, cleaned
    elif len(cleaned) == 12:
        # +91 format
        if cleaned.startswith('91') and cleaned[2] in '6789':
            return True, cleaned[2:]
    
    return False, None


def validate_upi(upi_id: str) -> Tuple[bool, Optional[str]]:
    """
    Validate UPI ID format
    
    Args:
        upi_id: UPI ID string
    
    Returns:
        (is_valid, cleaned_upi)
    """
    # Basic UPI format: username@provider
    pattern = r'^[\w\.-]+@[\w]+$'
    
    if re.match(pattern, upi_id, re.IGNORECASE):
        # Check minimum length
        if len(upi_id) >= 5:
            # Exclude email addresses
            if not upi_id.lower().endswith(('.com', '.in', '.org', '.net')):
                return True, upi_id.lower()
    
    return False, None


def validate_url(url: str) -> Tuple[bool, Optional[str]]:
    """
    Validate URL format
    
    Args:
        url: URL string
    
    Returns:
        (is_valid, cleaned_url)
    """
    # Basic URL pattern
    pattern = r'^(https?://|www\.)[^\s]+$'
    
    if re.match(pattern, url, re.IGNORECASE):
        # Add protocol if missing
        if url.lower().startswith('www.'):
            url = 'http://' + url
        return True, url.lower()
    
    return False, None


def validate_bank_account(account: str) -> Tuple[bool, Optional[str]]:
    """
    Validate bank account number
    
    Args:
        account: Account number string
    
    Returns:
        (is_valid, cleaned_account)
    """
    # Remove non-digits
    cleaned = re.sub(r'\D', '', account)
    
    # Indian bank accounts: 9-18 digits
    if 9 <= len(cleaned) <= 18:
        return True, cleaned
    
    return False, None


def validate_email(email: str) -> Tuple[bool, Optional[str]]:
    """
    Validate email address
    
    Args:
        email: Email string
    
    Returns:
        (is_valid, cleaned_email)
    """
    pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
    
    if re.match(pattern, email):
        return True, email.lower()
    
    return False, None


def sanitize_text(text: str, max_length: int = 5000) -> str:
    """
    Sanitize text input
    
    Args:
        text: Input text
        max_length: Maximum allowed length
    
    Returns:
        Sanitized text
    """
    # Truncate if too long
    if len(text) > max_length:
        text = text[:max_length]
    
    # Remove control characters (except newline and tab)
    text = ''.join(char for char in text if ord(char) >= 32 or char in '\n\t')
    
    # Remove excessive whitespace
    text = ' '.join(text.split())
    
    return text.strip()


# Example usage
if __name__ == "__main__":
    # Test phone validation
    test_phones = ["+91-9876543210", "9876543210", "1234567890", "98765"]
    for phone in test_phones:
        valid, cleaned = validate_phone(phone)
        print(f"Phone '{phone}': {'✅' if valid else '❌'} {cleaned}")
    
    # Test UPI validation
    test_upis = ["user@paytm", "test@upi", "invalid", "user@gmail.com"]
    for upi in test_upis:
        valid, cleaned = validate_upi(upi)
        print(f"UPI '{upi}': {'✅' if valid else '❌'} {cleaned}")
    
    # Test URL validation
    test_urls = ["https://example.com", "www.test.com", "invalid", "http://fake.com"]
    for url in test_urls:
        valid, cleaned = validate_url(url)
        print(f"URL '{url}': {'✅' if valid else '❌'} {cleaned}")
