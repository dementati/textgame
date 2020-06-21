import email_validator


def is_valid(email: str) -> bool:
    try:
        email_validator.validate_email(email)
        return True
    except email_validator.EmailNotValidError:
        return False


def normalize(email: str) -> str:
    return email_validator.validate_email(email).email
