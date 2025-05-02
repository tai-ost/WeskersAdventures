import pygame

from constants import WIDTH, HEIGHT, FPS, ACTUAL_HEIGHT, FLOOR_HEIGHT
from wesker import Wesker
from hud import HUD
from scenes import Scene, Door, Enemy, EnvironmentItem


class Game:
    def __init__(self, start_scene: int = 0):
        pygame.init()

        self.__start_time: int
        self.__time_passed: int
        self.__start_time = self.__time_passed = 0
        self.__in_menu_time: int = 0

        pygame.display.set_caption('Wesker\'s Adventures')
        self.__running: bool = True
        self.__in_menu: bool = True

        self.__width: int = WIDTH
        self.__height: int = HEIGHT
        self.__screensize: tuple = (self.__width, self.__height)
        self.__screen: pygame.Surface = pygame.display.set_mode(self.__screensize)

        self.__fps: int = FPS
        self.__clock: pygame.time.Clock = pygame.time.Clock()
        self.__seven_minutes: bool = False  # ... is all he can spare to play with you ;)

        self.__current_scene: int = start_scene
        self.__previous_scene: int = start_scene

        self.__alpha_level: int = 0

        self.__wesker: Wesker = Wesker()

        self.__menu: Menu
        self.__hud: HUD
        self.__font_re: pygame.font.Font
        self.__font_re_item: pygame.font.Font
        self.__font_special: pygame.font.Font
        self.__scenes: list

    def run(self):
        while self.__running:
            if not self.__in_menu:
                self.__check_time()
                self.__check_events()
                self.__move()
                self.__check_logic()
                self.__draw()
            else:
                self.__check_menu_events()
                self.__menu.draw_menu(self.__screen)

            self.__clock.tick(self.__fps)

    def __check_menu_events(self):
        event: pygame.event.Event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False
            elif event.type == pygame.MOUSEMOTION:
                self.__menu.check_button_hover(event.pos)
            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):
                if self.__menu.check_play_button_pressed():
                    self.__in_menu = False
                    self.__in_menu_time = pygame.time.get_ticks() - self.__menu.get_start_time_in_menu()
                self.__running = not self.__menu.check_exit_button_pressed()

    def __check_time(self):
        self.__time_passed = pygame.time.get_ticks() - self.__start_time - self.__in_menu_time
        self.__seven_minutes = self.__time_passed > 420_000

    def __check_events(self):
        self.__hud.update_ammo(self.__wesker.get_ammo())
        for event in pygame.event.get():
            if (event.type == pygame.QUIT) or (self.__hud.get_health_points() <= 0):
                self.__running = False
            elif (event.type == pygame.KEYDOWN) and (event.key == pygame.K_ESCAPE):
                self.__in_menu = True
                self.__menu.update_start_time(self.__time_passed)
            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                self.__wesker.check_aiming_event(event)
            elif (event.type == pygame.KEYDOWN or event.type == pygame.KEYUP) and \
                    event.key in self.__wesker.get_movement_keys():
                self.__wesker.check_movement_event(event)
            elif (event.type == pygame.KEYDOWN) and ((event.key == pygame.K_f) or (event.key == pygame.K_t)):
                action_code, action = self.__scenes[self.__current_scene].check_scene_event(self.__wesker, self.__hud,
                                                                                            event.key)
                if action_code == 1:
                    self.__change_current_scene(action)
                    self.__alpha_level = 80
                ...
            elif (event.type == pygame.KEYDOWN) and (event.key == pygame.K_h):
                self.__hud.hide_or_show()
            elif (event.type == pygame.KEYDOWN) and (event.key == pygame.K_r) and \
                    (self.__wesker.get_ammo() < 15) and (self.__hud.get_ammo_stored() > 0):
                self.__wesker.reload(self.__hud.reload())
            elif (event.type == pygame.KEYDOWN) and (event.key in self.__hud.get_inventory_keys()):
                self.__hud.activate_inventory_slot(event.key)
            elif (event.type == pygame.KEYDOWN) and (event.key == pygame.K_5):
                self.__hud.inventory_passive()
            elif (event.type == pygame.KEYDOWN) and (event.key == pygame.K_u):
                self.__hud.use_item()
            elif (event.type == pygame.KEYDOWN) and (event.key == pygame.K_c):
                self.__hud.combine_herbs()
            elif (event.type == pygame.KEYDOWN) and (event.key == pygame.K_p):  # delete after creating enemies
                self.__hud.got_poisoned()

    def __check_logic(self):
        self.__wesker.check_wesker_logic()
        self.__scenes[self.__current_scene].check_scene_logic(self.__wesker, self.__hud)
        self.__hud.check_health()
        self.__hud.update_time(self.__time_passed)

    def __move(self):
        self.__wesker.move()

    def __draw(self):
        self.__draw_scene()
        self.__draw_characters()
        self.__draw_hud()
        self.__draw_darkness()

        pygame.display.flip()

    def __draw_scene(self):
        self.__draw_floor()
        self.__scenes[self.__current_scene].draw(self.__screen, self.__wesker)

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

    def __draw_hud(self):
        self.__hud.draw_hud(self.__screen)

    def __change_current_scene(self, next_scene):
        self.__previous_scene = self.__current_scene
        self.__current_scene = next_scene

    def prepare_game(self):
        self.__prepare_font()
        self.__prepare_menu()
        self.__prepare_hud()
        self.__prepare_scenes()

    def __prepare_font(self):
        self.__font_special = pygame.font.Font('fonts/SpecialElite-Regular.ttf', 22)
        self.__font_special_menu = pygame.font.Font('fonts/SpecialElite-Regular.ttf', 40)
        self.__font_special_caption = pygame.font.Font('fonts/SpecialElite-Regular.ttf', 50)

    def __prepare_menu(self):
        self.__menu = Menu(self.__font_special_menu, self.__font_special_caption)
        self.__menu.update_start_time(self.__time_passed)

    def __prepare_hud(self):
        self.__hud = HUD(self.__font_special)

    def __prepare_scenes(self):
        # scene_0_entities = [
        #     Door(WIDTH - 170,
        #          'door_var_1', 150, 270,
        #          0, 1, 'scene2', WIDTH - 170, self.__font_special),
        #     Door(20,
        #          'door_var_2', 150, 270,
        #          0, 2, 'scene3', WIDTH - 170, self.__font_special),
        #     EnvironmentItem(self.__width // 2, ACTUAL_HEIGHT - 100, 2, self.__font_special),
        #     EnvironmentItem(self.__width // 3, ACTUAL_HEIGHT - 100, 3, self.__font_special),
        #     EnvironmentItem(self.__width // 4, ACTUAL_HEIGHT - 100, 4, self.__font_special)
        # ]
        #
        # scene_1_entities = [
        #     Door(WIDTH - 170,
        #          'door_var_1', 150, 270,
        #          1, 0, 'scene1', WIDTH - 170, self.__font_special),
        #     Door(20,
        #          'door_var_2', 150, 270,
        #          1, 2, 'scene3', 20, self.__font_special),
        #     Enemy(self.__width // 2, 0),
        #     Enemy(self.__width // 3, 0),
        #     Enemy(self.__width // 4, 0),
        #     EnvironmentItem(self.__width // 2, ACTUAL_HEIGHT - 80, 1, self.__font_special),
        #     EnvironmentItem(self.__width // 3, ACTUAL_HEIGHT - 80, 1, self.__font_special)
        # ]
        #
        # scene_2_entities = [
        #     Door(WIDTH - 170,
        #          'door_var_1', 150, 270,
        #          2, 0, 'scene1', 20, self.__font_special),
        #     Door(20,
        #          'door_var_2', 150, 270,
        #          2, 1, 'scene2', 20,  self.__font_special),
        #     EnvironmentItem(self.__width // 2, ACTUAL_HEIGHT - 80, 1, self.__font_special),
        #     EnvironmentItem(self.__width // 3, ACTUAL_HEIGHT - 80, 1, self.__font_special)
        # ]
        #
        # self.__scenes = [Scene(0, 'scene_1', scene_0_entities, self.__font_special),
        #                  Scene(1, 'scene_2', scene_1_entities, self.__font_special),
        #                  Scene(2, 'scene_3', scene_2_entities, self.__font_special)]

        # mansion - 0
        main_hall = [
            Door(WIDTH // 2 - 75,
                 'empty_door', 150, 270,
                 0, 1, 'Graveyard', WIDTH // 2,
                 self.__font_special)
        ]

        # graveyard_top - 1
        graveyard_top = [
            Door(WIDTH // 2 - 75,
                 'empty_door', 150, 270,
                 1, 0, 'Main Hall', WIDTH // 2 - 75,
                 self.__font_special),
            Door(WIDTH - 150,
                 'empty_door', 150, 270,
                 1, 2, 'the downstairs of Graveyard', WIDTH - 220,
                 self.__font_special)
        ]

        # graveyard_bottom - 2
        graveyard_bottom = [
            Door(WIDTH - 150,
                 'empty_door', 150, 270,
                 2, 1, 'the upstairs of Graveyard', WIDTH - 220,
                 self.__font_special),
            Door(200,
                 'empty_door', 150, 270,
                 2, 3, 'Large Gallery', 0,
                 self.__font_special)
        ]

        # large_gallery_front - 3
        large_gallery_front = [
            Door(0,
                 'empty_door', 150, 270,
                 3, 2, 'the downstairs of Graveyard', 200,
                 self.__font_special),
            Door(WIDTH - 150,
                 'empty_door', 150, 270,
                 3, 4, 'the back of Large Gallery', WIDTH - 220,
                 self.__font_special)
        ]

        # large_gallery_back - 4
        large_gallery_back = [
            Door(WIDTH - 150,
                 'empty_door', 150, 270,
                 4, 3, 'the front of Large Gallery', WIDTH - 220,
                 self.__font_special),
            Door(100,
                 'empty_door', 150, 270,
                 4, 5, 'Dark Corridor', 300,
                 self.__font_special)
        ]

        # dark_corridor - 5
        dark_corridor = [
            Door(300,
                 'empty_door', 150, 270,
                 5, 4, 'the back of Large Gallery', 100,
                 self.__font_special),
            Door(0,
                 'empty_door', 150, 270,
                 5, 8, 'Roofed Passage', WIDTH - 220,
                 self.__font_special),
            Door(WIDTH // 2 + 150,
                 'empty_door', 150, 270,
                 5, 6, 'East Wing Stairway', WIDTH - 220,
                 self.__font_special)
        ]

        # east_wing_stairway - 6
        east_wing_stairway = [
            Door(WIDTH - 150,
                 'empty_door', 150, 270,
                 6, 5, 'Dark Corridor', WIDTH // 2 + 150,
                 self.__font_special),
            Door(WIDTH // 2,
                 'empty_door', 150, 270,
                 6, 7, 'East Wing Storeroom', 0,
                 self.__font_special)
        ]

        # east_wing_storeroom - 7
        east_wing_storeroom = [
            Door(0,
                 'empty_door', 150, 270,
                 7, 6, 'East Wing Stairway', WIDTH // 2,
                 self.__font_special)
        ]

        # roofed_passage - 8
        roofed_passage = [
            Door(WIDTH - 150,
                 'empty_door', 150, 270,
                 8, 5, 'Dark Corridor', 0,
                 self.__font_special),
            Door(200,
                 'empty_door', 150, 270,
                 8, 9, 'Garden Shed', 0,
                 self.__font_special)
        ]

        # garden_shed - 9
        garden_shed = [
            Door(0,
                 'empty_door', 150, 270,
                 9, 8, 'Roofed Passage', 200,
                 self.__font_special),
            Door(WIDTH // 2 + 150,
                 'empty_door', 150, 270,
                 9, 10, 'Main Garden', 0,
                 self.__font_special)
        ]

        # main_garden - 10
        main_garden = [
            Door(100,
                 'empty_door', 150, 270,
                 10, 9, 'Garden Shed', WIDTH // 2 + 150 - 220,
                 self.__font_special),
            Door(WIDTH // 2 - 200,
                 'empty_door', 150, 270,
                 10, 11, 'Falls Area', WIDTH - 300,
                 self.__font_special)
        ]

        # falls_area - 11
        falls_area = [
            Door(WIDTH - 300,
                 'empty_door', 150, 270,
                 11, 10, 'Main Garden', WIDTH // 2 - 200,
                 self.__font_special),
            Door(WIDTH // 2 - 200,
                 'empty_door', 150, 270,
                 11, 12, 'the tunnel behind the Waterfall', 0,
                 self.__font_special)
        ]

        # fall_tunnel - 12
        fall_tunnel = [
            Door(0,
                 'empty_door', 150, 270,
                 12, 11, 'Falls Area', WIDTH // 2 - 200,
                 self.__font_special),
            Door(WIDTH - 150,
                 'empty_door', 150, 270,
                 12, 13, 'Mining Area', WIDTH - 220,
                 self.__font_special)
        ]

        # mining_area - 13
        mining_area = [
            Door(WIDTH - 150,
                 'empty_door', 150, 270,
                 13, 12, 'the tunnel behind the Waterfall', WIDTH - 220,
                 self.__font_special),
            Door(WIDTH // 2 + 100,
                 'empty_door', 150, 270,
                 13, 14, 'Forked Passage', 100,
                 self.__font_special)
        ]

        # forked_passage - 14
        forked_passage = [
            Door(100,
                 'empty_door', 150, 270,
                 14, 13, 'Mining Area', WIDTH // 2 + 100,
                 self.__font_special),
            Door(WIDTH - 150,
                 'empty_door', 150, 270,
                 14, 15, 'Generator Room', 50,
                 self.__font_special)
        ]

        # generator_room - 15
        generator_room = [
            Door(50,
                 'empty_door', 150, 270,
                 15, 14, 'Forked Passage', WIDTH - 220,
                 self.__font_special),
            Door(WIDTH - 150,
                 'empty_door', 150, 270,
                 15, 16, 'Enrico\'s Room', 0,
                 self.__font_special)
        ]

        # enrico_room - 16
        enrico_room = [
            Door(0,
                 'empty_door', 150, 270,
                 16, 15, 'Generator Room', WIDTH - 220,
                 self.__font_special)
        ]

        self.__scenes = [Scene(0, 'main_hall', main_hall,
                               self.__font_special),
                         Scene(1, 'graveyard_top', graveyard_top,
                               self.__font_special),
                         Scene(2, 'graveyard_bottom', graveyard_bottom,
                               self.__font_special),
                         Scene(3, 'large_gallery_front', large_gallery_front,
                               self.__font_special),
                         Scene(4, 'large_gallery_back', large_gallery_back,
                               self.__font_special),
                         Scene(5, 'dark_corridor', dark_corridor,
                               self.__font_special),
                         Scene(6, 'east_wing_stairway', east_wing_stairway,
                               self.__font_special),
                         Scene(7, 'east_wing_storeroom', east_wing_storeroom,
                               self.__font_special),
                         Scene(8, 'roofed_passage', roofed_passage,
                               self.__font_special),
                         Scene(9, 'garden_shed', garden_shed,
                               self.__font_special),
                         Scene(10, 'main_garden', main_garden,
                               self.__font_special),
                         Scene(11, 'falls_area', falls_area,
                               self.__font_special),
                         Scene(12, 'fall_tunnel', fall_tunnel,
                               self.__font_special),
                         Scene(13, 'mining_area', mining_area,
                               self.__font_special),
                         Scene(14, 'forked_passage', forked_passage,
                               self.__font_special),
                         Scene(15, 'generator_room', generator_room,
                               self.__font_special),
                         Scene(16, 'enrico_room', enrico_room,
                               self.__font_special),
                         ]

    def __del__(self):
        pygame.quit()


class Menu:
    def __init__(self, font_buttons: pygame.font.Font, font_caption: pygame.font.Font):
        self.__background_image = ''
        self.__background_rect = pygame.Rect(0, 0, WIDTH, HEIGHT)

        self.__start_time_in_menu = 0

        self.__font_buttons = font_buttons
        self.__font_caption = font_caption

        self.__caption_color = pygame.Color(250, 250, 250)
        self.__caption_text = self.__font_caption.render('Wesker\'s Adventures', 1, self.__caption_color)
        self.__caption_rect = self.__caption_text.get_rect()
        self.__caption_rect.x = WIDTH // 2 - self.__caption_rect.width // 2
        self.__caption_rect.y = HEIGHT // 4

        self.__button_color_idle = pygame.Color(150, 150, 150)
        self.__button_color_hover = pygame.Color(230, 230, 230)

        self.__play_button_state = False
        self.__play_button_surface = self.__font_buttons.render('Play', 1, self.__button_color_idle)
        self.__play_button_rect = self.__play_button_surface.get_rect()
        self.__play_button_rect.x = WIDTH // 2 - self.__play_button_rect.width // 2
        self.__play_button_rect.y = HEIGHT // 2 - self.__play_button_rect.height // 2

        self.__exit_button_state = False
        self.__exit_button_surface = self.__font_buttons.render('Exit', 1, self.__button_color_idle)
        self.__exit_button_rect = self.__exit_button_surface.get_rect()
        self.__exit_button_rect.x = WIDTH // 2 - self.__exit_button_rect.width // 2
        self.__exit_button_rect.y = self.__play_button_rect.y + 50

    def check_button_hover(self, mouse_pos):
        if self.__play_button_rect.collidepoint(mouse_pos):
            self.__play_button_surface = self.__font_buttons.render('Play', 1, self.__button_color_hover)
            self.__play_button_state = True
        else:
            self.__play_button_surface = self.__font_buttons.render('Play', 1, self.__button_color_idle)
            self.__play_button_state = False

        if self.__exit_button_rect.collidepoint(mouse_pos):
            self.__exit_button_surface = self.__font_buttons.render('Exit', 1, self.__button_color_hover)
            self.__exit_button_state = True
        else:
            self.__exit_button_surface = self.__font_buttons.render('Exit', 1, self.__button_color_idle)
            self.__exit_button_state = False

    def check_play_button_pressed(self):
        return self.__play_button_state

    def check_exit_button_pressed(self):
        return self.__exit_button_state

    def update_start_time(self, time):
        self.__start_time_in_menu = time

    def get_start_time_in_menu(self):
        return self.__start_time_in_menu

    def __draw_background(self, screen):
        pygame.draw.rect(screen, (50, 50, 50), self.__background_rect)  # Replace with actual background

    def __show_caption(self, screen):
        screen.blit(self.__caption_text, self.__caption_rect)

    def __show_buttons(self, screen):
        screen.blit(self.__play_button_surface, self.__play_button_rect)
        screen.blit(self.__exit_button_surface, self.__exit_button_rect)

    def draw_menu(self, screen):
        self.__draw_background(screen)
        self.__show_caption(screen)
        self.__show_buttons(screen)

        pygame.display.flip()
