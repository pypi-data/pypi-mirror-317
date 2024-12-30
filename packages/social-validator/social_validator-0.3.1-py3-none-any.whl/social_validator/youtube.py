from social_validator import shared
from social_validator.exceptions import ValidationError

# Restrictions for username
USERNAME_MIN_LENGTH = 3
USERNAME_MAX_LENGTH = 30

# YouTube has two types of links leading to a channel.
# The first type is displayed with an "@" symbol and contains the exact address
# with hyphens, underscores, and dots.
# The second type doesn't contain the "@" symbol and ignores any hyphens and
# underscores. The dots in this type also have significance.
_IGNORED_CHARACTERS = frozenset(("_", "-"))

RESERVED_USERNAMES = frozenset(
    (
        "blog",
        "browse",
        "channels",
        "explore",
        "favorites",
        "feed",
        "gaming",
        "help",
        "kids",
        "live",
        "logout",
        "movies",
        "music",
        "playlist",
        "search",
        "settings",
        "signin",
        "signup",
        "sports",
        "support",
        "trending",
        "upload",
        "video",
        "videos",
        "watch",
    )
)

# Restriction for videos
VIDEO_ID_LENGTH = 11
VIDEO_NAME_MIN_LENGTH = 1
VIDEO_NAME_MAX_LENGTH = 100
VIDEO_DESCRIPTION_SHORT_MAX_LENGTH = 135
VIDEO_DESCRIPTION_MAX_LENGTH = 5000
VIDEO_COMMENT_MIN_LENGTH = 1
VIDEO_COMMENT_MAX_LENGTH = 10000


def _replace_ignored_chars(s: str, replace: str) -> str:
    """
    Replaces all characters from the :py:const:`_IGNORED_CHARACTERS` with the
    specified one.
    """
    for char in _IGNORED_CHARACTERS:
        s = s.replace(char, replace)

    return s


def _contains_angle_brackets(s: str) -> bool:
    """
    Checks for the presence of angle brackets within a string.
    """
    return '>' in s or '<' in s


def _is_valid_text(text: str) -> bool:
    """
    Checks the text for compliance with YouTube restrictions.
    """
    return not _contains_angle_brackets(text) and text.isprintable()


def is_valid_username(username: str, *, strct: bool = True) -> bool:
    """
    Checks the given username for length restrictions and character correctness.
    More detailed validation criteria are described in
    :py:func:`validate_username`.

    :return: ``True``, if all the conditions are met, otherwise ``False``.
    """
    username = _replace_ignored_chars(username, "_" if strct else "")

    return (
        USERNAME_MIN_LENGTH <= len(username) <= USERNAME_MAX_LENGTH
        and username[0] != "."
        and not username.isdigit()
        and shared.is_valid_id(username.replace(".", "_"))
    )


def is_reserved_username(username: str) -> bool:
    """
    Checks whether the username is reserved.
    Case-insensitive.

    Refer to the :py:const:`RESERVED_USERNAMES` for the complete list of words.

    :return: ``True`` if **username** is reserved, ``False`` otherwise
    """
    return username.lower() in RESERVED_USERNAMES


def is_valid_video_id(_id: str) -> bool:
    """
    Checks the given ID for length restrictions and character correctness.
    More detailed validation criteria are described in
    :py:func:`validate_video_id`.

    :return: ``True``, if all the conditions are met, otherwise ``False``.
    """
    return (
        len(_id) == VIDEO_ID_LENGTH
        and shared.is_valid_id(_id.replace('-', '_'))
    )


def is_valid_video_name(text: str) -> bool:
    """
    Checks the given text for length restrictions and character correctness.
    More detailed validation criteria are described in
    :py:func:`validate_video_name`.

    :return: ``True``, if all the conditions are met, otherwise ``False``.
    """
    return (
        VIDEO_NAME_MIN_LENGTH <= len(text) <= VIDEO_NAME_MAX_LENGTH
        and _is_valid_text(text)
    )


def is_valid_video_comment(text: str) -> bool:
    """
    Checks the given text for length restrictions and character correctness.
    More detailed validation criteria are described in
    :py:func:`validate_video_comment`.

    :return: ``True``, if all the conditions are met, otherwise ``False``.
    """
    return (
        VIDEO_COMMENT_MIN_LENGTH <= len(text) <= VIDEO_COMMENT_MAX_LENGTH
        and text.isprintable()
    )


def is_valid_video_description(text: str, *, short: bool = False) -> bool:
    """
    Checks the given text for character correctness.
    More detailed validation criteria are described in
    :py:func:`validate_video_description`.

    :return: ``True``, if all the conditions are met, otherwise ``False``.
    """
    return (
        len(text) <= (VIDEO_DESCRIPTION_MAX_LENGTH if not short else VIDEO_DESCRIPTION_SHORT_MAX_LENGTH)
        and _is_valid_text(text)
    )


def validate_username(username: str, *, strict: bool = True) -> str:
    """
    Validates a username based on the following criteria:

    - It contains between 3 and 30 characters, inclusively;
    - It consist of A-Za-z, digits, hyphens, underscores, and dots;
    - It doesn't start with a dot;
    - It is not entirely composed of digits;
    - It is not a reserved word.

    All reserved words are listed in :py:const:`RESERVED_USERNAMES`

    It is important to highlight the "strict" argument. It determines whether
    the strict validation will be enabled or not.
    When it is enabled, the validation will be strict and all characters will
    be preserved.
    When it is disabled, a soft validation will be performed,
    ignoring dashes and underscores.

    This is due to the specific algorithms used by YouTube. When following a
    link that includes the "@" symbol, a strict search will be conducted.
    Otherwise, a soft search will be used.

    :param username: User text ID
    :param strict: Is the username includes "@" symbol
    :return: Input username, converted to lower-case. If the strict mode is
        disabled, all hyphens and underscores will be removed.
    :raise ValidationError: If the username doesn't meet the criteria
    """
    if not is_valid_username(username, strct=strict):
        raise ValidationError(
            f"Username must have between {USERNAME_MIN_LENGTH} and "
            f"{USERNAME_MAX_LENGTH} characters, including hyphens, "
            "underscores and dots, can't consist entirely of numbers, and can't "
            "start with a dot",
            input_value=username,
            strict=strict,
        )
    elif is_reserved_username(username):
        raise ValidationError(
            "Username must not be a reserved word",
            input_value=username,
            strict=strict,
        )

    if not strict:
        # Replace them because they are not considered by YouTube
        username = _replace_ignored_chars(username, "")

    return username.lower()


def validate_video_id(_id: str) -> str:
    """
    Validates a URL based on the following criteria:

    - It has a length of 11 characters;
    - It only contains the characters A-Za-z, 0-9, dashes, and underscores.

    :param _id: Value that stored in the argument "v" (/watch?v=)
    :return: Input value
    :raise ValidationError: If the URL doesn't meet the criteria
    """
    if not is_valid_video_id(_id):
        raise ValidationError(
            f'The ID must be exactly {VIDEO_ID_LENGTH} characters long and '
            f'can only contain alphanumeric characters (A-Z, a-z, 0-9), '
            f'dashes, and underscores',
            input_value=_id,
        )

    return _id


def validate_video_name(text: str) -> str:
    """
    Validates a text based on the following criteria:

    - It has a length of 1 to 100 characters, inclusive;
    - It consists of displayable characters;
    - It not contains angle brackets (>, <) within it.

    :param text: Video name
    :return: Input value
    :raise ValidationError: If the text doesn't meet the criteria
    """
    if not is_valid_video_name(text):
        raise ValidationError(
            f'The video name must have a length of {VIDEO_NAME_MIN_LENGTH} to '
            f'{VIDEO_NAME_MAX_LENGTH} characters, consist of displayable '
            f'characters and not have angle brackets within it',
            input_value=text,
        )

    return text


def validate_video_description(text: str, *, short: bool = False) -> str:
    """
    Validates a text based on the following criteria:

    - It has a length up to 5000 (or 135 for short) characters long;
    - it consists of displayable characters;
    - It not contains angle brackets (>, <) within it.

    :param text: Description text
    :param short: Is it short version
    :return: Input value
    :raise ValidationError: If the text doesn't meet the criteria
    """
    if not is_valid_video_description(text, short=short):
        raise ValidationError(
            f'The video description must be up to '
            f'{VIDEO_DESCRIPTION_MAX_LENGTH if not short else VIDEO_DESCRIPTION_SHORT_MAX_LENGTH} '
            f'characters long, not contain angle brackets, '
            f'and not have escaped characters or other special characters',
            input_value=text,
            short=short,
        )

    return text


def validate_video_comment(text: str) -> str:
    """
    Validates a text based on the following criteria:

    - It has a length of 1 to 10000 characters, inclusive;
    - it consists of displayable characters;

    :param text: Comment text
    :return: Input value
    :raise ValidationError: If the text doesn't meet the criteria
    """
    if not is_valid_video_comment(text):
        raise ValidationError(
            f'The video comment must have a length of '
            f'{VIDEO_COMMENT_MIN_LENGTH} to {VIDEO_COMMENT_MAX_LENGTH} '
            f'characters and consist of displayable characters',
            input_value=text,
        )

    return text
