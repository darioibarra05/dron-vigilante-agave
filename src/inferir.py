"""Corre el modelo sobre una foto, una carpeta, un video o la cámara.

Uso:
    python src/inferir.py --pesos best.pt --fuente foto.jpg
    python src/inferir.py --pesos best.pt --fuente carpeta_de_fotos/
    python src/inferir.py --pesos best.pt --fuente 0          # cámara

Guarda las imágenes con las cajas dibujadas y un archivo detecciones.json con, por cada
imagen: las detecciones (clase, confianza, caja en píxeles) y las coordenadas GPS de la foto
si las trae en el EXIF. Ese JSON es la base para el mapa de plantas afectadas.
"""
import argparse
import json
from pathlib import Path

from PIL import Image
from ultralytics import YOLO

from comun import RUNS


def _a_grados(v, ref):
    g = float(v[0]) + float(v[1]) / 60 + float(v[2]) / 3600
    return -g if ref in ("S", "W") else g


def gps_de_foto(ruta):
    """Lee latitud/longitud/altitud del EXIF. Devuelve None si la foto no trae GPS."""
    try:
        gps = Image.open(ruta).getexif().get_ifd(0x8825)
        if not gps or 2 not in gps:
            return None
        datos = {"lat": round(_a_grados(gps[2], gps.get(1, "N")), 7),
                 "lon": round(_a_grados(gps[4], gps.get(3, "E")), 7)}
        if 6 in gps:
            datos["alt_m"] = round(float(gps[6]), 2)
        return datos
    except Exception:
        return None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pesos", required=True)
    ap.add_argument("--fuente", required=True)
    ap.add_argument("--conf", type=float, default=0.35, help="confianza mínima (0-1)")
    ap.add_argument("--imgsz", type=int, default=640)
    ap.add_argument("--dispositivo", default=None)
    args = ap.parse_args()

    modelo = YOLO(args.pesos)
    fuente = int(args.fuente) if args.fuente.isdigit() else args.fuente
    resultados = []
    salida = None
    for r in modelo.predict(source=fuente, conf=args.conf, imgsz=args.imgsz, device=args.dispositivo,
                            save=True, project=str(RUNS), name="inferencia", stream=True):
        salida = Path(r.save_dir)
        dets = [{"clase": r.names[int(c)], "confianza": round(float(p), 3),
                 "caja_xyxy": [round(float(v), 1) for v in xyxy]}
                for c, p, xyxy in zip(r.boxes.cls, r.boxes.conf, r.boxes.xyxy)]
        entrada = {"imagen": Path(r.path).name, "detecciones": dets}
        if isinstance(fuente, str) and Path(r.path).is_file():
            entrada["gps"] = gps_de_foto(r.path)
        resultados.append(entrada)
        enfermas = sum(d["clase"] != "agave_sano" for d in dets)
        print(f"{entrada['imagen']}: {len(dets)} detecciones, {enfermas} con síntomas")

    if salida:
        (salida / "detecciones.json").write_text(json.dumps(resultados, indent=2, ensure_ascii=False),
                                                 encoding="utf-8")
        print(f"\nResultados en {salida}")


if __name__ == "__main__":
    main()
