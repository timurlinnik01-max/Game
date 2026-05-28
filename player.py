import math
import pygame


class Player:
    def __init__(self, image_path, spawn_x, spawn_y, player_scale):
        img = pygame.image.load(image_path)
        self.image = pygame.transform.scale(img, (int(img.get_width() * player_scale), int(img.get_height() * player_scale)))
        self.spawn_x = float(spawn_x)
        self.spawn_y = float(spawn_y)
        self.x = float(self.spawn_x)
        self.y = float(self.spawn_y)
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        self.on_ground = False
        self.on_ceiling = False
        self.on_wall = False
        self.wall_run_active = False
        self.current_wall_rect = None

    def respawn(self):
        self.x = float(self.spawn_x)
        self.y = float(self.spawn_y)
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        self.on_ground = False
        self.on_ceiling = False
        self.on_wall = False
        self.wall_run_active = False
        self.current_wall_rect = None

    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.image.get_width(), self.image.get_height())

    def draw(self, surface):
        surface.blit(self.image, (int(self.x), int(self.y)))

    def update(self, keys, level_blocks, saw_rects, speed, gravity, jump_speed, wall_run_slide_speed, wall_run_jump_multiplier):
        prev_x = self.x
        prev_y = self.y

        dx = 0
        if keys[pygame.K_d]:
            dx = speed
        if keys[pygame.K_a] and not self.on_wall:
            dx = -speed
        if keys[pygame.K_w] and self.on_ground:
            self.velocity_y = -jump_speed
            self.velocity_x = 0.0
            self.on_ground = False
            self.on_ceiling = False
        if keys[pygame.K_s] and self.on_ceiling:
            self.on_ceiling = False

        if self.on_wall:
            # Determine which side of the wall the player is on
            is_on_right_side = self.current_wall_rect and self.x + self.image.get_width() / 2 > self.current_wall_rect.centerx

            if keys[pygame.K_w]:
                # wall-jump: allow jump away from wall
                self.on_wall = False
                self.wall_run_active = False
                if is_on_right_side:
                    jump_magnitude = jump_speed * wall_run_jump_multiplier
                    self.velocity_x = jump_magnitude * math.cos(math.radians(45))
                    self.velocity_y = -jump_magnitude * math.sin(math.radians(45))
                else:
                    jump_magnitude = jump_speed * wall_run_jump_multiplier
                    self.velocity_x = -jump_magnitude * math.cos(math.radians(35))
                    self.velocity_y = -jump_magnitude * math.sin(math.radians(35))
            elif keys[pygame.K_d] and is_on_right_side:
                # move right off the wall only if player is on the right side
                self.on_wall = False
                self.velocity_x = 0.0
                self.x += speed
            elif keys[pygame.K_a] and not is_on_right_side:
                # only allow moving left if player is not on the right side of the wall
                self.on_wall = False
                self.velocity_x = 0.0
                self.x -= speed
            else:
                # stick to the wall surface while wall-running
                if self.current_wall_rect:
                    if self.x + self.image.get_width() / 2 < self.current_wall_rect.centerx:
                        self.x = self.current_wall_rect.left - self.image.get_width()
                    else:
                        self.x = self.current_wall_rect.right
                self.velocity_x = 0.0
                self.velocity_y = wall_run_slide_speed
        else:
            if self.velocity_x != 0.0:
                self.x += self.velocity_x
                self.velocity_x *= 0.92
                if abs(self.velocity_x) < 0.1:
                    self.velocity_x = 0.0
            self.x += dx
            hitbox_x = pygame.Rect(int(self.x), int(prev_y), self.image.get_width(), self.image.get_height())
            attached_wall = None
            for block_type, block_rect in level_blocks:
                if block_type == "wall" and hitbox_x.colliderect(block_rect) and not self.on_ground and not self.on_ceiling:
                    attached_wall = block_rect
                    break
            if attached_wall:
                self.on_wall = True
                self.current_wall_rect = attached_wall
                if self.x + self.image.get_width() / 2 < attached_wall.centerx:
                    self.x = attached_wall.left - self.image.get_width()
                else:
                    self.x = attached_wall.right
                self.wall_run_active = True
                self.velocity_x = 0.0
                self.velocity_y = wall_run_slide_speed
            else:
                for block_type, block_rect in level_blocks:
                    if hitbox_x.colliderect(block_rect):
                        self.x = prev_x
                        break

        hitbox = pygame.Rect(int(self.x), int(self.y), self.image.get_width(), self.image.get_height())

        for saw_rect in saw_rects:
            if hitbox.colliderect(saw_rect):
                self.respawn()
                hitbox = pygame.Rect(int(self.x), int(self.y), self.image.get_width(), self.image.get_height())
                break

        self.wall_run_active = self.on_wall

        # Horizontal collisions for non-wall blocks
        for block_type, block_rect in level_blocks:
            if block_type == "wall":
                continue
            if hitbox.colliderect(block_rect):
                self.x = prev_x
                hitbox.x = int(self.x)
                break

        if not self.on_ground and not self.on_ceiling and not self.wall_run_active:
            self.velocity_y += gravity
        self.y += self.velocity_y

        hitbox = pygame.Rect(int(self.x), int(self.y), self.image.get_width(), self.image.get_height())

        self.on_ground = False
        for block_type, block_rect in level_blocks:
            if hitbox.colliderect(block_rect):
                landing_tolerance = abs(self.velocity_y) + 1
                if self.velocity_y >= 0 and prev_y + self.image.get_height() <= block_rect.top + landing_tolerance:
                    self.y = block_rect.top - self.image.get_height()
                    self.velocity_y = 0
                    hitbox.y = int(self.y)
                    if block_type == "ceiling":
                        self.on_ceiling = True
                        self.on_ground = False
                    else:
                        self.on_ground = True
                        self.on_ceiling = False
                        self.velocity_x = 0.0
                    break
                elif self.velocity_y < 0 and prev_y >= block_rect.bottom - landing_tolerance:
                    self.y = block_rect.bottom
                    self.velocity_y = 0
                    hitbox.y = int(self.y)
                    if block_type == "ceiling":
                        self.on_ceiling = False
                    break
                else:
                    self.y = prev_y
                    self.velocity_y = 0
                    hitbox.y = int(self.y)
                    break
