import pygame
import os
import sys
from settings import *
from haptics import HapticController
from heart_mode import HeartMode
from train_mode import TrainMode
from texture_mode import TextureMode

os.environ['SDL_VIDEO_WINDOW_POS'] = f"{X_KOORDINATI},{Y_KOORDINATI}"

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
pygame.display.set_caption("Haptic System Main")

haptics = HapticController()

mode_heart = HeartMode()
mode_texture = TextureMode()
mode_train = TrainMode()

current_mode = mode_heart
mode_name = "HEART"

running = True
clock = pygame.time.Clock()

print(f"Sistem Başlatıldı. MAX VOLTAGE: {MAX_VOLTAGE}V")

while running:
    current_time = pygame.time.get_ticks()
    finger_pos = None
    
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT: running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: running = False
            elif event.key == pygame.K_RETURN:
                if mode_name == "HEART":
                    current_mode = mode_texture
                    mode_name = "TEXTURE"
                elif mode_name == "TEXTURE":
                    current_mode = mode_train
                    mode_name = "TRAIN"
                else:
                    current_mode = mode_heart
                    mode_name = "HEART"
                print(f"Mod: {mode_name}")

    mouse_x, mouse_y = pygame.mouse.get_pos()
    if pygame.mouse.get_pressed()[0]: 
        raw_x = mouse_x / WIDTH
        raw_y = mouse_y / HEIGHT
        if INVERT_X: raw_x = 1.0 - raw_x
        if INVERT_Y: raw_y = 1.0 - raw_y
        finger_pos = (int(raw_x * WIDTH), int(raw_y * HEIGHT))

    # --- SİNYAL GÜNCELLEME ---
    wave, freq, volt = current_mode.update(finger_pos, current_time)
    
    # Donanıma gönder
    haptics.update_signal(wave, freq, volt)

    current_mode.draw(screen, finger_pos)
    pygame.display.flip()
    clock.tick(60)

haptics.close()
pygame.quit()
sys.exit()