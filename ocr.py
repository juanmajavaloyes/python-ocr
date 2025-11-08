from paddleocr import PaddleOCR
import cv2

# Inicializa PaddleOCR en español, CPU
# Nota: en Railway free puede tardar 30-60s la primera carga del modelo.
ocr = PaddleOCR(use_angle_cls=True, lang='es', show_log=False)

def ocr_page(img_bgr):
    """
    Recibe imagen BGR (OpenCV). Devuelve el texto unido por líneas.
    """
    result = ocr.ocr(img_bgr, cls=True)
    lines = []
    if result and result[0]:
        for det in result[0]:
            txt = det[1][0]
            if txt:
                lines.append(txt)
    return "\n".join(lines)
