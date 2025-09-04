import pytest
from unittest.mock import Mock
import rich_click as click
from views.subgroups.helper_functions.validators import (
    valid_email,
    valid_string,
    valid_password,
    valid_phone,
    valid_date,
    valid_datetime,
    valid_int,
)


@pytest.fixture
def mock_prompt_and_echo(monkeypatch):
    """
    A fixture to mock click.prompt and click.echo for all tests.
    """
    mock_prompt = Mock()
    mock_echo = Mock()
    monkeypatch.setattr(click, "prompt", mock_prompt)
    monkeypatch.setattr(click, "echo", mock_echo)
    return mock_prompt, mock_echo


def test_valid_email_with_valid_input(mock_prompt_and_echo):
    mock_prompt, mock_echo = mock_prompt_and_echo
    mock_prompt.return_value = "test@example.com"

    result = valid_email()

    assert result == "test@example.com"
    assert mock_prompt.call_count == 1
    mock_echo.assert_not_called()


def test_valid_email_with_invalid_and_then_valid_input(mock_prompt_and_echo):
    mock_prompt, mock_echo = mock_prompt_and_echo
    mock_prompt.side_effect = ["invalid-email", "test@example.com"]

    result = valid_email()

    assert result == "test@example.com"
    assert mock_prompt.call_count == 2
    mock_echo.assert_called_with(
        "L'adresse e-mail n'est pas dans le bon format. Veuillez réessayer."
    )


def test_valid_string_with_invalid_and_then_valid_input(mock_prompt_and_echo):
    mock_prompt, mock_echo = mock_prompt_and_echo
    mock_prompt.side_effect = ["This is a very long string", "short"]

    result = valid_string(length=10, msg="Enter a string:")

    assert result == "short"
    assert mock_prompt.call_count == 2
    mock_echo.assert_called_with(
        "L'adresse e-mail n'est pas dans le bon format. Veuillez réessayer."
    )


def test_valid_password_with_invalid_and_then_valid_input(mock_prompt_and_echo):
    mock_prompt, mock_echo = mock_prompt_and_echo
    mock_prompt.side_effect = ["nouppers", "no!digit", "NoSpecial", "Valid!Password1"]

    result = valid_password()

    assert result == "Valid!Password1"
    assert mock_prompt.call_count == 4
    assert mock_echo.call_count == 3
    mock_echo.assert_called_with(
        "Le mot de passe doit contenir au moins : une majuscule, un caractère spécial et un chiffre."
    )


def test_valid_phone_with_invalid_and_then_valid_input(mock_prompt_and_echo):
    mock_prompt, mock_echo = mock_prompt_and_echo
    mock_prompt.side_effect = ["1234567890", "0612345678"]

    result = valid_phone()

    assert result == "0612345678"
    assert mock_prompt.call_count == 2
    mock_echo.assert_called_with(
        "Le numero de telephone n'est pas valide. Veuillez réessayer."
    )


def test_valid_date_with_invalid_and_then_valid_input(mock_prompt_and_echo):
    mock_prompt, mock_echo = mock_prompt_and_echo
    mock_prompt.side_effect = ["30/02/2023", "31/12/2023"]

    result = valid_date(msg="Enter a date:")

    assert result == "31/12/2023"
    assert mock_prompt.call_count == 2
    mock_echo.assert_called_with("La date doit être valide et au format: dd/mm/yyyy")


def test_valid_datetime_with_invalid_and_then_valid_input(mock_prompt_and_echo):
    mock_prompt, mock_echo = mock_prompt_and_echo
    mock_prompt.side_effect = ["31/12/2023 25:00", "31/12/2023 15:30"]

    result = valid_datetime(msg="Enter a datetime:")

    assert result == "31/12/2023 15:30"
    assert mock_prompt.call_count == 2
    mock_echo.assert_called_with(
        "L'heure doit être valide et au format: dd/mm/yyyy HH:MM"
    )


def test_valid_int_with_invalid_and_then_valid_input(mock_prompt_and_echo):
    mock_prompt, mock_echo = mock_prompt_and_echo
    mock_prompt.side_effect = ["abc", "123"]

    result = valid_int(msg="Enter an integer:")

    assert result == "123"
    assert mock_prompt.call_count == 2
    mock_echo.assert_called_with("Le montant doit être un nombre entier.")
