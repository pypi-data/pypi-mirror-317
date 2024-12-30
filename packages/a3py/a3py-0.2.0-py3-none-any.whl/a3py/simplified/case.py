# -*- coding: utf-8 -*-
import re


def snake2camel(snake: str) -> str:
    word_list = list()
    for word in snake.split("_"):
        word_list.append(word.capitalize())
    return "".join(word_list)


def camel2snake(camel: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", camel).lower()
