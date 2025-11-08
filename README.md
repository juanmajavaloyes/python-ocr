# Libro OCR Backend (FastAPI + PaddleOCR)

Servidor para convertir un **MP4** (libro abierto con dos páginas) en un **PDF buscable**:
- Extrae escenas y escoge el **fotograma más nítido** por página doble.
- Detecta el **pliegue oscuro** y separa en **izquierda/derecha**.
- **Endereza** (deskew) y corrige perspectiva.
- **OCR (PaddleOCR, español)** y genera **PDF con capa de texto**.

## Endpoints
- `GET /health` → `{ "ok": true }`
- `POST /procesar` → **Body:** `multipart/form-data` con `video: <mp4>` → **Return:** `application/pdf`

## Despliegue 1‑clic en Railway
1. Crea un proyecto en Railway e **importa este directorio** (o usa la CLI):
   ```bash
   npm i -g @railway/cli
   railway login
   railway init
   railway up
   ```
2. Railway detectará el **Dockerfile** y desplegará la app.
3. Cuando esté activo, comprueba:
   ```
   https://<tu-proyecto>.up.railway.app/health
   ```

## Variables de entorno
No necesita variables. Usa el puerto `$PORT` que inyecta Railway.

## Requisitos (solo si ejecutas local)
- Python 3.10+
- FFmpeg (para lectura de vídeo por OpenCV)
- Dependencias Python:
  ```bash
  pip install -r requirements.txt
  ```
- Ejecutar local:
  ```bash
  uvicorn main:app --reload
  ```
  Abrir: `http://127.0.0.1:8000/health`

## Notas de rendimiento
- La **primera llamada** a `/procesar` tarda más (descarga/carga del modelo PaddleOCR).
- Para vídeos muy largos, reduce movimientos de cámara y mejora iluminación.
- Si tu plan gratuito se queda sin memoria, considera cambiar `ocr.py` a Tesseract o subir de plan.

## Licencias
- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) (Apache 2.0)
- [FastAPI](https://fastapi.tiangolo.com/) (MIT)
- [OpenCV](https://opencv.org/) (BSD) 
