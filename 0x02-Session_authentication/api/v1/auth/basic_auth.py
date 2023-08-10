#!/usr/bin/env python3
""" BasicAuth module
"""
from api.v1.auth.auth import Auth
from base64 import b64decode
from typing import Tuple, TypeVar
from models.user import User


class BasicAuth(Auth):
    """ BasicAuth class
    """

    def extract_base64_authorization_header(
            self,
            authorization_header: str) -> str:
        """
            Returns the Base64 part of the Authorization
            header for a Basic Authentication

            Args:
                authorization_header: the header containing Authorization

            Returns:
                The Base64 part of the header or None
        """
        if authorization_header and type(authorization_header) is str:
            if authorization_header.startswith("Basic "):
                return authorization_header[6:]
        return None

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str) -> str:
        """
            Returns the decoded value of a Base64
            string base64_authorization_header

            Args:
                base64_authorization_header: the base_64 header

            Returns:
                The decoded value of the header
        """
        if base64_authorization_header \
                and type(base64_authorization_header) is str:
            try:
                return b64decode(base64_authorization_header).decode('utf-8')
            except Exception:
                return None
        return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str) -> Tuple[str, str]:
        """
            Returns the user email and password from the Base64 decoded value

            Args:
                decoded_base64_authorization_header: the base_64 decoded header

            Returns:
                A tuple containing the user email and password or (None, None)
        """
        if decoded_base64_authorization_header:
            if type(decoded_base64_authorization_header) is str:
                if ":" in decoded_base64_authorization_header:
                    split = decoded_base64_authorization_header.split(":", 1)
                    return (split[0], split[1])
        return (None, None)

    def user_object_from_credentials(
            self,
            user_email: str, user_pwd: str) -> TypeVar('User'):
        """
            Returns the User instance based on his email and password

            Args:
                user_email: the email of the user
                user_pwd: the password of the user

            Returns:
                A User instance, or None
        """
        if user_email and type(user_email) is str:
            if user_pwd and type(user_pwd) is str:
                try:
                    usr = User.search({"email": user_email})
                    if len(usr):
                        usr = usr[0]
                        return usr if usr.is_valid_password(user_pwd) else None
                except Exception:
                    return None
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
            Overloads Auth and retrieves the User instance for a request

            Args:
                request: the request

            Returns:
                A User instance, or None
        """
        header = self.authorization_header(request)
        b64hdr = self.extract_base64_authorization_header(header)
        dcdhdr = self.decode_base64_authorization_header(b64hdr)
        credentials = self.extract_user_credentials(dcdhdr)
        return self.user_object_from_credentials(*credentials)
