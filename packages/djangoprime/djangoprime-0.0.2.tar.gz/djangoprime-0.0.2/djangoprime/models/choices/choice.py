from django.utils.translation import gettext_lazy as _

from djangoprime.enum.models import StatusPublishTypeEnum, CustomRobotTagEnum

# List of choices for content status, representing different publication states
# These choices are used to display options for selecting content status (e.g., draft, published, withdrawn)
STATUS_CHOICES_LIST = (
    (StatusPublishTypeEnum.DRAFT.name.lower(), _(StatusPublishTypeEnum.DRAFT.value.capitalize())),  # Draft status
    (StatusPublishTypeEnum.PUBLISHED.name.lower(), _(StatusPublishTypeEnum.PUBLISHED.value.capitalize())),  # Published status
    (StatusPublishTypeEnum.WITHDRAW.name.lower(), _(StatusPublishTypeEnum.WITHDRAW.value.capitalize())),  # Withdrawn status
)

# List of choices for content status before publication, allowing selection of 'draft' or 'published'
# Used in cases where content is still in a pre-published state and needs to be either drafted or published
STATUS_CHOICES_BEFORE_PUBLICATION_LIST = (
    (StatusPublishTypeEnum.DRAFT.name.lower(), _(StatusPublishTypeEnum.DRAFT.value.capitalize())),  # Draft status
    (StatusPublishTypeEnum.PUBLISHED.name.lower(), _(StatusPublishTypeEnum.PUBLISHED.value.capitalize())),  # Published status
)

# List of choices for content status after publication, allowing selection of 'published' or 'withdrawn'
# Used when the content has already been published, and the user can choose to either keep it published or withdraw it
STATUS_CHOICES_AFTER_PUBLICATION_LIST = (
    (StatusPublishTypeEnum.PUBLISHED.name.lower(), _(StatusPublishTypeEnum.PUBLISHED.value.capitalize())),  # Published status
    (StatusPublishTypeEnum.WITHDRAW.name.lower(), _(StatusPublishTypeEnum.WITHDRAW.value.capitalize())),  # Withdrawn status
)

# List of choices for custom robot tags that define how web crawlers interact with the site.
# The choices define various options for how search engines and crawlers should handle indexing and following links.
CUSTOM_ROBOT_TAGS_CHOICES_LIST = (
    # Default tag, specifying the default behavior for robots
    (
        CustomRobotTagEnum.DEFAULT.name.lower(), (
            (CustomRobotTagEnum.DEFAULT.name.lower(), _(CustomRobotTagEnum.DEFAULT.value.lower())),  # Default setting
        )
    ),
    # 'All' tag, representing a broader set of robots directives to control indexing and following
    (
        CustomRobotTagEnum.ALL.name.lower(), (
            (CustomRobotTagEnum.ALL.name.lower(), _(CustomRobotTagEnum.ALL.value.capitalize())),  # All behavior (index, follow)
            (CustomRobotTagEnum.NOINDEX.name.lower(), _(CustomRobotTagEnum.NOINDEX.value.capitalize())),  # Do not index
            (CustomRobotTagEnum.NOFOLLOW.name.lower(), _(CustomRobotTagEnum.NOFOLLOW.value.capitalize())),  # Do not follow links
            (CustomRobotTagEnum.NONE.name.lower(), _(CustomRobotTagEnum.NONE.value.capitalize())),  # Default no robot directive
            (CustomRobotTagEnum.NOARCHIVE.name.lower(), _(CustomRobotTagEnum.NOARCHIVE.value.capitalize())),  # No archive of the page
            (CustomRobotTagEnum.NOSNIPPET.name.lower(), _(CustomRobotTagEnum.NOSNIPPET.value.capitalize())),  # No snippet in search results
            (CustomRobotTagEnum.NOODP.name.lower(), _(CustomRobotTagEnum.NOODP.value.capitalize())),  # No Open Directory title/description
            (CustomRobotTagEnum.NOTRANSLATE.name.lower(), _(CustomRobotTagEnum.NOTRANSLATE.value.capitalize())),  # Do not translate page content
            (CustomRobotTagEnum.NOIMAGEINDEX.name.lower(), _(CustomRobotTagEnum.NOIMAGEINDEX.value.capitalize())),  # Do not index images
            (CustomRobotTagEnum.UNAVAILABLE_AFTER.name.lower(), _(CustomRobotTagEnum.UNAVAILABLE_AFTER.value.capitalize())),
        # Prevent indexing after a certain time
        )
    )
)
