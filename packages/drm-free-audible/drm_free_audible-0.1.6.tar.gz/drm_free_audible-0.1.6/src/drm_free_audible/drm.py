"""Module provides functionality to remove DRM (Digital Righs Management) from Audible files."""

import logging

logger = logging.getLogger(__name__)

import subprocess
from pathlib import Path
import ffmpeg


# Audible activation code
# [aax] file checksum == fa6de07372739ef883a168936ecede1b3a463503
ACTIVATION_CODE = "7766aa03"


def remove_drm(src_file, dst_dir):
    # Remove DRM from src_file, and save the DRM free file in dst_dir.
    dst_file = dst_dir / (src_file.stem + ".m4b")
    # Confirm if the destination file already exists. If it does, skip the file.
    if dst_file.exists():
        # Prompt if overwrite the file.
        logger.info(f"{dst_file} already exists. Overwrite? (y/n)")
        if input().lower() == "y":
            logger.info(f"Overwriting {dst_file}...")
        else:
            logger.info(f"Skipping {dst_file}...")
            return
    logger.info(f"Removing DRM from {src_file} to {dst_file}")
    try:
        (
            ffmpeg.input(str(src_file), activation_bytes=ACTIVATION_CODE)
            .output(str(dst_file), codec="copy")
            .run(capture_stdout=True, capture_stderr=True)
        )
        logger.info(f"{dst_file} generated")
    except ffmpeg.Error as e:
        logger.error(f"Error occurred: {e.stderr.decode()}")
    logger.info(f"{dst_file} generated")


def create_drm_free_files(src: str, dst: str) -> None:
    """Create DRM free files in dst from aax files in src."""
    logger.info(f"Processing from {src} to {dst}")
    src_dir = Path(src)
    dst_dir = Path(dst)
    # Extension of Audbile files is .aax
    extension = ".aax"
    # Check if the source path is a directory and exists.
    if src_dir.is_dir():
        for src_file in src_dir.glob(f"*{extension}"):
            logger.info(f"Found DRM file {src_file}")
            # Remove DRM from the file
            remove_drm(src_file, dst_dir)
    # Check if the destination path is a directory and exists. If not, prompt to create it.
    if not dst_dir.is_dir():
        logger.info(f"Destination directory {dst_dir} does not exist. Create it? (y/n)")
        if input().lower() == "y":
            dst_dir.mkdir(parents=True)
            logger.info(f"Destination directory {dst_dir} created.")
        else:
            logger.info("Exiting program. Create destination directory and run the program again.")
            return

    logger.info("Successfully created DRM-free files.")
