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
