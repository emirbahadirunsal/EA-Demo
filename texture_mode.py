import pygame
import random
import math
from settings import *

class TextureMode:
    def __init__(self):
        box_size = 150
        self.box_sand = pygame.Rect(WIDTH * 0.25 - box_size//2, HEIGHT//2 - box_size//2, box_size, box_size)
        self.box_metal = pygame.Rect(WIDTH * 0.75 - box_size//2, HEIGHT//2 - box_size//2, box_size, box_size)
        
        self.dragging_sand = False
        self.dragging_metal = False
        self.offset_x = 0
        self.offset_y = 0
        
        self.sand_dots = [(random.randint(0, WIDTH // 2), random.randint(0, HEIGHT)) for _ in range(200)]
        self.prev_finger_pos = (0, 0)
        
        # Font Tanımı
        self.font_instr = pygame.font.SysFont("Arial", 40, bold=True)
        self.font_label = pygame.font.SysFont("Arial", 30, bold=True)

    def update(self, finger_pos, current_time):
        """
        Dönüş: (WaveformType, Frequency, Voltage)
        """
        target_wave = WAVE_SQUARE
        target_freq = CARRIER_FREQ
        target_volt = MIN_VOLTAGE
        
        if not finger_pos:
            self.dragging_sand = False
            self.dragging_metal = False
            return (WAVE_SQUARE, 125, MIN_VOLTAGE)

        # Kutu yakalama
        if not self.dragging_sand and not self.dragging_metal:
            if self.box_sand.collidepoint(finger_pos):
                self.dragging_sand = True
                self.offset_x = finger_pos[0] - self.box_sand.x
                self.offset_y = finger_pos[1] - self.box_sand.y
            elif self.box_metal.collidepoint(finger_pos):
                self.dragging_metal = True
                self.offset_x = finger_pos[0] - self.box_metal.x
                self.offset_y = finger_pos[1] - self.box_metal.y

        # --- KUM DOKUSU (SOL) - RASTGELE DÜŞÜK FREKANS ---
        if self.dragging_sand:
            self.box_sand.x = finger_pos[0] - self.offset_x
            self.box_sand.y = finger_pos[1] - self.offset_y
            
            target_wave = WAVE_SQUARE
            target_freq = random.choice([30, 40, 50, 60])
            target_volt = random.uniform(3.5, 4.0) # Yüksek Voltaj

        # --- METAL DOKUSU (SAĞ) - SABİT ÇOK DÜŞÜK FREKANS ---
        elif self.dragging_metal:
            self.box_metal.x = finger_pos[0] - self.offset_x
            self.box_metal.y = finger_pos[1] - self.offset_y
            
            target_wave = WAVE_SQUARE
            # Çok düşük frekans (2Hz) ve Maksimum Voltaj (4V)
            # Bu çok keskin, "tak-tak-tak" diye vuran bir his yaratacaktır.
            target_freq = 2
            target_volt = 4.0

        return (target_wave, target_freq, target_volt)

    def draw(self, screen, finger_pos):
        # Sol (Kum)
        pygame.draw.rect(screen, COLOR_SAND_BG, (0, 0, WIDTH//2, HEIGHT))
        for dot in self.sand_dots:
            pygame.draw.circle(screen, COLOR_SAND_DOTS, dot, 2)
        pygame.draw.rect(screen, COLOR_BOX_SAND, self.box_sand)
        
        # Sağ (Metal)
        pygame.draw.rect(screen, COLOR_METAL_BG, (WIDTH//2, 0, WIDTH//2, HEIGHT))
        for x in range(WIDTH // 2, WIDTH, 40):
            pygame.draw.line(screen, COLOR_METAL_GRID, (x, 0), (x, HEIGHT), 2)
        for y in range(0, HEIGHT, 40):
            pygame.draw.line(screen, COLOR_METAL_GRID, (WIDTH // 2, y), (WIDTH, y), 2)
        pygame.draw.rect(screen, COLOR_BOX_METAL, self.box_metal)
        
        pygame.draw.line(screen, COLOR_BLACK, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 5)
        
        # --- METİN ÇİZİMİ ---
        # Üst Yönerge
        text_instr = self.font_instr.render("Please drag the boxes to feel the different surfaces.", True, COLOR_BLACK)
        # Metin okunsun diye arkasına yarı saydam bir kutu koyalım
        bg_rect = text_instr.get_rect(center=(WIDTH // 2, 100))
        bg_rect.inflate_ip(20, 20) # Biraz genişlet
        
        # Yarı saydam arka plan için ayrı bir yüzey gerekir
        bg_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
        bg_surface.fill((255, 255, 255, 180)) # Yarı saydam beyaz
        screen.blit(bg_surface, bg_rect)
        screen.blit(text_instr, text_instr.get_rect(center=(WIDTH // 2, 100)))

        # Kutu Etiketleri
        label_sand = self.font_label.render("Sand (Rough)", True, COLOR_WHITE)
        screen.blit(label_sand, label_sand.get_rect(center=(WIDTH * 0.25, HEIGHT - 100)))
        
        label_metal = self.font_label.render("Metal (Impact)", True, COLOR_WHITE)
        screen.blit(label_metal, label_metal.get_rect(center=(WIDTH * 0.75, HEIGHT - 100)))
        
        if finger_pos:
            pygame.draw.circle(screen, (255, 255, 255), finger_pos, 20)