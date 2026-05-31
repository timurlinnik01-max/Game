import pygame
from player import Player
from levels import Level1
from levels import Level2
from levels import Level3
from levels import Level4

import math
 
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('music.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)
current_music = 'music.mp3'
clock = pygame.time.Clock()
 
# scaling and assets
scale = 0.8
player_scale = 0.15
saw_scale = 3
level_id = 1
spawn_id = 1
saw_angle = 0
game_started = False
show_leaderboard = False
start_time = 0
elapsed_time = 0.0
finish_time = None
death_count = 0
flash_timer = 0.0
flash_duration = 1.2
last_level_id = 1
victory_sound_played = False
name_input = ""
leaderboard_file = 'leaderboard.txt'
leaderboard_records = []

screen = pygame.display.set_mode((1920, 1080))
background_image = pygame.image.load('background.png').convert()
background_image = pygame.transform.scale(background_image, screen.get_size())
designer_background_image = pygame.image.load('designer.png').convert()
designer_background_image = pygame.transform.scale(designer_background_image, screen.get_size())
exit_image = pygame.image.load('pixel_door.png').convert_alpha()

font = pygame.font.SysFont('couriernew', 48, bold=True)
button_font = pygame.font.SysFont('couriernew', 28, bold=True)
button_width = 320
button_height = 90
start_button_rect = pygame.Rect((screen.get_width() - button_width) // 2, 420, button_width, button_height)
exit_button_rect = pygame.Rect((screen.get_width() - button_width) // 2, 540, button_width, button_height)
 

wall_tile_raw = pygame.image.load('wall.png').convert_alpha()
platform_tile_raw = pygame.image.load('platform.png').convert_alpha()
 

WALL_TILE_W = wall_tile_raw.get_width()
WALL_TILE_H = wall_tile_raw.get_height()
PLATFORM_TILE_W = platform_tile_raw.get_width()
PLATFORM_TILE_H = platform_tile_raw.get_height()
 
 
def draw_tiled(surface, tile, rect):
   
    tw = tile.get_width()
    th = tile.get_height()
    x0, y0, rw, rh = rect.x, rect.y, rect.width, rect.height
    for row in range(0, rh, th):
        for col in range(0, rw, tw):
            
            blit_w = min(tw, rw - col)
            blit_h = min(th, rh - row)
            area = pygame.Rect(0, 0, blit_w, blit_h)
            surface.blit(tile, (x0 + col, y0 + row), area)
 
 
def draw_level_blocks(surface, level_blocks, wall_tile, platform_tile, block_colors):
    for block_type, block_rect in level_blocks:
        if block_type == "wall":
            draw_tiled(surface, wall_tile, block_rect)
        else:
     
            draw_tiled(surface, platform_tile, block_rect)


def load_leaderboard(path=leaderboard_file):
    records = []
    try:
        with open(path, 'r', encoding='utf-8') as fh:
            for line in fh:
                parts = line.strip().split('|')
                if len(parts) == 3:
                    name, time_str, deaths_str = parts
                    try:
                        records.append((name, float(time_str), int(deaths_str)))
                    except ValueError:
                        continue
                elif len(parts) == 2:
                  
                    name, time_str = parts
                    try:
                        records.append((name, float(time_str), 0))
                    except ValueError:
                        continue
    except FileNotFoundError:
        pass
    return sorted(records, key=lambda item: item[1])[:10]


def save_leaderboard(records, path=leaderboard_file):
    with open(path, 'w', encoding='utf-8') as fh:
        for name, time_value, deaths in records[:10]:
            fh.write(f"{name}|{time_value:.2f}|{deaths}\n")


def format_time(seconds):
    return f"{seconds:.2f}s"

def render_text_with_outline(text, font, color, outline_color=(0, 0, 0), outline_width=2):
    base = font.render(text, False, color)
    outline_surf = pygame.Surface((base.get_width() + outline_width * 2, base.get_height() + outline_width * 2), pygame.SRCALPHA)
    for dx in range(-outline_width, outline_width + 1):
        for dy in range(-outline_width, outline_width + 1):
            if dx == 0 and dy == 0:
                continue
            outline_surf.blit(font.render(text, False, outline_color), (dx + outline_width, dy + outline_width))
    outline_surf.blit(base, (outline_width, outline_width))
    return outline_surf

def draw_button(surface, rect, text, font, bg_color=(30, 30, 30), text_color=(255, 255, 255),):
    pygame.draw.rect(surface, bg_color, rect, border_radius=12)
    pygame.draw.rect(surface, (255, 255, 255), rect, 3, border_radius=12)
    label = font.render(text, False, text_color)
    surface.blit(label, label.get_rect(center=rect.center))
 
leaderboard_records = load_leaderboard()

blood_splashes = []
BLOOD_LIFETIME = 0.45
BLOOD_RADIUS = 16


def spawn_blood_splash(center):
    blood_splashes.append({
        "pos": center,
        "time": 0.0,
        "lifetime": BLOOD_LIFETIME,
        "radius": BLOOD_RADIUS,
    })


def draw_blood_splashes(surface, splashes, dt):
    for splash in splashes[:]:
        splash["time"] += dt
        progress = splash["time"] / splash["lifetime"]
        if progress >= 1.0:
            splashes.remove(splash)
            continue

        alpha = int(220 * (1.0 - progress))
        radius = int(splash["radius"] * (1.0 + progress * 0.9))
        splash_size = radius * 6
        blood_surface = pygame.Surface((splash_size, splash_size), pygame.SRCALPHA)
        center = (splash_size // 2, splash_size // 2)

        pygame.draw.circle(blood_surface, (140, 0, 0, alpha), center, int(radius * 0.9))
        pygame.draw.circle(blood_surface, (240, 40, 40, alpha), center, int(radius * 0.55))

        burst_count = 0
        for i in range(burst_count):
            angle = math.radians(i * (360 / burst_count) + 15)
            length = int(radius * (1.8 + progress * 0.9))
            end_x = int(center[0] + math.cos(angle) * length)
            end_y = int(center[1] + math.sin(angle) * length)
            thickness = max(1, int(radius * 0.18 * (1.0 - progress) + 1))
            pygame.draw.line(
                blood_surface,
                (180, 0, 0, alpha),
                center,
                (end_x, end_y),
                thickness,
            )
            tip_radius = max(1, int(radius * 0.22 * (1.0 - progress) + 1))
            pygame.draw.circle(blood_surface, (255, 60, 60, alpha), (end_x, end_y), tip_radius)

        for i in range(8):
            angle = math.radians(i * 45)
            offset = radius * (1.2 + progress * 0.8)
            drop_x = int(center[0] + math.cos(angle) * offset)
            drop_y = int(center[1] + math.sin(angle) * offset)
            drop_radius = max(1, int(radius * 0.28 * (1.0 - progress) + 1))
            pygame.draw.circle(blood_surface, (220, 40, 40, alpha), (drop_x, drop_y), drop_radius)

        for angle in range(0, 360, 60):
            rad = math.radians(angle)
            inner_x = int(center[0] + math.cos(rad) * radius * 0.8)
            inner_y = int(center[1] + math.sin(rad) * radius * 0.8)
            pygame.draw.circle(blood_surface, (180, 0, 0, alpha), (inner_x, inner_y), max(1, int(radius * 0.14)))

        surface.blit(blood_surface, (splash["pos"][0] - splash_size // 2, splash["pos"][1] - splash_size // 2))



if level_id == 1:
    level = Level1(saw_scale, scale)
    saw_image = pygame.transform.scale(level.saw_image_raw, (int(40 * saw_scale), int(40 * saw_scale)))
 
player = Player('player (2).png', 100, 900, player_scale)
 

wall_tile = wall_tile_raw
platform_tile = platform_tile_raw
 
speed = 8
wall_run_slide_speed = 2
wall_run_jump_multiplier = 1.3
gravity = 0.5
jump_speed = 14
 
running = True
while running:
    clock.tick(60)
    dt = clock.get_time() / 1000.0
    if level_id == 4 and last_level_id == 3:
        flash_timer = flash_duration
        last_level_id = level_id
    if flash_timer > 0:
        flash_timer -= dt
    if level_id == 4 and not (show_leaderboard):
        screen.blit(designer_background_image, (0, 0))
    else:
        screen.blit(background_image, (0, 0))
    if show_leaderboard:
        title_text = render_text_with_outline("All levels complete!", font, (255, 255, 255))
        title_rect = title_text.get_rect(center=(screen.get_width() // 2, 140))
        screen.blit(title_text, title_rect)

        if finish_time is not None:
            time_text = render_text_with_outline(f"Time: {format_time(finish_time)}", button_font, (255, 255, 255))
            screen.blit(time_text, time_text.get_rect(center=(screen.get_width() // 2, 210)))
            deaths_display_text = render_text_with_outline(f"Deaths: {death_count}", button_font, (255, 100, 100))
            screen.blit(deaths_display_text, deaths_display_text.get_rect(center=(screen.get_width() // 2, 260)))

        prompt_text = render_text_with_outline("Enter name:", button_font, (255, 255, 255))
        prompt_rect = prompt_text.get_rect(center=(screen.get_width() // 2, 280))
        screen.blit(prompt_text, prompt_rect)

        name_text = render_text_with_outline(name_input + ("_" if pygame.time.get_ticks() % 1000 < 500 else ""), button_font, (255, 255, 255))
        name_rect = name_text.get_rect(center=(screen.get_width() // 2, 340))
        screen.blit(name_text, name_rect)

        leaderboard_title = render_text_with_outline("Leaderboard", button_font, (255, 255, 255))
        leaderboard_rect = leaderboard_title.get_rect(center=(screen.get_width() // 2, 420))
        screen.blit(leaderboard_title, leaderboard_rect)

        for index, (name, time_value, deaths) in enumerate(leaderboard_records[:5], start=1):
            record_text = render_text_with_outline(f"{index}. {name} - {format_time(time_value)} (Deaths: {deaths})", button_font, (220, 220, 220))
            screen.blit(record_text, record_text.get_rect(center=(screen.get_width() // 2, 460 + index * 36)))

        reminder_text = button_font.render("Press Enter to save, Esc for menu", False, (180, 180, 180))
        reminder_rect = reminder_text.get_rect(center=(screen.get_width() // 2, 660))
        screen.blit(reminder_text, reminder_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    name_input = name_input[:-1]
                elif event.key == pygame.K_RETURN:
                    if name_input.strip():
                        leaderboard_records.append((name_input.strip(), finish_time or elapsed_time, death_count))
                        leaderboard_records = sorted(leaderboard_records, key=lambda item: item[1])[:10]
                        save_leaderboard(leaderboard_records)
                        show_leaderboard = False
                        game_started = False
                        level_id = 1
                        spawn_id = 1
                        last_level_id = 1
                        victory_sound_played = False
                        player.respawn()
                        name_input = ""
                        finish_time = None
                        death_count = 0
                elif event.key == pygame.K_ESCAPE:
                    show_leaderboard = False
                    game_started = False
                    level_id = 1
                    spawn_id = 1
                    last_level_id = 1
                    victory_sound_played = False
                    player.respawn()
                    finish_time = None
                elif len(event.unicode) == 1 and event.unicode.isprintable() and len(name_input) < 12:
                    name_input += event.unicode

        pygame.display.flip()
        continue
    elif not game_started:
        title_text = font.render("Pixel runner", False, (255, 255, 255))
        title_rect = title_text.get_rect(center=(screen.get_width() // 2, 220))
        screen.blit(title_text, title_rect)

        draw_button(screen, start_button_rect, "Start Game", button_font)
        draw_button(screen, exit_button_rect, "Exit", button_font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if start_button_rect.collidepoint(event.pos):
                    game_started = True
                    show_leaderboard = False
                    level_id = 1
                    spawn_id = 1
                    saw_angle = 0
                    last_level_id = 1
                    victory_sound_played = False
                    start_time = pygame.time.get_ticks()
                    elapsed_time = 0.0
                    finish_time = None
                    death_count = 0
                    name_input = ""
                    if current_music != 'music.mp3':
                        pygame.mixer.music.load('music.mp3')
                        pygame.mixer.music.set_volume(0.5)
                        pygame.mixer.music.play(-1)
                        current_music = 'music.mp3'
                    level = Level1(saw_scale, scale)
                    saw_image = pygame.transform.scale(level.saw_image_raw, (int(40 * saw_scale), int(40 * saw_scale)))
                    player.respawn()
                elif exit_button_rect.collidepoint(event.pos):
                    running = False

        pygame.display.flip()
        continue

    if level_id == 1 or level_id == 2:
        finish_rect = pygame.Rect(int(1800), int(280), int(100), int(250))
        exit_image_scaled = pygame.transform.scale(exit_image, (finish_rect.width, finish_rect.height))
        screen.blit(exit_image_scaled, finish_rect.topleft)
 
    if level_id == 2:
        level = Level2(saw_scale, scale)
        saw_image = pygame.transform.scale(level.saw_image_raw, (int(40 * saw_scale), int(40 * saw_scale)))
 
    if level_id == 3:
        level = Level3(saw_scale, scale)
        finish_rect = pygame.Rect(int(860), int(40), int(100), int(206))
        exit_image_scaled = pygame.transform.scale(exit_image, (finish_rect.width, finish_rect.height))
        screen.blit(exit_image_scaled, finish_rect.topleft)
        saw_image = pygame.transform.scale(level.saw_image_raw, (int(40 * saw_scale), int(40 * saw_scale)))

    if level_id == 4:
        if current_music != 'last_level.mp3':
            pygame.mixer.music.load('last_level.mp3')
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
            current_music = 'last_level.mp3'
        level = Level4(saw_scale, scale)
        finish_rect = pygame.Rect(int(1780), int(120), int(100), int(250))
        exit_image_scaled = pygame.transform.scale(exit_image, (finish_rect.width, finish_rect.height))
        screen.blit(exit_image_scaled, finish_rect.topleft)
        saw_image = pygame.transform.scale(level.saw_image_raw, (int(40 * saw_scale), int(40 * saw_scale)))
 
    if game_started:
        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000.0
        timer_text = button_font.render(format_time(elapsed_time), False, (255, 255, 255))
        timer_rect = timer_text.get_rect(topright=(screen.get_width() - 24, 24))
        screen.blit(timer_text, timer_rect)
        
        deaths_text = button_font.render(f"Deaths: {death_count}", False, (255, 100, 100))
        deaths_rect = deaths_text.get_rect(topright=(screen.get_width() - 24, 70))
        screen.blit(deaths_text, deaths_rect)
 
    saw_angle = (saw_angle + 4) % 360
 
    if level_id == 1:
        if player.rect().colliderect(finish_rect):
            player.respawn()
            level_id += 1
        if spawn_id == 1:
            player.respawn()
            spawn_id = 2
        for block_type, block_rect in level.level_blocks:
            if level_id == 2:
                break
        draw_level_blocks(screen, level.level_blocks, wall_tile, platform_tile, level.block_colors)
        for saw_rect in level.saw_rects:
            if level_id == 2:
                break
            rotated_saw = pygame.transform.rotate(saw_image, saw_angle)
            rotated_rect = rotated_saw.get_rect(center=saw_rect.center)
            screen.blit(rotated_saw, rotated_rect.topleft)
 
    if level_id == 2:
        if player.rect().colliderect(finish_rect):
            player.respawn()
            level_id += 1
        if spawn_id == 2:
            player.respawn()
            spawn_id = 3
        draw_level_blocks(screen, level.level_blocks, wall_tile, platform_tile, level.block_colors)
        for saw_rect in level.saw_rects:
            if level_id == 3:
                break
            rotated_saw = pygame.transform.rotate(saw_image, saw_angle)
            rotated_rect = rotated_saw.get_rect(center=saw_rect.center)
            screen.blit(rotated_saw, rotated_rect.topleft)
 
    if level_id == 3:
        if player.rect().colliderect(finish_rect):
            player.respawn()
            level_id += 1
        if spawn_id == 3:
            player.respawn()
            spawn_id = 4
        draw_level_blocks(screen, level.level_blocks, wall_tile, platform_tile, level.block_colors)
        for saw_rect in level.saw_rects:
            if level_id == 4:
                break
            rotated_saw = pygame.transform.rotate(saw_image, saw_angle)
            rotated_rect = rotated_saw.get_rect(center=saw_rect.center)
            screen.blit(rotated_saw, rotated_rect.topleft)

    if level_id == 4:
        if player.rect().colliderect(finish_rect):
            show_leaderboard = True
            game_started = False
            finish_time = elapsed_time
            if not victory_sound_played:
                pygame.mixer.Sound('victory.mp3').play()
                victory_sound_played = True
        if spawn_id == 4:
            player.respawn()
            spawn_id = 5
        draw_level_blocks(screen, level.level_blocks, wall_tile, platform_tile, level.block_colors)
        for saw_rect in level.saw_rects:
            rotated_saw = pygame.transform.rotate(saw_image, saw_angle)
            rotated_rect = rotated_saw.get_rect(center=saw_rect.center)
            screen.blit(rotated_saw, rotated_rect.topleft)
 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
 
    keys = pygame.key.get_pressed()
 
    player.update(keys, level.level_blocks, level.saw_rects, speed, gravity, jump_speed, wall_run_slide_speed, wall_run_jump_multiplier)
    if player.hit_by_saw and player.hit_position is not None:
        death_count += 1
        spawn_blood_splash(player.hit_position)
        player.hit_by_saw = False
        player.hit_position = None

    player.draw(screen)
    draw_blood_splashes(screen, blood_splashes, dt)
    
    if flash_timer > 0:
        flash_alpha = int(255 * (flash_timer / flash_duration))
        flash_surface = pygame.Surface(screen.get_size())
        flash_surface.set_alpha(flash_alpha)
        flash_surface.fill((255, 255, 255))
        screen.blit(flash_surface, (0, 0))
 
    pygame.display.flip()
