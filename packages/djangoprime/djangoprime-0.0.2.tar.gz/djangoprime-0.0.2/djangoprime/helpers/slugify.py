from django.template import defaultfilters
from django.utils.text import slugify
from unidecode import unidecode


def create_slug_by_name(instance, sender, new_slug=None):
    """
    Creates a slug based on the 'name' attribute of the instance. If the generated slug already exists,
    it appends the ID of the first object with the same slug to create a unique slug.

    Args:
        instance (model instance): The instance for which the slug is being generated. It must have a 'name' attribute.
        sender (model class): The model class to check for existing slugs.
        new_slug (str, optional): A custom slug value to override the generated one. Defaults to None.

    Returns:
        str: A unique slug generated from the instance's name.
    """
    # Truncate the name if it exceeds 65 characters
    name = instance.name[:65] if len(instance.name) > 65 else instance.name

    # Normalize the name by removing diacritical marks (e.g., accents) and then convert it to a slug
    my_slug = defaultfilters.slugify(unidecode(name))

    # Use Django's slugify function to generate the slug
    slug = slugify(my_slug, allow_unicode=True)

    # If a custom slug is provided, use it instead
    if new_slug is not None:
        slug = new_slug

    # Check if the generated slug already exists and if so, append the ID of the first matching object
    if sender.objects.filter(slug=slug).order_by('id').exists():
        new_slug = "%s-%s" % (slug, sender.objects.filter(slug=slug).first().id)
        # Recursively call the function with the new slug to ensure uniqueness
        return create_slug_by_name(instance, sender, new_slug=new_slug.lower())

    return slug


def create_slug_by_heading(instance, sender, new_slug=None):
    """
    Creates a slug based on the 'heading' attribute of the instance. Similar to the `create_slug_by_name` function,
    it ensures that the slug is unique by appending the ID of the first object with the same slug if needed.

    Args:
        instance (model instance): The instance for which the slug is being generated. It must have a 'heading' attribute.
        sender (model class): The model class to check for existing slugs.
        new_slug (str, optional): A custom slug value to override the generated one. Defaults to None.

    Returns:
        str: A unique slug generated from the instance's heading.
    """
    # Truncate the heading if it exceeds 65 characters
    heading = instance.name[:65] if len(instance.heading) > 65 else instance.heading

    # Normalize the heading by removing diacritical marks and convert it to a slug
    my_slug = defaultfilters.slugify(unidecode(heading))

    # Use Django's slugify function to generate the slug
    slug = slugify(my_slug, allow_unicode=True)

    # If a custom slug is provided, use it instead
    if new_slug is not None:
        slug = new_slug

    # Check if the generated slug already exists and if so, append the ID of the first matching object
    if sender.objects.filter(slug=slug).order_by('id').exists():
        new_slug = "%s-%s" % (slug, sender.objects.filter(slug=slug).first().id)
        # Recursively call the function with the new slug to ensure uniqueness
        return create_slug_by_heading(instance, sender, new_slug=new_slug.lower())

    return slug


def create_slug_by_title(instance, sender, new_slug=None):
    """
    Creates a slug based on the 'title' attribute of the instance. Similar to the `create_slug_by_name` and
    `create_slug_by_heading` functions, it ensures the generated slug is unique by appending the ID of the first
    object with the same slug if necessary.

    Args:
        instance (model instance): The instance for which the slug is being generated. It must have a 'title' attribute.
        sender (model class): The model class to check for existing slugs.
        new_slug (str, optional): A custom slug value to override the generated one. Defaults to None.

    Returns:
        str: A unique slug generated from the instance's title.
    """
    # Truncate the title if it exceeds 65 characters
    title = instance.title[:65] if len(instance.title) > 65 else instance.title

    # Normalize the title by removing diacritical marks and convert it to a slug
    my_slug = defaultfilters.slugify(unidecode(title))

    # Use Django's slugify function to generate the slug
    slug = slugify(my_slug, allow_unicode=True)

    # If a custom slug is provided, use it instead
    if new_slug is not None:
        slug = new_slug

    # Check if the generated slug already exists and if so, append the ID of the first matching object
    if sender.objects.filter(slug=slug).order_by('id').exists():
        new_slug = "%s-%s" % (slug, sender.objects.filter(slug=slug).first().id)
        # Recursively call the function with the new slug to ensure uniqueness
        return create_slug_by_title(instance, sender, new_slug=new_slug.lower())

    return slug
