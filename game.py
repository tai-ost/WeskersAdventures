import pygame

from constants import WIDTH, HEIGHT, ACTUAL_HEIGHT, FLOOR_HEIGHT
from wesker import Wesker
from hud import HUD
from scenes import Scene, Door


class Game:
    def __init__(self, width, height, fps, start_scene=0):
        pygame.init()

        pygame.display.set_caption('Wesker\'s Adventures')
        self.__running = True

        self.__width = width
        self.__height = height
        self.__screensize = (self.__width, self.__height)
        self.__screen = pygame.display.set_mode(self.__screensize)

        self.__fps = fps
        self.__clock = pygame.time.Clock()
        self.__start_time = self.__time_passed = pygame.time.get_ticks()
        self.__seven_minutes = False  # ... is all he can spare to play with you ;)

        self.__current_scene = start_scene
        self.__previous_scene = start_scene

        self.__alpha_level = 0

        self.__wesker = Wesker()
        self.__hud = HUD(self.__wesker.get_ammo())

        self.__font = None
        self.__scenes = None

    def run(self):
        while self.__running:
            self.__check_time()
            self.__check_events()
            self.__move()
            self.__check_logic()
            self.__draw()

            self.__clock.tick(self.__fps)

    def __check_time(self):
        self.__time_passed = pygame.time.get_ticks() - self.__start_time
        self.__seven_minutes = self.__time_passed > 420_000

    def __check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False
            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                self.__wesker.check_aiming_event(event)
            elif (event.type == pygame.KEYDOWN or event.type == pygame.KEYUP) and \
                    event.key in self.__wesker.get_movement_keys():
                self.__wesker.check_movement_event(event)
            elif (event.type == pygame.KEYDOWN) and (event.key == pygame.K_f):
                action_code, action = self.__scenes[self.__current_scene].check_scene_event(self.__wesker)
                if action_code == 1:
                    self.__change_current_scene(action)
                    self.__alpha_level = 80

        self.__hud.update_ammo(self.__wesker.get_ammo())

    def __check_logic(self):
        self.__wesker.check_wesker_logic()
        self.__scenes[self.__current_scene].check_scene_logic(self.__wesker)

    def __move(self):
        self.__wesker.move()

    def __draw(self):
        self.__draw_scene()
        self.__draw_characters()
        self.__draw_darkness()

        pygame.display.flip()

    def __draw_scene(self):
        self.__draw_floor()
        self.__scenes[self.__current_scene].draw(self.__screen)

    def __draw_floor(self):
        floor_color = (10, 10, 10)
        floor_rect = pygame.Rect(0, ACTUAL_HEIGHT, WIDTH, FLOOR_HEIGHT)
        pygame.draw.rect(self.__screen, floor_color, floor_rect)

    def __draw_darkness(self):
        dark_rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
        dark_image = pygame.Surface((WIDTH, HEIGHT))
        dark_image.set_alpha(self.__alpha_level)
        dark_image.fill((0, 0, 0))
        self.__alpha_level = max(0, self.__alpha_level - 1)
        self.__screen.blit(dark_image, dark_rect)

    def __draw_characters(self):
        self.__wesker.draw_wesker(self.__screen)

    def __change_current_scene(self, next_scene):
        self.__previous_scene = self.__current_scene
        self.__current_scene = next_scene

    def prepare_game(self):
        self.__prepare_font()
        self.__prepare_scenes()

    def __prepare_font(self):
        self.__font = pygame.font.Font('fonts/re_font.ttf', 30)

    def __prepare_scenes(self):
        scene_0_entities = [
            Door(WIDTH - 170, ACTUAL_HEIGHT - 270,
                 'door_var_1', 150, 270,
                 0, 1, self.__font, 1),
            Door(20, ACTUAL_HEIGHT - 270,
                 'door_var_2', 150, 270,
                 0, 2, self.__font, 1)
        ]

        scene_1_entities = [
            Door(WIDTH - 170, ACTUAL_HEIGHT - 270,
                 'door_var_1', 150, 270,
                 1, 0, self.__font, 1),
            Door(20, ACTUAL_HEIGHT - 270,
                 'door_var_2', 150, 270,
                 1, 2, self.__font, 1)
        ]

        scene_2_entities = [
            Door(WIDTH - 170, ACTUAL_HEIGHT - 270,
                 'door_var_1', 150, 270,
                 2, 0, self.__font, 1),
            Door(20, ACTUAL_HEIGHT - 270,
                 'door_var_2', 150, 270,
                 2, 1, self.__font, 1)
        ]

        self.__scenes = [Scene(0, 'scene_1', scene_0_entities, self.__font),
                         Scene(1, 'scene_2', scene_1_entities, self.__font),
                         Scene(2, 'scene_3', scene_2_entities, self.__font)]

    def __del__(self):
        pygame.quit()
