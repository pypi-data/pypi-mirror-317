"""Helper for file upload."""

from __future__ import annotations

import asyncio
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
import re
import shutil
import tempfile

from fastapi import UploadFile

from pconn.core import PConn
from pconn.util.ulid import ulid_hex

RE_SANITIZE_FILENAME = re.compile(r"(~|\.\.|/|\\)")
RE_SANITIZE_PATH = re.compile(r"(~|\.(\.)+)")

DOMAIN = "file_upload"
TEMP_DIR_NAME = f"pconn-plugins-{DOMAIN}"


def raise_if_invalid_filename(filename: str) -> None:
    """Check if a filename is valid.

    Raises a ValueError if the filename is invalid.
    """
    if RE_SANITIZE_FILENAME.sub("", filename) != filename:
        raise ValueError(f"{filename} is not a safe filename")


def raise_if_invalid_path(path: str) -> None:
    """Check if a path is valid.

    Raises a ValueError if the path is invalid.
    """
    if RE_SANITIZE_PATH.sub("", path) != path:
        raise ValueError(f"{path} is not a safe path")


@contextmanager
def process_uploaded_file(pconn: PConn, file_id: str) -> Iterator[Path]:
    """Get an uploaded file.

    File is removed at the end of the context.
    """
    if DOMAIN not in pconn.data:
        raise ValueError("File does not exist")

    file_upload_data: FileUploadData = pconn.data[DOMAIN]

    if not file_upload_data.has_file(file_id):
        raise ValueError("File does not exist")

    try:
        yield file_upload_data.file_path(file_id)
    finally:
        file_upload_data.files.pop(file_id)
        shutil.rmtree(file_upload_data.file_dir(file_id))


@dataclass(frozen=True)
class FileUploadData:
    """File upload data."""

    temp_dir: Path
    files: dict[str, str]

    @classmethod
    def create(cls, pconn: PConn) -> FileUploadData:
        """Initialize the file upload data."""

        def _create_temp_dir() -> Path:
            """Create temporary directory."""
            temp_dir = Path(tempfile.gettempdir()) / TEMP_DIR_NAME

            # If it exists, it's an old one and Home Assistant didn't shut down correctly.
            if temp_dir.exists():
                shutil.rmtree(temp_dir)

            return Path(tempfile.mkdtemp())

        temp_dir = _create_temp_dir()

        return cls(temp_dir, {})

    def cleanup_unused_files(self) -> None:
        """Clean up unused files."""
        shutil.rmtree(self.temp_dir)

    def has_file(self, file_id: str) -> bool:
        """Return if file exists."""
        return file_id in self.files

    def file_dir(self, file_id: str) -> Path:
        """Return the file directory."""
        return self.temp_dir / file_id

    def file_path(self, file_id: str) -> Path:
        """Return the file path."""
        return self.file_dir(file_id) / self.files[file_id]


class FileUploadHandler:
    """Class to handle file upload."""

    def __init__(self, pconn: PConn) -> None:
        """Initiate file handler class."""
        self.pconn = pconn
        self._upload_lock: asyncio.Lock | None = None

    def _get_upload_lock(self) -> asyncio.Lock:
        """Get upload lock."""
        if self._upload_lock is None:
            self._upload_lock = asyncio.Lock()

        return self._upload_lock

    async def upload_file(self, file: UploadFile) -> str:
        """Upload a file."""
        async with self._get_upload_lock():
            return await self._upload_file(file)

    async def _upload_file(self, file: UploadFile) -> str:
        """Handle file upload."""
        assert file.filename
        raise_if_invalid_filename(file.filename)

        file_id = ulid_hex()

        if DOMAIN not in self.pconn.data:
            self.pconn.data[DOMAIN] = await self.pconn.async_add_executor_job(
                FileUploadData.create, self.pconn
            )

        file_upload_data: FileUploadData = self.pconn.data[DOMAIN]
        file_dir = file_upload_data.file_dir(file_id)
        file_dir.mkdir()
        with open(file_dir / file.filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        file_upload_data.files[file_id] = file.filename
        return file_id
