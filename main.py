from fastapi import FastAPI, File, UploadFile
from fastapi.responses import Response, JSONResponse
import tempfile, os, io, sys, traceback

from extract_frames import extract_best_frames
from split_and_deskew import split_and_fix_pages
from ocr import ocr_page
from make_pdf import build_pdf

app = FastAPI(title="Libro OCR Backend", version="1.0.0")

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/procesar")
async def procesar(video: UploadFile = File(...)):
    try:
        # 0) Guardar el vídeo temporalmente
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
            tmp.write(await video.read())
            video_path = tmp.name

        # 1) Extraer fotogramas relevantes (una 'página doble' por escena)
        frames = extract_best_frames(video_path)

        pages = []
        for img in frames:
            # 2) Separar izquierda/derecha + corregir inclinación/perspectiva
            left, right = split_and_fix_pages(img)

            # 3) OCR (texto por página)
            text_left = ocr_page(left)
            text_right = ocr_page(right)

            pages.append((left, text_left))
            pages.append((right, text_right))

        # 4) Generar PDF buscable (imagen + capa de texto)
        pdf_bytes = build_pdf(pages)

        # Limpieza
        try:
            os.remove(video_path)
        except Exception:
            pass

        return Response(pdf_bytes, media_type="application/pdf")
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})
