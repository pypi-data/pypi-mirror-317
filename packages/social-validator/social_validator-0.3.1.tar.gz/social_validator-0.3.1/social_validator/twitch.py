from social_validator import shared
from social_validator.exceptions import ValidationError

# Restrictions for usernames
USERNAME_MIN_LENGTH = 4
USERNAME_MAX_LENGTH = 25

RESERVED_USERNAMES = frozenset(
    {
        "about",
        "bits",
        "blog",
        "broadcast",
        "chat",
        "clips",
        "directory",
        "downloads",
        "events",
        "following",
        "game",
        "giftcard",
        "help",
        "host",
        "jobs",
        "legal",
        "live",
        "login",
        "moderator",
        "music",
        "partner",
        "point",
        "prime",
        "privacy",
        "raid",
        "redeem",
        "search",
        "security",
        "settings",
        "signup",
        "store",
        "stream",
        "subscriptions",
        "support",
        "team",
        "twitch",
        "twitchcon",
        "turbo",
        "user",
        "videos",
    }
)

# Restrictions for description (about) field
DESCRIPTION_MAX_LENGTH = 300

# Restrictions for messages
MESSAGE_MIN_LENGTH = 1
MESSAGE_MAX_LENGTH = 500


def is_valid_username(username: str) -> bool:
    """
    Checks the given username for character correctness.
    More detailed validation criteria are described in
    :py:func:`validate_username`.

    :return: ``True``, if all the conditions are met, otherwise ``False``.
    """
    return (
        USERNAME_MIN_LENGTH <= len(username) <= USERNAME_MAX_LENGTH
        and username[0] != "_"
        and not username.isdigit()
        and shared.is_valid_id(username)
    )


def is_reserved_username(username: str) -> bool:
    """
    Checks whether the username is reserved.
    The complete list of reserved words can be viewed in the
    :py:const:`RESERVED_USERNAMES`

    :return: ``True``, if username is reserved, otherwise ``False``.
    """
    return username.lower() in RESERVED_USERNAMES


def is_valid_description(text: str) -> bool:
    """
    Checks the given text for character correctness.
    More detailed validation criteria are described in
    :py:func:`validate_description`.

    :return: ``True``, if all the conditions are met, otherwise ``False``.
    """
    return len(text) <= DESCRIPTION_MAX_LENGTH and text.isprintable()


def is_valid_message(text: str) -> bool:
    """
    Checks the given text for character correctness.
    More detailed validation criteria are described in
    :py:func:`validate_message`.

    :return: ``True``, if all the conditions are met, otherwise ``False``
    """
    return MESSAGE_MIN_LENGTH <= len(text) <= MESSAGE_MAX_LENGTH and text.isprintable()


def validate_username(username: str) -> str:
    """
    Validates a username based on the following criteria:

    - The length of the username must be 4 to 25 characters long;
    - The username must not start with an underscore;
    - The username must not consist entirely of digits;
    - The username must consist of: A-Za-z, 0-9 and underscores;
    - The username must not be a reserved word.

    All reserved words are listed in :py:const:`RESERVED_USERNAMES`

    :param username: User text ID
    :return: Input username
    :raise ValidationError: If the username does not meet the criteria
    """
    if not is_valid_username(username):
        raise ValidationError(
            "Username must be 4 to 25 characters long, exclude the underscore as the first "
            "character, and can only consist of: A-Za-z, 0-9 and underscores",
            input_value=username,
        )

    if is_reserved_username(username):
        raise ValidationError(
            "Username must not be a reserved word",
            input_value=username,
        )

    return username


def validate_description(text: str) -> str:
    """
    Validates a text based on the following criteria:

    - The text must not exceed 300 characters;
    - The text must not be escaped.

    :param text: Description text
    :return: Input text
    :raise ValidationError: if the text does not meet the criteria
    """
    if not is_valid_description(text):
        raise ValidationError(
            "Description must not exceed 300 characters and must not be escaped",
            input_value=text,
        )

    return text


def validate_message(text: str) -> str:
    """
    Validates a text based on the following criteria:

    - The text must be between 1 and 500 characters, inclusive;
    - The text must not be escaped.

    :param text: Message text
    :return: Input text
    :raise ValidationError: if the text does not meet the criteria
    """
    if not is_valid_message(text):
        raise ValidationError(
            "Message must contain between 1 and 500 characters, inclusive, "
            "and must not be escaped",
            input_value=text,
        )

    return text
