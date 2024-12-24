from abc import ABC, abstractmethod
from typing import TypeVar, Callable

# ----

from tfdocs.db.handler import Db

T = TypeVar("T")


class LazyObject(ABC):
    _db = Db()
    _table_name: str | None = None

    @abstractmethod
    def id(self):
        """
        Subclasses must declare what key is used to identify the resource
        """
        pass

    def _late_bind(self, prop_name: str, handler: Callable[[], T]) -> T:
        """
        Simplified lazy loading logic
        """
        prop_val = getattr(self, prop_name, None)
        if prop_val is None:
            prop_val = handler()
            setattr(self, prop_name, prop_val)
        return prop_val

    def _mk_prop_handler(self, prop_name: str) -> Callable[[], str]:
        """
        A higher order function that returns generic prop handlers. These
        functions accept a hash or id and then uses that to pull a given
        property from the database. Assumes all handler return values will be
        strings.
        """
        if self._table_name is None:
            raise NotImplementedError(
                "The class must declare a _table_name class-variable"
            )

        def prop_handler() -> str:
            if self._table_name is None:
                raise NotImplementedError(
                    "The class must declare a _table_name class-variable"
                )
            res = self._db.sql(
                f"""
                SELECT {prop_name} FROM {self._table_name} 
                WHERE {self._table_name + "_id"} == ?;
            """,
                (self.id,),
            ).fetchone()
            if res is None:
                raise AttributeError(
                    f"Couldn't find prop name ({prop_name}) for that id ({self.id}) in the database"
                )
            return res[0]

        return prop_handler

    def _lazy_prop(self, prop_name) -> str:
        handler = self._mk_prop_handler(prop_name)
        return self._late_bind("_" + prop_name, handler)
