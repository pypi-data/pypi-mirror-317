"""Module sets up logging and runs the main application."""

import logging
import logging.config
from pathlib import Path
import yaml
from importlib import resources


def setup_logging():
    """Set up logging configuration from a YAML file."""
    # Determine the package's installation directory
    package_dir = Path(resources.files("drm_free_audible"))
    logs_dir = package_dir / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)

    # Load the logging configuration
    with resources.open_text("drm_free_audible", "logging_config.yaml") as file:
        config = yaml.safe_load(file)

    # Update the log file path in the configuration
    log_file_path = logs_dir / "app.log"
    config["handlers"]["file"]["filename"] = str(log_file_path)

    logging.config.dictConfig(config)

    # Log the location of the log file
    logger = logging.getLogger(__name__)
    logger.info(f"Log file is located at: {log_file_path}")


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
