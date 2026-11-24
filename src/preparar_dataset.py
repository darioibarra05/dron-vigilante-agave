"""Revisa las etiquetas de data/etiquetadas/ y arma data/dataset/ con train/val/test.

Uso:
    python src/preparar_dataset.py                    # 70 / 20 / 10
    python src/preparar_dataset.py --val 0.15 --test 0.15

Qué revisa:
  - cada imagen tiene su .txt (si no, se toma como imagen sin plantas y se avisa)
  - cada línea tiene 5 valores, la clase existe y las coordenadas están entre 0 y 1
  - etiquetas sin imagen
Al final imprime cuántas cajas hay por clase y en cada división.
"""
import argparse
import random
import shutil
from collections import Counter

import yaml

from comun import DATASET, DATASET_YAML, ETIQUETADAS, EXT_IMAGEN, cargar_clases


def leer_etiqueta(txt, n_clases):
    """Devuelve (lista de clases, lista de errores)."""
    clases, errores = [], []
    for i, linea in enumerate(txt.read_text(encoding="utf-8").splitlines(), 1):
        if not linea.strip():
            continue
        partes = linea.split()
        if len(partes) != 5:
            errores.append(f"{txt.name}:{i} tiene {len(partes)} valores (deben ser 5)")
            continue
        try:
            c = int(partes[0])
            coords = [float(v) for v in partes[1:]]
        except ValueError:
            errores.append(f"{txt.name}:{i} tiene valores que no son números")
            continue
        if not 0 <= c < n_clases:
            errores.append(f"{txt.name}:{i} clase {c} no existe (0 a {n_clases - 1})")
        if any(v < 0 or v > 1 for v in coords):
            errores.append(f"{txt.name}:{i} coordenadas fuera de 0-1")
        clases.append(c)
    return clases, errores


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--val", type=float, default=0.20)
    ap.add_argument("--test", type=float, default=0.10)
    ap.add_argument("--semilla", type=int, default=42, help="misma semilla = misma división")
    args = ap.parse_args()

    clases = cargar_clases()
    img_dir, lbl_dir = ETIQUETADAS / "images", ETIQUETADAS / "labels"
    imagenes = sorted(p for p in img_dir.rglob("*") if p.suffix.lower() in EXT_IMAGEN)
    if not imagenes:
        raise SystemExit(f"No hay imágenes en {img_dir}. Revisa docs/ETIQUETADO.md")

    errores, sin_etiqueta, items = [], [], []
    for img in imagenes:
        txt = lbl_dir / img.relative_to(img_dir).with_suffix(".txt")
        if txt.exists():
            cls, err = leer_etiqueta(txt, len(clases))
            errores += err
        else:
            cls = []
            sin_etiqueta.append(img.name)
        items.append((img, txt if txt.exists() else None, cls))

    nombres_img = {p.relative_to(img_dir).with_suffix("") for p in imagenes}
    huerfanas = [t.name for t in lbl_dir.rglob("*.txt")
                 if t.relative_to(lbl_dir).with_suffix("") not in nombres_img]

    if errores:
        print("ERRORES en etiquetas (corrígelos y vuelve a correr):")
        for e in errores[:50]:
            print("  -", e)
        if len(errores) > 50:
            print(f"  ... y {len(errores) - 50} más")
        raise SystemExit(1)
    if sin_etiqueta:
        print(f"Aviso: {len(sin_etiqueta)} imágenes sin .txt; se usan como 'sin plantas'. "
              f"Ej.: {', '.join(sin_etiqueta[:5])}")
    if huerfanas:
        print(f"Aviso: {len(huerfanas)} etiquetas sin imagen (se ignoran). Ej.: {', '.join(huerfanas[:5])}")

    random.Random(args.semilla).shuffle(items)
    n = len(items)
    n_test, n_val = round(n * args.test), round(n * args.val)
    divisiones = {"test": items[:n_test], "val": items[n_test:n_test + n_val], "train": items[n_test + n_val:]}

    if DATASET.exists():
        shutil.rmtree(DATASET)
    conteo = {}
    for nombre, grupo in divisiones.items():
        (DATASET / "images" / nombre).mkdir(parents=True)
        (DATASET / "labels" / nombre).mkdir(parents=True)
        c = Counter()
        for img, txt, cls in grupo:
            destino = img.relative_to(img_dir).as_posix().replace("/", "__")
            shutil.copy2(img, DATASET / "images" / nombre / destino)
            lbl = DATASET / "labels" / nombre / (destino.rsplit(".", 1)[0] + ".txt")
            if txt:
                shutil.copy2(txt, lbl)
            else:
                lbl.write_text("")
            c.update(cls)
        conteo[nombre] = (len(grupo), c)

    with open(DATASET_YAML, "w", encoding="utf-8") as f:
        yaml.safe_dump({"path": str(DATASET.resolve()), "train": "images/train", "val": "images/val",
                        "test": "images/test", "names": clases}, f, allow_unicode=True, sort_keys=False)

    print(f"\nDataset listo en {DATASET}  ({n} imágenes)\n")
    print(f"{'clase':<22}{'train':>8}{'val':>8}{'test':>8}")
    for k, v in clases.items():
        fila = [conteo[d][1].get(k, 0) for d in ("train", "val", "test")]
        alerta = "   <- pocas" if sum(fila) < 150 else ""
        print(f"{k:>2} {v:<19}" + "".join(f"{x:>8}" for x in fila) + alerta)
    print(f"{'imágenes':<22}" + "".join(f"{conteo[d][0]:>8}" for d in ("train", "val", "test")))
    if not divisiones["val"]:
        print("\nAviso: no hay imágenes de validación; agrega más fotos.")


if __name__ == "__main__":
    main()
