---
name: delegar-a-qwen
description: Decide si merece la pena delegar trabajo en Qwen (qwen3.5-4b) a través del MCP de LM Studio (mcp__lmstudio__ask_local_model) o con un script por lotes contra la API local, o si es mejor hacerlo tú. Úsala siempre antes de llamar a ask_local_model, y cuando el usuario hable de Qwen, LM Studio, «modelo local», «delegar», procesar muchos archivos/comentarios/transcripciones de golpe, datos que no deben salir del PC, o tareas repetitivas que corren sin Claude delante, aunque no nombre a Qwen.
---

# Delegar en Qwen: cuándo compensa

Qwen 3.5 4B corre en LM Studio, en el PC del usuario (API OpenAI-compatible en `http://localhost:1234/v1`). Es gratis y local, pero pequeño: se equivoca más que tú, tiene una ventana de contexto corta y gasta unos 150-200 tokens «pensando» antes de responder.

## La idea clave

Delegar por chat (`ask_local_model`) casi nunca ahorra nada, porque **todo lo que le mandas a Qwen tiene que pasar antes por tu contexto**:

- **Privacidad:** si lees el archivo para pasárselo, ya ha llegado a Anthropic. Delegar después no protege nada.
- **Contexto/uso:** el texto de entrada ya lo pagaste al leerlo; solo te ahorras escribir la respuesta, que suele ser lo corto.
- **Calidad:** tienes que revisar lo que devuelva; con frecuencia revisar cuesta casi lo mismo que hacerlo.

Qwen solo gana cuando **los datos van directos del disco a Qwen sin pasar por ti**: con un script que llama a la API local.

## Decisión

| Situación | Qué hacer |
|---|---|
| Tarea normal del chat (resumir un log que ya has leído, limpiar un JSON pequeño, un borrador) | Hazlo tú. No delegues. |
| Muchos elementos (decenas o cientos de archivos, comentarios, transcripciones) con una tarea simple y repetible (clasificar, etiquetar, resumir, extraer un campo) | Script por lotes con `scripts/qwen_lote.py`. Tú solo lees una muestra del resultado. |
| Datos que el usuario no quiere que salgan de su PC | Script por lotes **sin abrir tú los archivos**. Si ya los leíste, delegar no aporta. |
| Tarea recurrente sin Claude delante (cada noche, al soltar archivos en una carpeta) | Script + tarea programada de Windows; Qwen hace el trabajo, no tú. |
| Necesita razonar, contexto entre varios archivos, código delicado, dinero/seguridad, o el resultado se publica tal cual | Hazlo tú. Qwen no es fiable aquí. |
| El usuario pide explícitamente usar Qwen | Hazlo, pero si no compensa dilo en una línea. |

Regla rápida: si para delegar tienes que leer los datos tú primero, no delegues.

## Si usas `ask_local_model` igualmente

- Pon `max_tokens` ≥ 600: con menos, el razonamiento interno se come el límite y vuelve vacío (`finish: length`).
- Prompt autocontenido, corto, con el formato de salida exacto. Nada de archivos enteros.
- Revisa la salida antes de usarla.

## Script por lotes

`scripts/qwen_lote.py` (solo librería estándar) manda cada archivo de una carpeta a Qwen con la misma instrucción y guarda una respuesta por archivo:

```bash
python ~/.claude/skills/delegar-a-qwen/scripts/qwen_lote.py <carpeta_entrada> <carpeta_salida> "Instrucción, p. ej.: clasifica este comentario como positivo, negativo o pregunta. Responde solo la etiqueta."
```

Opciones: `--glob "*.txt"`, `--max-chars 6000` (recorta entradas largas), `--model`. Si LM Studio no responde, avisa al usuario de que lo abra y cargue el modelo.

Después: comprueba 3-5 salidas al azar. Si fallan, ajusta la instrucción (más concreta, formato fijo) antes de relanzar todo.
