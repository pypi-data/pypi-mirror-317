import pytest

import tfdocs.models.types as tf

test_cases = [
    # Primitives
    ("string", tf.String(), "string"),
    ("number", tf.Number(), "number"),
    ("bool", tf.Bool(), "bool"),
    ("any", tf.Any(), "any"),
    # List types
    (["list", "string"], tf.List(tf.String()), "list[string]"),
    (["list", "number"], tf.List(tf.Number()), "list[number]"),
    (["list", "bool"], tf.List(tf.Bool()), "list[bool]"),
    (["list", "any"], tf.List(tf.Any()), "list[any]"),
    (["list"], tf.List(), "list[any]"),
    ("list", tf.List(tf.Any()), "list[any]"),
    # Map Types
    (["map", "string"], tf.Map(tf.String()), "map[string]"),
    (["map", "number"], tf.Map(tf.Number()), "map[number]"),
    # Nested Types
    (["map", ["list", "string"]], tf.Map(tf.List(tf.String())), "map[list[string]]"),
    (["list", ["map", "string"]], tf.List(tf.Map(tf.String())), "list[map[string]]"),
    # Object Types
    (
        ["object", "{'name': 'string', 'age': 'number'}"],
        tf.Object({"name": tf.String(), "age": tf.Number()}),
        "object({'name': 'string', 'age': 'number'})",
    ),
    # Complex Nested Structures
    (
        ["list", ["object", '{"id": "string", "values": ["list", "number"]}']],
        tf.List(tf.Object({"id": tf.String(), "values": tf.List(tf.Number())})),
        "list[object({'id': 'string', 'values': 'list[number]'})]",
    ),
]


@pytest.mark.parametrize("case, exp", [case[0:2] for case in test_cases])
def test_from_some(case, exp):
    res = tf.from_some(case)
    assert res == exp


def test_from_some_dict():
    exp = tf.Object({"test": tf.Any(), "value": tf.String()})
    assert exp == tf.from_some(["object", {"test": "any", "value": "string"}])


def test_from_some_errors():
    with pytest.raises(ValueError):
        case = tf.from_some("invalid")

    # make sure invalid dictionaries are caught
    with pytest.raises(ValueError):
        case = tf.from_some(["object", "[{}]"])

    with pytest.raises(ValueError):
        case = tf.from_some(["list", "{}"])

    with pytest.raises(ValueError):
        print("testing for impossible types")
        case = tf.from_some(["string", "list", "string"])


def test_primitive_eq():
    passing_test = tf.String() == tf.String()
    failing_test = all(
        [
            tf.Number() != tf.String(),
            tf.String() != "",
        ]
    )
    assert passing_test and failing_test


def test_complex_eq():
    passing_test = tf.List() == tf.List()
    failing_test = all([tf.Set() != tf.String(), tf.Map() != tf.Set(), tf.List() != ""])
    assert passing_test and failing_test


@pytest.mark.parametrize("tf_type, expected_repr", [case[1:3] for case in test_cases])
def test_repr(tf_type, expected_repr):
    assert repr(tf_type) == expected_repr


@pytest.mark.parametrize("case, exp", [(case[2], case[1]) for case in test_cases])
def test_from_db_string(case, exp):
    o = tf.from_db_string(case)
    assert o == exp


def test_desc_type_repr():
    assert repr(tf.DescType.PLAIN) == "plain"
    assert repr(tf.DescType.MARKDOWN) == "markdown"


def test_desc_type_from_str():
    assert tf.DescType.from_str("plain") == tf.DescType.PLAIN
    assert tf.DescType.from_str("markdown") == tf.DescType.MARKDOWN
    with pytest.raises(
        ValueError, match="couldn't convert 'invalid' into a valid description type."
    ):
        tf.DescType.from_str("invalid")


def test_mask_braces_content_basic():
    input_str = "list[object({'id': string, 'values': list[number]})]"
    expected_masked = "list[object(__mask_1__)]"
    expected_dict = {"__mask_1__": "{'id': string, 'values': list[number]}"}

    masked_str, content_dict = tf.mask_braces_content(input_str)
    assert masked_str == expected_masked
    assert content_dict == expected_dict


def test_mask_braces_content_multiple():
    input_str = "map{'a': 1} and set{'b', 'c'}"
    expected_masked = "map__mask_1__ and set__mask_2__"
    expected_dict = {"__mask_1__": "{'a': 1}", "__mask_2__": "{'b', 'c'}"}

    masked_str, content_dict = tf.mask_braces_content(input_str)
    assert masked_str == expected_masked
    assert content_dict == expected_dict


def test_mask_braces_content_nested():
    input_str = "func({outer: {inner: value}})"
    expected_masked = "func(__mask_1__)"
    expected_dict = {"__mask_1__": "{outer: {inner: value}}"}

    masked_str, content_dict = tf.mask_braces_content(input_str)
    assert masked_str == expected_masked
    assert content_dict == expected_dict


def test_mask_braces_content_no_braces():
    input_str = "no braces here"
    expected_masked = "no braces here"
    expected_dict = {}

    masked_str, content_dict = tf.mask_braces_content(input_str)
    assert masked_str == expected_masked
    assert content_dict == expected_dict


def test_mask_braces_content_improper_nesting():
    input_str = "improper { nesting"
    # Since the braces are not properly closed, the function may not behave as expected.
    # Depending on implementation, this test may need to be adjusted.
    masked_str, content_dict = tf.mask_braces_content(input_str)
    # In this case, the function will consume until the end of the string.
    expected_masked = "improper __mask_1__"
    expected_dict = {"__mask_1__": "{ nesting"}

    assert masked_str == expected_masked
    assert content_dict == expected_dict


def test_unmask_content():
    input_str = "list[object({'id': string})] and map{'key': value}"
    masked_str, content_dict = tf.mask_braces_content(input_str)
    print("MASKED STRING", masked_str)
    unmasked_str = tf.unmask_content(masked_str, content_dict)
    print("UNMASKED STRING", unmasked_str)
    assert unmasked_str == input_str


def test_mask_braces_content_adjacent_braces():
    input_str = "{}{}"
    expected_masked = "__mask_1____mask_2__"
    expected_dict = {"__mask_1__": "{}", "__mask_2__": "{}"}

    masked_str, content_dict = tf.mask_braces_content(input_str)
    assert masked_str == expected_masked
    assert content_dict == expected_dict


def test_mask_braces_content_text_between_braces():
    input_str = "start{first}middle{second}end"
    expected_masked = "start__mask_1__middle__mask_2__end"
    expected_dict = {"__mask_1__": "{first}", "__mask_2__": "{second}"}

    masked_str, content_dict = tf.mask_braces_content(input_str)
    assert masked_str == expected_masked
    assert content_dict == expected_dict
