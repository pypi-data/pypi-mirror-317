import logging
import pytest
from tfdocs.db.test_handler import MockDb
from tfdocs.models.blocks.resource import Resource

log = logging.getLogger()


class MockResource(Resource):
    _db = MockDb()


@pytest.mark.parametrize(
    "case, exp",
    [
        ("time_offset", "79308e46475d463658c5e9bcd37ccfe2"),
        ("time_rotating", "1f3b97524b1efacbbd2b77679940710d"),
        ("time_sleep", "8cbde6725c88f9474cf8acaf239114c7"),
        ("time_static", "8f26c13e667a269ac45e8cd1909aaebf"),
    ],
)
def test_from_name(case, exp):
    subject = MockResource.from_name(case)
    assert subject.id == exp
