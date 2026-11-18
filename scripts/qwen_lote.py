"""Manda cada archivo de una carpeta a Qwen (LM Studio) con la misma instrucción.

Uso: python qwen_lote.py ENTRADA SALIDA "instrucción" [--glob "*.txt"] [--max-chars 6000] [--model qwen3.5-4b]
Los datos van del disco a LM Studio sin pasar por Claude.
"""
import argparse, json, pathlib, sys, urllib.request

API = "http://localhost:1234/v1/chat/completions"


def ask(model, instruction, text):
    body = json.dumps({
        "model": model,
        "messages": [{"role": "system", "content": instruction}, {"role": "user", "content": text}],
        "max_tokens": 1500,  # deja margen al razonamiento interno de Qwen
        "temperature": 0.3,
    }).encode()
    req = urllib.request.Request(API, body, {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.load(r)["choices"][0]["message"]["content"].strip()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("entrada"); p.add_argument("salida"); p.add_argument("instruccion")
    p.add_argument("--glob", default="*.*"); p.add_argument("--max-chars", type=int, default=6000)
    p.add_argument("--model", default="qwen3.5-4b")
    a = p.parse_args()

    out = pathlib.Path(a.salida); out.mkdir(parents=True, exist_ok=True)
    files = sorted(f for f in pathlib.Path(a.entrada).glob(a.glob) if f.is_file())
    if not files:
        sys.exit(f"No hay archivos que coincidan con {a.glob} en {a.entrada}")
    fallos = 0
    for i, f in enumerate(files, 1):
        dest = out / (f.stem + ".out.txt")
        if dest.exists():  # permite reanudar un lote cortado
            continue
        try:
            text = f.read_text(encoding="utf-8", errors="replace")[: a.max_chars]
            dest.write_text(ask(a.model, a.instruccion, text), encoding="utf-8")
            print(f"[{i}/{len(files)}] {f.name}")
        except OSError as e:  # URLError hereda de OSError
            fallos += 1
            print(f"[{i}/{len(files)}] {f.name} FALLO: {e}", file=sys.stderr)
    print(f"Hecho. {len(files) - fallos} ok, {fallos} fallos. Salida en {out}")


if __name__ == "__main__":
    main()
