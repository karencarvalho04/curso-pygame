import cv2
import mediapipe as mp

# Inicializa o MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Função para verificar se o gesto "paz e amor" está sendo feito
def is_peace_sign(hand_landmarks):
    # Verifica a posição dos dedos: True = levantado
    fingers = []

    # Indicador (8) está acima da junta (6)?
    fingers.append(hand_landmarks.landmark[8].y < hand_landmarks.landmark[6].y)

    # Médio (12) está acima da junta (10)?
    fingers.append(hand_landmarks.landmark[12].y < hand_landmarks.landmark[10].y)

    # Anelar (16) está abaixo da junta (14)?
    fingers.append(hand_landmarks.landmark[16].y > hand_landmarks.landmark[14].y)

    # Mínimo (20) está abaixo da junta (18)?
    fingers.append(hand_landmarks.landmark[20].y > hand_landmarks.landmark[18].y)

    # Se indicador e médio levantados e os demais abaixados
    return fingers == [True, True, True, True]

# Captura de vídeo
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            if is_peace_sign(hand_landmarks):
                cv2.putText(frame, "Bons ventos", (10, 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)

    cv2.imshow("Bons ventos", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
