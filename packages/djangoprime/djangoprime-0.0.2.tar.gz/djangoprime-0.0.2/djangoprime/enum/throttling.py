from djangoprime.core.base import BaseEnum


class ThrottlingExceptionTypeEnum(BaseEnum):
    RATE_LIMIT_EXCEEDED = 'Too many requests.'
    TEMPORARY_BLOCK = 'You have been temporarily blocked from making requests.'
    PERSISTENT_BLOCK = 'Your account has been permanently blocked from making requests due to repeated violations.'
    RATE_LIMIT_RESET = 'You must wait before making additional requests. Rate limit will reset in X seconds.'
    UNAUTHORIZED_ACCESS = 'Unauthorized access attempt detected.'
    SUSPICIOUS_ACTIVITY = 'Suspicious activity detected. Please contact support.'
    API_KEY_EXCEEDED = 'API key usage limit exceeded.'
    DAILY_LIMIT_EXCEEDED = 'Daily request limit exceeded.'
    MAX_CONNECTIONS_REACHED = 'Maximum number of concurrent connections reached.'
    RATE_LIMITING_ACTIVE = 'Rate limiting is currently active. Please slow down your requests.'
    OPERATION_IN_PROGRESS = "Please wait! The operation is still in progress."
