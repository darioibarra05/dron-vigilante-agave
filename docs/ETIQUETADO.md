# Guía de etiquetado

El modelo es de **detección** (YOLO), así que cada planta o zona afectada se marca con una caja.

## Herramienta recomendada: Roboflow (gratis, en línea, colaborativo)

1. Creen un proyecto tipo **Object Detection** e inviten a los tres integrantes.
2. Den de alta **las 8 clases con los mismos nombres y en el mismo orden** que en
   `data/agave.yaml`.
3. Suban las fotos de `data/crudas/` y repártanse el etiquetado.
4. Exporten en formato **YOLOv8** **sin** aumento de datos (el aumento lo hace el
   entrenamiento) y **sin** dividir en train/val/test (lo hace `preparar_dataset.py`).
5. Copien el contenido exportado a:
   ```
   data/etiquetadas/images/   ← las .jpg
   data/etiquetadas/labels/   ← los .txt (mismo nombre que su imagen)
   ```

Alternativas: CVAT o Label Studio (exportar como "YOLO 1.1").

## Reglas para que todos etiqueten igual

- **Una caja por planta.** La caja abarca la planta completa (la roseta), no solo la mancha,
  salvo que el daño se vea claramente en una sola zona de una planta grande.
- **Plantas sanas también se etiquetan** como `agave_sano`.
- Si una planta tiene **dos problemas**, pongan la clase del más grave.
- Si **no están seguros**, no la etiqueten y anótenlo en un issue con la foto para que el
  equipo (o el asesor) decida.
- Plantas cortadas en el borde de la foto: se etiquetan si se ve más de la mitad.

## Formato YOLO (por si lo editan a mano)

Cada línea del `.txt` es una caja:

```
<clase> <x_centro> <y_centro> <ancho> <alto>
```

Los cuatro números son proporciones de 0 a 1 respecto al tamaño de la imagen. Una imagen sin
plantas lleva un `.txt` vacío.
