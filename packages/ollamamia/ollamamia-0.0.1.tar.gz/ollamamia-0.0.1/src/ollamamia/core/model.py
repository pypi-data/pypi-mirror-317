from enum import Enum
from typing import Union, Sequence, Literal
from .model_config import ModelConfig
from src.ollamamia.globals_dir.globals import GLOBALS


class Role(Enum):
    USER = -1
    ASSISTANT = 0
    SYSTEM = 'a'


###########################


class BaseModel:

    def __init__(self, model_name,):
        self.config = ModelConfig(model_name)
        self.logs = []

    def _manage_logs(self, response):
        if len(self.logs) >= GLOBALS.len_logs:
            self.logs.pop(0)
        self.logs.append(response)

    def chat_stream(self, messages: list[dict]):
        response = ''
        for part in self.config.client.chat(self.config.model_name, messages=messages, stream=True):
            response += part['message']['content']
            print(part['message']['content'], end='', flush=True)
        return response

    def chat(self, messages: list[dict]):
        response = self.config.client.chat(
            model=self.config.model_name,
            messages=messages
        )

        self._manage_logs(response)
        return response.message.content

    def embed(self, query: Union[str, Sequence[str]]):
        response = self.config.client.embed(model=self.config.model_name, input=query)
        self._manage_logs(response)
        return response['embeddings']

    def generate(self, query):
        response = self.config.client.generate(
            model=self.config.model_name,
            prompt=query,
            suffix=self.config.suffix,
            system=self.config.system,
            template=self.config.template,
            context=self.config.context,
            raw=self.config.raw,
            format=self.config.format,
            keep_alive=self.config.keep_alive,
            options=self.config.options.__dict__
        )
        self._manage_logs(response)
        return response['response']

    def update_params(self, other: Union[dict, ModelConfig]):
        if isinstance(other, ModelConfig):
            self.config = other
        else:
            for key, value in other.items():
                if hasattr(self.config, key):
                    setattr(self.config, key, value)

    def infer(self, query):
        # overwrite
        pass

    def __lshift__(self, query):
        return self.infer(query)

    def __le__(self, other: Union[dict, ModelConfig]):
        self.update_params(other)
        return True

    def stop(self):
        self.config.keep_alive = 0
        self.infer("generate: i'm dying!!")
        return True


############################


class Chat(BaseModel):

    def __init__(self, model_name, prompt=None):
        super().__init__(model_name)
        self.messages = []
        self.prompt = prompt
        self._init_prompt()

    def _init_prompt(self):
        if self.prompt:
            self.messages.append({'role': 'assistant', 'content': self.prompt})

    def _add_step(self, role: Role, content: str):
        message = {
            "role": role.name.lower(),
            "content": content
        }
        self.messages.append(message)

    def infer(self, query) -> str:
        self._add_step(role=Role.USER, content=query)
        response = self.chat(messages=self.messages)
        self._add_step(role=Role.ASSISTANT, content=response)
        return response


############################

class Embed(BaseModel):

    def __init__(self, model_name, prefix=None):
        super().__init__(model_name)
        self.messages = []
        self.prefix = prefix

    def infer(self, query: Union[str, Sequence[str]]) -> list[list]:
        return self.embed(query)


###############################

class Generate(BaseModel):

    def __init__(
            self,
            model_name
    ):
        super().__init__(model_name)

    def infer(self, query):
        return self.generate(query)


def Model(model_name, task: Literal[tuple(GLOBALS.available_tasks)]):
    match task:
        case "null":  # "null"
            raise ValueError("Task cannot be 'null'")
        case "chat":
            return Chat(model_name)
        case "generate":
            return Generate(model_name)
        case "embed":
            return Embed(model_name)
        case _:
            raise ValueError(f"Unsupported task: {task}")
