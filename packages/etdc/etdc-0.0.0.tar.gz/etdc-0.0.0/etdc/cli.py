import logging
import os
import shutil
from typing import Optional

import typer

from etdc.collect import collect_data
from etdc.upload.google.key import initialize_service
from etdc.upload.google.storage import (
    delete_file,
    download_all_files,
    download_file,
    list_files,
    upload_file,
)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger("etdc")

app = typer.Typer()


key_opt = typer.Option(None, "--key", help="Encryption key for the service account")


@app.command()
def collect(
    key: Optional[str] = key_opt,
    push=typer.Option(True, "--push", help="Upload to Google Drive"),
):
    """Take hand images."""
    collect_data()
    if push:
        upload(file="output.zip", key=key)


@app.command()
def upload(
    file: str = typer.Argument(
        "output.zip",
        help="Path to zip file to upload to Google Drive",
    ),
    key: Optional[str] = key_opt,
):
    """Upload files to Google Drive."""
    if os.path.exists(file):
        service = initialize_service(key)
        if os.path.isdir(file):
            shutil.make_archive("output", "zip", file)
            file = "output.zip"
        upload_file(file, service)
    else:
        logging.info(f"File {file} does not exist")


@app.command()
def list(
    key: Optional[str] = key_opt,
):
    """List files in Google Drive."""
    service = initialize_service(key)
    list_files(service)


@app.command()
def delete(
    file_id: str = typer.Option(None, "--file-id", help="File ID to download"),
    key: Optional[str] = key_opt,
):
    """List files in Google Drive."""
    service = initialize_service(key)
    delete_file(file_id, service)


@app.command()
def download(
    file_id: Optional[str] = typer.Option(
        None, "--file-id", help="File ID to download"
    ),
    key: Optional[str] = key_opt,
    unpack_dir: Optional[str] = typer.Option(
        None, "--unpack-dir", "-ud", help="Directory to unpack files"
    ),
):
    """Download files from Google Drive."""
    service = initialize_service(key)
    if file_id:
        fn = f"{file_id}.zip"
        download_file(file_id, fn, service)
        if unpack_dir:
            logging.info("Unpacked to %s", unpack_dir)
            os.makedirs(unpack_dir, exist_ok=True)
            shutil.unpack_archive(fn, unpack_dir, "zip")
            os.remove(fn)
    else:
        download_all_files("./output", service)
