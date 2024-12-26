from logging import *

KISESI_DEFAULT_FORMAT_STRING = (
    "[%(asctime)s] %(levelname)s @ %(filename)s:%(lineno)d %(funcName)s :: %(message)s"
)
NOT_SET = NOTSET


class Color:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    REVERSE = "\033[7m"

    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"
    
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"


class ColoredFormatter(Formatter):
    LEVEL_COLORS = {
        DEBUG: Color.BRIGHT_CYAN,
        INFO: Color.BRIGHT_GREEN,
        WARNING: Color.BRIGHT_YELLOW,
        ERROR: Color.BRIGHT_RED,
        CRITICAL: f"{Color.BG_RED}{Color.BRIGHT_WHITE}",
    }
    LEVEL_NAMES = {
        WARNING: "WARN",
    }

    def format(self, record):
        level_color = self.LEVEL_COLORS.get(record.levelno, "")
        level_name = self.LEVEL_NAMES.get(record.levelno, record.levelname)
        record.levelname = f"{level_color}[{level_name}]{Color.RESET}"
        return super().format(record)


def _get_default_kisesi_handler(fmt, datefmt):
    handler = StreamHandler()
    handler.setFormatter(ColoredFormatter(fmt, datefmt=datefmt))
    return handler


def monkeypatch_logger(logger):
    if not logger:
        return None

    # somewhere down the line in recursion, it returns a `logging.RootLogger`,
    # we handle that case here by not patching a `logging.RootLogger`
    if not isinstance(logger, Logger):
        return logger

    if getattr(logger, "__KISESI__", False):
        return logger

    logger.set_level = logger.setLevel
    logger.is_enabled_for = logger.isEnabledFor
    logger.get_child = lambda *args, **kwargs: monkeypatch_logger(
        logger.getChild(*args, **kwargs)
    )
    logger.get_children = lambda *args, **kwargs: monkeypatch_logger(
        logger.getChildren(*args, **kwargs)
    )
    logger.add_filter = logger.addFilter
    logger.remove_filter = logger.removeFilter
    logger.find_caller = logger.findCaller
    logger.make_record = logger.makeRecord
    logger.has_handlers = logger.hasHandlers

    logger.parent = monkeypatch_logger(logger.parent)

    logger.__KISESI__ = True

    return logger


def get_logger(name=None):
    return monkeypatch_logger(getLogger(name))


def basic_config(*, incdate=False, use12h=True, **kwargs):
    if not kwargs.get("format"):
        kwargs["format"] = KISESI_DEFAULT_FORMAT_STRING

    if not kwargs.get("datefmt"):
        if use12h:
            kwargs["datefmt"] = "%I:%M:%S %p"
        else:
            kwargs["datefmt"] = "%T"

        if incdate:
            kwargs["datefmt"] = "%D " + kwargs["datefmt"]

    if not kwargs.get("handlers"):
        kwargs["handlers"] = [
            _get_default_kisesi_handler(kwargs.get("format"), kwargs.get("datefmt"))
        ]

    return basicConfig(**kwargs)
