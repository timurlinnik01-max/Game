import pygame
from player import Player
from map_elements import Level1
from map_elements import Level2

import math

pygame.init()
clock = pygame.time.Clock()

# scaling and assets
scale = 0.8
player_scale = 0.28
saw_scale = 3
level_id = 1
spawn_id=1

screen = pygame.display.set_mode((1920, 1080))

# Build level and player objects
if level_id == 1:
    level = Level1(saw_scale,scale)
    # scale saw image to match previous size
    saw_image = pygame.transform.scale(level.saw_image_raw, (int(40 * saw_scale), int(40 * saw_scale)))

player = Player('player.png', level.spawn_x, level.spawn_y, player_scale)

# physics/game constants (same as before)
speed = 8
wall_run_slide_speed = 2
wall_run_jump_multiplier = 1.3
gravity = 0.5
jump_speed = 14

running = True
while running:
    clock.tick(60)
    screen.fill((255, 255, 255))
    finish_rect = pygame.Rect(int(1800), int(280), int(100), int(250))
    pygame.draw.rect(screen, (0, 255, 0), finish_rect)
    if level_id == 2:
        level = Level2(saw_scale,scale)
        # scale saw image to match previous size
        saw_image = pygame.transform.scale(level.saw_image_raw, (int(40 * saw_scale), int(40 * saw_scale)))
    if level_id==1:
        if player.rect().colliderect(finish_rect):
            clock.tick(0.5)  # Pause for a moment to show the message
            level_id += 1
        if spawn_id==1:
            player.respawn()
            spawn_id=2
    # draw level blocks
        for block_type, block_rect in level.level_blocks:
            if level_id==2:
                break
            pygame.draw.rect(screen, level.block_colors[block_type], block_rect)

        # draw saws
        for saw_rect in level.saw_rects:
            if level_id==2:
                break
            screen.blit(saw_image, (saw_rect.x, saw_rect.y))
            pygame.draw.rect(screen, (255, 0, 0), saw_rect, 2)  # Draw red outline for debugging
            
    if level_id==2:
        if spawn_id==2:
            player.respawn()
            spawn_id=3
    # draw level blocks
        for block_type, block_rect in level.level_blocks:
            pygame.draw.rect(screen, level.block_colors[block_type], block_rect)

        # draw saws
        for saw_rect in level.saw_rects:
            screen.blit(saw_image, (saw_rect.x, saw_rect.y))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # update player and draw
    if level_id==1:
        player.update(keys, level.level_blocks, level.saw_rects, speed, gravity, jump_speed, wall_run_slide_speed, wall_run_jump_multiplier)
    if level_id==2:
        player.update(keys, level.level_blocks, level.saw_rects, speed, gravity, jump_speed, wall_run_slide_speed, wall_run_jump_multiplier)
    player.draw(screen)

    pygame.display.flip()
    
