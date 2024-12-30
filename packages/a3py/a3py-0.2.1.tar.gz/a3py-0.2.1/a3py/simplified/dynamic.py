# -*- coding: utf-8 -*-
import inspect
from importlib import import_module
from types import ModuleType
from typing import List, Type, TypeVar

T = TypeVar("T")


def find_all_subclasses(module: str | ModuleType, base_class: Type[T]) -> List[Type[T]]:
    if isinstance(module, str):
        module = import_module(module)

    all_class_list = list()
    for name in dir(module):
        obj = getattr(module, name)
        if inspect.isclass(obj):
            all_class_list.append(obj)

    all_subclass_list = list()
    for the_class in all_class_list:
        if issubclass(the_class, base_class) and the_class != base_class:
            all_subclass_list.append(the_class)

    return all_subclass_list


def import_string(dotted_path: str):
    try:
        module_path, class_name = dotted_path.rsplit(".", 1)
    except ValueError as err:
        raise ImportError(f"{dotted_path} doesn't look like a module path") from err

    module = import_module(module_path)

    try:
        return getattr(module, class_name)
    except AttributeError as err:
        raise ImportError(
            f'Module "{module}" does not define a "{class_name}" attribute/class'
        ) from err
