from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import white
import io
from PIL import Image
import cv2

def _cv_bgr_to_pil(img_bgr):
    rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    return Image.fromarray(rgb)

def build_pdf(pages):
    """
    pages: lista de tuplas (img_bgr, text)
    Devuelve bytes de PDF con imagen completa + capa de texto (pequeña) para búsqueda.
    """
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    pw, ph = A4  # puntos (72 dpi)

    for img_bgr, text in pages:
        pil = _cv_bgr_to_pil(img_bgr)
        iw, ih = pil.size
        # Ajuste a página manteniendo aspecto
        scale = min(pw/iw, ph/ih)
        w = iw * scale
        h = ih * scale
        x = (pw - w) / 2
        y = (ph - h) / 2

        c.drawImage(ImageReader(pil), x, y, width=w, height=h)

        # Capa de texto OCR (tamaño mínimo, color blanco sobre blanco para "ocultarlo")
        if text:
            c.setFillColor(white)
            c.setFont("Helvetica", 6)
            lines = text.split("\n")
            ty = 12  # margen inferior
            for line in lines:
                for chunk in [line[i:i+90] for i in range(0, len(line), 90)]:
                    c.drawString(10, ty, chunk)
                    ty += 7
                    if ty > ph - 10:
                        break

        c.showPage()

    c.save()
    return buffer.getvalue()
