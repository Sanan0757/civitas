import argparse
import asyncio
import logging

from src.app import create_app
from src.pkg.config import get_settings

settings = get_settings()

logging.basicConfig(
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
    level=settings.LOG_LEVEL,
)
logger = logging.getLogger(__name__)


def main():
    """Main entry point for the application."""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Run the desired app.")
    parser.add_argument(
        "app",
        choices=["web", "etl"],
        help="The app to run: 'web' for the web app, 'etl' for the ETL app.",
    )
    parser.add_argument(
        "--automigrate",
        action="store_true",
        help="Run Alembic migrations before starting the app",
    )
    args = parser.parse_args()
    app = create_app(settings)

    # Run the selected application
    if args.app == "web":
        logger.info("Starting the web app...")
        app.serve()
    elif args.app == "etl":
        logger.info("Starting the ETL process...")
        asyncio.run(app.sync())
        logger.info("ETL process completed.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.warning("Shutdown requested. Exiting...")
