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


class Logger(Logger):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def set_level(self, level):
        return self.setLevel(level)

    def is_enabled_for(self, level):
        return self.isEnabledFor(level)

    def get_child(self, suffix):
        return self.getChild(suffix)

    def get_children(self):
        return self.getChildren()

    def add_filter(self, filter):
        return self.addFilter(filter)

    def remove_filter(self, filter):
        return self.removeFilter(filter)

    def add_handler(self, hdlr):
        return self.addHandler(hdlr)

    def remove_handler(self, hdlr):
        return self.removeHandler(hdlr)

    def find_caller(self, stack_info=False, stacklevel=1):
        return self.findCaller(stack_info, stacklevel)

    def make_record(
        self,
        name,
        level,
        fn,
        lno,
        msg,
        args,
        exc_info,
        func=None,
        extra=None,
        sinfo=None,
    ):
        return self.makeRecord(
            name, level, fn, lno, msg, args, exc_info, func, extra, sinfo
        )

    def has_handlers():
        return self.hasHandlers()


def _get_default_kisesi_handler(fmt, datefmt):
    handler = StreamHandler()
    handler.setFormatter(ColoredFormatter(fmt, datefmt=datefmt))
    return handler


def get_logger(name=None):
    return getLogger(name)


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
