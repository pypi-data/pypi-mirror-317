import re
import ast
from functools import reduce
import typing
from typing import Union
from enum import Enum, auto

# ----
from tfdocs.utils import flatten


# ------------------------- BASE CLASS DEFINITION -----------------------------#
class Primitive:
    def __init__(self):
        pass

    @classmethod
    def type_name(cls) -> str:
        return cls.__name__.lower()

    def __eq__(self, o) -> bool:
        if isinstance(o, Primitive):
            return o.type_name() == self.type_name()
        return False

    def __repr__(self) -> str:
        return self.type_name()


# -------------------------- TERRAFORM PRIMITIVES -----------------------------#


class Any(Primitive): ...


class String(Primitive): ...


class Number(Primitive): ...


class Bool(Primitive): ...


# ------------------------ COMPLEX TYPE BASE CLASS ----------------------------#


class Complex(Primitive):
    def __init__(self, element_type: Primitive = Any()):
        self._element_type = element_type

    def __eq__(self, o) -> bool:
        if (
            isinstance(o, Complex)
            and self._element_type == o._element_type
            and self.type_name() == o.type_name()
        ):
            return True
        return False

    def __repr__(self) -> str:
        return f"{self.type_name()}[{self._element_type}]"


# ------------------------ TERRAFORM COMPLEX TYPES ----------------------------#


class List(Complex): ...


class Map(Complex): ...


class Set(Complex): ...


class Object(Complex):
    def __init__(self, attrs: dict):
        for k, v in attrs.items():
            if isinstance(v, Primitive):
                continue
            try:
                attrs[k] = from_some(v)
            except:
                attrs[k] = from_db_string(v)
        self.attrs = attrs

    def __repr__(self) -> str:
        output = {}
        for k, v in self.attrs.items():
            output[k] = f"{v}"
        return f"object({repr(output)})"

    def __eq__(self, o) -> bool:
        return self.attrs == o.attrs


# ---------------------------- TYPE UTILITIES ---------------------------------#

all_types: list[type[Union[Primitive, Complex]]] = [
    Any,
    String,
    Number,
    Bool,
    List,
    Map,
    Set,
    Object,
]


def from_some(inp: list | str):
    types = [t.type_name() for t in all_types]
    type_stack: list[str] = flatten([inp])
    type_stack.reverse()

    def from_reducer(acc: Primitive | dict | None, i: str | dict) -> Primitive | dict:
        # dictionaries are already in the correct format
        if isinstance(i, dict):
            return i

        if "{" in i:
            new_type = ast.literal_eval(i)
            if not isinstance(new_type, dict):
                raise ValueError("Malformed type dictionary")
            return new_type

        # if the accumulator holds a dictionary, then the new type must be Object
        if isinstance(acc, dict):
            if i != "object":
                raise ValueError("Malformed type dictionary")
            return Object(acc)

        # see if the string matches any of the type names (errors out if not)
        t = types.index(i)
        new_type = all_types[t]

        # if this is the first element then we can instantiate it directly without any params
        if acc is None:
            return new_type()

        # if it's not the first element then it should be a complex type
        if issubclass(new_type, Complex):
            return new_type(acc)

        raise ValueError()

    try:
        tf_type = reduce(from_reducer, type_stack, None)
        return tf_type
    except ValueError as e:
        raise ValueError(f"Couldn't convert '{inp}' into a valid Terraform type.\n{e}")


def from_db_string(inp: str) -> Primitive:
    """
    Takes an input formatted as it is in the DB and returns a python object
    representation.
    """
    masked_str, og_content = mask_braces_content(inp)
    types = re.split(r"\(|\[", masked_str)
    for i, t in enumerate(types):
        types[i] = t.replace("]", "")
        types[i] = types[i].replace(")", "")
        types[i] = unmask_content(types[i], og_content)
        # print(types[i])

    return from_some(types)


# --------------------------- DESCRIPTION TYPES -------------------------------#


class DescType(Enum):
    PLAIN = "plain"
    MARKDOWN = "markdown"

    def __repr__(self):
        return self.name.lower()

    @staticmethod
    def from_str(inp: str) -> "DescType":
        for i in [DescType.PLAIN, DescType.MARKDOWN]:
            if inp == repr(i):
                return i
        raise ValueError(f"couldn't convert '{inp}' into a valid description type.")


# --------------------- DICT MASKING FOR DB STRINGS ---------------------------#


def mask_braces_content(s: str):
    content_dict = {}
    masked_s = ""
    idx = 1
    i = 0
    n = len(s)

    while i < n:
        if s[i] == "{":
            start = i
            nesting = 1
            i += 1
            while i < n and nesting > 0:
                if s[i] == "{":
                    nesting += 1
                elif s[i] == "}":
                    nesting -= 1
                i += 1
            content = s[start:i]
            key = f"__mask_{idx}__"
            content_dict[key] = content
            masked_s += key
            idx += 1
        else:
            masked_s += s[i]
            i += 1

    return masked_s, content_dict


def unmask_content(masked_s: str, content_dict: dict) -> str:
    for key, content in content_dict.items():
        masked_s = masked_s.replace(key, content)
    return masked_s
