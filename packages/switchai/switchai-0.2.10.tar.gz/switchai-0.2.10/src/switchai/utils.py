import base64
import re


def encode_image(image_path: str | bytes) -> str:
    if isinstance(image_path, bytes):
        return base64.b64encode(image_path).decode("utf-8")

    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def is_url(path: str) -> bool:
    url_pattern = re.compile(r"^[a-zA-Z][a-zA-Z\d+\-.]*://")
    return bool(url_pattern.match(path))
