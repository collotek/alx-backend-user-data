#!/usr/bin/env python3
"""_summary_"""

from os import getenv
from api.v1.auth.auth import Auth
from uuid import uuid4
from typing import Dict
from models.user import User


class SessionAuth(Auth):
    """_summary_

    Args:
        Auth (_type_): _description_
    """
    user_id_by_session_id: Dict = {}

    def create_session(self, user_id: str = None) -> str:
        """_summary_

        Args:
            user_id (str, optional): _description_. Defaults to None.

        Returns:
            str: _description_
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        sesh_id = str(uuid4())
        SessionAuth.user_id_by_session_id[sesh_id] = user_id

        return sesh_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """_summary_

        Args:
            session_id (str, optional): _description_. Defaults to None.

        Returns:
            str: _description_
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        return SessionAuth.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """_summary_

        Args:
            request (_type_, optional): _description_. Defaults to None.
        """
        cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(cookie)
        return User.get(user_id)

    def destroy_session(self, request=None) -> bool:
        """_summary_

        Args:
            request (_type_, optional): _description_. Defaults to None.

        Returns:
            bool: _description_
        """
        if not request:
            return False
        session_id = request.cookies.get(getenv('SESSION_NAME'))
        if not session_id:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return False
        SessionAuth.user_id_by_session_id.pop(session_id)
        return True
