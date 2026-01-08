import re
from fastapi import HTTPException

def validate_password(password: str) -> None:
    """
    Rules:
    - Starts with capital letter
    - Contains at least one special character
    - Ends with a number
    - Minimum 8 characters
    """

    pattern = r"^[A-Z].*[!@#$%^&*(),.?\":{}|<>].*\d+$"

    if len(password) < 8:
        raise HTTPException(
            status_code=400,
            detail="Password must be at least 8 characters long"
        )

    if not re.match(pattern, password):
        raise HTTPException(
            status_code=400,
            detail=(
                "Password must start with a capital letter, "
                "contain a special character, "
                "and end with a number"
            )
        )
