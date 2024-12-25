## first, download ollama
## and run in the cli ```ollama serve```
----------
### on docker, just put ollama docker and your docker-program on the same pridge, using port 11434:11434


```python
from ollamamia import Ollamamia
```


```python
ollamamia = Ollamamia()
```


```python
model_name = "gemma2:2b"
```


```python
model_config = ollamamia.model_config(model_name=model_name, task="generate")
model_config.options.temperature = 0.0
model_config.format = 'json'
model_config.options.num_predict = 100
```

# init the model:


```python
# option 1
ollamamia[model_name] = model_config
# option 2
ollamamia[model_name:model_config]
```

# inference


```python
query = "120 / 32.3"

# option 1:
response = ollamamia.infer(model_name=model_name, query=query)
# option 2:
response = ollamamia[model_name] << query
# option 3:
response = ollamamia[model_name::query]

response
```


```python
# note - you can do it all at once:
ollamamia[model_name:model_config:query]
```

### choose one option as you like. its not that complicated...

# embed model


```python
model_config = ollamamia.model_config(model_name="snowflake-arctic-embed:137m", task="embed")
query = "its so easy! but i also can use simply in ollama. but it make my life easier and me stupider!!!"
```


```python
ollamamia["rag_model":model_config:query] # in embed it also can be list of queries.
```

# simple chat


```python
ollamamia.chitchat(model_name=model_name, prompt=None)
```

# help


```python
# don't work. in the future...
ollamamia.Luminary()
```
