from social_validator import youtube
from tests.shared.input import ESCAPED_STRING, RANDOM_UNICODE_STRING

VALID_STRICT_USERNAMES = (
    "t" * youtube.USERNAME_MIN_LENGTH,
    "t" * youtube.USERNAME_MAX_LENGTH,
    "1test",
    "1test1",
    "1test-",
    "1TEST-",
    "1test-----",
    "1test-----____",
    "1test-----____----",
    "1test-----___asd_--123--",
    "1test-----___asd_--.123--",
    "1test-----___asd_....123--",
    "-------___asd_....123--",
    "__-----___asd_....123--",
    "__-----___asd_....123--",
    "__--____",
    "__-",
    "___",
    "---",
    "1.....",
    "2.....----____",
    "----____......",
)
VALID_SOFT_USERNAMES = (
    ('-' * 100) + 'tes',
    ('-' * 100) + 'test',
    ('-' * 100) + 'TEST',
    ('-' * 100) + 'test.',
    ('-' * 100) + 'test___----',
    ('-' * 100) + 'test' + ('-' * 100),
    ('-' * 100) + 'test' + ('_' * 100),
    ('-' * 100) + '1..' + ('_' * 100),
    ('-' * 100) + '2-._._-' + ('_' * 100),
)
INVALID_SOFT_USERNAMES = (
    '',
    '---___---',
    '___---',
    '--a',
    ('_' * 100) + ('a' * (youtube.USERNAME_MIN_LENGTH - 1)),
    ('_' * 100) + ('a' * (youtube.USERNAME_MAX_LENGTH + 1)),
    ('-' * 100) + ('a' * (youtube.USERNAME_MIN_LENGTH - 1)),
    ('-' * 100) + ('a' * (youtube.USERNAME_MAX_LENGTH + 1)),
    ('_' * 100) + ('1' * (youtube.USERNAME_MIN_LENGTH - 1)),
    ('-' * 100) + ('1' * (youtube.USERNAME_MAX_LENGTH + 1)),
    RANDOM_UNICODE_STRING,
    ESCAPED_STRING,
)
INVALID_STRICT_USERNAMES = (
    '',
    't' * (youtube.USERNAME_MIN_LENGTH - 1),
    't' * (youtube.USERNAME_MAX_LENGTH + 1),
    '.' * youtube.USERNAME_MIN_LENGTH,
    '......1',
    '.____',
    '.----',
    '.____----',
    '.____----123',
    '.____----123test',
    RANDOM_UNICODE_STRING,
    ESCAPED_STRING,
)

VALID_VIDEO_IDS = (
    '1asdfgher14',
    '1asdfgher--',
    '1asdfgh__--',
    '-asdfgh__--',
    '_asdfgh__--',
    '___----__--',
    '___----__-1',
    '___----__-a',
    '___----__a1',
    '___--a-__a1',
)
INVALID_VIDEO_IDS = (
    '',
    'a' * (youtube.VIDEO_ID_LENGTH - 1),
    'a' * (youtube.VIDEO_ID_LENGTH + 1),
    'a.12ijd2h3j',
    'a=12ijd2h3j',
    'a+12ijd2h3j',
    'a!12ijd2h3j',
    'a@12ijd2h3j',
    'a#12ijd2h3j',
    'a$12ijd2h3j',
    'a%12ijd2h3j',
    'a&12ijd2h3j',
    'a?12ijd2h3j',
    'a*12ijd2h3j',
    'a<>()d2h3j',
    RANDOM_UNICODE_STRING[:youtube.VIDEO_ID_LENGTH],
    (ESCAPED_STRING * 2)[:youtube.VIDEO_ID_LENGTH],
)

VALID_VIDEO_NAMES = (
    'a' * youtube.VIDEO_NAME_MIN_LENGTH,
    'a' * youtube.VIDEO_NAME_MAX_LENGTH,
    RANDOM_UNICODE_STRING,
)
INVALID_VIDEO_NAMES = (
    '',
    'a' * (youtube.VIDEO_NAME_MIN_LENGTH - 1),
    'a' * (youtube.VIDEO_NAME_MAX_LENGTH + 1),
    '<',
    '>',
    ESCAPED_STRING,
)

VALID_VIDEO_DESCRIPTIONS = (
    '',
    'a' * youtube.VIDEO_DESCRIPTION_MAX_LENGTH,
    RANDOM_UNICODE_STRING,
)
VALID_VIDEO_DESCRIPTIONS_SHORT = (
    '',
    'a' * youtube.VIDEO_DESCRIPTION_SHORT_MAX_LENGTH,
    RANDOM_UNICODE_STRING,
)
INVALID_VIDEO_DESCRIPTIONS = (
    'a' * (youtube.VIDEO_DESCRIPTION_MAX_LENGTH + 1),
    '<',
    '>',
    ESCAPED_STRING,
)
INVALID_VIDEO_DESCRIPTIONS_SHORT = (
    'a' * (youtube.VIDEO_DESCRIPTION_SHORT_MAX_LENGTH + 1),
    '<',
    '>',
    ESCAPED_STRING,
)

VALID_VIDEO_COMMENTS = (
    'a' * youtube.VIDEO_COMMENT_MIN_LENGTH,
    'a' * youtube.VIDEO_COMMENT_MAX_LENGTH,
    RANDOM_UNICODE_STRING,
)
INVALID_VIDEO_COMMENTS = (
    '',
    'a' * (youtube.VIDEO_COMMENT_MIN_LENGTH - 1),
    'a' * (youtube.VIDEO_COMMENT_MAX_LENGTH + 1),
    ESCAPED_STRING,
)

# combine a lower and upper case
RESERVED_USERNAMES = list(youtube.RESERVED_USERNAMES) + [w.upper() for w in youtube.RESERVED_USERNAMES]
