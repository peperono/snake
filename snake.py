import pygame
import random
import sys
import numpy as np

# Configuracion
ANCHO = 608
ALTO = 608
CELDA = 16
BORDE = 2 * CELDA   # grosor del muro de ladrillos
FPS = 4

# Colores
FONDO  = (0, 0, 0)
OSCURO = (24,  56,  24)
D3 = 3  # profundidad del efecto 3D (bisel)

COLORES_GATO = [
    (220,  60,  60),   # rojo
    (60,  120, 220),   # azul
    (220, 160,  30),   # naranja
    (160,  60, 220),   # morado
    (30,  200, 180),   # turquesa
    (220,  80, 160),   # rosa
    (255, 220,  40),   # amarillo
]

def dibujar_caja_3d(surf, x, y, color):
    """Dibuja una celda de serpiente como caja 3D con bisel (luz desde arriba-izquierda)."""
    d = D3
    S = CELDA
    light = tuple(min(c + 90, 255) for c in color)
    dark  = tuple(max(c - 90, 0)  for c in color)
    pygame.draw.rect(surf, color, (x, y, S, S))
    for i in range(d):
        t = 1.0 - i / d
        li = tuple(int(color[j] + (light[j] - color[j]) * t) for j in range(3))
        da = tuple(int(color[j] + (dark[j]  - color[j]) * t) for j in range(3))
        pygame.draw.line(surf, li, (x+i, y+S-1-i), (x+i, y+i))
        pygame.draw.line(surf, li, (x+i, y+i), (x+S-1-i, y+i))
        pygame.draw.line(surf, da, (x+S-1-i, y+i+1), (x+S-1-i, y+S-1-i))
        pygame.draw.line(surf, da, (x+i+1, y+S-1-i), (x+S-1-i, y+S-1-i))


def dibujar_panel_3d(surf, x, y, w, h, color, d=3, radio=6):
    """Dibuja un panel rectangular con efecto 3D elevado (bisel + sombra exterior)."""
    luz  = tuple(min(c + 80, 255) for c in color)
    osc  = tuple(max(c - 80, 0)  for c in color)
    somb = (0, 0, 0, 60)
    # Sombra exterior (superficie semitransparente desplazada)
    s = pygame.Surface((w + d, h + d), pygame.SRCALPHA)
    pygame.draw.rect(s, somb, (d, d, w, h), border_radius=radio)
    surf.blit(s, (x, y))
    # Cara principal
    pygame.draw.rect(surf, color, (x, y, w, h), border_radius=radio)
    # Bisel claro: borde superior e izquierdo
    for i in range(d):
        t = 1.0 - i / d
        li = tuple(int(color[j] + (luz[j] - color[j]) * t) for j in range(3))
        pygame.draw.line(surf, li, (x+i+radio//2, y+i), (x+w-1-i-radio//2, y+i))
        pygame.draw.line(surf, li, (x+i, y+i+radio//2), (x+i, y+h-1-i-radio//2))
    # Bisel oscuro: borde inferior y derecho
    for i in range(d):
        t = 1.0 - i / d
        da = tuple(int(color[j] + (osc[j] - color[j]) * t) for j in range(3))
        pygame.draw.line(surf, da, (x+i+radio//2, y+h-1-i), (x+w-1-i-radio//2, y+h-1-i))
        pygame.draw.line(surf, da, (x+w-1-i, y+i+radio//2), (x+w-1-i, y+h-1-i-radio//2))


def dibujar_sombra(surf, x, y):
    """Sombra eliptica bajo una presa para simular flotacion 3D."""
    s = pygame.Surface((CELDA, 6), pygame.SRCALPHA)
    pygame.draw.ellipse(s, (0, 0, 0, 110), (1, 0, CELDA - 2, 5))
    surf.blit(s, (x, y + CELDA - 3))


def dibujar_gato(superficie, x, y, color):
    """Dibuja un gatito pixelado en (x, y). y ya incluye el offset de la barra."""
    claro = tuple(min(c + 120, 255) for c in color)
    # Orejas
    pygame.draw.polygon(superficie, color, [(x+1, y+6), (x+4, y+1), (x+7, y+6)])
    pygame.draw.polygon(superficie, color, [(x+9, y+6), (x+12, y+1), (x+15, y+6)])
    # Cabeza
    pygame.draw.ellipse(superficie, color, (x+1, y+4, 14, 11))
    # Ojos
    pygame.draw.rect(superficie, claro, (x+3,  y+7, 3, 3))
    pygame.draw.rect(superficie, claro, (x+10, y+7, 3, 3))
    # Nariz
    pygame.draw.rect(superficie, claro, (x+7, y+11, 2, 1))
    # Bigotes
    pygame.draw.line(superficie, claro, (x+1,  y+11), (x+6,  y+10), 1)
    pygame.draw.line(superficie, claro, (x+10, y+10), (x+15, y+11), 1)

COLOR_PERRO  = (180, 120,  60)
COLOR_PAJARO = (100, 160, 220)
COLOR_CEREZA = (200,  30,  60)
COLOR_PEZ    = ( 80, 180, 230)

def dibujar_perro(superficie, x, y):
    """Dibuja un perrito pixelado en (x, y)."""
    color  = COLOR_PERRO
    oscuro = tuple(max(c - 60, 0) for c in color)
    claro  = tuple(min(c + 80, 255) for c in color)
    # Orejas caidas a los lados
    pygame.draw.rect(superficie, oscuro, (x+0,  y+2, 4, 7))
    pygame.draw.rect(superficie, oscuro, (x+12, y+2, 4, 7))
    # Cabeza
    pygame.draw.ellipse(superficie, color, (x+2, y+2, 12, 10))
    # Hocico
    pygame.draw.ellipse(superficie, claro, (x+5, y+8, 6, 5))
    # Ojos
    pygame.draw.rect(superficie, oscuro, (x+3,  y+5, 2, 2))
    pygame.draw.rect(superficie, oscuro, (x+11, y+5, 2, 2))
    # Nariz
    pygame.draw.rect(superficie, oscuro, (x+7, y+9, 2, 2))

def dibujar_pajaro(superficie, x, y):
    """Dibuja un pajarito pixelado en (x, y)."""
    color  = COLOR_PAJARO
    oscuro = tuple(max(c - 60, 0) for c in color)
    claro  = tuple(min(c + 80, 255) for c in color)
    # Cuerpo
    pygame.draw.ellipse(superficie, color, (x+3, y+5, 10, 8))
    # Cabeza
    pygame.draw.ellipse(superficie, color, (x+9, y+2, 7, 7))
    # Ala
    pygame.draw.ellipse(superficie, oscuro, (x+3, y+6, 7, 5))
    # Pico
    pygame.draw.polygon(superficie, (255, 200, 0), [(x+15, y+5), (x+15, y+7), (x+13, y+6)])
    # Ojo
    pygame.draw.rect(superficie, oscuro, (x+11, y+4, 2, 2))
    pygame.draw.rect(superficie, claro,  (x+11, y+4, 1, 1))
    # Patas
    pygame.draw.line(superficie, oscuro, (x+7, y+13), (x+6,  y+15), 1)
    pygame.draw.line(superficie, oscuro, (x+9, y+13), (x+10, y+15), 1)

def dibujar_cereza(superficie, x, y):
    """Dos cerezas rojas con tallo verde."""
    # Tallos
    pygame.draw.line(superficie, (0, 140, 0), (x+5, y+7), (x+5, y+2), 2)
    pygame.draw.line(superficie, (0, 140, 0), (x+10, y+7), (x+10, y+2), 2)
    pygame.draw.line(superficie, (0, 140, 0), (x+5, y+2), (x+10, y+2), 1)
    # Cerezas
    pygame.draw.circle(superficie, COLOR_CEREZA, (x+5,  y+10), 4)
    pygame.draw.circle(superficie, COLOR_CEREZA, (x+11, y+10), 4)
    # Brillo
    pygame.draw.circle(superficie, (255, 120, 140), (x+4,  y+8), 1)
    pygame.draw.circle(superficie, (255, 120, 140), (x+10, y+8), 1)

def dibujar_pez(superficie, x, y):
    """Pez con cuerpo, cola, ojo y escamas."""
    c = COLOR_PEZ
    osc = tuple(max(v-60, 0) for v in c)
    _ = tuple(min(v+70, 255) for v in c)  # reservado para brillo futuro
    # Cola
    pygame.draw.polygon(superficie, osc, [(x+1, y+4), (x+1, y+12), (x+5, y+8)])
    # Cuerpo
    pygame.draw.ellipse(superficie, c, (x+4, y+4, 11, 9))
    # Aleta dorsal
    pygame.draw.polygon(superficie, osc, [(x+7, y+4), (x+10, y+1), (x+13, y+4)])
    # Escamas
    pygame.draw.arc(superficie, osc, (x+5, y+5, 5, 5), 0, 3.14, 1)
    pygame.draw.arc(superficie, osc, (x+9, y+5, 5, 5), 0, 3.14, 1)
    # Ojo
    pygame.draw.circle(superficie, (255, 255, 255), (x+13, y+7), 2)
    pygame.draw.circle(superficie, (0, 0, 0),       (x+13, y+7), 1)

def dibujar_ladrillos(superficie, oy=36):
    """Dibuja ladrillos 3D en los cuatro bordes del campo."""
    LADRILLO = (165, 55, 30)
    LAD_LUZ  = (215, 110,  70)   # arista iluminada (arriba/izquierda)
    LAD_OSC  = ( 90,  25,  10)   # arista en sombra (abajo/derecha)
    MORTERO  = (210, 190, 170)
    BW = CELDA * 2
    BH = CELDA

    def franja(rx, ry, rw, rh):
        pygame.draw.rect(superficie, MORTERO, (rx, ry, rw, rh))
        for fila in range(rh // BH + 1):
            y0 = ry + fila * BH
            if y0 >= ry + rh:
                break
            h = min(BH - 2, ry + rh - y0 - 1)
            if h <= 0:
                continue
            desp = (fila % 2) * (BW // 2)
            x = rx - desp
            while x < rx + rw:
                x0 = max(x + 1, rx + 1)
                x1 = min(x + BW - 1, rx + rw - 1)
                if x1 > x0:
                    w = x1 - x0
                    # Cara principal
                    pygame.draw.rect(superficie, LADRILLO, (x0, y0 + 1, w, h))
                    # Bisel claro: aristas superior e izquierda
                    pygame.draw.line(superficie, LAD_LUZ, (x0, y0+1), (x0+w-1, y0+1), 2)
                    pygame.draw.line(superficie, LAD_LUZ, (x0, y0+1), (x0, y0+h),     2)
                    # Bisel oscuro: aristas inferior y derecha
                    pygame.draw.line(superficie, LAD_OSC, (x0, y0+h),   (x0+w-1, y0+h),   2)
                    pygame.draw.line(superficie, LAD_OSC, (x0+w-1, y0+2), (x0+w-1, y0+h), 2)
                x += BW

    franja(0,           oy,                ANCHO,       BORDE)
    franja(0,           oy + ALTO - BORDE, ANCHO,       BORDE)
    franja(0,           oy + BORDE,        BORDE,       ALTO - 2*BORDE)
    franja(ANCHO-BORDE, oy + BORDE,        BORDE,       ALTO - 2*BORDE)

def crear_musica(sample_rate=44100):
    """Genera una melodia suave y agradable en bucle."""
    F = {
        'C4':261.63,'D4':293.66,'E4':329.63,'F4':349.23,
        'G4':392.00,'A4':440.00,'B4':493.88,'C5':523.25,
        'D5':587.33,'E5':659.25,
        'C3':130.81,'E3':164.81,'F3':174.61,'G3':196.00,'A3':220.00,
        'R':0
    }
    # Melodia tipo vals/nana suave en Do mayor
    melodia = [
        ('G4',.30),('E4',.20),('R',.05),
        ('F4',.20),('A4',.20),('R',.05),
        ('G4',.40),('R',.10),
        ('E4',.30),('C4',.20),('R',.05),
        ('D4',.20),('F4',.20),('R',.05),
        ('E4',.40),('R',.10),
        ('A4',.30),('G4',.20),('R',.05),
        ('F4',.20),('E4',.20),('R',.05),
        ('D4',.20),('E4',.20),('R',.05),
        ('C4',.50),('R',.20),
        ('G4',.30),('A4',.20),('R',.05),
        ('B4',.20),('A4',.20),('R',.05),
        ('G4',.40),('R',.10),
        ('F4',.30),('G4',.20),('R',.05),
        ('A4',.20),('G4',.20),('R',.05),
        ('E4',.40),('R',.10),
        ('D4',.20),('E4',.20),('R',.05),
        ('F4',.20),('E4',.20),('R',.05),
        ('D4',.20),('C4',.20),('R',.05),
        ('C4',.60),('R',.30),
    ]
    # Bajo arpegiado suave: C-E-G-E patron
    bajo_patron = [
        ('C3',.25),('E3',.25),('G3',.25),('E3',.25),
        ('F3',.25),('A3',.25),('C4',.25),('A3',.25),
        ('G3',.25),('B4',.25),('D4',.25),('B4',.25),
    ]
    # Generar bajo con duracion total igual a melodia
    dur_mel = sum(d for _, d in melodia)
    bajo = []
    t_acum = 0.0
    i = 0
    while t_acum < dur_mel:
        nota = bajo_patron[i % len(bajo_patron)]
        bajo.append(nota)
        t_acum += nota[1]
        i += 1

    def sintetizar(secuencia, volumen):
        partes = []
        for nota, dur in secuencia:
            n = int(sample_rate * dur)
            t = np.linspace(0, dur, n, endpoint=False)
            freq = F[nota]
            if freq == 0:
                wave = np.zeros(n)
            else:
                # Seno puro + segundo armonico suave para calidez
                wave = np.sin(2 * np.pi * freq * t)
                # Envolvente: ataque largo, caida muy larga
                attack  = max(1, int(n * 0.10))
                release = max(1, int(n * 0.50))
                env = np.ones(n)
                env[:attack] = np.linspace(0, 1, attack)
                env[-release:] = np.linspace(1, 0, release)
                wave *= env
            partes.append(wave * volumen)
        return np.concatenate(partes)

    mel  = sintetizar(melodia, 0.18)
    bass = sintetizar(bajo,    0.08)
    length = min(len(mel), len(bass))
    mix = np.clip(mel[:length] + bass[:length], -1, 1)
    audio = (mix * 8000).astype(np.int16)
    stereo = np.column_stack([audio, audio])
    return pygame.sndarray.make_sound(stereo)

def crear_miau():
    """Genera 'miau' con voz TTS en español."""
    import pyttsx3, tempfile, os
    engine = pyttsx3.init()
    engine.setProperty('rate', 120)
    engine.setProperty('volume', 1.0)
    for v in engine.getProperty('voices'):
        if 'es' in v.id.lower() or 'ES' in v.id:
            engine.setProperty('voice', v.id)
            break
    tmp = tempfile.mktemp(suffix='.wav')
    engine.save_to_file('miau', tmp)
    engine.runAndWait()
    sound = pygame.mixer.Sound(tmp)
    os.unlink(tmp)
    return sound

def crear_guau(sample_rate=44100):
    """Genera un 'boing!' sintetizado: tono que sube rapido y cae con vibrato."""
    sr = sample_rate
    dur = 0.55
    n = int(sr * dur)
    t = np.linspace(0, dur, n, endpoint=False)

    # Frecuencia: sube rapido al inicio y luego cae (efecto muelle)
    f = 80 + 600 * np.exp(-t * 9) + 40 * np.sin(2 * np.pi * 18 * t) * np.exp(-t * 5)
    phase = np.cumsum(2 * np.pi * f / sr)
    wave = np.sin(phase) + 0.4 * np.sin(2 * phase) + 0.15 * np.sin(3 * phase)

    # Envolvente: ataque instantaneo, caida lenta
    env = np.exp(-t * 4.5)
    env[:int(0.005 * sr)] = np.linspace(0, 1, int(0.005 * sr))
    wave *= env

    wave /= np.max(np.abs(wave) + 1e-8)
    audio = (wave * 24000).astype(np.int16)
    stereo = np.column_stack([audio, audio])
    return pygame.sndarray.make_sound(stereo)

def crear_pio(sample_rate=44100):
    """Genera un pío sintetizado."""
    duration = 0.2
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    freq = 2000 + 800 * np.sin(2 * np.pi * 8 * t)
    phase = np.cumsum(2 * np.pi * freq / sample_rate)
    wave = np.sin(phase)
    envelope = np.exp(-t * 10)
    wave = (wave * envelope * 28000).astype(np.int16)
    stereo = np.column_stack([wave, wave])
    return pygame.sndarray.make_sound(stereo)

def crear_explosion(sample_rate=44100):
    """BUUUM profundo para la cereza: sub-grave + cuerpo + cola."""
    sr = sample_rate
    rng = np.random.default_rng(11)
    dur = 0.75
    t = np.linspace(0, dur, int(sr * dur), endpoint=False)

    # Sub-grave: onda sinusoidal muy baja que cae (60→25 Hz)
    f_sub = 60 * np.exp(-t * 4) + 25
    sub = np.sin(np.cumsum(2 * np.pi * f_sub / sr)) * np.exp(-t * 3) * 0.9

    # Cuerpo: ruido grave con envolvente percusiva agresiva
    noise = rng.uniform(-1, 1, len(t))
    f_body = 120 * np.exp(-t * 10) + 40
    body_tone = np.sin(np.cumsum(2 * np.pi * f_body / sr))
    body = (noise * 0.5 + body_tone * 0.5) * np.exp(-t * 9) * 0.8

    # Crujido de alta frecuencia en el ataque
    crujido = rng.uniform(-1, 1, len(t)) * np.exp(-t * 40) * 0.4

    wave = sub + body + crujido
    wave /= np.max(np.abs(wave) + 1e-8)
    audio = (wave * 32700).astype(np.int16)
    return pygame.sndarray.make_sound(np.column_stack([audio, audio]))

def crear_agua(sample_rate=44100):
    """Chapoteo de agua para el pez: splash inicial + burbujas descendentes."""
    sr = sample_rate
    rng = np.random.default_rng(5)
    dur = 0.55
    t = np.linspace(0, dur, int(sr * dur), endpoint=False)
    # Splash inicial: ruido filtrado con envolvente percusiva
    noise = rng.normal(0, 1, len(t))
    env_splash = np.exp(-t * 22)
    splash = noise * env_splash * 0.6
    # Burbujas: series de tonos que suben (aire escapando)
    burbujas = np.zeros(len(t))
    for t0, f0 in [(0.05, 800), (0.12, 1100), (0.20, 1400), (0.30, 1000)]:
        mask = t >= t0
        tb = t[mask] - t0
        fb = f0 + 600 * np.exp(-tb * 20)
        phase = np.cumsum(2 * np.pi * fb / sr)
        burbuja = np.sin(phase) * np.exp(-tb * 25) * 0.35
        burbujas[mask] += burbuja
    # Rumor de agua de fondo
    rumor = rng.normal(0, 1, len(t)) * np.exp(-t * 4) * 0.15
    wave = splash + burbujas + rumor
    wave /= np.max(np.abs(wave) + 1e-8)
    audio = (wave * 26000).astype(np.int16)
    return pygame.sndarray.make_sound(np.column_stack([audio, audio]))

def crear_jiji(sample_rate=44100):
    """Genera un 'mmmm' de satisfaccion sintetizado."""
    sr = sample_rate
    dur = 0.45
    n = int(sr * dur)
    t = np.linspace(0, dur, n, endpoint=False)

    # Tono nasal ~220 Hz con vibrato suave (vocal M cerrada)
    f = 220 + 6 * np.sin(2 * np.pi * 5.5 * t)
    phase = np.cumsum(2 * np.pi * f / sr)
    # Armonicos con formante nasal (~250 Hz y ~2500 Hz atenuado)
    wave = np.sin(phase)
    for k in range(2, 8):
        amp = np.exp(-0.5 * ((k * 220 - 250) / 180) ** 2) * 0.6 / k
        wave += amp * np.sin(k * phase)
    # Envolvente: ataque suave, sustain, caida
    env = np.ones(n)
    env[:int(0.05*sr)] = np.linspace(0, 1, int(0.05*sr))
    env[-int(0.15*sr):] = np.linspace(1, 0, int(0.15*sr))
    wave *= env

    wave /= np.max(np.abs(wave) + 1e-8)
    audio = (wave * 20000).astype(np.int16)
    return pygame.sndarray.make_sound(np.column_stack([audio, audio]))

def dibujar_borde_exterior(surf):
    """Dibuja un borde decorativo en el perimetro de la ventana."""
    W, H = surf.get_size()
    pygame.draw.rect(surf, (0,   0,   0),    (0, 0, W, H),       1)  # negro exterior
    pygame.draw.rect(surf, (255, 220,  50),  (1, 1, W-2, H-2),   3)  # amarillo brillante
    pygame.draw.rect(surf, (180, 140,  20),  (4, 4, W-8, H-8),   1)  # amarillo oscuro interior


def posicion_aleatoria(serpiente):
    while True:
        x = random.randrange(BORDE, ANCHO - BORDE, CELDA)
        y = random.randrange(BORDE, ALTO  - BORDE, CELDA)
        if (x, y) not in serpiente:
            return (x, y)


def main():
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()
    musica = crear_musica()
    miau   = crear_miau()
    guau   = crear_guau()
    pio    = crear_pio()
    explosion = crear_explosion()
    agua      = crear_agua()
    jiji      = crear_jiji()
    canal_presa = pygame.mixer.Channel(1)
    pantalla = pygame.display.set_mode((ANCHO, ALTO + 52), pygame.NOFRAME)
    pygame.display.set_caption("Snake")
    reloj = pygame.time.Clock()
    fuente_label  = pygame.font.SysFont("consolas", 11, bold=False)
    fuente_valor  = pygame.font.SysFont("consolas", 26, bold=True)
    fuente_grande = pygame.font.SysFont("consolas", 36, bold=True)

    # --- Pantalla de inicio ---
    fuente_titulo = pygame.font.SysFont("consolas", 42, bold=True)
    fuente_tecla  = pygame.font.SysFont("consolas", 15, bold=False)
    fuente_sub    = pygame.font.SysFont("consolas", 18, bold=True)

    teclas = [
        ("FLECHAS",       "Mover la serpiente"),
        ("ESPACIO",       "Pausar / Reanudar"),
        ("S",             "Activar / Desactivar sonido"),
        ("+  /  -",       "Aumentar / Reducir velocidad"),
        ("R",             "Reiniciar (game over)"),
        ("ESC",           "Salir"),
    ]
    puntos_items = [
        ("Gato",    "+1 pt",   COLORES_GATO[0]),
        ("Perro",   "+2 pts",  COLOR_PERRO),
        ("Pajaro",  "+3 pts",  COLOR_PAJARO),
        ("Cereza",  "+1 pt",   COLOR_CEREZA),
        ("Pez",     "+4 pts",  COLOR_PEZ),
    ]

    esperando = True
    while esperando:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_SPACE:
                    esperando = False
                elif ev.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()

        pantalla.fill((10, 25, 10))

        # Título
        t = fuente_titulo.render("S N A K E", True, (80, 220, 80))
        pantalla.blit(t, (ANCHO // 2 - t.get_width() // 2, 30))
        pygame.draw.line(pantalla, (50, 130, 50), (40, 82), (ANCHO - 40, 82), 1)

        # Controles
        lbl = fuente_sub.render("CONTROLES", True, (100, 200, 100))
        pantalla.blit(lbl, (ANCHO // 2 - lbl.get_width() // 2, 95))
        for i, (key, desc) in enumerate(teclas):
            y = 122 + i * 22
            k_surf = fuente_tecla.render(f"[ {key:<10} ]", True, (180, 255, 180))
            d_surf = fuente_tecla.render(desc, True, (160, 200, 160))
            pantalla.blit(k_surf, (ANCHO // 2 - 190, y))
            pantalla.blit(d_surf, (ANCHO // 2 + 10,  y))

        pygame.draw.line(pantalla, (50, 130, 50), (40, 264), (ANCHO - 40, 264), 1)

        # Puntuaciones
        lbl2 = fuente_sub.render("PUNTUACION POR ANIMAL", True, (100, 200, 100))
        pantalla.blit(lbl2, (ANCHO // 2 - lbl2.get_width() // 2, 276))
        for i, (nombre, pts, color) in enumerate(puntos_items):
            y = 303 + i * 22
            pygame.draw.circle(pantalla, color, (ANCHO // 2 - 120, y + 7), 7)
            n_surf = fuente_tecla.render(nombre, True, color)
            p_surf = fuente_tecla.render(pts, True, (200, 255, 200))
            pantalla.blit(n_surf, (ANCHO // 2 - 105, y))
            pantalla.blit(p_surf, (ANCHO // 2 + 60,  y))

        pygame.draw.line(pantalla, (50, 130, 50), (40, 418), (ANCHO - 40, 418), 1)

        # Pulsa espacio
        pulsa = fuente_sub.render("Pulsa ESPACIO para empezar", True, (80, 220, 80))
        pantalla.blit(pulsa, (ANCHO // 2 - pulsa.get_width() // 2, 435))

        # Copyright
        copy = fuente_label.render("(c) peperono", True, (60, 100, 60))
        pantalla.blit(copy, (ANCHO // 2 - copy.get_width() // 2, 590))

        dibujar_borde_exterior(pantalla)
        pygame.display.flip()
        reloj.tick(30)

    while True:  # bucle exterior: reinicia la partida
        serpiente = [(240, 240), (224, 240), (208, 240)]
        serpiente_colores = [OSCURO, OSCURO, OSCURO]
        direccion = (CELDA, 0)
        siguiente_dir = direccion
        comidas = [posicion_aleatoria(serpiente) for _ in range(2)]
        comidas_colores = [random.choice(COLORES_GATO) for _ in range(2)]
        perros  = [posicion_aleatoria(serpiente) for _ in range(2)]
        pajaros = [posicion_aleatoria(serpiente) for _ in range(2)]
        cerezas = [posicion_aleatoria(serpiente) for _ in range(2)]
        peces   = [posicion_aleatoria(serpiente) for _ in range(2)]
        puntuacion = 0
        game_over = False
        pausado = False
        fps = FPS
        sonido_activo = True
        musica.play(-1)

        while True:  # bucle interior: una partida
            reiniciar_juego = False

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        if game_over:
                            pygame.quit()
                            sys.exit()
                        else:
                            game_over = True
                            musica.stop()
                    if game_over:
                        if evento.key == pygame.K_r:
                            reiniciar_juego = True
                    else:
                        if evento.key == pygame.K_SPACE:
                            pausado = not pausado
                            if pausado:
                                musica.stop()
                            else:
                                if sonido_activo:
                                    musica.play(-1)
                        elif evento.key == pygame.K_s:
                            sonido_activo = not sonido_activo
                            if sonido_activo and not pausado:
                                musica.play(-1)
                            else:
                                musica.stop()
                        elif evento.key == pygame.K_UP and direccion != (0, CELDA):
                            siguiente_dir = (0, -CELDA)
                        elif evento.key == pygame.K_DOWN and direccion != (0, -CELDA):
                            siguiente_dir = (0, CELDA)
                        elif evento.key == pygame.K_LEFT and direccion != (CELDA, 0):
                            siguiente_dir = (-CELDA, 0)
                        elif evento.key == pygame.K_RIGHT and direccion != (-CELDA, 0):
                            siguiente_dir = (CELDA, 0)
                        elif evento.key in (pygame.K_PLUS, pygame.K_EQUALS, pygame.K_KP_PLUS):
                            fps = min(fps + 2, 30)
                        elif evento.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                            fps = max(fps - 2, 2)

            if reiniciar_juego:
                musica.stop()
                break  # sale del bucle interior → el exterior reinicia todo

            if not game_over and not pausado:
                direccion = siguiente_dir
                cabeza = (serpiente[0][0] + direccion[0], serpiente[0][1] + direccion[1])

                if cabeza[0] < BORDE or cabeza[0] >= ANCHO - BORDE or cabeza[1] < BORDE or cabeza[1] >= ALTO - BORDE:
                    game_over = True
                    musica.stop()
                elif cabeza in serpiente:
                    game_over = True
                    musica.stop()
                else:
                    serpiente.insert(0, cabeza)
                    if cabeza in comidas:
                        idx = comidas.index(cabeza)
                        serpiente_colores.insert(0, comidas_colores[idx])
                        puntuacion += 1
                        comidas[idx] = posicion_aleatoria(serpiente)
                        comidas_colores[idx] = random.choice(COLORES_GATO)
                        if sonido_activo: canal_presa.play(miau); canal_presa.queue(jiji)
                    elif cabeza in perros:
                        idx = perros.index(cabeza)
                        serpiente_colores.insert(0, COLOR_PERRO)
                        puntuacion += 2
                        perros[idx] = posicion_aleatoria(serpiente)
                        if sonido_activo: canal_presa.play(guau); canal_presa.queue(jiji)
                    elif cabeza in pajaros:
                        idx = pajaros.index(cabeza)
                        serpiente_colores.insert(0, COLOR_PAJARO)
                        puntuacion += 3
                        pajaros[idx] = posicion_aleatoria(serpiente)
                        if sonido_activo: canal_presa.play(pio); canal_presa.queue(jiji)
                    elif cabeza in cerezas:
                        idx = cerezas.index(cabeza)
                        serpiente_colores.insert(0, COLOR_CEREZA)
                        puntuacion += 1
                        cerezas[idx] = posicion_aleatoria(serpiente)
                        if sonido_activo: canal_presa.play(explosion); canal_presa.queue(jiji)
                    elif cabeza in peces:
                        idx = peces.index(cabeza)
                        serpiente_colores.insert(0, COLOR_PEZ)
                        puntuacion += 4
                        peces[idx] = posicion_aleatoria(serpiente)
                        if sonido_activo: canal_presa.play(agua); canal_presa.queue(jiji)
                    else:
                        serpiente_colores.insert(0, serpiente_colores[0])
                        serpiente.pop()
                        serpiente_colores.pop()

            # --- Dibujar ---
            # Barra superior
            pantalla.fill((15, 35, 15), (0, 0, ANCHO, 52))
            pygame.draw.line(pantalla, (60, 100, 60), (0, 51), (ANCHO, 51), 1)

            # Bloque PUNTUACION (izquierda)
            dibujar_panel_3d(pantalla, 8, 4, 160, 44, (70, 120, 70))
            lbl_p = fuente_label.render("PUNTUACION", True, (120, 180, 120))
            val_p = fuente_valor.render(str(puntuacion), True, (255, 220, 50))
            pantalla.blit(lbl_p, (88 - lbl_p.get_width() // 2, 8))
            pantalla.blit(val_p, (88 - val_p.get_width() // 2, 21))

            # Icono sonido (centro)
            icono_txt = "[S] SFX: ON " if sonido_activo else "[S] SFX: OFF"
            icono_color = (150, 255, 150) if sonido_activo else (180, 80, 80)
            icono_surf = fuente_label.render(icono_txt, True, icono_color)
            pantalla.blit(icono_surf, (ANCHO // 2 - icono_surf.get_width() // 2, 20))

            # Separador central
            pygame.draw.line(pantalla, (50, 90, 50), (ANCHO//2, 8), (ANCHO//2, 44), 1)

            # Bloque VELOCIDAD (derecha)
            rx = ANCHO - 168
            dibujar_panel_3d(pantalla, rx, 4, 160, 44, (70, 120, 70))
            lbl_v = fuente_label.render("VELOCIDAD  [+/-]", True, (120, 180, 120))
            val_v = fuente_valor.render(f"{fps}", True, (255, 220, 50))
            pantalla.blit(lbl_v, (rx + 80 - lbl_v.get_width() // 2, 8))
            pantalla.blit(val_v, (rx + 80 - val_v.get_width() // 2, 21))

            pantalla.fill(FONDO, (0, 52, ANCHO, ALTO))
            dibujar_ladrillos(pantalla, oy=52)

            ELEV = 2  # pixeles de elevacion 3D para las presas
            for (fx, fy), fc in zip(comidas, comidas_colores):
                dibujar_sombra(pantalla, fx, fy + 52)
                dibujar_gato(pantalla, fx, fy + 52 - ELEV, fc)
            for px, py in perros:
                dibujar_sombra(pantalla, px, py + 52)
                dibujar_perro(pantalla, px, py + 52 - ELEV)
            for bx, by in pajaros:
                dibujar_sombra(pantalla, bx, by + 52)
                dibujar_pajaro(pantalla, bx, by + 52 - ELEV)
            for cx, cy in cerezas:
                dibujar_sombra(pantalla, cx, cy + 52)
                dibujar_cereza(pantalla, cx, cy + 52 - ELEV)
            for fx, fy in peces:
                dibujar_sombra(pantalla, fx, fy + 52)
                dibujar_pez(pantalla, fx, fy + 52 - ELEV)

            for i, ((sx, sy), color) in enumerate(zip(serpiente, serpiente_colores)):
                dibujar_caja_3d(pantalla, sx, sy + 52, color)
                if i == 0:  # ojos en la cabeza segun la direccion
                    dx, dy = direccion
                    base_y = sy + 52
                    if dx == CELDA:    # derecha
                        o1, o2 = (sx+12, base_y+4), (sx+12, base_y+11)
                    elif dx == -CELDA: # izquierda
                        o1, o2 = (sx+3,  base_y+4), (sx+3,  base_y+11)
                    elif dy == -CELDA: # arriba
                        o1, o2 = (sx+4,  base_y+3), (sx+11, base_y+3)
                    else:              # abajo
                        o1, o2 = (sx+4,  base_y+12),(sx+11, base_y+12)
                    pygame.draw.circle(pantalla, (255,255,255), o1, 3)
                    pygame.draw.circle(pantalla, (255,255,255), o2, 3)
                    pygame.draw.circle(pantalla, (0,0,0),       o1, 1)
                    pygame.draw.circle(pantalla, (0,0,0),       o2, 1)

            if pausado:
                t_pausa = fuente_grande.render("PAUSA", True, OSCURO)
                cx, cy = ANCHO // 2, 52 + ALTO // 2
                pantalla.blit(t_pausa, (cx - t_pausa.get_width() // 2, cy - 18))

            if game_over:
                t1 = fuente_grande.render("GAME OVER", True, (220, 60, 60))
                t2 = fuente_valor.render(f"Puntuacion: {puntuacion}", True, (220, 220, 220))
                t3 = fuente_label.render("R reiniciar   ESC salir", True, (180, 180, 180))
                cx, cy = ANCHO // 2, 52 + ALTO // 2
                pantalla.blit(t1, (cx - t1.get_width() // 2, cy - 50))
                pantalla.blit(t2, (cx - t2.get_width() // 2, cy + 10))
                pantalla.blit(t3, (cx - t3.get_width() // 2, cy + 40))

            dibujar_borde_exterior(pantalla)
            pygame.display.flip()
            reloj.tick(fps)

if __name__ == "__main__":
    main()
