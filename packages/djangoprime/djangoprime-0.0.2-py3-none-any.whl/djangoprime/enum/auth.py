from djangoprime.core.base import BaseEnum


class UsernameExceptionEnum(BaseEnum):
    """
    Enum class for handling exceptions related to username operations.

    This class inherits from BaseEnum and defines error messages related to username
    validation and operations.

    Attributes:
        USERNAME_ALREADY_EXISTS (str): Error message when the username already exists.
        USERNAME_NOT_FOUND (str): Error message when the username is not found.
        USERNAME_REQUIRED (str): Error message when the username is required.
    """
    USERNAME_ALREADY_EXISTS = 'username already exists.'  # Username already exists in the system
    USERNAME_NOT_FOUND = 'username not found.'  # Username is not found in the system
    USERNAME_REQUIRED = 'username is required.'  # Username is a mandatory field


class PasswordExceptionEnum(BaseEnum):
    """
    Enum class for handling exceptions related to password operations.

    This class inherits from BaseEnum and defines error messages for various password
    issues such as validation errors, required fields, and password reset scenarios.

    Attributes:
        PASSWORD_ERROR (str): Error message for invalid password format.
        PASSWORD_NOT_VALID (str): Error message when the password is invalid.
        PASSWORD_REQUIRED (str): Error message when the password field is required.
        PASSWORD_RESET_SUCCESS (str): Success message for password reset.
        PASSWORD_WRONG (str): Error message when the entered password is incorrect.
        NEW_AND_OLD_PASSWORD_SAME (str): Error message when new and old password are the same.
        NEW_AND_CONFIRM_PASSWORD (str): Error message when new and confirm password don't match.
    """
    PASSWORD_ERROR = 'This field is required | Must be (a-z), (0, 9) and minimum 8 characters'  # Invalid password format
    PASSWORD_NOT_VALID = 'Your password is invalid.'  # Invalid password format
    PASSWORD_REQUIRED = 'Password is required'  # Password is mandatory
    PASSWORD_RESET_SUCCESS = 'Your password has been reset successfully.'  # Successful password reset
    PASSWORD_WRONG = 'Enter correct password, your password is incorrect.'  # Incorrect password entered
    NEW_AND_OLD_PASSWORD_SAME = 'New and old password cannot be same.'  # Old and new passwords cannot be the same
    NEW_AND_CONFIRM_PASSWORD = 'New and confirm password must be same.'  # New and confirm password must match


class AuthenticationExceptionEnum(BaseEnum):
    """
    Enum class for handling authentication-related exceptions.

    This class inherits from BaseEnum and defines various error messages related to
    authentication issues such as incorrect credentials, expired links, account states,
    and permission issues.

    Attributes:
        AUTHENTICATION_FAILED (str): Error message when authentication fails.
        EMAIL_AND_PASSWORD_REQUIRED (str): Error message when both email and password are required.
        USERNAME_AND_PASSWORD_REQUIRED (str): Error message when both username and password are required.
        LINK_EXPIRED (str): Error message when the verification link is expired.
        ACCOUNT_ALREADY_EXISTS (str): Error message when the account already exists.
        ACCOUNT_NOT_EXIST (str): Error message when the account does not exist.
        ACCOUNT_VERIFIED (str): Message when the account is verified and can be logged in.
        ACCOUNT_NOT_ACTIVE (str): Error message when the account is not active.
        ANONYMOUS_USER (str): Message for anonymous users who are not authenticated.
        LOGOUT_FAILED (str): Error message when logout fails.
        VERIFICATION_LINK_EXPIRE (str): Error message when verification link has expired.
        NOT_AUTHENTICATED (str): Error message when authentication credentials are missing.
        UNAUTHORIZED_USER (str): Error message when a user is not authorized for an action.
        ALREADY_AUTHENTICATED (str): Message when the user is already authenticated.

        Password related attributes (repeated from PasswordExceptionEnum):
            PASSWORD_ERROR (str): Invalid password format error.
            PASSWORD_NOT_VALID (str): Invalid password error.
            PASSWORD_REQUIRED (str): Password required error.
            PASSWORD_RESET_SUCCESS (str): Password reset success message.
            WRONG_PASSWORD (str): Incorrect password error.
            INCORRECT_PASSWORD (str): Incorrect password error.
            INVALID_PASSWORD (str): Incorrect password error.
            NEW_AND_OLD_PASSWORD_SAME (str): Error message when new and old password are same.
            NEW_AND_CONFIRM_PASSWORD (str): Error message when new and confirm password don't match.

        Username related attributes (repeated from UsernameExceptionEnum):
            USERNAME_ALREADY_EXISTS (str): Error message when the username already exists.
            USERNAME_NOT_FOUND (str): Error message when the username is not found.
            USERNAME_REQUIRED (str): Error message when the username is required.
    """
    AUTHENTICATION_FAILED = 'Incorrect authentication credentials.'  # Authentication credentials are incorrect
    EMAIL_AND_PASSWORD_REQUIRED = 'Email and password are required.'  # Both email and password must be provided
    USERNAME_AND_PASSWORD_REQUIRED = 'username and password are required.'  # Both username and password must be provided
    LINK_EXPIRED = 'link is expired, please generate new link.'  # Expired verification link
    ACCOUNT_ALREADY_EXISTS = "Account Already Exists"  # Account already exists
    ACCOUNT_NOT_EXIST = 'Account does not exist!'  # Account does not exist
    ACCOUNT_VERIFIED = 'your account is verified, please login.'  # Account verified, ready for login
    ACCOUNT_NOT_ACTIVE = 'Account is not active, Please activate your account.'  # Account inactive, needs activation
    ANONYMOUS__USER = 'Anonymous user'  # Message for anonymous users
    LOGOUT_FAILED = 'logout failed'  # Logout failed message
    VERIFICATION_LINK_EXPIRE = 'This link is expired, please resend your verification link.'  # Expired verification link
    NOT_AUTHENTICATED = 'Authentication credentials were not provided.'  # Missing authentication credentials
    UNAUTHORIZED_USER = 'You do not have permission to perform this action.'  # Unauthorized access attempt
    ALREADY_AUTHENTICATED = 'You are already authenticated.'  # User is already authenticated

    # Password-related exceptions
    PASSWORD_ERROR = 'This field is required | Must be (a-z), (0, 9) and minimum 8 characters'  # Invalid password format
    PASSWORD_NOT_VALID = 'Your password is invalid.'  # Invalid password
    PASSWORD_REQUIRED = 'Password is required'  # Password is mandatory
    PASSWORD_RESET_SUCCESS = 'Your password has been reset successfully.'  # Password reset success
    WRONG_PASSWORD = 'Enter correct password, your password is incorrect.'  # Incorrect password entered
    INCORRECT_PASSWORD = 'Enter correct password, your password is incorrect.'  # Incorrect password entered
    INVALID_PASSWORD = 'Enter correct password, your password is incorrect.'  # Incorrect password entered
    NEW_AND_OLD_PASSWORD_SAME = 'New and old password cannot be same.'  # Old and new passwords can't be identical
    NEW_AND_CONFIRM_PASSWORD = 'New and confirm password must be same.'  # New and confirm passwords must match

    # Username-related exceptions
    USERNAME_ALREADY_EXISTS = 'username already exists.'  # Username already exists
    USERNAME_NOT_FOUND = 'username not found.'  # Username not found
    USERNAME_REQUIRED = 'username is required.'  # Username is mandatory
