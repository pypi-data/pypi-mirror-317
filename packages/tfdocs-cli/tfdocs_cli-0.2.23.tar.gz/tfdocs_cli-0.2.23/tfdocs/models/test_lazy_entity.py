from tfdocs.models.lazy_entity import LazyObject
from tfdocs.db.test_handler import MockDb


class MockLazy(LazyObject):
    _db = MockDb()
    _table_name = "test"

    @property
    def id(self):
        return 0


def test_late_bind():
    pass
