import logging

logger = logging.getLogger(__name__)


class ColoredFormatter(logging.Formatter):
    COLOR_CODES = {
        logging.CRITICAL: "\033[1;35m",  # Magenta
        logging.ERROR: "\033[1;31m",  # Red
        logging.WARNING: "\033[1;33m",  # Yellow
        logging.INFO: "\033[0;37m",  # White
        logging.DEBUG: "\033[1;34m",  # Blue
    }

    def format(self, record):
        color = self.COLOR_CODES.get(record.levelno, "")
        reset = "\033[0m"
        formatted = super().format(record)
        return f"{color}{formatted}{reset}"


def set_logger_level(level):
    """
    Set the logger level.

    Args:
        level (str): The desired logger level.
            Possible values: "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"
    """
    try:
        logger.setLevel(getattr(logging, level.upper()))
    except AttributeError:
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        raise ValueError(
            f"Invalid logger level: {level}. Valid levels are: {', '.join(valid_levels)}"
        )


handler = logging.StreamHandler()
handler.setFormatter(ColoredFormatter())
logger.addHandler(handler)
