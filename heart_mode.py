import pygame
import math
from settings import *

class HeartMode:
    def __init__(self):
        self.heart_points = self.create_heart_polygon(WIDTH // 2, HEIGHT // 2, 25)
        temp_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.polygon(temp_surface, (255, 255, 255), self.heart_points)
        self.mask = pygame.mask.from_surface(temp_surface)
        self.visual_color = COLOR_HEART_DIM
        
        # Font Tanımları
        self.font_title = pygame.font.SysFont("Arial", 50, bold=True)
        self.font_sub = pygame.font.SysFont("Arial", 30, italic=True)

    def create_heart_polygon(self, center_x, center_y, scale):
        points = []
        for t in range(0, 628, 5):
            angle = t / 100.0
            x = 16 * math.sin(angle) ** 3
            y = 13 * math.cos(angle) - 5 * math.cos(2*angle) - 2 * math.cos(3*angle) - math.cos(4*angle)
            px = center_x + (x * scale)
            py = center_y - (y * scale)
            points.append((px, py))
        return points

    def update(self, finger_pos, current_time):
        """
        Dönüş: (Waveform, Freq, Volt)
        """
        target_freq = CARRIER_FREQ
        target_volt = MIN_VOLTAGE
        self.visual_color = COLOR_HEART_DIM

        if finger_pos:
            try:
                if self.mask.get_at(finger_pos):
                    cycle_time = current_time % 1000 
                    is_lub = 0 < cycle_time < 150
                    is_dub = 300 < cycle_time < 450
                    
                    if is_lub or is_dub:
                        target_volt = MAX_VOLTAGE # Atışta Max Volt (4.0V)
                        self.visual_color = COLOR_HEART_BEAT
                    else:
                        target_volt = MIN_VOLTAGE
                        self.visual_color = COLOR_HEART_SILENT
            except IndexError: pass

        return (WAVE_SQUARE, target_freq, target_volt)

    def draw(self, screen, finger_pos):
        screen.fill(COLOR_BLACK)
        pygame.draw.polygon(screen, self.visual_color, self.heart_points)
        
        # --- METİN ÇİZİMİ ---
        # Ana Başlık
        text_title = self.font_title.render("Touch the heart to feel the rhythm.", True, COLOR_WHITE)
        rect_title = text_title.get_rect(center=(WIDTH // 2, HEIGHT - 150))
        screen.blit(text_title, rect_title)
        
        # Alt Başlık (Tematik)
        text_sub = self.font_sub.render("\"Can you feel my heart?\"", True, (200, 200, 200))
        rect_sub = text_sub.get_rect(center=(WIDTH // 2, HEIGHT - 100))
        screen.blit(text_sub, rect_sub)

        if finger_pos:
            pygame.draw.circle(screen, COLOR_WHITE, finger_pos, 20)