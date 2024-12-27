#!/usr/bin/env python3
# coding: utf-8
from __future__ import annotations

import base64
import hashlib
import math
import mimetypes
import os
import shutil
from pathlib import Path
from typing import Generator, Union, Iterable
from uuid import uuid4

Pathlike = Union[str, os.PathLike]
Filelike = Union[str, os.PathLike, Iterable[bytes]]

# for compatibility; will be removed in version 0.3.0
PathLike = Pathlike
FileLike = Filelike


def read_as_chunks(
    path: Pathlike, length=-1, offset=0, chunksize=65536
) -> Generator[bytes, None, None]:
    if length == 0:
        return
    if length < 0:
        length = float("inf")
    chunksize = min(chunksize, length)
    with open(path, "rb") as fin:
        fin.seek(offset)
        while chunksize:
            chunk = fin.read(chunksize)
            if not chunk:
                break
            yield chunk
            length -= chunksize
            chunksize = min(chunksize, length)


def compute_checksum(path_or_chunks: Filelike, algo="sha1"):
    hashobj = hashlib.new(algo) if isinstance(algo, str) else algo
    # path_or_chunks:str - a path
    if isinstance(path_or_chunks, str):
        chunks = read_as_chunks(path_or_chunks)
    else:
        chunks = path_or_chunks
    for chunk in chunks:
        hashobj.update(chunk)
    return hashobj


def checksum(path: Pathlike, algo="sha1", length=-1, offset=0):
    chunks = read_as_chunks(path, length=length, offset=offset)
    return compute_checksum(chunks, algo=algo)


def checksum_hexdigest(path: Pathlike, algo="sha1", length=-1, offset=0):
    hashobj = checksum(path, algo=algo, length=length, offset=offset)
    return hashobj.hexdigest()


def b32_sha1sum(path: Pathlike, length=-1, offset=0):
    hashobj = checksum(path, algo="sha1", length=length, offset=offset)
    return base64.b32encode(hashobj.digest()).upper().decode()


def b64_sha384sum(path: Pathlike, length=-1, offset=0):
    hashobj = checksum(path, algo="sha384", length=length, offset=offset)
    return base64.urlsafe_b64encode(hashobj.digest()).decode()


def b64_encode_data_url(mediatype: str, content: bytes) -> str:
    b64 = base64.b64encode(content).decode("ascii")
    return "data:{};base64,{}".format(mediatype, b64)


def b64_encode_local_file(path: Pathlike) -> str:
    mediatype = mimetypes.guess_type(path)[0]
    with open(path, "rb") as fin:
        return b64_encode_data_url(mediatype, fin.read())


def spread_by_prefix(filename: str, depth: int = 2, width: int = 2) -> list:
    names = []
    for i in range(depth):
        start = i * width
        stop = start + width
        part = filename[start:stop]
        if not part:
            break
        names.append(part)
    names.append(filename)
    return names


def compute_collision_probability(buckets: int, balls: int) -> float:
    x = -balls * (balls - 1) / 2.0 / buckets
    return 1.0 - math.exp(x)


def random_hex(length=24) -> str:
    size = sum(divmod(length, 2))
    bs = os.urandom(size)
    return bs.hex()[:length]


def guess_content_type(content: bytes):
    if content.startswith(b"%PDF-"):
        return "application/pdf"
    if content.startswith(b"\x89PNG\r\n\x1a\n"):
        return "image/png"
    if content.startswith(b"\xFF\xD8\xFF"):
        return "image/jpeg"


def gen_unique_filename(title: str = "tmp"):
    u = uuid4().bytes.hex().upper()
    return f"{title}.{u}.part"


def moves(old: Pathlike, new: Path):
    # old and new are possibly on different volumes
    # tmp and new are surely on the same volume
    new.parent.mkdir(parents=True, exist_ok=True)
    tmp = new.parent / gen_unique_filename(new.name)
    try:
        shutil.move(old, tmp)
        os.rename(tmp, new)
    finally:
        if tmp.exists():
            tmp.unlink(missing_ok=True)


def saves(path: Pathlike, chunks: Iterable[bytes]):
    """
    Save content safely.
    Args:
        path: the file to be created or replaced
        chunks: iterable of chunks of content to be saved
    """
    if not isinstance(path, Path):
        path = Path(path)
    tmp = path.with_name(gen_unique_filename())
    with open(tmp, "wb") as fout:
        for chunk in chunks:
            fout.write(chunk)
    tmp.rename(path)


def find_regular_files(dirpath, **kwargs):
    for root, dirs, files in os.walk(dirpath, **kwargs):
        for name in files:
            path = os.path.join(root, name)
            if os.path.isfile(path):
                yield path


def infer_st_dev(path: Pathlike) -> int:
    while True:
        if os.path.exists(path):
            return os.stat(path).st_dev
        path = os.path.split(path)[0]
