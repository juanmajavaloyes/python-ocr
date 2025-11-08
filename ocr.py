from paddleocr import PaddleOCR
import cv2

ocr = PaddleOCR(use_angle_cls=True, lang='es', show_log=False)

def ocr_page(img_bgr):
    result = ocr.ocr(img_bgr, cls=True)
    lines = []
    if result and result[0]:
        for det in result[0]:
            txt = det[1][0]
            if txt:
                lines.append(txt)
    return "\n".join(lines)
