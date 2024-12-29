from djangoprime.core.base import BaseEnum


class PermissionExceptionTypeEnum(BaseEnum):
    PERMISSION_DENIED = 'You do not have permission to perform this action.'
    PERMISSION_REQUIRED = 'Permission is required to access this resource.'
    ACCESS_RESTRICTED = 'Access to this resource is restricted.'
    ROLE_NOT_AUTHORIZED = 'The role associated with your account does not have the necessary authorization.'
    INSUFFICIENT_PRIVILEGES = 'Your account does not have sufficient privileges to perform this action.'
    RESOURCE_LOCKED = 'The resource is locked and cannot be accessed at this time.'
