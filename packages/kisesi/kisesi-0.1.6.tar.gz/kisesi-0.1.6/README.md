# Kisesi
Kisesi is a light wrapper around the built-in `logging` module of Python standard library. This module is written in a hacky way and thus is meant for personal use.

# Demos
```python
import kisesi


def main() -> None:
    kisesi.basic_config(level=kisesi.DEBUG, incdate=True)

    log = kisesi.get_logger(__name__)
    log.debug("This is a \"debug\" message.")
    log.info("This is a \"info\" message.")
    log.warning("This is a \"warning\" message.")
    log.error("This is a \"error\" message.")
    log.critical("This is a \"critical\" message.")


if __name__ == "__main__":
    main()
```

## Preview
### Maple Font
![Demo Image](https://files.catbox.moe/wmmvsx.png)

### Normal
```
[12/25/24 09:28:35 PM] [DEBUG] @ __main__.py:8 main :: This is a "debug" message.
[12/25/24 09:28:35 PM] [INFO] @ __main__.py:9 main :: This is a "info" message.
[12/25/24 09:28:35 PM] [WARN] @ __main__.py:10 main :: This is a "warning" message.
[12/25/24 09:28:35 PM] [ERROR] @ __main__.py:11 main :: This is a "error" message.
[12/25/24 09:28:35 PM] [CRITICAL] @ __main__.py:12 main :: This is a "critical" message.
```
(You'll get colored level names in normal fonts as well)

# Guide
You are expected to read the source code to figure out all the features.

# Installation
Pypi
```shell
user:~$ pip install kisesi
```
Git
```shell
user:~$ pip install git+https://github.com/eeriemyxi/kisesi
