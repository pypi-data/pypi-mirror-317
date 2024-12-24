from typing import Tuple

# ----

from tfdocs.models.lazy_entity import LazyObject
from tfdocs.models.types import Primitive, from_db_string, DescType
from tfdocs.utils import hash_path, clamp_string


class Attribute(LazyObject):
    _table_name = "attribute"

    def __init__(
        self,
        attribute_id: str | None = None,
        attribute_name: str | None = None,
        attribute_type: Primitive | None = None,
        description: str | None = None,
        description_type: DescType | None = None,
        optional: bool | None = None,
        computed: bool | None = None,
        block_id: str | None = None,
        parent_path: str | None = None,
    ):
        self._attribute_id = attribute_id
        self._attribute_name = attribute_name
        self._attribute_type = attribute_type
        self._description = description
        self._description_type = description_type
        self._optional = optional
        self._computed = computed
        self._block_id = block_id
        self._parent_path = parent_path

    @property
    def id(self):
        return self._attribute_id

    # ---------         LATE-BOUND PROPERTIES         -----------
    @property
    def name(self) -> str:
        return self._lazy_prop("attribute_name")

    @property
    def type(self) -> Primitive:
        def type_handler():
            db_string = self._mk_prop_handler("attribute_type")()
            return from_db_string(db_string)

        return self._late_bind("_attribute_type", type_handler)

    @property
    def description(self) -> str:
        return self._lazy_prop("description")

    @property
    def description_type(self) -> DescType:
        def desc_type_handler():
            desc_type = self._mk_prop_handler("description_type")()
            print("GOT FROM DB", desc_type)
            return DescType.from_str(desc_type)

        return self._late_bind("_description_type", desc_type_handler)

    @property
    def optional(self) -> bool:
        def optional_handler():
            func = self._mk_prop_handler("optional")
            res = func()
            return True if res == 1 else False

        return self._late_bind("_optional", optional_handler)

    @property
    def computed(self) -> bool:
        def computed_handler():
            func = self._mk_prop_handler("computed")
            res = func()
            return True if res == 1 else False

        return self._late_bind("_computed", computed_handler)

    @property
    def block_id(self) -> str:
        # if attr_id is set use standard fetcher
        def hash_generator():
            parent_id = hash_path(self._parent_path)
            return parent_id

        return self._late_bind(
            "_block_id",
            (
                hash_generator
                if self._attribute_id is None
                else self._mk_prop_handler("block_id")
            ),
        )

    @property
    def document(self) -> str:
        types = repr(self.type)
        if self.optional:
            types += ", optional"
        if self.computed:
            types += ", computed"
        desc = ""
        if self.description != "None":
            desc += f": {self.description}"
        string = f"**{self.name}** (*{types}*){desc}\n"
        return string

    # ---------          REFORMATTER METHODS          ----------

    def as_record(self) -> Tuple[str, str, str, object, int, int, str]:
        if self._attribute_type is None or self._attribute_name is None:
            raise AttributeError("A required value is missing")
        return (
            self._attribute_name,
            repr(self._attribute_type),
            self._description if self._description is not None else "",
            (
                repr(self._description_type)
                if self._description_type is not None
                else "plain"
            ),
            1 if self._optional else 0,
            1 if self._computed else 0,
            self.block_id,
        )

    # ---------        METHOD IMPLEMENTATIONS         ----------

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Attribute):
            attribute_match = all(
                [
                    self.name == o.name,
                    self.type == o.type,
                    self.description == o.description,
                    self.description_type == o.description_type,
                    self.optional == o.optional,
                    self.computed == o.computed,
                    self.block_id == o.block_id,
                ]
            )
            hash_match = self.id == o.id
            return attribute_match or hash_match
        return False

    def __repr__(self) -> str:
        toggles = [
            t
            for t in [
                "optional" if self.optional else "",
                "computed" if self.computed else "",
            ]
            if t != ""
        ]
        details = f" ({', '.join(toggles)})" if len(toggles) > 0 else ""
        desc = clamp_string(self.description, 20)
        return f"[{self.id}/{self.block_id[:2]+'-'+self.block_id[-2:]}] {self.name} : {self.type} = '{desc}' : {repr(self.description_type)}{details}"


"""
    An example object that would need to be displayed is as follows
    Mock Attribute : {
        id
        name
        attr_type
        description
        description_type
        optional
        computed
        block_id
    }        

    [id/block_id] name : attr_type
    [1/asdfasdfasdf] example : string = "description text" : plain (optional, computed)

        
"""
