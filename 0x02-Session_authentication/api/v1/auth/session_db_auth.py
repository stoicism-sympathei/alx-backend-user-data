#!/usr/bin/env python3
"""
API session db module
"""

from api.v1.auth.session_exp_auth import SessionExpAuth
from os import getenv


class SessionDBAuth(SessionExpAuth):
    """ Session DB Auth """

    def create_session(self, user_id: str = None) -> str:
        """ Creates a Session ID for user_id """
        pass

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Returns User ID based on Session ID """

        if session_id is None or isinstance(session_id, str) is False:
            return None
        else:
            pass

    def destroy_session(self, request=None):
        """ Deletes user session to logout """
        pass
