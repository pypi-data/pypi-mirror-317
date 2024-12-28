"""Module sets up logging and runs the main application."""

import logging.config
import yaml


def setup_logging():
    with open("logging_config.yaml", "r") as file:
        config = yaml.safe_load(file)
    logging.config.dictConfig(config)


setup_logging()
logger = logging.getLogger(__name__)

import argparse

from drm_free_audible.drm import create_drm_free_files


def main() -> None:
    """Set up logging and run the application."""
    logger.debug("Program started.")
    parser = argparse.ArgumentParser(description="Create DRM-free files from src to dst")
    parser.add_argument("src", type=str, help="Source path")
    parser.add_argument("dst", type=str, help="Destination path")
    args = parser.parse_args()
    create_drm_free_files(args.src, args.dst)
    logger.info("Program completed.")


if __name__ == "__main__":
    main()
