import pytest
from assertpy import assert_that

from social_validator import twitch
from social_validator.exceptions import ValidationError
from tests.twitch import input


@pytest.mark.parametrize("username", input.VALID_USERNAMES)
def test_valid_username(username: str) -> None:
    assert_that(twitch.validate_username(username)).is_equal_to(username)


@pytest.mark.parametrize("username", input.INVALID_USERNAMES)
def test_invalid_username(username: str) -> None:
    with pytest.raises(ValidationError):
        twitch.validate_username(username)


@pytest.mark.parametrize("username", input.RESERVED_USERNAMES)
def test_reserved_username(username: str) -> None:
    with pytest.raises(ValidationError):
        twitch.validate_username(username)


@pytest.mark.parametrize("text", input.VALID_DESCRIPTIONS)
def test_valid_description(text: str) -> None:
    assert_that(twitch.validate_description(text)).is_equal_to(text)


@pytest.mark.parametrize("text", input.INVALID_DESCRIPTIONS)
def test_invalid_description(text: str) -> None:
    with pytest.raises(ValidationError):
        twitch.validate_description(text)


@pytest.mark.parametrize("text", input.VALID_MESSAGES)
def test_valid_message(text: str) -> None:
    assert_that(twitch.validate_message(text)).is_equal_to(text)


@pytest.mark.parametrize("text", input.INVALID_MESSAGES)
def test_invalid_message(text: str) -> None:
    with pytest.raises(ValidationError):
        twitch.validate_message(text)
