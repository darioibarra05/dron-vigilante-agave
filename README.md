# Dron vigilante para detección y cuidado de cultivos de Agave Azul

Proyecto de titulación — Ingeniería en Mecatrónica, CETI Guadalajara (2026).

**Equipo**
- Jesús Antonio Báez Ortega
- Rubén Darío Ibarra Tirado
- Héctor Manuel Castañeda Godoy

Este repositorio tiene el **modelo de visión artificial (YOLOv8)** que corre a bordo del dron
(Orange Pi 5 Pro + cámara IMX708). El modelo detecta plantas de *Agave tequilana* Weber sanas
y con plagas, enfermedades o estrés.

---

## Estructura

```
dron-vigilante-agave/
├── data/
│   ├── crudas/            ← fotos SIN etiquetar, separadas por lo que se ve en ellas
│   │   ├── agave_sano/
│   │   ├── picudo/
│   │   ├── marchitez_fusarium/
│   │   ├── pudricion_blanda/
│   │   ├── mancha_gris/
│   │   ├── escama_armada/
│   │   ├── piojo_harinoso/
│   │   ├── estres_hidrico/
│   │   └── sin_clasificar/
│   ├── etiquetadas/       ← fotos YA etiquetadas en formato YOLO (images/ + labels/)
│   ├── dataset/           ← lo genera el script: train / val / test (no se edita a mano)
│   └── agave.yaml         ← clases del modelo
├── src/                   ← código del modelo
│   ├── preparar_dataset.py
│   ├── entrenar.py
│   ├── evaluar.py
│   ├── inferir.py
│   └── exportar.py
├── tools/
│   └── reducir_imagenes.py
├── modelos/               ← pesos entrenados (.pt / .onnx) que valga la pena guardar
├── notebooks/
│   └── entrenar_en_colab.ipynb
└── docs/
    ├── CAPTURA_DE_IMAGENES.md
    ├── ETIQUETADO.md
    └── CONTRIBUIR.md
```

## Clases

| ID | Clase | Qué es |
|---|---|---|
| 0 | `agave_sano` | Planta sin síntomas |
| 1 | `picudo` | Daño por *Scyphophorus acupunctatus* (picudo del agave) |
| 2 | `marchitez_fusarium` | Marchitez / pudrición por *Fusarium oxysporum* o *F. solani* |
| 3 | `pudricion_blanda` | Pudrición blanda (*Pectobacterium carotovorum* / *Dickeya dadantii*) |
| 4 | `mancha_gris` | *Cercospora agavicola* |
| 5 | `escama_armada` | *Acutaspis agavis* |
| 6 | `piojo_harinoso` | *Pseudococcus agavis* / *Caeparis fici* |
| 7 | `estres_hidrico` | Estrés hídrico o abiótico |

> ⚠️ **No cambien el orden de las clases** una vez que haya etiquetas: el número de cada clase
> está escrito dentro de los archivos `.txt` de las etiquetas. Si hace falta una clase nueva,
> agréguenla **al final**.

## Flujo de trabajo

1. **Capturar** fotos y subirlas a `data/crudas/<clase>/` → ver [docs/CAPTURA_DE_IMAGENES.md](docs/CAPTURA_DE_IMAGENES.md)
2. **Etiquetar** con cajas (Roboflow, CVAT o Label Studio), exportar en formato YOLO y
   copiar el resultado a `data/etiquetadas/` → ver [docs/ETIQUETADO.md](docs/ETIQUETADO.md)
3. **Preparar** el dataset (revisa las etiquetas y hace la división 70/20/10):
   ```bash
   python src/preparar_dataset.py
   ```
4. **Entrenar**:
   ```bash
   python src/entrenar.py --epocas 100 --modelo yolov8n.pt
   ```
5. **Evaluar** con el conjunto de prueba (Precision, Recall, mAP@50, mAP@50-95):
   ```bash
   python src/evaluar.py --pesos runs/agave/entrenamiento/weights/best.pt
   ```
6. **Probar** en fotos nuevas:
   ```bash
   python src/inferir.py --pesos runs/agave/entrenamiento/weights/best.pt --fuente foto.jpg
   ```
7. **Exportar** para la Orange Pi 5 Pro:
   ```bash
   python src/exportar.py --pesos runs/agave/entrenamiento/weights/best.pt
   ```

## Instalación

Se necesita Python 3.10 o más nuevo.

```bash
git clone https://github.com/darioibarra05/dron-vigilante-agave.git
cd dron-vigilante-agave
python -m venv .venv
# Windows: .venv\Scripts\activate     Linux/Mac: source .venv/bin/activate
pip install -r requirements.txt
```

Para entrenar conviene usar GPU (NVIDIA con CUDA). Si no tienen, usen
[`notebooks/entrenar_en_colab.ipynb`](notebooks/entrenar_en_colab.ipynb) en **Google Colab** (GPU gratis).
Con CPU funciona, pero es lento.

## Meta del proyecto

Según el protocolo, el modelo debe identificar y georreferenciar patologías en tiempo real con
**precisión superior al 80 %**, medida con Precision, Recall y mAP sobre el conjunto de prueba.

## Licencia

El código está bajo licencia MIT (ver `LICENSE`). Las imágenes del dataset son del equipo y
de los productores que dieron permiso; pidan autorización antes de reutilizarlas fuera del proyecto.
