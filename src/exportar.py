"""Exporta el modelo entrenado para correrlo en la Orange Pi 5 Pro.

Uso:
    python src/exportar.py --pesos runs/agave/entrenamiento/weights/best.pt
    python src/exportar.py --pesos best.pt --formato rknn      # NPU del RK3588 (ver nota)

Formatos:
  onnx  (por defecto) -> corre en la CPU de la Orange Pi con onnxruntime. Es el paso
                         intermedio para cualquier otro formato.
  rknn                -> usa la NPU del RK3588 (mucho más rápido). Ultralytics lo exporta
                         directamente en versiones recientes, pero requiere instalar
                         rknn-toolkit2 y correrlo en una PC con Linux x86_64 (no en Windows
                         ni en la propia Orange Pi).

El archivo exportado queda junto a los pesos .pt.
"""
import argparse

from ultralytics import YOLO


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pesos", required=True)
    ap.add_argument("--formato", default="onnx", choices=["onnx", "rknn"])
    ap.add_argument("--imgsz", type=int, default=640)
    args = ap.parse_args()

    modelo = YOLO(args.pesos)
    if args.formato == "rknn":
        ruta = modelo.export(format="rknn", name="rk3588", imgsz=args.imgsz)
    else:
        ruta = modelo.export(format="onnx", imgsz=args.imgsz, simplify=True, opset=12)
    print(f"\nExportado: {ruta}")


if __name__ == "__main__":
    main()
