import pygame as pg
import random
import threading
import cv2
import mediapipe as mp
import time

# ========== VISÃO COMPUTACIONAL ==========
class BodyTracker:
    def __init__(self):
        self.jump = False
        self.running = True
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Ajuda no Windows
        self.pose = mp.solutions.pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.thread = threading.Thread(target=self.track_body)
        self.thread.start()

    def track_body(self):
        print("🟢 Iniciando rastreamento corporal...")
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                print("❌ Erro ao capturar da webcam.")
                time.sleep(0.5)
                continue

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.pose.process(frame_rgb)

            if results.pose_landmarks:
                shoulder = results.pose_landmarks.landmark[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER]
                wrist = results.pose_landmarks.landmark[mp.solutions.pose.PoseLandmark.RIGHT_WRIST]
                self.jump = wrist.y < shoulder.y
            else:
                self.jump = False

            time.sleep(0.02)

        self.cap.release()
        print("🔴 Rastreamento finalizado.")

    def stop(self):
        self.running = False
        self.thread.join()

# ========== JOGO FLAPPY BIRD ==========
class FlapBirds:
    def __init__(self, window_size):
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.orange = (255, 165, 0)

        self.window = pg.display.set_mode(window_size)
        pg.display.set_caption("Flappy Bird com Controle Corporal")
        self.clock = pg.time.Clock()
        self.font = pg.font.SysFont("Courier New", 50, bold=True)

        self.gravity = 5
        self.in_play = True
        self.bird_pos = [100, 100]
        self.vertical_speed = 0
        self.score = 0
        self.last_click_status = (False, False, False)
        self.bird_passing_through_obstacle = False

        # Pipes e cenário
        self.pipe_positions = [[x, self.new_height()] for x in range(400, 2001, 400)]
        self.bg_positions = [[0, 0], [2120, 0]]
        self.ground_positions = [[0, 634], [1010, 634], [2020, 634]]

        # Elementos visuais simples
        self.background = pg.Surface((2120, 634)); self.background.fill((135, 206, 235))
        self.bird = pg.Surface((51, 36)); self.bird.fill((255, 255, 0))
        self.ground = pg.Surface((1010, 86)); self.ground.fill((139, 69, 19))
        self.pipe = pg.Surface((123, 600)); self.pipe.fill((0, 128, 0))
        self.pipe_usd = pg.transform.flip(self.pipe, False, True)

    def new_height(self):
        return random.randint(6, 10) * 50

    def clear_window(self):
        self.window.fill(self.white)

    def draw(self):
        for bg in self.bg_positions:
            self.window.blit(self.background, bg)
        for pipe in self.pipe_positions:
            self.window.blit(self.pipe, (pipe[0], pipe[1]))
            self.window.blit(self.pipe_usd, (pipe[0], pipe[1] - 800))
        for g in self.ground_positions:
            self.window.blit(self.ground, g)
        self.window.blit(self.bird, self.bird_pos)

    def move(self, key):
        if key == 'space':
            self.vertical_speed = -10
        elif key == 'r':
            self.__init__((1280, 720))

    def update_positions(self):
        if not self.in_play:
            return

        for p in self.pipe_positions:
            p[0] -= 1.2
        if self.pipe_positions[0][0] <= -123:
            self.pipe_positions.pop(0)
            self.pipe_positions.append([self.pipe_positions[-1][0] + 400, self.new_height()])

        for bg in self.bg_positions:
            bg[0] -= 1.2
        if self.bg_positions[0][0] <= -2120:
            self.bg_positions = [[0, 0], [2120, 0]]

        for g in self.ground_positions:
            g[0] -= 1.2
        if self.ground_positions[0][0] <= -1010:
            self.ground_positions = [[0, 634], [1010, 634], [2020, 634]]

        if self.vertical_speed <= 5:
            self.vertical_speed += self.gravity / 15
        self.bird_pos[1] += self.vertical_speed

    def detect_collision(self):
        pipe = self.pipe_positions[0]
        if pipe[0] < self.bird_pos[0] + 51 < pipe[0] + 123:
            if self.bird_pos[1] < pipe[1] - 200 or self.bird_pos[1] + 36 > pipe[1]:
                self.in_play = False
        if self.bird_pos[1] + 36 >= 634:
            self.in_play = False

    def update_score(self):
        pipe = self.pipe_positions[0]
        if pipe[0] < self.bird_pos[0] + 51 and pipe[0] + 123 > self.bird_pos[0]:
            self.bird_passing_through_obstacle = True
        else:
            if self.bird_passing_through_obstacle:
                self.score += 1
            self.bird_passing_through_obstacle = False

        score_text = self.font.render(str(self.score), True, self.black)
        self.window.blit(score_text, (1100, 50))

# ========== EXECUÇÃO ==========
pg.init()
jogo = FlapBirds((1280, 720))
body_tracker = BodyTracker()

try:
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                body_tracker.stop()
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN:
                jogo.move(pg.key.name(event.key))
                if pg.key.name(event.key) == 'escape':
                    body_tracker.stop()
                    pg.quit()
                    quit()

        # Controle por gesto
        if jogo.in_play and body_tracker.jump:
            jogo.move('space')

        # Atualização do jogo
        jogo.clock.tick(60)
        jogo.clear_window()
        jogo.update_positions()
        jogo.draw()
        jogo.update_score()
        jogo.detect_collision()
        pg.display.update()

except Exception as e:
    print(f"❌ Erro: {e}")
    body_tracker.stop()
    pg.quit()
