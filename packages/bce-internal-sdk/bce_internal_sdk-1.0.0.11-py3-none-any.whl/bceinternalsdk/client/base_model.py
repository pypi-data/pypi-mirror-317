#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/11/1
# @Author  : zhoubohan
# @File    : base_model.py
"""
from enum import Enum
from typing import Any, Type, Dict, TypeVar

import pydantic

T = TypeVar("T", bound="BaseModel")


class BaseModel(pydantic.BaseModel):
    """
    Base Model contains the common configuration for all pydantic models
    """

    class Config:
        """
        Config contains the common configuration for all pydantic models
        """

        populate_by_name = True
        protected_namespaces = []
        use_uppercase_id = False

        @classmethod
        def alias_generator(cls, field_name: str) -> str:
            """
            alias_generator generates the alias for the field name.
            """
            parts = field_name.split("_")
            # 处理以'id'结尾的特殊情况
            if parts[-1].lower() == "id":
                id_suffix = "ID" if cls.use_uppercase_id else "Id"
                if len(parts) == 1:
                    return id_suffix
                return "".join(
                    [parts[0], *[word.capitalize() for word in parts[1:-1]], id_suffix]
                )

            return parts[0] + "".join(word.capitalize() for word in parts[1:])

    def json(self, **kwargs):
        """
        Override the json method to convert Enum to its value
        """
        original_dict = super().model_dump(**kwargs)
        for key, value in original_dict.items():
            if isinstance(value, Enum):
                original_dict[key] = value.value
        return super().model_dump_json(by_alias=True, exclude_unset=True, **kwargs)

    def model_dump_json(self, **kwargs):
        """
        Override the model_dump_json method to convert Enum to its value
        """
        return self.json(**kwargs)

    @classmethod
    def from_response(cls: Type[T], response: Dict[str, Any]) -> T:
        """
        Convert the response to the model.
        """
        data = {}
        for key in dir(response):
            if not key.startswith("_"):
                value = getattr(response, key)
                data[key] = value

        return cls.model_validate(data)

    def model_dump(self, **kwargs):
        """
        Override the model_dump method to convert Enum to its value
        """
        original_dict = dict(self.__dict__)
        result = {}
        for key, value in original_dict.items():
            if value is None:
                continue
            if isinstance(value, Enum):
                result[key] = value.value
                continue
            result[key] = value
        return result

    def field_exists(self, field_name: str) -> bool:
        """
        Check if the specified field exists in the model.

        :param field_name: The name of the field to check for existence.
        :return: True if the field exists, False otherwise.
        """
        return field_name in self.model_fields
