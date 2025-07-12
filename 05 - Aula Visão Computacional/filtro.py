import cv2
import numpy as np

# Carrega o classificador de rosto
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Carrega a imagem PNG (sem transparência)
overlay_img = cv2.imread("BITCASH - adesivo.png")  # Substitua pelo nome da sua imagem

# Verifica se a imagem foi carregada corretamente
if overlay_img is None:
    raise FileNotFoundError("A imagem 'imagem.png' não foi encontrada ou não pôde ser carregada.")

def sobrepor_imagem(frame, overlay, x, y, w, h):
    # Redimensiona a imagem para a largura do rosto e altura proporcional (1/2 da altura do rosto)
    overlay_resized = cv2.resize(overlay, (w, h // 2), interpolation=cv2.INTER_AREA)

    h_overlay, w_overlay, _ = overlay_resized.shape

    # Posição sobre a testa (acima do rosto)
    y1 = max(0, y - h_overlay)
    y2 = y1 + h_overlay
    x1 = x
    x2 = x + w

    # Verifica limites da imagem principal
    if y2 > frame.shape[0] or x2 > frame.shape[1]:
        return  # Não desenha se a imagem estiver fora do quadro

    roi = frame[y1:y2, x1:x2]
    frame[y1:y2, x1:x2] = overlay_resized

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    for (x, y, w, h) in faces:
        try:
            sobrepor_imagem(frame, overlay_img, x, y, w, h)
        except Exception as e:
            print(f"Erro ao sobrepor imagem: {e}")

    cv2.imshow("Detector de Rostos com Imagem", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()