from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import discord

try:
    from replit import Database
    from replit import db as DB
except (ImportError, ModuleNotFoundError):
    DB = {}

LANGS = []
LANG_CODES = [item[1] for item in LANGS]
db: dict | Any = DB or {}

data = {"db": db, "path": "translation/"}


class loc:
    """Represents the localization class."""

    def __init__(self, c: dict[str, str | dict | int | float | bool]):
        self.c = c

    def obj(self, key: str, /, default=None) -> Any:
        """
        Retrieve an object / anything instead of strings.

        :param str key: The key.
        :param Any default: Default value.
        """
        return self.c.get(key, default)

    def __call__(
        self, key: str, /, default: str | None = "<Not Translated>", **kwargs
    ) -> str | None:
        """
        Retrieve the localization string.

        ```python
        reg = region(ctx)
        reg("my-key", "Not Translated!", wow=True)

        # example loadable JSON:
        {
            "my-key": "Is wow true? {wow}"
        }
        ```

        :param str key: The key.
        :param Any default: Default value if not found. Must be literal strings.
        :kwargs: String interpolation.
        """
        prep: str | Any = self.c.get(key, default)

        if not isinstance(prep, str):
            raise TypeError(f"Value expected to be string, got {type(prep)}")

        if prep:
            for target, content in kwargs.items():
                prep = prep.replace("{" + target + "}", content)

        return prep


def init(
    translation_path: str | Path, database: dict | Any, langs: list[tuple[str, str]]
) -> None:
    """
    Initialize Region.

    ```python
    from replit import db
    from region import init, region
    
    init(
      translation_path"translation/", # path to the translation files
      database="database": db, # your database, for here: Replit db
      langs=[
        # pairs of supported languages
        # NAME            CODE
        ("English (US)", "en-US"),
        ("中文（繁體）",  "zh-TW")
      ]
    )
    ```

    :param translation_path: Translation path, such as `translation/`
    :param database: The database, such as `replit.db`
    :param langs: Pair of supported languages:  `("LANGUAGE NAME", "LANGUAGE CODE")`
    """
    # NO_EQU
    for lang in langs:
        LANGS.append(lang)

    LANG_CODES.clear()
    for item in LANGS:
        LANG_CODES.append(item[1])

    data["db"] = database
    data["path"] = translation_path


def region(
    context: discord.Interaction
    | discord.ApplicationContext
    | discord.Message
    | discord.AutocompleteContext,
) -> loc:
    """
    Represents the Region localization helper function. `db` must be configered first.
    """
    db = data["db"]

    if getattr(context, "author", None):
        user: int = context.author.id  # type: ignore
    elif getattr(context, "user", None):
        user: int = context.user.id  # type: ignore
    elif getattr(context, "interaction", None):
        user: int = context.interaction.user.id  # type: ignore
    else:
        raise TypeError(f"Unknown type: {context!r}")

    res = db["region"].get(str(user), None)

    if not res:
        match context:
            case discord.ApplicationContext():
                locale: str = context.interaction.locale  # type: ignore
            case _:
                try:
                    locale: str = context.locale  # type: ignore
                except AttributeError:
                    locale: str = "en-US"

        LOCALE: str = locale if locale in LANG_CODES else "en-US"
        db["region"][str(context.author.id)] = LOCALE  # type: ignore
    else:
        LOCALE: str = res

    with open(data['path'] + LOCALE + ".json") as file:
        return loc(json.load(file))
