import pygame


class Level1:
    def __init__(self,saw_scale,scale):
        self.saw_scale = saw_scale
        self.scale = scale
        self.wall_x = 0
        self.wall_y = 0
        self.spawn_x = 80
        self.spawn_y = 100
        wall_rect = pygame.Rect(0, 0, int(20), int(1050))
        self.level_blocks = [
            ("floor", pygame.Rect(0, int(1050), int(1920), int(40))),
            ("wall", wall_rect),
            ("ceiling", pygame.Rect(0, 0, int(1920), int(20))),
            ("platform", pygame.Rect(int(450 * scale), int(1100 * scale), int(240 * scale), int(20 * scale))),
            ("platform", pygame.Rect(int(720 * scale), int(1000 * scale), int(220 * scale), int(20 * scale))),
            ("platform", pygame.Rect(int(980 * scale), int(760 * scale), int(240 * scale), int(20 * scale))),
            ("platform", pygame.Rect(int(1310 * scale), int(650 * scale), int(1220 * scale), int(20 * scale))),
            ("wall", pygame.Rect(int(750 * scale), int(480 * scale), int(20 * scale), int(360 * scale))),
            ("wall", pygame.Rect(int(1310 * scale), int(650 * scale), int(20 * scale), int(1000 * scale))),
            ("wall", pygame.Rect(int(1500 * scale), int(180 * scale), int(20 * scale), int(350 * scale))),
            ("wall", pygame.Rect(int(1700 * scale), int(280 * scale), int(20 * scale), int(370 * scale))),
        ]

        self.saw_rects = [
            pygame.Rect(int(600 * scale), int(520 * scale), int(40 * saw_scale), int(40 * saw_scale)),
            pygame.Rect(int(1180 * scale), int(620 * scale), int(40 * saw_scale), int(40 * saw_scale)),
            pygame.Rect(int(1350 * scale), int(230 * scale), int(40 * saw_scale), int(40 * saw_scale)),
        ]

        self.wall_run_zone = pygame.Rect(wall_rect.right, 0, int(10), int(700))

        self.block_colors = {
            "floor": (55, 52, 198),
            "wall": (55, 52, 198),
            "ceiling": (55, 52, 198),
            "platform": (80, 120, 210),
        }

        # Load saw image once; calling code will scale it as needed
        self.saw_image_raw = pygame.image.load('f520849307b5501.webp').convert_alpha()
class Level2:
    def __init__(self,saw_scale,scale):
        self.saw_scale = saw_scale
        self.scale = scale
        self.wall_x = 0
        self.wall_y = 0
        self.spawn_x = 80
        self.spawn_y = 100
        wall_rect = pygame.Rect(0, 0, int(20), int(1050))
        self.level_blocks = [
            ("floor", pygame.Rect(0, int(1050), int(1920), int(40))),
            ("wall", wall_rect),
            ("ceiling", pygame.Rect(0, 0, int(1920), int(20))),
            ("platform", pygame.Rect(int(550 * scale), int(900 * scale), int(240 * scale), int(20 * scale))),
            ("platform", pygame.Rect(int(420 * scale), int(800 * scale), int(220 * scale), int(20 * scale))),
            ("platform", pygame.Rect(int(780 * scale), int(560 * scale), int(240 * scale), int(20 * scale))),
            ("platform", pygame.Rect(int(1110 * scale), int(450 * scale), int(720 * scale), int(20 * scale))),
            ("wall", pygame.Rect(int(750 * scale), int(280 * scale), int(20 * scale), int(360 * scale))),
            ("wall", pygame.Rect(int(1310 * scale), int(450 * scale), int(20 * scale), int(1000 * scale))),
        ]
        self.saw_rects = [
            pygame.Rect(int(600 * scale), int(420 * scale), int(40 * saw_scale), int(40 * saw_scale)),
            pygame.Rect(int(1180 * scale), int(420 * scale), int(40 * saw_scale), int(40 * saw_scale)),
            pygame.Rect(int(1560 * scale), int(340 * scale), int(40 * saw_scale), int(40 * saw_scale)),
        ]
        self.wall_run_zone = pygame.Rect(wall_rect.right, 0, int(10), int(700))
        self.block_colors = {
            "floor": (55, 52, 198),
            "wall": (55, 52, 198),
            "ceiling": (55, 52, 198),
            "platform": (80, 120, 210),
        }
        self.saw_image_raw = pygame.image.load('f520849307b5501.webp').convert_alpha()
