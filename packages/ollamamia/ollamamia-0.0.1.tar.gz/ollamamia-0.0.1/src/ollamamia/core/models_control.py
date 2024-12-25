from .model import BaseModel


class ModelsControl:

    def __init__(self):
        self.models = {}

    def add(self, model_name, model: BaseModel):
        if model_name in self.models.keys():
            to_continue = input("this model has been loaded to ollamamia already. are you sure you want to load it "
                                "again? [y,n]")
            if to_continue.lower() == 'y':
                self.models[model_name].stop()
                self.models[model_name] = model
            else:
                del model
        else:
            self.models[model_name] = model
