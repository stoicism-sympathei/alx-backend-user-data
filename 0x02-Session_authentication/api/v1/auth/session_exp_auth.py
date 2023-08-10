#!/usr/bin/env python3
""" Session Expiration Auth module
"""
from os import getenv
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """ Session Expiration Auth class
    """

    def __init__(self):
        SESSION_DURATION = getenv("SESSION_DURATION")

        try:
            SESSION_DURATION = int(SESSION_DURATION)
        except Exception:
            SESSION_DURATION = 0

        self.session_duration = SESSION_DURATION

    def create_session(self, user_id=None):
        """ Creates a session with timeout """
        try:
            session_id = super().create_session(user_id)
        except Exception:
            return None

        self.user_id_by_session_id[session_id] = {
            "user_id": user_id,
            "created_at": datetime.now()
        }

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Returns a user_id with session_id given """
        if not session_id \
                or session_id not in self.user_id_by_session_id.keys():
            return None

        session_dictionnary = self.user_id_by_session_id.get(session_id)

        if self.session_duration <= 0 or not session_dictionnary:
            return session_dictionnary.get("user_id", None)

        created_at = session_dictionnary.get("created_at", None)
        if not created_at:
            return None

        expiration = created_at + \
            timedelta(seconds=self.session_duration)

        if expiration < datetime.now():
            return None

        return session_dictionnary.get("user_id", None)
