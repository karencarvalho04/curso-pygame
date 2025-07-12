import cv2
import mediapipe as mp
import numpy as np

# Inicializa o MediaPipe
mp_selfie = mp.solutions.selfie_segmentation
segment = mp_selfie.SelfieSegmentation(model_selection=1)

# Captura da webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)  # Espelha horizontalmente
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Processa a imagem
    results = segment.process(rgb)

    # Gera a máscara (fundo = 0, pessoa = 1)
    mask = results.segmentation_mask
    condition = mask > 0.6  # Ajuste de sensibilidade

    # Cria o fundo desfocado
    blurred = cv2.GaussianBlur(frame, (55, 55), 0)

    # Combina a imagem original com o fundo desfocado
    output = np.where(condition[..., None], frame, blurred)

    cv2.imshow("Modo Retrato - Fundo Desfocado", output)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
