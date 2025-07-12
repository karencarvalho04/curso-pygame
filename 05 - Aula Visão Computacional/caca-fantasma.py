import cv2
import numpy as np

# Captura da câmera
cap = cv2.VideoCapture(0)
# Criação do subtrator de fundo
fgbg = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=80, detectShadows=True)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    fgmask = fgbg.apply(gray)

    # Limpa ruídos e realça "anomalias"
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
    mask = cv2.GaussianBlur(mask, (21, 21), 0)

    # Detecta contornos (possíveis "espíritos")
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    ghost_frame = frame.copy()

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if 500 < area < 5000:  # Limite de área para não detectar pessoas reais
            x, y, w, h = cv2.boundingRect(cnt)
            ghost = frame[y:y+h, x:x+w]
            ghost = cv2.cvtColor(ghost, cv2.COLOR_BGR2GRAY)
            ghost = cv2.applyColorMap(ghost, cv2.COLORMAP_BONE)
            ghost = cv2.addWeighted(ghost_frame[y:y+h, x:x+w], 0.5, ghost, 0.5, 0)
            ghost_frame[y:y+h, x:x+w] = ghost
            cv2.rectangle(ghost_frame, (x, y), (x+w, y+h), (255, 255, 255), 1)
            cv2.putText(ghost_frame, "Possível Espírito 👻", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    cv2.imshow('Detector Paranormal (modo artístico)', ghost_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
