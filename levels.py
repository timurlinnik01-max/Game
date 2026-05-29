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
            ("wall", pygame.Rect(int(2400 * scale), int(0 * scale), int(20 * scale), int(2050 * scale))),
            ("ceiling", pygame.Rect(0, 0, int(1920), int(20))),
            ("platform", pygame.Rect(int(25 * scale), int(600 * scale), int(240 * scale), int(20 * scale))),
            ("wall", pygame.Rect(int(255 * scale), int(600 * scale), int(20 * scale), int(360 * scale))),
            ("platform", pygame.Rect(int(300 * scale), int(430 * scale), int(620 * scale), int(20 * scale))),
            ("wall", pygame.Rect(int(720 * scale), int(450 * scale), int(20 * scale), int(2000 * scale))),
            ("wall", pygame.Rect(int(510 * scale), int(1000 * scale), int(20 * scale), int(500 * scale))),
            ("wall", pygame.Rect(int(250 * scale), int(200 * scale), int(20 * scale), int(200 * scale))),
            ("wall", pygame.Rect(int(900 * scale), int(170 * scale), int(20 * scale), int(260 * scale))),
            ("wall", pygame.Rect(int(1550 * scale), int(0 * scale), int(20 * scale), int(320 * scale))),
            ("platform", pygame.Rect(int(900 * scale), int(560 * scale), int(240 * scale), int(20 * scale))),
            ("platform", pygame.Rect(int(1110 * scale), int(300 * scale), int(440 * scale), int(20 * scale))),
            ("platform", pygame.Rect(int(1250 * scale), int(450 * scale), int(440 * scale), int(20 * scale))),
            ("platform", pygame.Rect(int(1750 * scale), int(300 * scale), int(140 * scale), int(20 * scale))),
            ("wall", pygame.Rect(int(1870 * scale), int(150 * scale), int(20 * scale), int(450 * scale))),
            ("wall", pygame.Rect(int(2050 * scale), int(0 * scale), int(20 * scale), int(250 * scale))),
            ("wall", pygame.Rect(int(2200 * scale), int(250 * scale), int(20 * scale), int(420 * scale))),
            ("platform", pygame.Rect(int(2200 * scale), int(660 * scale), int(240 * scale), int(20 * scale))),
            ]
        self.saw_rects = [
            pygame.Rect(int(550 * scale), int(1020 * scale), int(40 * saw_scale), int(40 * saw_scale)),
            pygame.Rect(int(750 * scale), int(1180 * scale), int(40 * saw_scale), int(40 * saw_scale)),
            pygame.Rect(int(950 * scale), int(1180 * scale), int(40 * saw_scale), int(40 * saw_scale)),
            pygame.Rect(int(1150 * scale), int(1180 * scale), int(40 * saw_scale), int(40 * saw_scale)),
            pygame.Rect(int(1350 * scale), int(1180 * scale), int(40 * saw_scale), int(40 * saw_scale)),
            pygame.Rect(int(1550 * scale), int(1180 * scale), int(40 * saw_scale), int(40 * saw_scale)),
            pygame.Rect(int(1750 * scale), int(1180 * scale), int(40 * saw_scale), int(40 * saw_scale)),
            pygame.Rect(int(1950 * scale), int(1180 * scale), int(40 * saw_scale), int(40 * saw_scale)),
            pygame.Rect(int(2150 * scale), int(1180 * scale), int(40 * saw_scale), int(40 * saw_scale)),
        ]
        self.wall_run_zone = pygame.Rect(wall_rect.right, 0, int(10), int(700))
        self.block_colors = {
            "floor": (55, 52, 198),
            "wall": (55, 52, 198),
            "ceiling": (55, 52, 198),
            "platform": (80, 120, 210),
        }
        self.saw_image_raw = pygame.image.load('f520849307b5501.webp').convert_alpha()

class Level3:
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
            ("wall", pygame.Rect(int(2380 * scale), int(0 * scale), int(20 * scale), int(2050 * scale))),
            ("ceiling", pygame.Rect(0, 0, int(1920), int(20))),
            ("platform", pygame.Rect(int(25 * scale), int(1000 * scale), int(400 * scale), int(20 * scale))),
            ("wall", pygame.Rect(int(405 * scale), int(640 * scale), int(20 * scale), int(360 * scale))),
            ("platform", pygame.Rect(int(25 * scale), int(630 * scale), int(400 * scale), int(20 * scale))),
            ("wall", pygame.Rect(int(610 * scale), int(500 * scale), int(20 * scale), int(200 * scale))),
            ("wall", pygame.Rect(int(610 * scale), int(900 * scale), int(20 * scale), int(700 * scale))),
            ("wall", pygame.Rect(int(200 * scale), int(150 * scale), int(20 * scale), int(200 * scale))),
            ("wall", pygame.Rect(int(880 * scale), int(150 * scale), int(20 * scale), int(860 * scale))),
            ("wall", pygame.Rect(int(1060 * scale), int(0 * scale), int(20 * scale), int(320 * scale))),
            ("platform", pygame.Rect(int(200 * scale), int(480 * scale), int(430 * scale), int(20 * scale))),
            ("platform", pygame.Rect(int(200 * scale), int(350 * scale), int(700 * scale), int(20 * scale))),
            ("platform", pygame.Rect(int(200 * scale), int(150 * scale), int(700 * scale), int(20 * scale))),
            ("platform", pygame.Rect(int(770 * scale), int(550 * scale), int(110 * scale), int(20 * scale))),
            ("wall", pygame.Rect(int(1200 * scale), int(-300 * scale), int(20 * scale), int(450 * scale))),
            ("wall", pygame.Rect(int(1380 * scale), int(200 * scale), int(20 * scale), int(730 * scale))),
            ("wall", pygame.Rect(int(1100 * scale), int(550 * scale), int(20 * scale), int(1020 * scale))),
            ("platform", pygame.Rect(int(880 * scale), int(414 * scale), int(500 * scale), int(20 * scale))),
            ("platform", pygame.Rect(int(1080 * scale), int(300 * scale), int(140 * scale), int(20 * scale))),
            ("platform", pygame.Rect(int(770 * scale), int(990 * scale), int(110 * scale), int(20 * scale))),
            ("platform", pygame.Rect(int(790 * scale), int(1160 * scale), int(200 * scale), int(20 * scale))),
            ("wall", pygame.Rect(int(1560 * scale), int(430 * scale), int(20 * scale), int(500 * scale))),
            ("platform", pygame.Rect(int(1300 * scale), int(1110 * scale), int(200 * scale), int(20 * scale))),
            ("platform", pygame.Rect(int(1380 * scale), int(200 * scale), int(300 * scale), int(20 * scale))),
            ("platform", pygame.Rect(int(2000 * scale), int(1100 * scale), int(200 * scale), int(20 * scale))),
            ("platform", pygame.Rect(int(1950 * scale), int(200 * scale), int(250 * scale), int(20 * scale))),
            ]
        self.saw_rects = [
            pygame.Rect(int(560 * scale), int(725 * scale), int(40 * saw_scale), int(40 * saw_scale)),
            pygame.Rect(int(650 * scale), int(1180 * scale), int(40 * saw_scale), int(40 * saw_scale)),
            pygame.Rect(int(800 * scale), int(1180 * scale), int(40 * saw_scale), int(40 * saw_scale)),
            pygame.Rect(int(950 * scale), int(1180 * scale), int(40 * saw_scale), int(40 * saw_scale)),
            pygame.Rect(int(1150 * scale), int(1180 * scale), int(40 * saw_scale), int(40 * saw_scale)),
            pygame.Rect(int(1350 * scale), int(1180 * scale), int(40 * saw_scale), int(40 * saw_scale)),
            pygame.Rect(int(1550 * scale), int(1180 * scale), int(40 * saw_scale), int(40 * saw_scale)),
            pygame.Rect(int(1750 * scale), int(1180 * scale), int(40 * saw_scale), int(40 * saw_scale)),
            pygame.Rect(int(1950 * scale), int(1180 * scale), int(40 * saw_scale), int(40 * saw_scale)),
            pygame.Rect(int(2150 * scale), int(1180 * scale), int(40 * saw_scale), int(40 * saw_scale)),
            pygame.Rect(int(1120 * scale), int(660 * scale), int(40 * saw_scale), int(40 * saw_scale)),
        ]
        self.wall_run_zone = pygame.Rect(wall_rect.right, 0, int(10), int(700))
        self.block_colors = {
            "floor": (55, 52, 198),
            "wall": (55, 52, 198),
            "ceiling": (55, 52, 198),
            "platform": (80, 120, 210),
        }
        self.saw_image_raw = pygame.image.load('f520849307b5501.webp').convert_alpha()
