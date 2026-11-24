"""Rutas y utilidades compartidas por los scripts."""
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parents[1]
DATA = RAIZ / "data"
ETIQUETADAS = DATA / "etiquetadas"
DATASET = DATA / "dataset"
CLASES_YAML = DATA / "agave.yaml"
DATASET_YAML = DATASET / "dataset.yaml"
RUNS = RAIZ / "runs" / "agave"

EXT_IMAGEN = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def cargar_clases() -> dict[int, str]:
    with open(CLASES_YAML, encoding="utf-8") as f:
        nombres = yaml.safe_load(f)["names"]
    return {int(k): v for k, v in nombres.items()}


def exigir_dataset():
    if not DATASET_YAML.exists():
        raise SystemExit(
            "No existe data/dataset/dataset.yaml.\n"
            "Primero corre:  python src/preparar_dataset.py"
        )
    return DATASET_YAML
