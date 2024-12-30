import pytest as pytest
from assertpy import assert_that

from social_validator import youtube
from social_validator.exceptions import ValidationError
from tests.youtube import input


@pytest.mark.parametrize('username', input.VALID_STRICT_USERNAMES)
def test_valid_strict_username(username: str) -> None:
    assert_that(youtube.validate_username(username, strict=True)).is_equal_to(username.lower())


@pytest.mark.parametrize('username', input.VALID_SOFT_USERNAMES)
def test_valid_soft_username(username: str) -> None:
    expected = username.replace('-', '').replace('_', '').lower()
    assert_that(youtube.validate_username(username, strict=False)).is_equal_to(expected)


@pytest.mark.parametrize('username', input.INVALID_STRICT_USERNAMES)
def test_invalid_strict_username(username: str) -> None:
    with pytest.raises(ValidationError) as e:
        youtube.validate_username(username, strict=True)
    assert_that(e.value.input_value).is_equal_to(username)
    assert_that(e.value.arguments).contains('strict')


@pytest.mark.parametrize('username', input.INVALID_SOFT_USERNAMES)
def test_invalid_soft_username(username: str) -> None:
    with pytest.raises(ValidationError) as e:
        youtube.validate_username(username, strict=False)
    assert_that(e.value.input_value).is_equal_to(username)
    assert_that(e.value.arguments).contains('strict')


@pytest.mark.parametrize('username', input.RESERVED_USERNAMES)
def test_reserved_username(username: str) -> None:
    with pytest.raises(ValidationError) as e:
        youtube.validate_username(username)
    assert_that(e.value.input_value).is_equal_to(username)


@pytest.mark.parametrize('_id', input.VALID_VIDEO_IDS)
def test_valid_video_id(_id: str) -> None:
    assert_that(youtube.validate_video_id(_id)).is_equal_to(_id)


@pytest.mark.parametrize('_id', input.INVALID_VIDEO_IDS)
def test_invalid_video_id(_id: str) -> None:
    with pytest.raises(ValidationError) as e:
        youtube.validate_video_id(_id)
    assert_that(e.value.input_value).is_equal_to(_id)


@pytest.mark.parametrize('text', input.VALID_VIDEO_NAMES)
def test_valid_video_name(text: str) -> None:
    assert_that(youtube.validate_video_name(text)).is_equal_to(text)


@pytest.mark.parametrize('text', input.INVALID_VIDEO_NAMES)
def test_invalid_video_name(text: str) -> None:
    with pytest.raises(ValidationError) as e:
        youtube.validate_video_name(text)
    assert_that(e.value.input_value).is_equal_to(text)


@pytest.mark.parametrize('text', input.VALID_VIDEO_DESCRIPTIONS)
def test_valid_video_description(text: str) -> None:
    assert_that(youtube.validate_video_description(text, short=False)).is_equal_to(text)


@pytest.mark.parametrize('text', input.VALID_VIDEO_DESCRIPTIONS_SHORT)
def test_valid_video_description_short(text: str) -> None:
    assert_that(youtube.validate_video_description(text, short=True)).is_equal_to(text)


@pytest.mark.parametrize('text', input.INVALID_VIDEO_DESCRIPTIONS)
def test_invalid_video_description(text: str) -> None:
    with pytest.raises(ValidationError) as e:
        youtube.validate_video_description(text, short=False)
    assert_that(e.value.input_value).is_equal_to(text)
    assert_that(e.value.arguments).contains('short')


@pytest.mark.parametrize('text', input.INVALID_VIDEO_DESCRIPTIONS_SHORT)
def test_invalid_video_description_short(text: str) -> None:
    with pytest.raises(ValidationError) as e:
        youtube.validate_video_description(text, short=True)
    assert_that(e.value.input_value).is_equal_to(text)
    assert_that(e.value.arguments).contains('short')


@pytest.mark.parametrize('text', input.VALID_VIDEO_COMMENTS)
def test_valid_video_comment(text: str) -> None:
    assert_that(youtube.validate_video_comment(text)).is_equal_to(text)


@pytest.mark.parametrize('text', input.INVALID_VIDEO_COMMENTS)
def test_invalid_video_comment(text: str) -> None:
    with pytest.raises(ValidationError) as e:
        assert_that(youtube.validate_video_comment(text))
    assert_that(e.value.input_value).is_equal_to(text)
