from social_validator import twitch
from tests.shared.input import ESCAPED_STRING, RANDOM_UNICODE_STRING

VALID_USERNAMES = {
    "a" * twitch.USERNAME_MIN_LENGTH,
    "a" * twitch.USERNAME_MAX_LENGTH,
    "a123",
    "123a",
    "a_12",
    "username",
    "user_name",
    "user___name",
    "u_s_e_r_n_a_m_e",
    "u_1_2_3_4_5_6",
    "username_______",
}

INVALID_USERNAMES = {
    "",  # empty
    "a" * (twitch.USERNAME_MIN_LENGTH - 1),  # too short
    "a" * (twitch.USERNAME_MAX_LENGTH + 1),  # too long
    "_username",  # starts with underscore
    "_" * twitch.USERNAME_MIN_LENGTH,  # consist entirely of special chars
    "123456",  # consist entirely of digits
    "user name",  # special char
    "username@",  # special char
    RANDOM_UNICODE_STRING,  # invalid chars
    ESCAPED_STRING,  # escaped chars
}

VALID_DESCRIPTIONS = {
    "",
    "a",
    "1" * twitch.DESCRIPTION_MAX_LENGTH,
    RANDOM_UNICODE_STRING,
}

INVALID_DESCRIPTIONS = {
    "1" * (twitch.DESCRIPTION_MAX_LENGTH + 1),  # too long
    ESCAPED_STRING,  # escaped chars
}

VALID_MESSAGES = {
    "a",
    "1" * twitch.MESSAGE_MAX_LENGTH,
    RANDOM_UNICODE_STRING,
}

INVALID_MESSAGES = {
    "",  # empty
    "1" * (twitch.MESSAGE_MAX_LENGTH + 1),  # too long
    ESCAPED_STRING,  # escaped chars
}

# Combine lower and upper cases
RESERVED_USERNAMES = list(twitch.RESERVED_USERNAMES) + [
    word.upper() for word in twitch.RESERVED_USERNAMES
]
