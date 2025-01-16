from loguru import logger

# Configure logger
logger.add(
    "logs/app.log", rotation="500 MB", level="INFO", format="{time} {level} {message}"
)
