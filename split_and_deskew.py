import cv2
import numpy as np

def _deskew(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 60, 180)
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 120)
    if lines is None or len(lines) == 0:
        return img
    angles = [theta for (rho, theta) in lines[:, 0]]
    angle = np.median(angles)
    angle_deg = (angle - np.pi / 2) * 180 / np.pi
    M = cv2.getRotationMatrix2D((img.shape[1] // 2, img.shape[0] // 2), angle_deg, 1.0)
    return cv2.warpAffine(img, M, (img.shape[1], img.shape[0]), borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255))

def split_and_fix_pages(image):
    h, w = image.shape[:2]
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    profile = gray.mean(axis=0).astype(np.float32)
    profile = cv2.GaussianBlur(profile.reshape(1, -1), (1, 31), 0).ravel()

    fold_x = int(np.argmin(profile))
    margin = max(20, w // 40)
    fold_x = int(np.clip(fold_x, margin, w - margin))

    left = image[:, :fold_x]
    right = image[:, fold_x:]

    left = _deskew(left)
    right = _deskew(right)

    return left, right
