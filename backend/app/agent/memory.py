from langchain_core.messages import BaseMessage


class SessionMemory:

    def __init__(self):

        self.sessions = {}


    def get_messages(
        self,
        session_id: str
    ):

        if session_id not in self.sessions:

            self.sessions[session_id] = []

        return self.sessions[session_id]


    def add_messages(
        self,
        session_id: str,
        messages: list[BaseMessage]
    ):

        if session_id not in self.sessions:

            self.sessions[session_id] = []

        self.sessions[session_id].extend(
            messages
        )


    def clear(
        self,
        session_id: str
    ):

        if session_id in self.sessions:

            del self.sessions[session_id]