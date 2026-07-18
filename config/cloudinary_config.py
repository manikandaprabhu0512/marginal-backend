import os
from urllib.parse import urlparse

import cloudinary
import cloudinary.api
import cloudinary.uploader
from dotenv import load_dotenv

load_dotenv(override=True)

def _env(name: str) -> str | None:
    value = os.getenv(name)
    return value.strip() if value else None


def _credentials_from_url() -> tuple[str | None, str | None, str | None]:
    cloudinary_url = _env("CLOUDINARY_URL")
    if not cloudinary_url:
        return None, None, None

    parsed = urlparse(cloudinary_url)
    return parsed.hostname, parsed.username, parsed.password


url_cloud_name, url_api_key, url_api_secret = _credentials_from_url()
cloud_name = _env("CLOUDINARY_CLOUD_NAME") or url_cloud_name
api_key = _env("CLOUDINARY_API_KEY") or url_api_key
api_secret = _env("CLOUDINARY_API_SECRET") or url_api_secret

missing = [
    name
    for name, value in {
        "CLOUDINARY_CLOUD_NAME": cloud_name,
        "CLOUDINARY_API_KEY": api_key,
        "CLOUDINARY_API_SECRET": api_secret,
    }.items()
    if not value
]

if missing:
    raise RuntimeError(
        "Missing Cloudinary configuration: "
        + ", ".join(missing)
        + ". Set CLOUDINARY_URL or all three CLOUDINARY_* variables."
    )

cloudinary.config(
    cloud_name=cloud_name,
    api_key=api_key,
    api_secret=api_secret,
    secure=True
)   
