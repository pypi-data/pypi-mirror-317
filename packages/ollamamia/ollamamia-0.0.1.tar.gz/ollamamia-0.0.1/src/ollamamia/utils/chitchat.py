from src.ollamamia.core.model import Chat, Role
from .utils import input_with_placeholder, exiting_ollamamia


class ChitChat(Chat):

    def __init__(self, model_name, prompt=None):
        super().__init__(model_name, prompt)
        while True:
            query = self.get_user_text()
            if not query:
                break
            self.infer(query)

    def infer(self, query) -> str:
        self._add_step(role=Role.USER, content=query)
        response = self.chat_stream(messages=self.messages)
        self._add_step(role=Role.ASSISTANT, content=response)
        return response

    def get_user_text(self):
        try:
            user_input = input_with_placeholder()
            if user_input.lower() in ['exit', 'quit', 'q']:
                exiting_ollamamia()
            else:
                return user_input
        except:
            exiting_ollamamia()
