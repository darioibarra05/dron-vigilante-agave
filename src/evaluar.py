"""Evalúa un modelo con el conjunto de PRUEBA (test) y muestra las métricas del protocolo.

Uso:
    python src/evaluar.py --pesos runs/agave/entrenamiento/weights/best.pt
    python src/evaluar.py --pesos modelos/v1.pt --conjunto val

Imprime Precision, Recall, mAP@50 y mAP@50-95 globales y por clase, y guarda la matriz
de confusión en runs/agave/evaluacion*/. Usa el conjunto test para los resultados de la
tesis: el modelo nunca lo vio al entrenar.
"""
import argparse

from ultralytics import YOLO

from comun import RUNS, cargar_clases, exigir_dataset

META = 0.80  # precisión objetivo del protocolo


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pesos", required=True)
    ap.add_argument("--conjunto", default="test", choices=["test", "val"])
    ap.add_argument("--imgsz", type=int, default=640)
    ap.add_argument("--dispositivo", default=None)
    args = ap.parse_args()

    m = YOLO(args.pesos).val(data=str(exigir_dataset()), split=args.conjunto, imgsz=args.imgsz,
                             device=args.dispositivo, project=str(RUNS), name="evaluacion", plots=True)
    clases = cargar_clases()
    b = m.box
    print(f"\n=== Resultados en '{args.conjunto}' ===")
    print(f"Precision   {b.mp:.3f}")
    print(f"Recall      {b.mr:.3f}")
    print(f"mAP@50      {b.map50:.3f}")
    print(f"mAP@50-95   {b.map:.3f}")
    print(f"Meta del protocolo (precisión > {META:.0%}): {'CUMPLE' if b.mp > META else 'aún no'}\n")

    print(f"{'clase':<22}{'P':>7}{'R':>7}{'mAP50':>8}{'mAP50-95':>10}")
    for i, c in enumerate(b.ap_class_index):
        p, r, ap50, ap = b.class_result(i)
        print(f"{clases.get(int(c), c):<22}{p:>7.3f}{r:>7.3f}{ap50:>8.3f}{ap:>10.3f}")
    print(f"\nGráficas y matriz de confusión: {m.save_dir}")
    print("Anota estos números en docs/EXPERIMENTOS.md")


if __name__ == "__main__":
    main()
