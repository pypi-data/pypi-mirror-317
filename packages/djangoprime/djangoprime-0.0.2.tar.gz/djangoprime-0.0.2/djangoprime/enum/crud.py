from djangoprime.core.base import BaseEnum


class CreateResponseCodeEnum(BaseEnum):
    CREATE_SUCCESS = 'New record created successfully.'
    NEW_REQUEST_CREATED = 'New request created successfully.'
    REQUEST_CREATED = 'Request created successfully.'
    TASK_CREATED = 'Task created successfully.'
    NEW_TASK_CREATED = 'New task created successfully.'
    TRANSACTION_SUCCESS = 'Transaction successfully completed.'
    INVALID_DATA_PROVIDED = 'You provided invalid data. Please try again.'
    DUPLICATE_ENTRY = 'This entry already exists.'


class UpdateResponseCodeEnum(BaseEnum):
    UPDATE_SUCCESS = 'Record updated successfully.'
    REQUEST_UPDATED = 'Request updated successfully.'
    TASK_UPDATED = 'Task updated successfully.'
    TRANSACTION_UPDATED = 'Transaction successfully updated.'
    INVALID_UPDATE_DATA = 'You provided invalid data for update. Please try again.'
    NO_CHANGES_DETECTED = 'No changes were detected in the provided update data.'
    UPDATE_FAILED = 'Failed to update the record. Please try again.'
    ENTRY_NOT_FOUND = 'The entry you are trying to update does not exist.'


class DeleteResponseCodeEnum(BaseEnum):
    DELETE_SUCCESS = 'Record deleted successfully.'
    REQUEST_DELETED = 'Request deleted successfully.'
    TASK_DELETED = 'Task deleted successfully.'
    TRANSACTION_DELETED = 'Transaction successfully deleted.'
    DELETE_FAILED = 'Failed to delete the record. Please try again.'
    ENTRY_NOT_FOUND = 'The entry you are trying to delete does not exist.'
    UNAUTHORIZED_DELETE = 'You are not authorized to delete this record.'
    DELETE_CONFLICT = 'Cannot delete the record due to a conflict.'


class LoginResponseCodeEnum(BaseEnum):
    LOGIN_SUCCESS = 'Login successful.'
    LOGIN_FAILED = "You're now logged in."


class PasswordResponseCodeEnum(BaseEnum):
    PASSWORD_CHANGED_SUCCESS = 'Password changed successfully.'
