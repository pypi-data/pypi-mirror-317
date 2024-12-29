from .media import AudioExceptionEnum, ImageExceptionEnum, FileExceptionEnum, VideoExceptionEnum
from .auth import AuthenticationExceptionEnum
from .crud import CreateResponseCodeEnum, UpdateResponseCodeEnum, DeleteResponseCodeEnum, LoginResponseCodeEnum, PasswordResponseCodeEnum
from .database import DatabaseExceptionEnum
from .mail import EmailExceptionEnum
from .permissions import PermissionExceptionTypeEnum
from .response import ResponseKeyEnum, ResponseExceptionTypeEnum
from .throttling import ThrottlingExceptionTypeEnum
from .token import TokenEnum, TokenExceptionTypeEnum


class MediaType:
    """
    A class that groups all media-related exception enumerations under one category.

    Attributes:
        AUDIO (Enum): Enum for audio-related exceptions.
        FILE (Enum): Enum for file-related exceptions.
        IMAGE (Enum): Enum for image-related exceptions.
        VIDEO (Enum): Enum for video-related exceptions.
    """
    AUDIO = AudioExceptionEnum  # Enum related to audio exceptions
    FILE = FileExceptionEnum    # Enum related to file exceptions
    IMAGE = ImageExceptionEnum  # Enum related to image exceptions
    VIDEO = VideoExceptionEnum  # Enum related to video exceptions


class ExceptionsType:
    """
    A class that categorizes various exception enumerations into specific domains.

    Attributes:
        MEDIA (MediaType): Enum related to media exception types.
        DATABASE (Enum): Enum related to database exceptions.
        EMAIL (Enum): Enum related to email exceptions.
        RESPONSE (Enum): Enum related to response exceptions.
        PERMISSION (Enum): Enum related to permission exceptions.
        TOKEN (Enum): Enum related to token exceptions.
        THROTTLING (Enum): Enum related to throttling exceptions.
        AUTHENTICATION (Enum): Enum related to authentication exceptions.
    """
    MEDIA = MediaType               # Group of media-related exception enumerations
    DATABASE = DatabaseExceptionEnum  # Enum for database-related exceptions
    EMAIL = EmailExceptionEnum      # Enum for email-related exceptions
    RESPONSE = ResponseExceptionTypeEnum  # Enum for response-related exceptions
    PERMISSION = PermissionExceptionTypeEnum  # Enum for permission-related exceptions
    TOKEN = TokenExceptionTypeEnum  # Enum for token-related exceptions
    THROTTLING = ThrottlingExceptionTypeEnum  # Enum for throttling-related exceptions
    AUTHENTICATION = AuthenticationExceptionEnum  # Enum for authentication-related exceptions


class MessageType:
    """
    A class that organizes response codes for different CRUD operations and authentication actions.

    Attributes:
        CREATE (Enum): Enum for the response codes related to the creation process.
        UPDATE (Enum): Enum for the response codes related to the update process.
        DELETE (Enum): Enum for the response codes related to the deletion process.
        LOGIN (Enum): Enum for the response codes related to the login process.
        PASSWORD (Enum): Enum for the response codes related to password-related actions.
    """
    CREATE = CreateResponseCodeEnum      # Enum for response codes when creating resources
    UPDATE = UpdateResponseCodeEnum      # Enum for response codes when updating resources
    DELETE = DeleteResponseCodeEnum      # Enum for response codes when deleting resources
    LOGIN = LoginResponseCodeEnum        # Enum for response codes during login
    PASSWORD = PasswordResponseCodeEnum  # Enum for response codes related to password actions


class ResponseEnum:
    """
    A central class that categorizes and organizes response-related enumerations.

    Attributes:
        RESPONSE_KEY (Enum): Enum related to the response key.
        EXCEPTIONS (ExceptionsType): Grouping of all exception-related enumerations.
        MESSAGE (MessageType): Grouping of response codes for various operations.
        TOKEN (Enum): Enum for token-related response codes.
    """
    RESPONSE_KEY = ResponseKeyEnum   # Enum for response keys used in API responses
    EXCEPTIONS = ExceptionsType      # Grouping of exception enumerations
    MESSAGE = MessageType            # Grouping of response codes for CRUD operations and authentication
    TOKEN = TokenEnum                # Enum for token-related response types
