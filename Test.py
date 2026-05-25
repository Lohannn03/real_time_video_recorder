import cv2
import numpy as np

def quantize_soft(img, levels=10):
    img = img.astype(np.float32)
    step = 256.0 / levels
    q = np.floor(img / step) * step + step * 0.5
    return np.clip(q, 0, 255).astype(np.uint8)

def smooth_paint(img):
    out = img.copy()
    for _ in range(3):
        out = cv2.bilateralFilter(out, 9, 45, 45)
    out = cv2.edgePreservingFilter(out, flags=1, sigma_s=60, sigma_r=0.35)
    return out

def soft_edges(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edge = cv2.Laplacian(gray, cv2.CV_8U, ksize=3)
    edge = cv2.threshold(edge, 28, 255, cv2.THRESH_BINARY_INV)[1]
    edge = cv2.GaussianBlur(edge, (3, 3), 0)
    return edge

def warm_tone(img):
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    l = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8)).apply(l)
    lab = cv2.merge([l, a, b])
    img = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    s = cv2.convertScaleAbs(s, alpha=1.18, beta=6)
    v = cv2.convertScaleAbs(v, alpha=1.08, beta=10)
    hsv = cv2.merge([h, s, v])
    img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    b, g, r = cv2.split(img)
    r = cv2.add(r, 10)
    g = cv2.add(g, 4)
    return cv2.merge([b, g, r])

def blend_edges(color, edge):
    edge3 = cv2.cvtColor(edge, cv2.COLOR_GRAY2BGR)
    edge3 = edge3.astype(np.float32) / 255.0
    color = color.astype(np.float32)
    out = color * (0.82 + 0.18 * edge3)
    return np.clip(out, 0, 255).astype(np.uint8)

def painterly_glow(img):
    blur = cv2.GaussianBlur(img, (0, 0), 3)
    return cv2.addWeighted(img, 1.08, blur, -0.08, 4)

def cartoon_paint_style(img):
    base = smooth_paint(img)
    base = quantize_soft(base, levels=10)
    base = warm_tone(base)
    edge = soft_edges(img)
    out = blend_edges(base, edge)
    out = painterly_glow(out)
    return out

img = cv2.imread("Bad.jpg")


cartoon = cartoon_paint_style(img)
cv2.imwrite("BadDemo.jpg", cartoon)
cv2.imshow("Original Image", img)
cv2.imshow("Cartoon Image(Bad)", cartoon)
cv2.waitKey(0)
cv2.destroyAllWindows()