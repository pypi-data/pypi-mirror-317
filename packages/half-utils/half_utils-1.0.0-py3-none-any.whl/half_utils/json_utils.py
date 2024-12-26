from json import dumps as js_dumps, load as js_load
from typing import Optional, Union

from json5 import dumps as js5_dumps, load as js5_load
from loguru import logger

from .file_utils import check_file


def read_json(filename: str, *,
              skip_file_check: bool = False,
              create_if_not_exist: bool = False,
              file_content: str = "{}") -> Optional[dict]:
    if not skip_file_check:
        if not check_file(filename, create_if_not_exist=create_if_not_exist,
                          file_content=file_content) and not create_if_not_exist:
            logger.error(f"File {filename} not found.")
    try:
        with open(filename, "r", encoding="utf-8") as f:
            if filename.endswith(".json"):
                return js_load(f)
            return js5_load(f)
    except Exception as e:
        logger.exception(e)
        logger.error(f"Broken file {filename}.")
        return None


def write_json(filename: str, data: Union[dict, list]) -> None:
    try:
        with open(filename, "w", encoding="utf-8") as f:
            if filename.endswith(".json"):
                f.write(js_dumps(data, indent=4, ensure_ascii=False))
            else:
                f.write(js5_dumps(data, indent=4, ensure_ascii=False))
    except Exception as e:
        logger.exception(e)
        logger.error(f"Broken file {filename}.")
