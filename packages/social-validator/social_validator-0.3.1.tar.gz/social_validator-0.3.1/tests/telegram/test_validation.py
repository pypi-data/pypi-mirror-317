import pytest as pytest
from assertpy import assert_that

from social_validator import telegram
from social_validator.exceptions import ValidationError
from tests.telegram import input

# *** Validation functions ***


@pytest.mark.parametrize("_id", input.VALID_IDS)
def test_valid_id(_id: str) -> None:
    v = telegram.validate_id(_id)
    assert_that(v).is_equal_to(_id.lower())


@pytest.mark.parametrize("_id", input.INVALID_IDS)
def test_invalid_id(_id: str) -> None:
    with pytest.raises(ValidationError):
        telegram.validate_id(_id)


@pytest.mark.parametrize("_id", input.VALID_BOT_IDS)
def test_valid_bot_id(_id: str) -> None:
    v = telegram.validate_bot_id(_id)
    assert_that(v).is_equal_to(_id.lower())


@pytest.mark.parametrize("_id", input.INVALID_BOT_IDS)
def test_invalid_bot_id(_id: str) -> None:
    with pytest.raises(ValidationError):
        telegram.validate_bot_id(_id)


@pytest.mark.parametrize("_id", input.RESERVED_IDS)
def test_reserved_id(_id: str) -> None:
    with pytest.raises(ValidationError):
        telegram.validate_id(_id)

    with pytest.raises(ValidationError):
        telegram.validate_bot_id(_id)


@pytest.mark.parametrize("_id", input.RESERVED_START_IDS)
def test_reserved_start_id(_id: str) -> None:
    with pytest.raises(ValidationError):
        telegram.validate_id(_id)

    with pytest.raises(ValidationError):
        telegram.validate_bot_id(_id)


@pytest.mark.parametrize("text, chat_type", input.VALID_DESCRIPTIONS)
def test_valid_description(text: str, chat_type: telegram.ChatType) -> None:
    v = telegram.validate_description(text, chat_type=chat_type)
    assert_that(v).is_equal_to(text)


@pytest.mark.parametrize("text, chat_type", input.INVALID_DESCRIPTIONS)
def test_invalid_description(text: str, chat_type: telegram.ChatType) -> None:
    with pytest.raises(ValidationError):
        telegram.validate_description(text, chat_type=chat_type)


@pytest.mark.parametrize("text, chat_type", input.INVALID_DESCRIPTIONS_CHAT_TYPES)
def test_invalid_chat_type(text: str, chat_type: telegram.ChatType) -> None:
    with pytest.raises(ValueError):
        telegram.validate_description(text, chat_type=chat_type)


@pytest.mark.parametrize("name", input.VALID_CHAT_NAMES)
def test_valid_chat_name(name: str) -> None:
    v = telegram.validate_chat_name(name)
    assert_that(v).is_equal_to(name)


@pytest.mark.parametrize("name", input.INVALID_CHAT_NAMES)
def test_invalid_chat_name(name: str) -> None:
    with pytest.raises(ValidationError):
        telegram.validate_chat_name(name)


@pytest.mark.parametrize("first_name, last_name", input.VALID_FULL_NAMES)
def test_valid_full_name(first_name: str, last_name: str) -> None:
    out_first_name, out_last_name = telegram.validate_full_name(
        first_name=first_name, last_name=last_name
    )
    assert_that(out_first_name).is_equal_to(first_name)
    assert_that(out_last_name).is_equal_to(last_name)


@pytest.mark.parametrize("first_name, last_name", input.INVALID_FULL_NAMES)
def test_invalid_full_name(first_name: str, last_name: str) -> None:
    with pytest.raises(ValidationError):
        telegram.validate_full_name(first_name=first_name, last_name=last_name)


@pytest.mark.parametrize("text, include_media", input.VALID_MESSAGES)
def test_valid_message(text: str, include_media: bool) -> None:
    v = telegram.validate_message(text, include_media=include_media)
    assert_that(v).is_equal_to(text)


@pytest.mark.parametrize("text, include_media", input.INVALID_MESSAGES)
def test_invalid_message(text: str, include_media: bool) -> None:
    with pytest.raises(ValidationError):
        telegram.validate_message(text, include_media=include_media)


@pytest.mark.parametrize("cmd", input.VALID_COMMANDS)
def test_valid_command(cmd: str) -> None:
    v = telegram.validate_command(cmd)
    assert_that(v).is_equal_to(cmd.lower())


@pytest.mark.parametrize("cmd", input.INVALID_COMMANDS)
def test_invalid_command(cmd: str) -> None:
    with pytest.raises(ValidationError):
        telegram.validate_command(cmd)


# *** Check functions ***


@pytest.mark.parametrize("first_name, last_name", input.VALID_FULL_NAMES)
def test_is_valid_full_name(first_name: str, last_name: str) -> None:
    assert_that(telegram.is_valid_full_name(first_name, last_name)).is_true()


@pytest.mark.parametrize("first_name, last_name", input.INVALID_FULL_NAMES)
def test_is_invalid_full_name(first_name: str, last_name: str) -> None:
    assert_that(telegram.is_valid_full_name(first_name, last_name)).is_false()
