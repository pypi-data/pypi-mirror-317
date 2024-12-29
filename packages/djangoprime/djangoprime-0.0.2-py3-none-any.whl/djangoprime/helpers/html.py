from enum import Enum
from django.utils.html import format_html


def get_view_on_site_html(url):
    """
    Generates an HTML anchor tag that links to the provided URL with the text 'View on site'.

    Args:
        url (str): The URL to be linked in the anchor tag.

    Returns:
        str: An HTML anchor tag linking to the provided URL.
    """
    # Generates an HTML link using the format_html function, which safely escapes any input.
    return format_html(f'<a href="{url}">View on site</a>')


def get_image_with_html(image_path, width=70, height=48):
    """
    Generates an HTML snippet to display an image within an anchor tag, making it clickable.
    The image is displayed with the specified width and height. The image is also styled for
    opacity and rounded corners.

    Args:
        image_path (str): The path to the image to be displayed.
        width (int, optional): The width of the image. Default is 70.
        height (int, optional): The height of the image. Default is 48.

    Returns:
        str: An HTML anchor tag containing the image, styled and with the ability to open the image in a new tab.
    """
    # Define custom styles for the anchor tag and image
    a_tag_style = 'style="background-color:#000; width:fit-content;"'  # Anchor tag style
    img_tag_style = 'style="opacity:0.75; border-radius: 5px;"'  # Image tag style

    # Generate HTML using format_html, which ensures the URL is properly escaped
    return format_html(
        f'<a href="{image_path}" {a_tag_style} target="_blank"><img {img_tag_style} src="{image_path}" height="{height}" width="{width}" /></a>'
    )


class ImageTrueFalseEnum(Enum):
    """
    Enum for representing boolean-like values using images for 'True' and 'False'.

    This Enum class uses the format_html function to return HTML images representing
    a 'True' or 'False' state, suitable for use in Django admin or other templates.

    Attributes:
        TRUE (str): HTML image tag for the "True" state (a green check icon).
        FALSE (str): HTML image tag for the "False" state (a red cross icon).
    """
    TRUE = format_html('<img src="/static/admin/img/icon-yes.svg">')  # Image representing "True"
    FALSE = format_html('<img src="/static/admin/img/icon-no.svg" />')  # Image representing "False"
