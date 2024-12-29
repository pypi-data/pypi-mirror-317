from djangoprime.core.base import BaseEnum


class TokenEnum(BaseEnum):
    TOKEN_CREATED = "Access token created successfully"
    TOKEN_REFRESHED = "Access token refreshed successfully"
    TOKEN_INVALIDATED = "Access token invalidated"
    TOKEN_VERIFIED = "Access token verified successfully"
    TOKEN_EXPIRED = "Access token has expired"
    TOKEN_REVOKED = "Access token has been revoked"
    TOKEN_BLACKLISTED = "Access token has been blacklisted"
    TOKEN_CLAIMS_UPDATED = "Token claims updated successfully"
    TOKEN_GENERATED_FOR_USER = "Token generated for user"
    TOKEN_RENEWED = "Token renewed successfully"
    TOKEN_NOT_FOUND = "Token not found"
    TOKEN_NOT_VALID = "Token is invalid or expired"

class TokenExceptionTypeEnum(BaseEnum):
    TOKEN_NOT_VALID = "Token is invalid or expired"
    TOKEN_EXPIRED = "The token has expired and is no longer valid."
    TOKEN_MISSING = "Token is missing from the request."
    TOKEN_REVOKED = "The token has been revoked and is no longer valid."
