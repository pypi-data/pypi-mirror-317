from djangoprime.core.base import BaseEnum


class GeolocationProviderEnum(BaseEnum):
    """
    Enum class that defines common geolocation providers.

    This enum represents different types of geolocation providers that can be used
    to determine the location of a user or device. It includes both well-known services
    like Google Maps and OpenStreetMap, as well as more specialized ones like GeoIP.
    """
    GEOIP = "GeoIP"  # Geolocation based on IP address
    GPS = "GPS"  # Geolocation using Global Positioning System
    WIFI = "WiFi"  # Geolocation based on WiFi access points
    CELLULAR = "Cellular"  # Geolocation based on cellular network signals
    IP2LOCATION = "IP2Location"  # IP2Location geolocation service
    GOOGLE_MAPS = "Google Maps"  # Google Maps geolocation service
    OPENSTREETMAP = "OpenStreetMap"  # OpenStreetMap geolocation service
    MAXMIND = "MaxMind"  # MaxMind geolocation service
    BING_MAPS = "Bing Maps"  # Bing Maps geolocation service
    HERE = "HERE"  # HERE geolocation service
    IPINFO = "IPInfo"  # IPInfo geolocation service
    IPSTACK = "IPStack"  # IPStack geolocation service
    OTHER = "Other"  # For any other provider not listed


class CustomRobotTagEnum(BaseEnum):
    """
    Enum class that defines the available options for the custom_robot_tags field.

    This enum is used to specify different types of metadata that can be included in
    robots.txt or meta tags for controlling how search engines and web crawlers interact
    with the website. It provides common tags used for indexing, following links,
    and other directives.
    """
    DEFAULT = 'default'  # Default setting for robots
    ALL = 'all'  # Allow all actions (index, follow)
    NOINDEX = 'noindex'  # Do not index the page
    NOFOLLOW = 'nofollow'  # Do not follow links on the page
    NONE = 'none'  # No robots directive (default behavior for some crawlers)
    NOARCHIVE = 'noarchive'  # Prevent storing a cached copy of the page
    NOSNIPPET = 'nosnippet'  # Prevent showing a snippet in search results
    NOODP = 'noodp'  # Prevent using the Open Directory Project title/description
    NOTRANSLATE = 'notranslate'  # Prevent translation of the page
    NOIMAGEINDEX = 'noimageindex'  # Prevent indexing of images on the page
    UNAVAILABLE_AFTER = 'unavailable_after'  # Prevent indexing after a certain time


class StatusPublishTypeEnum(BaseEnum):
    """
    Enum class that defines the possible status types for publication.

    This enum is used to track the status of content or items, specifically for
    determining if the content is in a draft, published, or withdrawn state.
    It is helpful for content management and workflow processes.
    """
    DRAFT = 'draft'  # Item is in draft, not published
    PUBLISHED = 'published'  # Item is published and visible to users
    WITHDRAW = 'withdraw'  # Item has been withdrawn, not available


class AdsStatus(BaseEnum):
    """
    Enum class that defines the possible statuses for advertisements.

    This enum is used to manage the state of advertisements within a system,
    whether they are active (open), inactive (stopped), or automatically managed (auto).
    """
    AUTO = 'auto'  # Advertisement status managed automatically
    OPEN = 'open'  # Advertisement is open and visible to users
    STOP = 'stop'  # Advertisement is stopped and not visible


class BlockAndFlaggedEnum(BaseEnum):
    """
    Enum class that defines various types of flagged content reasons.

    This enum is used to categorize different types of flagged or blocked content,
    such as adult content, spam, hate speech, and other harmful or inappropriate material.
    It is useful for moderation, reporting, or filtering content.
    """
    ADULT = 'Adult content'  # Content flagged as adult material
    COPYRIGHT = 'Copyright & Duplicate issue'  # Content flagged for copyright issues or duplication
    HATEFUL = 'Hateful or abusive content'  # Content flagged for hate speech or abuse
    HARMFUL = 'Harmful or dangerous acts'  # Content flagged for promoting harmful behavior
    SPAM = 'Spam, Suspicious, fake or misleading'  # Content flagged as spam or misleading
    UNCLEAR = 'Unclear'  # Content flagged as unclear or ambiguous
    OFFENSIVE = 'Offensive'  # Content flagged for offensive language or actions
    UNRELATED = 'Unrelated'  # Content flagged as unrelated to its context or topic
    OTHER = 'Other'  # For any other content not listed in the categories above
