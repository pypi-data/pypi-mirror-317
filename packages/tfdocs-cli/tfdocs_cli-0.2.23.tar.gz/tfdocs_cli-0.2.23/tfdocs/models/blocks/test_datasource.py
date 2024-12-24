import logging
import pytest
from tfdocs.db.test_handler import MockDb
from tfdocs.models.blocks.datasource import DataSource

log = logging.getLogger()


class MockDataSource(DataSource):
    _db = MockDb()


@pytest.mark.parametrize(
    "case, exp",
    [
        ("null_data_source", "48052ad9e3ae785a9030b2c8628b6b54"),
        ("archive_file", "743e19765c5244e08afe83dca406e244"),
    ],
)
def test_from_name(case, exp):
    subject = MockDataSource.from_name(case)
    assert subject.id == exp
