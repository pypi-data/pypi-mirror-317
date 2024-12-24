import logging
from unittest import mock

from tfdocs.utils import hash_path
from tfdocs.models.block import Block
from tfdocs.models.attribute import Attribute
from tfdocs.db.test_handler import MockDb

log = logging.getLogger(__name__)


class MockBlock(Block):
    _db = MockDb()


def test_block_initialization():
    # Set up sample attributes and blocks
    attr1 = Attribute("attr1", "string", "desc1", "markdown", True, False)
    attr2 = Attribute("attr2", "int", "desc2", "plaintext", False, True)
    child_block = MockBlock(name="child_block", type="misc", attributes=[], blocks=[])
    parent_block = MockBlock(
        name="parent_block",
        type="Resource",
        attributes=[attr1, attr2],
        blocks=[child_block],
    )

    # Verify initialization
    assert parent_block.name == "parent_block"
    assert parent_block.type == "Resource"
    assert parent_block.attributes == [attr1, attr2]
    assert parent_block.blocks == [child_block]


def test_block_as_record():
    # Set up sample block
    parent_block = MockBlock(name="parent_block", type="misc", attributes=[], blocks=[])

    # Test as_record method
    expected_hash = hash_path("parent_block")
    name, hash_value, block_type, parent_hash = parent_block.as_record()

    assert name == "parent_block"
    assert hash_value == expected_hash
    assert block_type == "misc"
    assert parent_hash == ""


def test_block_flatten():
    # Set up sample attributes and blocks
    attr1 = Attribute("attr1", "string", "desc1", "markdown", True, False)
    attr2 = Attribute("attr2", "int", "desc2", "plaintext", False, True)
    child_block = MockBlock(name="child_block", type="misc", attributes=[], blocks=[])
    parent_block = MockBlock(
        name="parent_block",
        type="misc",
        attributes=[attr1, attr2],
        blocks=[child_block],
    )

    # Test flatten method
    flattened_blocks, flattened_attributes = parent_block.flatten()

    assert flattened_blocks == [child_block, parent_block]
    assert flattened_attributes == [attr1, attr2]


def test_late_name():
    exp = "null_resource"
    test_r = MockBlock(hash="e832cce309a19eb2d126e41ac2f54997", type="Resource")
    assert exp == test_r.name


@mock.patch("tfdocs.models.attribute.Attribute._db", new=MockDb())
def test_late_attributes():
    exp_attributes = ["id", "triggers"]
    test_r = MockBlock(hash="e832cce309a19eb2d126e41ac2f54997", type="Resource")
    test_attributes = [a.name for a in test_r.attributes]
    assert exp_attributes == test_attributes


@mock.patch("tfdocs.models.block.Block._db", new=MockDb())
def test_late_blocks():
    exp_blocks = ["source"]
    test_r = MockBlock(hash="743e19765c5244e08afe83dca406e244", type="DataSource")
    test_blocks = [b.name for b in test_r.blocks]
    assert exp_blocks == test_blocks
