#!/usr/bin/env python3
""" Session DB Auth module
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import date, datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """ Session DB Auth class
    """

    def create_session(self, user_id=None):
        """ Creates a session with timeout """
        if user_id:
            session_id = super().create_session(user_id)

            if session_id:
                session = UserSession(
                    user_id=user_id,
                    session_id=session_id
                )

            if session:
                session.save()
                UserSession.save_to_file()
                return session_id

        return None

    def user_id_for_session_id(self, session_id=None):
        """ Returns a user_id with session_id given """
        if session_id:
            UserSession.load_from_file()
            session = UserSession.search({"session_id": session_id})

            if session:
                user = session[0]
                if user:
                    expiration = user.created_at + \
                        timedelta(seconds=self.session_duration)

                    if expiration < datetime.now():
                        return None

                    return user.user_id
        return None

    def destroy_session(self, request=None):
        """ Destroys a session by request """

        if request:
            session_id = self.session_cookie(request)

            if session_id:
                user_id = self.user_id_for_session_id(session_id)

                if user_id:
                    user_session = UserSession.search(
                        {"session_id": session_id})

                    if user_session:
                        try:
                            user_session[0].remove()
                            UserSession.save_to_file()
                        except Exception:
                            return False

                        return True

        return False
