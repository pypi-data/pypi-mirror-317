import tfdocs.models.types as tf
from tfdocs.db.test_handler import MockDb
from tfdocs.models.attribute import Attribute
from tfdocs.utils import hash_path


class MockAttribute(Attribute):
    _db = MockDb()


def test_attribute_initialization():
    # Set up sample attribute
    attribute = MockAttribute(
        attribute_name="attr1",
        attribute_type=tf.String(),
        description="desc1",
        description_type=tf.DescType.MARKDOWN,
        optional=True,
        computed=False,
    )

    # Verify initialization
    assert attribute.name == "attr1"
    assert attribute._attribute_type == tf.String()
    assert attribute._description == "desc1"
    assert attribute._description_type == tf.DescType.MARKDOWN
    assert attribute._optional is True
    assert attribute._computed is False


def test_attribute_as_record():
    # Set up sample attribute
    attribute = MockAttribute(
        attribute_name="attr1",
        attribute_type=tf.String(),
        description="desc1",
        description_type=tf.DescType.MARKDOWN,
        optional=True,
        computed=False,
    )

    # Test as_record method
    expected_hash = hash_path(None)  # Parent path is None in this case
    result = attribute.as_record()

    expected_result = (
        "attr1",
        "string",
        "desc1",
        repr(tf.DescType.MARKDOWN),
        1,
        0,
        expected_hash,
    )
    assert result == expected_result


def test_late_properties():
    attribute = MockAttribute(attribute_id="39")
    exp = MockAttribute(
        attribute_name="id",
        attribute_type=tf.String(),
        description="This is set to a random value at create time.",
        description_type=tf.DescType.PLAIN,
        optional=False,
        computed=True,
        block_id="e832cce309a19eb2d126e41ac2f54997",
    )
    assert exp.name == attribute.name
    assert exp.type == attribute.type
    assert exp.description == attribute.description
    assert exp.description_type == attribute.description_type
    assert exp.computed == attribute.computed
    assert exp.optional == attribute.optional
    assert exp.block_id == attribute.block_id

    assert exp == attribute


def test_repr():
    attribute = MockAttribute(
        attribute_id="39",
        attribute_name="id",
        attribute_type=tf.String(),
        description="This is set to a random value at create time.",
        description_type=tf.DescType.PLAIN,
        optional=True,
        computed=True,
    )
    assert (
        repr(attribute)
        == "[39/e8-97] id : string = 'This is set to a...' : plain (optional, computed)"
    )
