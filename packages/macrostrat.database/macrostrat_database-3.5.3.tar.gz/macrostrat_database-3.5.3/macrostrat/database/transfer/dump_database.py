import asyncio
import sys
from pathlib import Path
from typing import Optional

import aiofiles
from sqlalchemy.engine import Engine

from macrostrat.utils import get_logger

from .stream_utils import print_stdout, print_stream_progress
from .utils import _create_command

log = get_logger(__name__)


async def pg_dump(
    engine: Engine,
    *,
    command_prefix: Optional[list] = None,
    args: list = [],
    postgres_container: str = "postgres:15",
    user: Optional[str] = "postgres",
    stdout=asyncio.subprocess.PIPE,
    custom_format: bool = True,
):
    _args = []
    if custom_format:
        _args.append("-Fc")

    if user is not None:
        _args += ["-U", user]
    _args += args

    _cmd = _create_command(
        engine,
        "pg_dump",
        args=_args,
        prefix=command_prefix,
        container=postgres_container,
    )

    return await asyncio.create_subprocess_exec(
        *_cmd,
        stdout=stdout,
        stderr=asyncio.subprocess.PIPE,
    )


async def pg_dump_to_file(engine: Engine, dumpfile: Path | None, **kwargs):
    proc = await pg_dump(engine, **kwargs)
    if dumpfile is None or dumpfile == sys.stdout:
        # If we have no dumpfile, just print to stdout
        await _monitor_stdout(proc)
        return
    # Open dump file as an async stream
    async with aiofiles.open(dumpfile, mode="wb") as dest:
        await asyncio.gather(
            asyncio.create_task(print_stream_progress(proc.stdout, dest)),
            asyncio.create_task(print_stdout(proc.stderr)),
        )


async def _monitor_stdout(proc):
    await asyncio.gather(
        asyncio.create_task(print_stdout(proc.stdout)),
        asyncio.create_task(print_stream_progress(proc.stderr, None)),
    )
