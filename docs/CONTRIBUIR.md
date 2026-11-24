# Cómo trabajar en equipo en este repositorio

## Acceso

Que el repositorio sea **público** quiere decir que cualquiera puede verlo, **no** que cualquiera
puede modificarlo. El dueño debe agregar a cada integrante en
**Settings → Collaborators → Add people** para que puedan subir cambios.

## Reglas básicas

1. Antes de empezar: `git pull`
2. Trabajen en una rama propia para cambios de código:
   ```bash
   git checkout -b nombre/lo-que-hago      # ej. hector/mejorar-inferencia
   ```
3. Suban cambios pequeños y frecuentes, con mensajes claros:
   ```bash
   git add src/inferir.py
   git commit -m "Inferir: guarda resultados en JSON con coordenadas GPS"
   git push -u origin hector/mejorar-inferencia
   ```
4. Abran un **Pull Request** en GitHub y que otro integrante lo revise antes de unirlo a `main`.

Para **subir fotos** pueden hacerlo directo en `main`, siempre que sean fotos reducidas
(ver CAPTURA_DE_IMAGENES.md).

## Qué NO se sube

- Fotos originales sin reducir
- Carpetas `runs/`, `data/dataset/`, `.venv/` (ya están en `.gitignore`)
- Pesos de entrenamientos de prueba. Solo se guardan en `modelos/` los que valga la pena
  conservar, con un nombre que diga qué son: `modelos/v1_yolov8n_640_map50-0.72.pt`

## Registro de experimentos

Cada entrenamiento que se reporte va en `docs/EXPERIMENTOS.md` con: fecha, quién, modelo
base, épocas, tamaño de imagen, número de imágenes y resultados (P, R, mAP@50, mAP@50-95).
Esto sale directo en el capítulo de resultados de la tesis.
