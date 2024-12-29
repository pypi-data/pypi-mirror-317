from enum import Enum, unique


@unique
class BaseEnum(str, Enum):
    """
    A custom Enum class that inherits from both `str` and `Enum`.

    This class overrides the default string representation and provides
    properties to generate response keys from enum names.
    """

    def __str__(self):
        """
        Override the string representation to return the enum value with title case.

        Returns:
            str: The title-cased value of the enum.
        """
        return self.value.title()

    @property
    def response_key(self):
        """
        Generate a response key by converting the enum name to lowercase
        and replacing underscores with double underscores.

        Returns:
            str: The formatted response key.
        """
        return self.name.lower().replace("_", "__")

    @property
    def name_key(self):
        """
        Generate a lowercase version of the enum name.

        Returns:
            str: The lowercase enum name.
        """
        return self.name.lower()
