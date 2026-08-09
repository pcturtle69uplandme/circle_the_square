import math, wave, struct, os, random

out_dir = r"C:\kontitemp\ai\circle_the_square\audio-refs"
os.makedirs(out_dir, exist_ok=True)

def write_wav(filename, samples, sample_rate=44100):
    filepath = os.path.join(out_dir, filename)
    with wave.open(filepath, 'w') as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(sample_rate)
        for s in samples:
            val = int(max(-32768, min(32767, s * 32767)))
            f.writeframes(struct.pack('<h', val))
    print(f"Generated SFX: {filepath} ({os.path.getsize(filepath)} bytes)")

sr = 44100

# SFX-01: Chair Creak (Swivel metal creak)
c01 = []
for i in range(int(sr * 0.5)):
    t = i / sr
    env = math.exp(-t * 8.0)
    creak = math.sin(2 * math.pi * (300 + 150 * math.sin(2 * math.pi * 15 * t)) * t)
    c01.append(creak * 0.5 * env)
write_wav("sfx_01_chair_creak.wav", c01)

# SFX-02: Tablet Tap & Swipe
c02 = []
for i in range(int(sr * 0.3)):
    t = i / sr
    env = math.exp(-t * 25.0)
    tap = math.sin(2 * math.pi * 1200 * t) + random.uniform(-0.2, 0.2)
    c02.append(tap * 0.6 * env)
write_wav("sfx_02_tablet_tap.wav", c02)

# SFX-03: Music Dead Drop Silence
c03 = [0.0] * int(sr * 0.5)
write_wav("sfx_03_music_drop.wav", c03)

# SFX-04: Door Hydraulic Click
c04 = []
for i in range(int(sr * 0.2)):
    t = i / sr
    env = math.exp(-t * 30.0)
    click = math.sin(2 * math.pi * 900 * t) + (1.0 if t < 0.01 else 0.0)
    c04.append(click * 0.7 * env)
write_wav("sfx_04_door_click.wav", c04)

# SFX-05: Shirt Fabric Rustle & Breath
c05 = []
for i in range(int(sr * 0.6)):
    t = i / sr
    env = math.sin(math.pi * t / 0.6)
    rustle = random.uniform(-0.5, 0.5) * (1.0 + 0.5 * math.sin(2 * math.pi * 8 * t))
    c05.append(rustle * 0.4 * env)
write_wav("sfx_05_shirt_rustle.wav", c05)

# SFX-06: Door Open Burst
c06 = []
for i in range(int(sr * 0.4)):
    t = i / sr
    env = math.exp(-t * 10.0)
    burst = random.uniform(-0.6, 0.6) + math.sin(2 * math.pi * 400 * t)
    c06.append(burst * 0.5 * env)
write_wav("sfx_06_door_burst.wav", c06)

# SFX-07: Brass Sting (Comedic baritone note)
c07 = []
for i in range(int(sr * 0.8)):
    t = i / sr
    env = (1.0 - math.exp(-t * 20.0)) * math.exp(-t * 2.5)
    f = 110.0
    brass = math.sin(2 * math.pi * f * t) + 0.5 * math.sin(2 * math.pi * f * 2 * t)
    c07.append(brass * 0.4 * env)
write_wav("sfx_07_brass_sting.wav", c07)

# SFX-08: Blinds Snap Rattle
c08 = []
for i in range(int(sr * 0.4)):
    t = i / sr
    env = math.exp(-t * 15.0)
    noise = random.uniform(-0.8, 0.8)
    clack = math.sin(2 * math.pi * 800 * t) * math.exp(-t * 25.0)
    c08.append((noise * 0.5 + clack * 0.5) * env)
write_wav("sfx_08_blinds_snap.wav", c08)

# SFX-09: Door Lock Clack
c09 = []
for i in range(int(sr * 0.3)):
    t = i / sr
    env1 = math.exp(-t * 40.0)
    env2 = math.exp(-(t - 0.08) * 40.0) if t > 0.08 else 0.0
    k1 = math.sin(2 * math.pi * 1100 * t) * env1
    k2 = math.sin(2 * math.pi * 900 * t) * env2
    c09.append((k1 + k2) * 0.8)
write_wav("sfx_09_door_lock.wav", c09)

# SFX-10: Double Handclap
c10 = []
for i in range(int(sr * 0.5)):
    t = i / sr
    env1 = math.exp(-t * 35.0)
    env2 = math.exp(-(t - 0.15) * 35.0) if t > 0.15 else 0.0
    n1 = random.uniform(-0.8, 0.8) * env1
    n2 = random.uniform(-0.8, 0.8) * env2
    c10.append((n1 + n2) * 0.7)
write_wav("sfx_10_handclap.wav", c10)

# SFX-11: Sniggering Murmur Ambience
c11 = []
for i in range(int(sr * 1.0)):
    t = i / sr
    env = math.sin(math.pi * t / 1.0)
    m = random.uniform(-0.3, 0.3) * math.sin(2 * math.pi * 5 * t)
    c11.append(m * env)
write_wav("sfx_11_sniggering.wav", c11)

# SFX-12: Stress Ball Squeeze Squeak
c12 = []
for i in range(int(sr * 0.4)):
    t = i / sr
    env = math.sin(math.pi * t / 0.4)
    squeak = math.sin(2 * math.pi * (1500 + 400 * t) * t)
    c12.append(squeak * 0.3 * env)
write_wav("sfx_12_stressball.wav", c12)

# SFX-13: Crowd Groan
c13 = []
for i in range(int(sr * 1.2)):
    t = i / sr
    env = math.sin(math.pi * t / 1.2)
    groan = math.sin(2 * math.pi * (140 - 20 * t) * t) + random.uniform(-0.2, 0.2)
    c13.append(groan * 0.4 * env)
write_wav("sfx_13_groan.wav", c13)

# SFX-14: Task Chairs Scuffle
c14 = []
for i in range(int(sr * 0.8)):
    t = i / sr
    env = math.exp(-t * 4.0)
    scuffle = random.uniform(-0.6, 0.6) * math.sin(2 * math.pi * 50 * t)
    c14.append(scuffle * 0.5 * env)
write_wav("sfx_14_chairs_scuffle.wav", c14)

# SFX-15: Pastry Tray Scrape
c15 = []
for i in range(int(sr * 0.5)):
    t = i / sr
    env = math.exp(-t * 6.0)
    scrape = random.uniform(-0.7, 0.7) * math.sin(2 * math.pi * 1800 * t)
    c15.append(scrape * 0.4 * env)
write_wav("sfx_15_tray_scrape.wav", c15)

# SFX-16: Plate Shatter Crash
c16 = []
for i in range(int(sr * 1.0)):
    t = i / sr
    env = math.exp(-t * 5.0)
    noise = random.uniform(-0.9, 0.9)
    ring = math.sin(2 * math.pi * 2400 * t) * math.exp(-t * 12.0)
    c16.append((noise * 0.7 + ring * 0.3) * env)
write_wav("sfx_16_plate_crash.wav", c16)

# SFX-17: Total Mute Silence
c17 = [0.0] * int(sr * 0.5)
write_wav("sfx_17_room_silence.wav", c17)

# SFX-18: Glass Explosion Smash
c18 = []
for i in range(int(sr * 1.5)):
    t = i / sr
    env = math.exp(-t * 3.5)
    glass = random.uniform(-1.0, 1.0) * (1.0 + math.sin(2 * math.pi * 3200 * t))
    c18.append(glass * 0.7 * env)
write_wav("sfx_18_glass_smash.wav", c18)

# SFX-19: Taser Arc Zap
c19 = []
for i in range(int(sr * 0.8)):
    t = i / sr
    env = math.exp(-t * 3.0)
    buzz = 1.0 if (t * 120) % 1 > 0.5 else -1.0
    spark = random.uniform(-1, 1) if (i % 8 < 3) else 0
    c19.append((buzz * 0.4 + spark * 0.6) * env * 0.8)
write_wav("sfx_19_taser_zap.wav", c19)

# SFX-20: Body Thud
c20 = []
for i in range(int(sr * 0.6)):
    t = i / sr
    env = math.exp(-t * 8.0)
    thud = math.sin(2 * math.pi * (60 - 20 * t) * t) * 0.8 + random.uniform(-0.3, 0.3) * math.exp(-t * 15.0)
    c20.append(thud * env)
write_wav("sfx_20_body_thud.wav", c20)

# SFX-21: Holster Clip
c21 = []
for i in range(int(sr * 0.3)):
    t = i / sr
    env = math.exp(-t * 25.0)
    clip = math.sin(2 * math.pi * 1400 * t) + random.uniform(-0.4, 0.4)
    c21.append(clip * 0.6 * env)
write_wav("sfx_21_holster_clip.wav", c21)

# SFX-22: Police Siren Fade
c22 = []
for i in range(int(sr * 2.0)):
    t = i / sr
    env = (1.0 - math.exp(-t * 2.0))
    siren = math.sin(2 * math.pi * (700 + 300 * math.sin(2 * math.pi * 1.5 * t)) * t)
    c22.append(siren * 0.4 * env)
write_wav("sfx_22_siren_fade.wav", c22)
