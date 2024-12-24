"""
Entry point for running the Dell Unisphere Mock API.
"""
import uvicorn

from dell_unisphere_mock_api.main import app


def main():
    """Run the application using uvicorn."""
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")


if __name__ == "__main__":
    main()
