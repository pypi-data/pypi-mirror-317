import base64
import re
from typing import Any, Union

from PIL.Image import Image


def encode_image(image_path: Union[str, bytes]) -> str:
    if isinstance(image_path, bytes):
        return base64.b64encode(image_path).decode("utf-8")

    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def is_url(path: str) -> bool:
    url_pattern = re.compile(r"^[a-zA-Z][a-zA-Z\d+\-.]*://")
    return bool(url_pattern.match(path))


def contains_image(inputs: Any) -> bool:
    if isinstance(inputs, list):
        return any(isinstance(item, Image) for item in inputs)
    return isinstance(inputs, Image)
