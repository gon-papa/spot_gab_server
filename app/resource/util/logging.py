import logging
import traceback

logger = logging.getLogger("app.exception")


class Log:
    def errorLog(self, e: Exception):
        tb = traceback.format_exc()
        logger.error(f"An error occurred: {e}\n{tb}")
