import logging
from textwrap import dedent, indent
from typing import Tuple, Union

# ----
from tfdocs.utils import hash_path
from tfdocs.models.attribute import Attribute
from tfdocs.models.lazy_entity import LazyObject

"""
    Basically, the idea is to make lean objects that can either have its values
    set at initialisation OR pulled late from a local sqlite database.
"""

log = logging.getLogger()


class Block(LazyObject):
    _table_name = "block"

    @classmethod
    def from_id(cls, id: str) -> Union["Block", None]:
        try:
            res = cls._db.sql(
                """
                SELECT block_type, block_name FROM block
                WHERE block_id == ?;
            """,
                (id,),
            ).fetchone()
            return Block(type=res[0], hash=id, name=res[1])
        except:
            return None

    def __init__(
        self,
        type: str = "misc",
        name: str | None = None,
        hash: str | None = None,
        parent_path: str | None = None,
        parent_hash: str | None = None,
        attributes: list["Attribute"] | None = None,
        document: str | None = None,
        blocks: list["Block"] | None = None,
    ):
        self._block_type = type
        self._block_name = name
        self._block_hash = hash
        self._parent_path = parent_path
        self._parent_hash = parent_hash
        self._attributes = attributes
        self._document = document
        self._blocks = blocks

    @property
    def id(self):
        return self.hash

    # ---------         LATE-BOUND PROPERTIES         -----------

    # PULLED FROM STORE ------------- *these are mostly used for interaction*
    @property
    def name(self):
        return self._lazy_prop("block_name")

    @property
    def type(self):
        return self._lazy_prop("block_type")

    @property
    def attributes(self) -> list["Attribute"]:
        """
        Returns a list of all attributes that point to this block
        """

        def attribute_handler():
            res = self._db.sql(
                "SELECT attribute_id FROM attribute WHERE block_id == ?;",
                (self.hash,),
            ).fetchall()
            return [Attribute(attribute_id=a[0]) for a in res]

        return self._late_bind("_attributes", attribute_handler)

    @property
    def blocks(self) -> list["Block"]:
        """
        Returns a list of all blocks that point to this block
        """

        def block_handler():
            res = self._db.sql(
                "SELECT block_id FROM block WHERE parent_id == ? AND block_type == 'misc'",
                (self.hash,),
            ).fetchall()
            blocks = [Block(hash=b[0], type="misc") for b in res]
            return blocks

        return self._late_bind("_blocks", block_handler)

    # CALCULATED --------------------- *these are mostly used during sync*
    @property
    def hash(self) -> str:
        """
        Creates a hash from the block and its absolute path in the schema hierarchy
        """

        def hash_handler():
            path = (
                self.name
                if self._parent_path == None
                else f"{self._parent_path}.{self.type}.{self.name}"
            )
            return hash_path(path)

        return self._late_bind("_block_hash", hash_handler)

    @property
    def parent_hash(self) -> str:
        """
        Calculates the hash that identifies the block's parentage - if it has any
        """
        if self._parent_hash is None:
            self._parent_hash = hash_path(self._parent_path)
        return self._parent_hash

    @property
    def document(self) -> str:
        """
        Formats a block into a markdown document
        """

        def make_document():
            attributes = "\n".join(["- " + a.document for a in self.attributes])
            blocks = "\n".join([b.document for b in self.blocks])
            doc = (
                dedent(
                    f"""
                    # {self.name}
                    ## Attributes
                    """
                )
                + attributes
                + "## Nested Blocks"
                + indent(blocks, "> ")
            )
            log.info(doc)
            return doc

        return self._late_bind("_document", make_document)

    # ---------            STATIC METHODS             ----------

    # @abstractmethod
    # def from_name(self) -> "Block":
    #     """Sub-classes must provide a method to instantiate from"""
    #     pass

    # ---------          REFORMATTER METHODS          ----------

    def as_record(self) -> Tuple[str, str, str, str | None]:
        return (self.name, self.hash, self.type, self.parent_hash)

    def flatten(self) -> Tuple[list["Block"], list["Attribute"]]:
        """
        A recursive flattening method that takes a nested structure of
        blocks and attributes and returns a tuple pair of block and
        attribute lists. This allows us to convert each resource into a set
        of flat structures we can insert into the local database.
        """
        blocks = []
        attributes = []
        for blk in self.blocks:
            up = blk.flatten()
            blocks.extend(up[0])
            attributes.extend(up[1])
        attributes.extend(self.attributes)
        blocks.append(self)
        return (blocks, attributes)

    # ---------        METHOD IMPLEMENTATIONS         ----------

    def __eq__(self, o: object):
        if isinstance(o, Block):
            attribute_match = all(
                [
                    self.name == o.name,
                    self.type == o.type,
                    self.attributes == o.attributes,
                    self.blocks == o.blocks,
                ]
            )
            hash_match = self.hash == o.hash
            return attribute_match or hash_match
        return False

    def __repr__(self):
        attrs = "\n\t".join([f"{attr}" for attr in self.attributes])
        blks = "\n\t".join([f"{blk}" for blk in self.blocks])
        return dedent(
            f"""
            {self.type} {self.name} {{
                parent = {self._parent_path}  
                attributes = [{attrs}]
                blocks = [{blks}]
            }}
            """
        )
