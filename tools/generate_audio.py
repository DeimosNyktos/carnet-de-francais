"""Genera los audios de pronunciación francesa de Carnet de Français.

Cada texto de tools/texts.json se convierte en audio/<hash>.wav, donde <hash> es el
FNV-1a de 32 bits (8 caracteres hexadecimales) del texto en UTF-8. La app calcula el mismo
nombre en JavaScript, así que no hace falta ningún índice para encontrar cada audio.

Requisitos (dentro de un entorno virtual):
    pip install piper-tts
    python -m piper.download_voices fr_FR-siwis-medium --download-dir voces

Uso:
    python tools/generate_audio.py --voice voces/fr_FR-siwis-medium.onnx
    python tools/generate_audio.py --voice voces/fr_FR-siwis-medium.onnx --force   # regenerar todo

Voz: fr_FR-siwis-medium, entrenada con la base SIWIS (Universidad de Edimburgo, CC BY 4.0).
"""
import argparse
import json
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def fnv1a(text: str) -> str:
    h = 0x811C9DC5
    for b in text.encode("utf-8"):
        h ^= b
        h = (h * 0x01000193) & 0xFFFFFFFF
    return format(h, "08x")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--voice", required=True, help="ruta al .onnx de la voz")
    ap.add_argument("--texts", default=str(ROOT / "tools" / "texts.json"))
    ap.add_argument("--out", default=str(ROOT / "audio"))
    ap.add_argument("--force", action="store_true", help="regenerar aunque el audio ya exista")
    args = ap.parse_args()

    from piper import PiperVoice  # import tardío: solo hace falta al generar

    texts = json.loads(Path(args.texts).read_text(encoding="utf-8"))
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    names: dict[str, str] = {}
    for t in texts:
        name = fnv1a(t) + ".wav"
        if name in names and names[name] != t:
            raise SystemExit(f"Colisión de hash entre {names[name]!r} y {t!r}")
        names[name] = t

    voice = PiperVoice.load(args.voice)
    made = skipped = 0
    for name, text in names.items():
        path = out / name
        if path.exists() and not args.force:
            skipped += 1
            continue
        with wave.open(str(path), "wb") as wav:
            voice.synthesize_wav(text, wav)
        made += 1

    (out / "index.json").write_text(json.dumps(sorted(names), indent=1) + "\n", encoding="utf-8")
    total_mb = sum(p.stat().st_size for p in out.glob("*.wav")) / 1e6
    print(f"Audios nuevos: {made} · ya existían: {skipped} · total {len(names)} · {total_mb:.1f} MB")


if __name__ == "__main__":
    main()
