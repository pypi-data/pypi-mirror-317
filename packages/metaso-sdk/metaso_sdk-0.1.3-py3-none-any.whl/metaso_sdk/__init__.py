"""metaso-sdk package.

The official Python SDK for https://metaso.cn
"""

from __future__ import annotations

from .model import File, Query, Status, Topic
from .search import search
from .subject import create_topic, delete_file, delete_topic, update_progress, upload_directory, upload_file

__all__: list[str] = [
    "Status",
    "Query",
    "Topic",
    "File",
    "search",
    "create_topic",
    "delete_topic",
    "upload_file",
    "update_progress",
    "delete_file",
    "upload_directory",
]
