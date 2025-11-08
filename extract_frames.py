import cv2
import numpy as np

def sharpness(gray):
    return cv2.Laplacian(gray, cv2.CV_64F).var()

def extract_best_frames(video_path, thresh=0.35, min_gap_sec=8):
    """
    - Detecta cambios de escena por diferencia media de fotogramas.
    - Cada vez que hay cambio, empieza un nuevo segmento.
    - De cada segmento elige el fotograma más nítido (máxima varianza de Laplaciano).
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise RuntimeError("No se pudo abrir el vídeo.")

    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    min_gap_frames = int(fps * min_gap_sec)

    prev_gray = None
    best_frame = None
    best_sharp = -1.0
    last_key_idx = -10**9
    idx = 0
    chosen = []

    while True:
        ok, frame = cap.read()
        if not ok:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if prev_gray is None:
            prev_gray = gray
            best_frame = frame
            best_sharp = sharpness(gray)
            last_key_idx = idx
            idx += 1
            continue

        diff = cv2.absdiff(gray, prev_gray)
        score = float(diff.mean())

        if score > thresh and (idx - last_key_idx) > min_gap_frames:
            # Cierra segmento anterior
            if best_frame is not None:
                chosen.append(best_frame)
            # Nuevo segmento
            best_frame = frame
            best_sharp = sharpness(gray)
            last_key_idx = idx
        else:
            # Sigue dentro del mismo segmento: quedarnos con el más nítido
            s = sharpness(gray)
            if s > best_sharp:
                best_sharp = s
                best_frame = frame

        prev_gray = gray
        idx += 1

    if best_frame is not None:
        chosen.append(best_frame)

    cap.release()
    return chosen
