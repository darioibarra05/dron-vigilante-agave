"""Entrena el detector YOLOv8 con data/dataset/.

Uso:
    python src/entrenar.py                                  # yolov8n, 100 épocas, 640 px
    python src/entrenar.py --modelo yolov8s.pt --epocas 150 --imgsz 960
    python src/entrenar.py --reanudar                       # continúa el último entrenamiento

Modelo base:
  yolov8n.pt  -> el más ligero; buena opción para la Orange Pi 5 Pro
  yolov8s.pt  -> más preciso, ~3 veces más lento
Los pesos se descargan solos la primera vez.

Resultado: runs/agave/<nombre>/weights/best.pt  (+ gráficas y matriz de confusión)
"""
import argparse

from ultralytics import YOLO

from comun import RUNS, exigir_dataset


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--modelo", default="yolov8n.pt")
    ap.add_argument("--epocas", type=int, default=100)
    ap.add_argument("--imgsz", type=int, default=640, help="tamaño de entrada (640, 960, 1280)")
    ap.add_argument("--lote", type=int, default=16, help="batch; bájalo si te quedas sin memoria")
    ap.add_argument("--dispositivo", default=None, help="'0' para GPU, 'cpu' para CPU (auto por defecto)")
    ap.add_argument("--nombre", default="entrenamiento")
    ap.add_argument("--paciencia", type=int, default=30, help="épocas sin mejora antes de parar")
    ap.add_argument("--reanudar", action="store_true")
    args = ap.parse_args()

    if args.reanudar:
        YOLO(str(RUNS / args.nombre / "weights" / "last.pt")).train(resume=True)
        return

    datos = exigir_dataset()
    modelo = YOLO(args.modelo)
    modelo.train(
        data=str(datos),
        epochs=args.epocas,
        imgsz=args.imgsz,
        batch=args.lote,
        device=args.dispositivo,
        project=str(RUNS),
        name=args.nombre,
        exist_ok=False,
        patience=args.paciencia,
        seed=42,
        # Aumento de datos pensado para fotos aéreas de agave:
        flipud=0.5,        # desde arriba no hay "arriba/abajo"
        fliplr=0.5,
        degrees=180,       # cualquier rotación es válida en vista cenital
        hsv_h=0.015,       # variación de color pequeña (el color es síntoma, no exagerar)
        hsv_s=0.5,
        hsv_v=0.4,         # cambios de iluminación (mañana / mediodía / nublado)
        scale=0.4,         # distintas alturas de vuelo
        mosaic=1.0,
        mixup=0.0,
    )
    print(f"\nListo. Mejores pesos: {modelo.trainer.best}")


if __name__ == "__main__":
    main()
