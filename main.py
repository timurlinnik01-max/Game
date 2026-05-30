import pygame
from player import Player
from map_elements import Level1
from map_elements import Level2
from map_elements import Level3
 
import math
 
pygame.init()
clock = pygame.time.Clock()
 
# scaling and assets
scale = 0.8
player_scale = 0.15
saw_scale = 3
level_id = 1
spawn_id = 1
saw_angle = 0
 
screen = pygame.display.set_mode((1920, 1080))
background_image = pygame.image.load('background.png').convert()
background_image = pygame.transform.scale(background_image, screen.get_size())
 
# Load wall and platform tile images once
wall_tile_raw = pygame.image.load('wall.png').convert_alpha()
platform_tile_raw = pygame.image.load('platform.png').convert_alpha()
 
# Scale tiles to sensible sizes (keep aspect ratio, cap height)
WALL_TILE_W = wall_tile_raw.get_width()
WALL_TILE_H = wall_tile_raw.get_height()
PLATFORM_TILE_W = platform_tile_raw.get_width()
PLATFORM_TILE_H = platform_tile_raw.get_height()
 
 
def draw_tiled(surface, tile, rect):
    """Tile `tile` image to fill `rect` by clipping each tile piece."""
    tw = tile.get_width()
    th = tile.get_height()
    x0, y0, rw, rh = rect.x, rect.y, rect.width, rect.height
    for row in range(0, rh, th):
        for col in range(0, rw, tw):
            # How much of this tile actually fits
            blit_w = min(tw, rw - col)
            blit_h = min(th, rh - row)
            area = pygame.Rect(0, 0, blit_w, blit_h)
            surface.blit(tile, (x0 + col, y0 + row), area)
 
 
def draw_level_blocks(surface, level_blocks, wall_tile, platform_tile, block_colors):
    for block_type, block_rect in level_blocks:
        if block_type == "wall":
            draw_tiled(surface, wall_tile, block_rect)
        else:
            # platform, floor and ceiling all use the platform texture
            draw_tiled(surface, platform_tile, block_rect)
 
 
# Build level and player objects
if level_id == 1:
    level = Level1(saw_scale, scale)
    saw_image = pygame.transform.scale(level.saw_image_raw, (int(40 * saw_scale), int(40 * saw_scale)))
 
player = Player('player (2).png', 100, 900, player_scale)
 
# Use tiles at their natural resolution — draw_tiled will repeat them without stretching
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
    screen.blit(background_image, (0, 0))
    if level_id == 1 or level_id == 2:
        finish_rect = pygame.Rect(int(1800), int(280), int(100), int(250))
        pygame.draw.rect(screen, (0, 255, 0), finish_rect)
 
    if level_id == 2:
        level = Level2(saw_scale, scale)
        saw_image = pygame.transform.scale(level.saw_image_raw, (int(40 * saw_scale), int(40 * saw_scale)))
 
    if level_id == 3:
        level = Level3(saw_scale, scale)
        finish_rect = pygame.Rect(int(860), int(40), int(100), int(206))
        pygame.draw.rect(screen, (0, 255, 0), finish_rect)
        saw_image = pygame.transform.scale(level.saw_image_raw, (int(40 * saw_scale), int(40 * saw_scale)))
 
 
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
            pygame.draw.rect(screen, (255, 0, 0), saw_rect, 2)
 
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
            pygame.draw.rect(screen, (255, 0, 0), saw_rect, 2)
 
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
            pygame.draw.rect(screen, (255, 0, 0), saw_rect, 2)
 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
 
    keys = pygame.key.get_pressed()
 
    player.update(keys, level.level_blocks, level.saw_rects, speed, gravity, jump_speed, wall_run_slide_speed, wall_run_jump_multiplier)
    player.draw(screen)
 
    pygame.display.flip()
