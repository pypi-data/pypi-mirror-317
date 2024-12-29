from djangoprime.core.base import BaseEnum


class ResponseKeyEnum(BaseEnum):
    RESULTS = 'results'
    CONTEXT = 'context'
    RESPONSE_CODE = 'response_code'
    STATUS_CODE = 'status_code'
    MESSAGE = 'message'
    DETAIL = 'detail'
    TIMESTAMP = 'timestamp'
    CUSTOM_EXCEPTION = 'custom_exception'
    EXCEPTION = 'exceptions'
    INFO = 'info'
    SUCCESS = 'success'
    WARNING = 'warning'
    ERRORS = 'errors'
    ACCESS_TOKEN = 'access_token'
    REFRESH_TOKEN = 'refresh_token'
    TOKEN = 'token'
    TYPE = 'type'
    STATUS = 'status'

    @property
    def response_key(self):
        # Override response_key - convert to lowercase
        return self.name.lower()


class ResponseExceptionTypeEnum(BaseEnum):
    NOT_FOUND = 'Resource not found'
    METHOD_NOT_ALLOWED = 'Method not allowed'
    HTTP_EXCEPTION = 'HTTP Exception occurred.'
    GENERAL_EXCEPTION = 'A general exceptions occurred.'
    INVALID_VALUE_ERROR = 'Please provide a valid value.'
    INVALID_INPUT_ERROR = 'Please provide a valid input value.'
    VALUE_ERROR = 'A value error occurred.'
    VALIDATION_ERROR = 'A validation error occurred.'
    DATABASE_ERROR = 'A database error occurred.'
    AUTHENTICATION_ERROR = 'Authentication failed.'
    AUTHORIZATION_ERROR = 'Authorization failed.'
    RESOURCE_NOT_FOUND = 'Resource not found.'
    DUPLICATE_ENTRY_ERROR = 'Duplicate entry found.'
    TIMEOUT_ERROR = 'A timeout error occurred.'
    SERVER_ERROR = 'A server error occurred.'
    UNSUPPORTED_MEDIA_TYPE = 'Unsupported media type "{media_type}" in request.'
