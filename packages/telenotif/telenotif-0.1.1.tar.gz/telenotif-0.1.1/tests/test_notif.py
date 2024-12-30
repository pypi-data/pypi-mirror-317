import pytest
from telenotif import notif
from own.telenotif.telenotif.exceptions import TelenotifError

def test_invalid_token():
    with pytest.raises(TelenotifError):
        notifier = notif("invalid_token", "123456")

def test_initialization():
    # Note: Add your test bot token and user ID for testing
    notifier = notif("YOUR_TEST_BOT_TOKEN", "YOUR_TEST_USER_ID")
    assert notifier is not None