from django.contrib import admin
from djangoprime.enum.models import StatusPublishTypeEnum


# Action to mark selected items as 'draft'
@admin.action(description='Mark selected items as draft')
def make_draft(modeladmin, request, queryset):
    """
    Custom admin action to update the status of selected items to 'draft'.

    Args:
        modeladmin: The model admin class that handles the request.
        request: The HTTP request object that contains metadata about the request.
        queryset: A QuerySet of the selected items in the admin list view.

    This action updates the 'status' field of the selected items in the queryset
    to 'draft'. The status value is retrieved from the StatusPublishTypeEnum.
    """
    updated = queryset.update(status=StatusPublishTypeEnum.DRAFT.name.lower())
    # Optionally, you can log the number of updated items
    # print(f'{updated} items marked as draft.')


# Action to mark selected items as 'published'
@admin.action(description='Mark selected items as published')
def make_published(modeladmin, request, queryset):
    """
    Custom admin action to update the status of selected items to 'published'.

    Args:
        modeladmin: The model admin class that handles the request.
        request: The HTTP request object that contains metadata about the request.
        queryset: A QuerySet of the selected items in the admin list view.

    This action updates the 'status' field of the selected items in the queryset
    to 'published'. The status value is retrieved from the StatusPublishTypeEnum.
    """
    updated = queryset.update(status=StatusPublishTypeEnum.PUBLISHED.name.lower())
    # Optionally, you can log the number of updated items
    # print(f'{updated} items marked as published.')


# Action to mark selected items as 'withdrawn'
@admin.action(description='Mark selected items as withdraw')
def make_withdraw(modeladmin, request, queryset):
    """
    Custom admin action to update the status of selected items to 'withdrawn'.

    Args:
        modeladmin: The model admin class that handles the request.
        request: The HTTP request object that contains metadata about the request.
        queryset: A QuerySet of the selected items in the admin list view.

    This action updates the 'status' field of the selected items in the queryset
    to 'withdrawn'. The status value is retrieved from the StatusPublishTypeEnum.
    """
    updated = queryset.update(status=StatusPublishTypeEnum.WITHDRAW.name.lower())
    # Optionally, you can log the number of updated items
    # print(f'{updated} items marked as withdrawn.')
