#!/usr/bin/env python3
""" Auth module
"""
from flask import request
from typing import List, TypeVar
import re


class Auth():
    """ Auth class
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
            Args:
                path: the path
                excluded_paths: a list of excluded paths

            Returns:
                True or False
        """
        if path and not path.endswith("/"):
            path += "/"
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path is None:
            return True
        for item in excluded_paths:
            if '*' in item:
                item = item.replace('*', '.*')
                item = item.replace('/', r'\/')
                if re.compile(item).match(path) is not None:
                    return False
        if path not in excluded_paths:
            return True

        return False

    def authorization_header(self, request=None) -> str:
        """
            Args:
                request: the Flask request object.

            Returns:
                None
        """
        if request and "Authorization" in request.headers:
            return request.headers.get("Authorization", default=None)
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
            Args:
                request: the Flask request object.

            Returns:
                None
        """
        return None
