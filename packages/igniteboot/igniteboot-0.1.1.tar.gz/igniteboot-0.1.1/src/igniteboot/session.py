import secrets

class SessionManager:
    def __init__(self):
        self._sessions = {}

    def create_session(self):
        session_id = secrets.token_urlsafe(16)
        self._sessions[session_id] = {}
        return session_id

    def get_session(self, session_id):
        return self._sessions.get(session_id)

    def set_session_data(self, session_id, key, value):
        session = self._sessions.get(session_id)
        if session is not None:
            session[key] = value

    def destroy_session(self, session_id):
        if session_id in self._sessions:
            del self._sessions[session_id]
