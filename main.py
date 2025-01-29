import argparse
import asyncio

import uvicorn

from src.app.web import create_web_app
from src.app.etl import create_etl_app


async def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Run the desired app.")
    parser.add_argument(
        "app",
        choices=["web", "etl"],
        help="The app to run: 'web' for the web app, 'etl' for the ETL app.",
    )
    args = parser.parse_args()

    # Run the appropriate app based on the argument
    if args.app == "web":
        print("Starting the web app...")
        app = create_web_app()
        uvicorn.run(app)
    elif args.app == "etl":
        print("Starting the ETL app...")
        app = create_etl_app()
        await app.sync()


if __name__ == "__main__":
    asyncio.run(main())
