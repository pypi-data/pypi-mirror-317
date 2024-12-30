# -*- coding: utf-8 -*-
import os
from typing import Optional


def get_str(key: str, default: str = None) -> Optional[str]:
    v: Optional[str] = os.getenv(key, None)
    if v in ("None",):
        v = None

    if v is None and default is not None:
        v = default
    return v


def get_int(key: str, default: int = None) -> Optional[int]:
    v: str = get_str(key)
    try:
        return int(v)
    except (TypeError, ValueError):
        return default


def get_bool(key: str, default: Optional[bool] = None) -> Optional[bool]:
    v: str = get_str(key)
    if v is None:
        return default

    if v in ("True", "true", "t", "1"):
        return True
    else:
        return False
