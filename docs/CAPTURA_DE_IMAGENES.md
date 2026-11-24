# Guía de captura de imágenes

La calidad del modelo depende más de las fotos que del código. Esta guía es para que todo el
equipo capture igual.

## Dónde van

Fotos sin etiquetar → `data/crudas/<clase>/`. Si una foto tiene varias cosas, o no saben qué
tiene, va a `data/crudas/sin_clasificar/`. La clasificación final la dan las cajas al
etiquetar; estas carpetas solo sirven para llevar la cuenta de cuántas fotos hay de cada caso.

## Nombre de archivo

```
AAAAMMDD_predio_altura_numero.jpg
20261124_tequila-norte_10m_0001.jpg
20261124_tequila-norte_suelo_0002.jpg     ← tomada a pie
```

Sin espacios, sin acentos, sin ñ.

## Tamaño

Las fotos de la IMX708 pesan varios MB. **Antes de subirlas**, redúzcanlas:

```bash
python tools/reducir_imagenes.py carpeta_original/ data/crudas/picudo/
```

Así quedan con un lado largo de 1920 px, conservan los datos GPS (EXIF) y el repo no se satura.
**Los originales guárdenlos en el Drive del equipo**, no en GitHub (GitHub rechaza archivos de
más de 100 MB y el repo se vuelve lento después de unos cuantos GB).

## Qué fotografiar

- **Variedad de condiciones:** mañana, mediodía y tarde, nublado y soleado. El protocolo lo pide
  explícitamente.
- **Etapas del cultivo:** plantas de 1 a 7 años.
- **Alturas:** las mismas a las que va a volar el dron, más algunas a pie para tener detalle.
- **Plantas sanas también:** el modelo necesita saber cómo se ve una planta sana. Busquen que
  haya proporción parecida entre sanas y enfermas.
- **Meta mínima:** al menos **150 a 200 ejemplos (cajas) por clase**. Si una clase tiene
  muy pocas, va a fallar en esa.

## Registro

Por cada salida a campo, agreguen una línea a `data/registro_capturas.csv`
(fecha, predio, ubicación, condiciones de luz, quién capturó, número de fotos, observaciones).
Esto sirve para la sección de metodología de la tesis.
