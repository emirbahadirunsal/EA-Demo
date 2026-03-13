import pyvisa
import time
from settings import *

class HapticController:
    def __init__(self):
        self.rm = pyvisa.ResourceManager()
        self.device = None
        self.is_connected = False
        
        # Durum Takibi
        self.current_freq = 0
        self.current_volt = 0.0
        self.current_wave = WAVE_SQUARE # Şu anki dalga tipi
        
        self.connect()

    def connect(self):
        try:
            self.device = self.rm.open_resource(VISA_ADDRESS)
            self.device.write_termination = '\n'
            self.device.read_termination = '\n'
            
            print(f"Bağlandı: {self.device.query('*IDN?')}")
            
            # Reset ve Temel Ayarlar
            self.device.write('*RST')
            self.device.write('VOLT:UNIT VPP')
            self.device.write('OUTP:LOAD INF')
            self.device.write(f'VOLT:OFFS {OFFSET_V}')
            
            # Varsayılan: Kare Dalga
            self.device.write(f'FUNC {WAVE_SQUARE}')
            self.device.write('FUNC:SQU:DCYC 50')
            
            # Başlangıç Değerleri
            self.device.write(f'FREQ {CARRIER_FREQ}')
            self.device.write(f'VOLT {MIN_VOLTAGE}')
            
            # ALWAYS ON Prensibi
            self.device.write('OUTP ON')
            
            self.current_wave = WAVE_SQUARE
            self.current_freq = CARRIER_FREQ
            self.current_volt = MIN_VOLTAGE
            self.is_connected = True
            
        except Exception as e:
            print(f"HATA: Bağlantı kurulamadı ({e}). Dummy mod.")
            self.is_connected = False

    def update_signal(self, waveform, frequency, voltage):
        """
        Sinyali günceller.
        waveform: WAVE_SQUARE veya WAVE_NOISE
        """
        if not self.is_connected or not self.device:
            return

        # 1. Voltaj Limitleme (Ayarlardan gelen MAX_VOLTAGE)
        if voltage > MAX_VOLTAGE: voltage = MAX_VOLTAGE
        if voltage < MIN_VOLTAGE: voltage = MIN_VOLTAGE
        
        try:
            # 2. Dalga Tipi Değişimi
            if waveform != self.current_wave:
                self.device.write(f'FUNC {waveform}')
                self.current_wave = waveform

            # 3. Parametre Güncellemeleri
            # Noise modunda FREQ komutu işlevsizdir, sadece Square'de yolla.
            if waveform == WAVE_SQUARE:
                if int(frequency) != int(self.current_freq):
                    self.device.write(f'FREQ {int(frequency)}')
                    self.current_freq = int(frequency)
            
            # Voltaj (Her iki modda da geçerli)
            # Gereksiz trafiği önlemek için küçük değişimleri yoksay
            if abs(voltage - self.current_volt) > 0.05:
                self.device.write(f'VOLT {voltage:.2f}')
                self.current_volt = voltage
                
        except Exception as e:
            print(f"Komut Hatası: {e}")

    def close(self):
        if self.is_connected and self.device:
            try:
                self.device.write(f'VOLT {MIN_VOLTAGE}')
                self.device.write('OUTP OFF')
                self.device.close()
            except: pass