# Lia: Asistente Educativo Personalizado 

## Presentación

Ver online: https://tomasreisenman.github.io/lia/

Presentación Reveal.js en `docs/index.html` (GitHub Pages). Usa CDN de Reveal.js, no requiere archivos locales.

## Instalación

```bash
python -m venv venv
source venv/bin/activate  # Para Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install google-adk
```


## Entorno (`.env`)

```
GOOGLE_API_KEY=your_api_key          # API key de Google AI Studio (requerido)
GOOGLE_GENAI_USE_VERTEXAI=0          # Usar AI Studio (0) o Vertex AI (1)
GH_TOKEN=ghp_...                     # Token de GitHub (requerido para github_agent)
HF_TOKEN=hf_...                      # Token de HuggingFace (requerido para descargar modelos)
```

## Testing 

Correr dentro de la carpeta lia

```
adk eval . tests/evalset.json --config_file_path=tests/test_config.json
```

Utiliza LLM as a judge 

# Generar índice FAISS

El script `scripts/embed.py` genera un índice FAISS con embeddings de los archivos JSON utilizados por los agentes (templates de ejercicios y temas de estudio). Se usa un modelo multilingual (`paraphrase-multilingual-MiniLM-L12-v2`) con 384 dimensiones y normalización.

**Uso:**

```bash
# Embed de un directorio (todos los .json del directorio)
python scripts/embed.py <directorio>

# Embed de un archivo individual
python scripts/embed.py <archivo.json>
```

Los JSON del proyecto se encuentran en la carpeta `info/`.

**Qué genera:**
- `faiss_store/faiss_index` — Índice FAISS (IndexFlatIP, inner product)
- `faiss_store/metadata.json` — Metadatos de cada vector (id, tipo, archivo, etc.)

**Notas:**
- La carpeta `faiss_store/` se crea automáticamente si no existe.
- Cada ejecución **sobrescribe** el índice anterior (no es acumulativo).
- No requiere configuración adicional ni variables de entorno.
- Dependencias: `faiss-cpu`, `sentence-transformers`, `numpy`.

# Levantar 

Correr adk web --port 8000 en una carpeta que contenga la carpeta de lia y elegir lia de la lista de app

# Metricas

Se utilizo un Grafana y Prometheus local para capturar metricas. Se utilizó Docker para correrlo localmente

```
docker run --name local-otel-server -p 4317:4317 -p 4318:4318 -p 3000:3000 grafana/otel-lgtm:latest
```

Para poder capturar metricas se realizó este comando antes de correr adk web --port 8000:   

``` bash
export OTEL_EXPORTER_OTLP_ENDPOINT="http://localhost:4318"
```

``` powershell
$env:OTEL_EXPORTER_OTLP_ENDPOINT = "http://localhost:4318"
```

Las metricas disponibles para count,bucket y sum son:  

- gen_ai_client_operation_duration_seconds		
- gen_ai_client_token_usage		
- gen_ai_execute_tool_duration_seconds		
- gen_ai_invoke_agent_duration_seconds		
- gen_ai_invoke_agent_inference_calls		
- gen_ai_invoke_agent_tool_calls
