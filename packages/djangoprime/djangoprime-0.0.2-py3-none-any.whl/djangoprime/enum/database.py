from djangoprime.core.base import BaseEnum


class DatabaseExceptionEnum(BaseEnum):
    DATABASE_NOT_FOUND = 'Database not found'
    DATABASE_NOT_SUPPORTED = 'Database not supported'
    DATABASE_INVALID = 'Database invalid'
    DATABASE_INVALID_PASSWORD = 'Database invalid password'
    DATABASE_INVALID_USERNAME = 'Database invalid username'
    DATABASE_INVALID_EMAIL = 'Database invalid email'
    DATA_FETCH_FAILED = 'Failed to fetch data from database'
    CONNECTION_FAILED = 'Database connection failed'
    QUERY_EXECUTION_FAILED = 'Query execution failed'
    RECORD_NOT_FOUND = 'Record not found'
    DATA_VALIDATION_FAILED = 'Data validation failed'
    DATA_CONFLICT = 'Data conflict'
    TIMEOUT_ERROR = 'Database operation timed out'
    UNAUTHORIZED_ACCESS = 'Unauthorized access to the database'
    INSUFFICIENT_PRIVILEGES = 'Insufficient privileges for this operation'
    TRANSACTION_FAILED = 'Transaction failed'
    INVALID_QUERY = 'Invalid database query'
