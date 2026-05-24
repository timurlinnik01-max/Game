import pygame
import math

pygame.init()
clock = pygame.time.Clock() 
player=pygame.image.load('player.png')
scale = 0.5
player_scale = 0.2
player = pygame.transform.scale(player, (int(player.get_width() * player_scale), int(player.get_height() * player_scale)))
screen=pygame.display.set_mode((1280, 720))
wall_x=0
wall_y=0
x=float(80 * scale)
y=float(100 * scale)

print("something")

wall_rect = pygame.Rect(0, 0, int(20*scale), int(700*scale))
level_blocks = [
    ("floor", pygame.Rect(0, int(700*scale), int(1280*scale), int(40*scale))),
    ("wall", wall_rect),
    ("ceiling", pygame.Rect(0, 0, int(1280*scale), int(20*scale))),
    ("wall", pygame.Rect(int(100), int(150*scale), int(20*scale), int(550*scale))),
    ("platform", pygame.Rect(int(200*scale), int(520*scale), int(200*scale), int(20*scale))),
    ("platform", pygame.Rect(int(520*scale), int(430*scale), int(200*scale), int(20*scale))),
    ("platform", pygame.Rect(int(860*scale), int(340*scale), int(200*scale), int(20*scale))),
]
wall_run_zone = pygame.Rect(wall_rect.right, 0, int(10*scale), int(700*scale))
block_colors = {
    "floor": (55, 52, 198),
    "wall": (55, 52, 198),
    "ceiling": (55, 52, 198),
    "platform": (80, 120, 210),
}
speed=8 * scale
wall_run_slide_speed = 2 * scale
wall_run_jump_multiplier = 1.3
wall_run_active = False
gravity=0.5 * scale  # Reduced gravity for smoother jump
jump_speed = 15 * scale  # Initial upward velocity for jump
velocity_y = 0.0  # Vertical velocity
velocity_x = 0.0  # Horizontal velocity for wall jump
on_ground = False  # Will be set based on collision
on_ceiling = False  # True when standing on top of ceiling
on_wall = False  # True when stuck to wall
current_wall_rect = None
running=True
while running:
    clock.tick(60)
    screen.fill((255,255,255))
    screen.blit(player,(int(x),int(y)))
    hitbox=pygame.Rect(int(x), int(y), player.get_width(), player.get_height())
    for block_type, block_rect in level_blocks:
        pygame.draw.rect(screen, block_colors[block_type], block_rect)
    pygame.draw.rect(screen,(55,52,19),wall_run_zone)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
    keys = pygame.key.get_pressed()
    prev_x = x
    prev_y = y

    dx = 0
    if keys[pygame.K_d]:
        dx = speed
    if keys[pygame.K_a] and not on_wall:
        dx = -speed
    if keys[pygame.K_w] and on_ground:  # Jump only if on ground
        velocity_y = -jump_speed
        velocity_x = 0.0
        on_ground = False
        on_ceiling = False
    if keys[pygame.K_s] and on_ceiling:  # drop from ceiling
        on_ceiling = False

    if on_wall:
        if keys[pygame.K_w]:
            on_wall = False
            wall_run_active = False
            
            # Determine which side of the wall the player is on
            is_on_right_side = current_wall_rect and x + player.get_width() / 2 > current_wall_rect.centerx
            
            if is_on_right_side:
                # Jump at 45 degrees (up-right)
                jump_magnitude = jump_speed * wall_run_jump_multiplier
                velocity_x = jump_magnitude * math.cos(math.radians(45))
                velocity_y = -jump_magnitude * math.sin(math.radians(45))
            else:
                # Jump at 145 degrees (up-left)
                jump_magnitude = jump_speed * wall_run_jump_multiplier
                velocity_x = -jump_magnitude * math.cos(math.radians(35))
                velocity_y = -jump_magnitude * math.sin(math.radians(35))
        elif keys[pygame.K_d]:
            on_wall = False
            velocity_x = 0.0
            x += speed
        elif keys[pygame.K_a]:
            on_wall = False
            velocity_x = 0.0
            x -= speed
        else:
            if current_wall_rect:
                if x + player.get_width() / 2 < current_wall_rect.centerx:
                    x = current_wall_rect.left - player.get_width()
                else:
                    x = current_wall_rect.right
            velocity_x = 0.0
            velocity_y = wall_run_slide_speed
    else:
        if velocity_x != 0.0:
            x += velocity_x
            velocity_x *= 0.92
            if abs(velocity_x) < 0.1 * scale:
                velocity_x = 0.0
        x += dx
        hitbox_x = pygame.Rect(int(x), int(prev_y), player.get_width(), player.get_height())
        attached_wall = None
        for block_type, block_rect in level_blocks:
            if block_type == "wall" and hitbox_x.colliderect(block_rect) and not on_ground and not on_ceiling:
                attached_wall = block_rect
                break
        if attached_wall:
            on_wall = True
            current_wall_rect = attached_wall
            if x + player.get_width() / 2 < attached_wall.centerx:
                x = attached_wall.left - player.get_width()
            else:
                x = attached_wall.right
            wall_run_active = True
            velocity_x = 0.0
            velocity_y = wall_run_slide_speed
        else:
            for block_type, block_rect in level_blocks:
                if hitbox_x.colliderect(block_rect):
                    x = prev_x
                    break

    hitbox = pygame.Rect(int(x), int(y), player.get_width(), player.get_height())
    wall_run_active = on_wall

    # Horizontal collisions
    for block_type, block_rect in level_blocks:
        if block_type == "wall":
            continue
        if hitbox.colliderect(block_rect):
            x = prev_x
            hitbox.x = int(x)
            break

    if not on_ground and not on_ceiling and not wall_run_active:
        velocity_y += gravity
    y += velocity_y

    hitbox = pygame.Rect(int(x), int(y), player.get_width(), player.get_height())

    on_ground = False
    for block_type, block_rect in level_blocks:
        if hitbox.colliderect(block_rect):
            landing_tolerance = abs(velocity_y) + 1
            if velocity_y >= 0 and prev_y + player.get_height() <= block_rect.top + landing_tolerance:
                y = block_rect.top - player.get_height()
                velocity_y = 0
                hitbox.y = int(y)
                if block_type == "ceiling":
                    on_ceiling = True
                    on_ground = False
                else:
                    on_ground = True
                    on_ceiling = False
                    velocity_x = 0.0
                break
            elif velocity_y < 0 and prev_y >= block_rect.bottom - landing_tolerance:
                y = block_rect.bottom
                velocity_y = 0
                hitbox.y = int(y)
                if block_type == "ceiling":
                    on_ceiling = False
                break
            else:
                y = prev_y
                velocity_y = 0
                hitbox.y = int(y)
                break

    pygame.display.flip()
    