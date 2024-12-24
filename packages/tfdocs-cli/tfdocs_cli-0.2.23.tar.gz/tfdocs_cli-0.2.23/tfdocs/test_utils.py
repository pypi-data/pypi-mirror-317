import json
import tempfile
import pytest
from unittest.mock import patch, mock_open

from tfdocs.utils import (
    hash_path,
    clamp_string,
    flatten,
    clamp_string,
    flatten_iters,
    chunk_iter,
    refmt,
)


@pytest.mark.parametrize(
    "input_string, max_length, expected_output",
    [
        # Test cases where string length is less than or equal to max_length
        ("hello", 10, "hello"),  # No clamping needed
        ("world", 5, "world"),  # Exactly the max length
        # Test cases where string length is greater than max_length
        ("hello world", 5, "he..."),  # Clamp and add ellipsis
        ("truncate me", 10, "truncat..."),  # Clamp and add ellipsis
        # Test case where max_length is less than 3
        ("small", 2, "..."),  # Can't show part of the string, just ellipsis
        # Test case with an empty string
        ("", 5, ""),  # Should return the empty string
    ],
)
def test_clamp_string(input_string, max_length, expected_output):
    assert clamp_string(input_string, max_length) == expected_output


def test_hasher():
    """
    This test ensures the hasher stays functional
    """
    exps = ["8dd066a9072cfaca57bcedd7f233432f", "b3983e305a7a18c356122f7df1496f14"]
    inps = [
        "test_value",
        "another_test_value",
    ]

    for inp, exp in zip(inps, exps):
        inp = hash_path(inp)
        assert inp == exp


def test_flatten_iterator():
    gen1 = (x for x in range(1, 4))
    gen2 = (x for x in range(4, 7))
    gen3 = (x for x in range(7, 10))
    res = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    assert list(flatten_iters(gen1, gen2, gen3)) == res


def test_chunk_iterator():
    res = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    inp = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    assert list(chunk_iter(inp, batch_size=3)) == res
    res = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10]]
    inp = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    assert list(chunk_iter(inp, batch_size=3)) == res


def test_refmt():
    # Input JSON string to simulate stdin input
    input_json = '{"key": "value", "list": [1, 2, 3]}'

    # Expected formatted JSON string
    expected_output = json.dumps(json.loads(input_json), indent=4)

    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as temp_input:
        # Write the input data to the temporary file and reset the file pointer
        temp_input.write(input_json)
        temp_input.seek(0)

        # Patch sys.stdin to simulate input
        with patch("sys.stdin", temp_input):
            # Patch open to simulate file writing
            with patch("builtins.open", mock_open()) as mock_file:
                refmt()

                # Check that open was called to write the formatted output
                mock_file.assert_called_once_with("fmt.json", "w+")

                # Get the handle to the mocked file and check the written data
                handle = mock_file()
                handle.write.assert_called_once_with(expected_output)
