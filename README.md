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
GOOGLE_API_KEY=your_api_key          # API key de Google AI Studio (requerido)
GOOGLE_GENAI_USE_VERTEXAI=0          # Usar AI Studio (0) o Vertex AI (1)
GH_TOKEN=ghp_...                     # Token de GitHub (requerido para github_agent)
HF_TOKEN=hf_...                      # Token de HuggingFace (requerido para descargar modelos)
```


## Presentación

Presentación Reveal.js en `docs/index.html` (GitHub Pages). Usa CDN de Reveal.js, no requiere archivos locales.

## Testing 

Correr dentro de la carpeta lia

```
adk eval . tests/evalset.json --config_file_path=tests/test_config.json
```

Utiliza LLM as a judge 

# Levantar 

Correr adk web --port 8000 en una carpeta que contenga la carpeta de lia y elegir lia de la lista de app
