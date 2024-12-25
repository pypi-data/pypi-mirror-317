from src.ollamamia.core.model_config import ModelConfig
from src.ollamamia.core.models_control import ModelsControl
from src.ollamamia.core.model import Model
from src.ollamamia.globals_dir.globals import GLOBALS
from src.ollamamia.utils.chitchat import ChitChat


class Ollamamia:
    def __init__(self, models_location=GLOBALS.default_ollama_folder):
        GLOBALS.init()
        self.model_config = ModelConfig
        self._models_control = ModelsControl()

    def add(self, model_name, model_config: ModelConfig):
        model = Model(model_name=model_name, task=model_config.task)
        model.config = model_config
        self._models_control.add(model_name, model)

    def infer(self, model_name, query):
        return self._models_control.models[model_name].infer(query)

    def __getitem__(self, key):
        if isinstance(key, slice):
            model_name: str
            model_config: ModelConfig
            query: str
            model_name, model_config, query = key.start, key.stop, key.step
            # if model_name not in self._models_control.models:
            #     raise KeyError(f"Model '{key}' not found.")
            if model_config:
                self.add(model_name, model_config)
                if not query:
                    return self._models_control.models[model_name]
            if query:
                return self.infer(model_name, query)
        if isinstance(key, str):
            return self._models_control.models[key]

    def __setitem__(self, model_name: str, model_config: ModelConfig):
        self.add(model_name, model_config)

    def stop(self):
        # for the future.
        pass

    def ps(self):
        return list(self._models_control.models.keys())

    def chitchat(self, model_name, prompt=None):
        ChitChat(model_name, prompt)
