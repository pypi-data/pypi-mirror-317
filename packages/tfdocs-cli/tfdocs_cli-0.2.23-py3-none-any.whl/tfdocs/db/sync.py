# parses tf schema data into an sqlite database
import ast
import asyncio
import ijson
import sqlite3
import logging
from sqlite3 import Cursor
from functools import reduce
from typing import Iterator, Union, Any
from rich.status import Status
from tfdocs.db.handler import Db
from tfdocs.models.block import Block
from tfdocs.models.attribute import Attribute
from tfdocs.models.types import from_some, DescType
from tfdocs.utils import flatten_iters, chunk_iter


def main():
    asyncio.run(load_local_schemas())


log = logging.getLogger()


async def load_local_schemas(cursor) -> None:
    """
    This function loads the local terraform environment schema into the db
    provided.
    """
    with Status(
        "Fetching Provider Schemas from Terraform", spinner="bouncingBar"
    ) as status:
        try:
            stream: asyncio.StreamReader = await fetch_schemas()
            log.info("Fetched schema stream from terraform binary")
            await parse_schemas(cursor, stream, status)
        except Exception as e:
            log.fatal(f"Couldn't sync database: {e}")
            exit(1)
    return None


async def parse_schemas(cursor: Cursor, stream: asyncio.StreamReader, status: Status):
    try:
        async for name, provider in ijson.kvitems_async(stream, "provider_schemas"):
            # breakpoint()
            log.info(f"parsing {name}")
            status.update(status=f"[cyan]Processing '{name}'")
            # create block obj for the provider
            p = [parse_block(name, provider["provider"]["block"], "Provider")]

            # create generator of blocks for the
            ## resources
            r = block_iter(provider, "resource_schemas", "Resource", parent=name)

            ## data sources
            d = block_iter(provider, "data_source_schemas", "DataSource", parent=name)

            ## functions -- needs special handling (doesn't follow block/attribute model)
            # f = block_iter(provider, 'functions')

            # flatten generators into one and then divide into batches
            queue = flatten_iters(p, r, d)
            chunks = chunk_iter(queue, batch_size=500)

            # insert from generator into db in batches
            total = 0
            for chunk in chunks:
                total += db_insert_batch(chunk, cursor, status)
            status.console.print(
                f"[bright_black]> Completed processing [medium_purple]'{name}'[/] ({total} records created)"
            )

    except ijson.common.IncompleteJSONError as e:
        print(
            "Couldn't parse the output from terraform. Please check you are in the correct directory and have run 'tf init'."
        )
        exit(1)


async def fetch_schemas() -> asyncio.StreamReader:
    process = await asyncio.subprocess.create_subprocess_exec(
        *["terraform", "providers", "schema", "-json"],
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    if process.stdout is None:
        raise OSError(
            "Couldn't find any config in this directory. Please make sure this directory contains terraform files."
        )
    return process.stdout


#     ------     ------ recursive parsing structure ------     ------     ------


def parse_block(name, block_data: dict, type="misc", parent=None) -> Block | None:
    if block_data is None:
        return None

    parent_path = f"{parent}.{type}.{name}"
    # print(parent_path)
    attrs = []
    blks = []
    for attr_name, attr in block_data.get("attributes", {}).items():
        new_attribute = parse_attribute(attr_name, attr, parent_path=parent_path)
        if new_attribute is not None:
            attrs.append(new_attribute)
    for blk_name, blk in block_data.get("block_types", {}).items():
        new_block = parse_block(blk_name, blk.get("block"), parent=parent_path)
        if new_block is not None:
            blks.append(new_block)

    return Block(
        name=name,
        type=type,
        attributes=attrs,
        blocks=blks,
        parent_path=parent,
    )


def block_iter(provider: dict, target: str, type: str, parent=None) -> Iterator[Block]:
    """
    Acts as an entrypoint for non-provider based recursive block structures.
    Passes each applicable object through the block parser and yields it to
    the iterator
    """
    for name, obj in provider.get(target, {}).items():
        parser = parse_block(name, obj["block"], type, parent=parent)
        # This one is only really triggered if parse_block returns None, which is rare
        if parser is None:
            continue
        else:
            yield parser


def parse_attribute(name, attr_data: dict, parent_path=None) -> Attribute | None:
    if attr_data == None:
        return None

    attr_type = attr_data.get("type", None)

    if not isinstance(attr_type, str) and not isinstance(attr_type, list):
        raise ValueError(f"Cannot parse type {attr_type}, not a list or string")

    return Attribute(
        attribute_name=name,
        attribute_type=from_some(attr_type),
        description=attr_data.get("description", "None"),
        description_type=DescType.from_str(
            str(attr_data.get("description_kind", "plain"))
        ),
        optional=True if attr_data.get("optional") != None else False,
        computed=True if attr_data.get("computed") != None else False,
        parent_path=parent_path,
    )


#     ------     ------     batch insertion code    ------     ------     ------


def db_insert_batch(chunk: list, cursor: Cursor, status: Status) -> int:
    # takes recursive hierarchy and converts into a pair of lists of objects
    flat_chunks = [blk.flatten() for blk in chunk]

    blks = [blk.as_record() for chunk in flat_chunks for blk in chunk[0]]
    attrs = [attr.as_record() for chunk in flat_chunks for attr in chunk[1]]
    total = len(blks) + len(attrs)

    # print(blks)
    try:
        # insert blocks into db
        cursor.executemany(
            "INSERT OR REPLACE INTO block (block_name, block_id, block_type, parent_id) VALUES (?,?,?,?);",
            blks,
        )
        # insert attributes into db
        cursor.executemany(
            """
            INSERT OR REPLACE INTO attribute (
                attribute_name, 
                attribute_type, 
                description, 
                description_type, 
                optional, 
                computed, 
                block_id
            ) VALUES (?,?,?,?,?,?,?);""",
            attrs,
        )
        # status.console.print(f"[bright_black italic]> Inserted [medium_purple]{len(blks) + len(attrs)}[/] records")
        log.debug(f"Inserted {total} records into DB")

    except Exception as e:
        log.critical(e)
        print("Encountered the following error:" + repr(e))
        exit(1)

    return total
