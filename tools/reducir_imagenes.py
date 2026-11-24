"""Reduce fotos antes de subirlas al repo, conservando el EXIF (incluido el GPS).

Uso:
    python tools/reducir_imagenes.py <carpeta_origen> <carpeta_destino> [--lado 1920] [--calidad 90]

Ejemplo:
    python tools/reducir_imagenes.py D:/salida_24nov/ data/crudas/sin_clasificar/

No modifica los originales. Las fotos que ya son más chicas solo se copian como JPG.
"""
import argparse
from pathlib import Path

from PIL import Image, ImageOps

EXT = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tif", ".tiff"}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("origen")
    ap.add_argument("destino")
    ap.add_argument("--lado", type=int, default=1920, help="lado más largo en píxeles")
    ap.add_argument("--calidad", type=int, default=90)
    args = ap.parse_args()

    origen, destino = Path(args.origen), Path(args.destino)
    destino.mkdir(parents=True, exist_ok=True)
    fotos = sorted(p for p in origen.rglob("*") if p.suffix.lower() in EXT)
    if not fotos:
        raise SystemExit(f"No encontré imágenes en {origen}")

    antes = despues = 0
    for p in fotos:
        img = Image.open(p)
        exif = img.getexif()
        img = ImageOps.exif_transpose(img).convert("RGB")   # aplica la rotación de la cámara
        exif[0x0112] = 1                                     # y la marca como ya aplicada
        img.thumbnail((args.lado, args.lado), Image.LANCZOS)
        nombre = p.relative_to(origen).with_suffix(".jpg").as_posix().replace("/", "_").replace(" ", "_")
        out = destino / nombre
        img.save(out, "JPEG", quality=args.calidad, exif=exif.tobytes(), optimize=True)
        antes += p.stat().st_size
        despues += out.stat().st_size
    print(f"{len(fotos)} fotos: {antes / 1e6:.1f} MB -> {despues / 1e6:.1f} MB en {destino}")


if __name__ == "__main__":
    main()
