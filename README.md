Asistente Educativo Personalizado 

## Instalación

```bash
python -m venv venv
source venv/bin/activate  # Para Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install google-adk
```


## Entorno (`.env`)

```
HF_TOKEN=hf_your_token_here          # Solo para modelos que lo requieren
FAISS_DIR=faiss_store                # FAISS store ruta local
EMBED_MODEL=all-MiniLM-L6-v2         # Modelo Embedding
```


## Presentación  

Hay una presentación del proyecto en presentation/index.html . Se puede abrir con un 
web browser luego de descargar el proyecto. 

## Testing 

Correr dentro de la carpeta destino
adk eval . tests/evalset.json --config_file_path=tests/test_config.json
