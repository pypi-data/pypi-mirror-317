import hashlib
import sys
import json
from result import as_result, Ok, Err, Result
from typing import Callable, Iterator


def chunk_iter(iter: Iterator, batch_size=100) -> Iterator[list]:
    batch = []
    for item in iter:
        batch.append(item)
        if len(batch) >= batch_size:
            yield batch
            batch = []
    if batch:
        yield batch


def hash_path(inp: str | None) -> str:
    if inp == None or inp == "":
        return ""
    inp = str(inp)
    hasher = hashlib.md5()
    hasher.update(inp.encode("utf-8"))
    hash = hasher.hexdigest()
    return hash


def try_wrap(f: Callable, *args, **kwargs) -> Result:
    """
    Wraps a function that can error with a Result type, allowing for safe
    type based error handling. This is best used in cases where a function
    can't return a critical error
    """
    try:
        return Ok(f(*args, **kwargs))
    except Exception as e:
        return Err(e)


def flatten(nested_list: list):
    flattened = []
    for element in nested_list:
        if isinstance(element, list):
            # Recursively flatten the sublist
            flattened.extend(flatten(element))
        else:
            # Append the non-list element to the result
            flattened.append(element)
    return flattened


def flatten_iters(*args) -> Iterator:
    for iter in args:
        yield from iter


def clamp_string(s: str, max_length: int) -> str:
    if max_length < 3:
        return "..."  # Directly return "..." if max_length is too small
    if len(s) <= max_length:
        return s
    # Reserve 3 characters for the ellipsis
    return s[: max_length - 3].strip() + "..."


def refmt():
    # Read all input from stdin
    input_data = str(sys.stdin.read())

    info = json.loads(input_data)
    formatted = json.dumps(info, indent=4)

    open("fmt.json", "w+").write(formatted)
