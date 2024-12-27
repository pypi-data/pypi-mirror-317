"""
Run Tests on the Pushover Plugin
"""

import logging
from typing import List

import pytest
from lunchable.models import TransactionObject

from lunchable_pushlunch import PushLunch
from tests.conftest import lunchable_cassette

logger = logging.getLogger(__name__)


@pytest.mark.asyncio
@lunchable_cassette
async def test_send_notification() -> None:
    """
    Send a Generic Notification
    """
    pusher = PushLunch()
    await pusher.send_notification(
        message="This is a test notification from lunchable.", title="Test"
    )


@pytest.mark.asyncio
@lunchable_cassette
async def test_post_transaction(test_transactions: List[TransactionObject]) -> None:
    """
    Send
    """
    pusher = PushLunch()
    example_notification = test_transactions[0]
    example_notification.payee = "Test"
    example_notification.notes = "Example Test Notification from lunchable"
    await pusher.post_transaction(transaction=example_notification)
