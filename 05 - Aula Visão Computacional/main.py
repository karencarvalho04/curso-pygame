import cv2

# Acessa a câmera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()  # Captura o frame da câmera
    if not ret:
        break

    cv2.imshow("Minha Webcam", frame)  # Mostra o vídeo na tela

    # Pressione 'q' para sair
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
