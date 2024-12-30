import random
import string



def generate_password(length=30, include_special_chars=True):
    """
    Generate a unique alphanumeric code of a specified length.
    
    Args:
        length (int): Length of the generated code. Default is 30; include_special_chars (bool): Include special characters in the generated code. Default is True.
    
    Returns:
        str: Generated unique code.
    """
    
    if length < 6:
        raise ValueError("Length must be at least 6.")
    
    chars = string.ascii_letters + string.digits
    if include_special_chars:
        chars += "!@#$%^&*()_+-=[]{}|;:,.<>?/"
        
    return "".join(random.choice(chars) for _ in range(length))