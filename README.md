# delegar-a-qwen

Skill para Claude Code que decide cuándo merece la pena delegar trabajo en un modelo local (Qwen 3.5 4B en LM Studio) y cuándo no.

**La idea:** delegar por chat casi nunca ahorra nada, porque Claude tiene que leer los datos para pasárselos a Qwen. Delegar compensa cuando los datos van directos del disco al modelo local, con un script por lotes: muchos archivos, datos privados o tareas que se repiten sin Claude delante.

## Requisitos

- [LM Studio](https://lmstudio.ai) con `qwen3.5-4b` cargado y el servidor local activo (`http://localhost:1234`).
- El MCP de LM Studio en Claude Code (`ask_local_model`). Es opcional: el script por lotes no lo necesita.
- Python 3 (solo usa la librería estándar).

## Instalación

```bash
git clone https://github.com/pietrodrame/Qwen-For-Claude.git ~/.claude/skills/delegar-a-qwen
```

## Script por lotes

```bash
python scripts/qwen_lote.py <carpeta_entrada> <carpeta_salida> "Clasifica el comentario como positivo, negativo o pregunta. Responde solo la etiqueta." --glob "*.txt"
```

Guarda un `<nombre>.out.txt` por archivo. Si el lote se corta, al relanzarlo continúa donde se quedó.
