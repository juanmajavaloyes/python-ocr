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
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    pw, ph = A4

    for img_bgr, text in pages:
        pil = _cv_bgr_to_pil(img_bgr)
        iw, ih = pil.size
        scale = min(pw/iw, ph/ih)
        w = iw * scale
        h = ih * scale
        x = (pw - w) / 2
        y = (ph - h) / 2

        c.drawImage(ImageReader(pil), x, y, width=w, height=h)

        if text:
            c.setFillColor(white)
            c.setFont("Helvetica", 6)
            lines = text.split("\n")
            ty = 12
            for line in lines:
                for chunk in [line[i:i+90] for i in range(0, len(line), 90)]:
                    c.drawString(10, ty, chunk)
                    ty += 7
                    if ty > ph - 10:
                        break

        c.showPage()

    c.save()
    return buffer.getvalue()
