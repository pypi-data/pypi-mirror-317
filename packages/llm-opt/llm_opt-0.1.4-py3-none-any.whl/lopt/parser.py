import json
import re
from typing import Any

import yaml
from pydantic import ValidationError

from lopt.errors import NoCodeFoundError, ParseModelError, ParseObjectError
from lopt.models import Language, ModelT


def parse_multi_line(s: str, *, lang: Language) -> str | None:
    if match := re.search(rf"```(?:{re.escape(lang)})?(.+)```", s, re.DOTALL):
        return match[1]

    return None


def parse_inline(s: str) -> str | None:
    if match := re.search(r"`(.+)`", s):
        return match[1]

    return None


def parse_code(s: str, *, lang: Language) -> str:
    if multi_line := parse_multi_line(s, lang=lang):
        return multi_line

    if inline := parse_inline(s):
        return inline

    raise NoCodeFoundError(data=s, lang=lang)


def _parse_object(
    s: str,
    *,
    lang: Language,
    ignore_errors: bool = True,
) -> Any:
    parsers = {
        "json": json.loads,
        "yaml": yaml.safe_load,
    }

    try:
        return parsers[lang](s)

    except BaseException as error:
        if not ignore_errors:
            raise ParseObjectError(data=s) from error

    return None


def parse_object(
    s: str,
    *,
    lang: Language,
    ignore_errors: bool = True,
) -> Any | None:
    try:
        data_str = parse_code(s, lang=lang)

    except NoCodeFoundError:
        if not ignore_errors:
            raise

        data_str = s.strip("`")

    if not data_str:
        if ignore_errors:
            return None

        raise NoCodeFoundError(data=s, lang=lang)

    return _parse_object(data_str, lang=lang, ignore_errors=ignore_errors)


def parse_model(
    s: str,
    *,
    lang: Language,
    model: type[ModelT],
    ignore_errors: bool = True,
) -> ModelT | None:
    try:
        data_str = parse_code(s, lang=lang)

    except NoCodeFoundError:
        data_str = s.strip("`")

    if not data_str:
        if ignore_errors:
            return None

        raise NoCodeFoundError(data=s, lang=lang)

    try:
        obj = _parse_object(data_str, lang=lang)

    except ParseObjectError:
        if not ignore_errors:
            raise

        return None

    else:
        try:
            return model.model_validate(obj)

        except ValidationError as error:
            if not ignore_errors:
                raise ParseModelError(model=model, data=data_str) from error

            return None
