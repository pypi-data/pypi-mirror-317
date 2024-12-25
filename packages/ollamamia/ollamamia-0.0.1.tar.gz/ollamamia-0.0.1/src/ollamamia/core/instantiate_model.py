import ollama
from ollama import ListResponse
from tqdm import tqdm


class InstantiateModels:

    def change_models_dir(self, _to):
        # move all the old models to the new dir
        pass

    def ps(self, details=True, log=False) -> list:
        response: ListResponse = ollama.list()
        models_info = []
        for model_object in response.models:
            if details:
                models_info.append(model_object.model)
                continue
            temp = {'Name': model_object.model}
            if model_object.details and details:
                temp['Size (MB)'] = f'{(model_object.size.real / 1024 / 1024):.2f}'
                temp['Size vram (MB)'] = f'{(model_object.model.size_vram / 1024 / 1024):.2f}'
                temp['Digest'] = model_object.digest
                temp['Expires at'] = model_object.expires_at
                temp['Format'] = model_object.details.format
                temp['Family'] = model_object.details.family
                temp['Parameter Size'] = model_object.details.parameter_size
                temp['Quantization Level'] = model_object.details.quantization_level

            models_info.append(temp)
        if log:
            print([f"info\n" for info in models_info], "\n")
        return models_info

    def pull(self, model_name) -> bool:
        current_digest, bars = '', {}
        for progress in ollama.pull(model_name, stream=True):
            digest = progress.get('digest', '')
            if digest != current_digest and current_digest in bars:
                bars[current_digest].close()

            if not digest:
                print(progress.get('status'))
                continue

            if digest not in bars and (total := progress.get('total')):
                bars[digest] = tqdm(total=total, desc=f'pulling {digest[7:19]}', unit='B', unit_scale=True)

            if completed := progress.get('completed'):
                bars[digest].update(completed - bars[digest].n)

        current_digest = digest
        return True

    def create(self, model_name, local_path, modelfile="") -> bool:
        if model_name not in self.ps(details=False, log=False):
            return False
        if modelfile == "":
            modelfile = None

        for response in ollama.create(model=model_name, modelfile=modelfile, stream=True):
            print(response['status'])
        return True

    def rm(self, ):
        pass
