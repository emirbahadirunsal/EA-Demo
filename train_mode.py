import pygame
import math
from settings import *

class TrainMode:
    def __init__(self):
        self.start_time = pygame.time.get_ticks()
        self.duration = 20000 # 20 Saniye döngü
        self.sleepers = [i / 20.0 for i in range(20)] 
        self.current_freq = 1.0 
        self.speed_factor = 0.0
        
        # Font Tanımı
        self.font_instr = pygame.font.SysFont("Arial", 40, bold=True)
        self.font_info = pygame.font.SysFont("Arial", 30)

    def update(self, finger_pos, current_time):
        """
        Dönüş: (Waveform, Frequency, Voltage)
        """
        # Döngü zamanı (0.0 - 1.0 arası)
        cycle_time = (current_time - self.start_time) % self.duration
        progress = cycle_time / self.duration 
        
        # --- LOGARİTMİK / ÜSTEL HIZLANMA MANTIĞI ---
        # Yavaş başlayıp sonradan hızlanan eğri (progress^4)
        self.speed_factor = math.pow(progress, 4)
        
        # Frekans: 1 Hz ile 200 Hz arası
        target_freq = 1 + (199 * self.speed_factor)
        self.current_freq = target_freq
        
        # Görsel ray hızı
        move_speed = 0.001 + (0.03 * self.speed_factor)
        
        for i in range(len(self.sleepers)):
            self.sleepers[i] += move_speed
            if self.sleepers[i] > 1.0:
                self.sleepers[i] -= 1.0
        
        # --- VOLTAJ AYARI ---
        # İstek: Tren voltajı sabit 4.0V olsun.
        target_volt = MIN_VOLTAGE
        if finger_pos:
            target_volt = 4.0
            
        return (WAVE_SQUARE, target_freq, target_volt)

    def draw(self, screen, finger_pos):
        horizon_y = HEIGHT // 2
        pygame.draw.rect(screen, COLOR_SKY, (0, 0, WIDTH, horizon_y))
        pygame.draw.rect(screen, COLOR_GROUND, (0, horizon_y, WIDTH, HEIGHT - horizon_y))
        
        center_x = WIDTH // 2
        bottom_width = 800
        top_width = 20
        
        p1 = (center_x - top_width, horizon_y)
        p2 = (center_x - bottom_width, HEIGHT)
        p3 = (center_x + bottom_width, HEIGHT)
        p4 = (center_x + top_width, horizon_y)
        
        pygame.draw.line(screen, COLOR_RAIL, p1, p2, 5)
        pygame.draw.line(screen, COLOR_RAIL, p4, p3, 5)
        
        for pos_factor in self.sleepers:
            visual_y_factor = pos_factor * pos_factor 
            draw_y = horizon_y + (visual_y_factor * (HEIGHT - horizon_y))
            current_width = top_width + (visual_y_factor * (bottom_width - top_width)) * 2
            rect_x = center_x - (current_width // 2)
            rect_h = 2 + (20 * visual_y_factor)
            pygame.draw.rect(screen, COLOR_SLEEPER, (rect_x, draw_y, current_width, rect_h))

        # --- METİN ÇİZİMİ ---
        # Ana Yönerge (Circular Movement)
        text_instr = self.font_instr.render("Please perform circular movements on the tracks.", True, COLOR_WHITE)
        # Okunabilirlik için arka plan ekleyelim
        bg_rect = text_instr.get_rect(center=(WIDTH // 2, 150))
        bg_rect.inflate_ip(40, 20)
        bg_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
        bg_surface.fill(COLOR_TEXT_BG) # Yarı saydam siyah ayarı settings'den
        screen.blit(bg_surface, bg_rect)
        screen.blit(text_instr, text_instr.get_rect(center=(WIDTH // 2, 150)))

        # Frekans Bilgisi (Sol üst)
        freq_text = self.font_info.render(f"Frequency: {int(self.current_freq)} Hz", True, COLOR_WHITE)
        screen.blit(freq_text, (50, 50))

        if finger_pos:
            pygame.draw.circle(screen, (255, 100, 100), finger_pos, 30)