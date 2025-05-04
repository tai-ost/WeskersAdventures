import pygame

from constants import WIDTH, HEIGHT, FPS, ACTUAL_HEIGHT, FLOOR_HEIGHT
from wesker import Wesker
from hud import HUD
from scenes import Scene, Door, Enemy, EnvironmentItem
from scripts import (script_main_hall, script_gh_corr, script_gh_gallery,
                     script_enrico_room, script_altar, script_main_lab,
                     script_east_wing_stairway, script_dark_corridor, script_garden_shed,
                     script_generator_room, script_altar_after_fight)


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

        self.__lisa = True

        self.__next_script = 1

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
            if (event.type == pygame.QUIT) or (self.__hud.get_health_points() <= 0) or (self.__next_script == 0):
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
            elif (event.type == pygame.KEYDOWN) and (event.key == pygame.K_p):
                self.__next_script = script_main_hall(self.__scenes[self.__current_scene], self.__wesker,
                                                      self.__screen, self.__clock)
                self.__wesker.change_x_velocity(0)
                self.__wesker.change_y_velocity(0)
                self.__wesker.change_y_position(ACTUAL_HEIGHT - self.__wesker.get_hitbox_rect().height)

    def __check_logic(self):
        self.__wesker.check_wesker_logic(self.__scenes[self.__current_scene])
        self.__scenes[self.__current_scene].check_scene_logic(self.__wesker, self.__hud)
        self.__hud.check_health()
        self.__hud.update_time(self.__time_passed)
        self.__lisa = self.__hud.check_lisa_state()
        self.__check_scripts()

    def __check_scripts(self):
        # Entry script
        if (self.__current_scene == 0) and (self.__next_script == 1):
            self.__next_script = script_main_hall(self.__scenes[self.__current_scene], self.__wesker,
                                                  self.__screen, self.__clock)
            self.__wesker.change_x_velocity(0)
            self.__wesker.change_y_velocity(0)
            self.__wesker.change_y_position(ACTUAL_HEIGHT - self.__wesker.get_hitbox_rect().height)

        # East Wing Stairway script - Wesker leaves a note for Chris
        elif (self.__current_scene == 6) and (self.__next_script == 2):
            self.__next_script = script_east_wing_stairway(self.__scenes[self.__current_scene], self.__wesker,
                                                           self.__screen, self.__clock)
            self.__wesker.change_x_velocity(0)
            self.__wesker.change_y_velocity(0)
            self.__wesker.change_y_position(ACTUAL_HEIGHT - self.__wesker.get_hitbox_rect().height)

            self.__scenes[6].add_entity(Door(WIDTH // 2, 'empty_door',
                                             150, 270,
                                             6, 7, 'East Wing Storeroom',
                                             0, self.__font_special))

            self.__scenes[5].add_entity(Door(0, 'empty_door',
                                             150, 270,
                                             5, 8, 'Roofed Passage',
                                             WIDTH - 220, self.__font_special),)

        # Dark Corridor script - Wesker repairs the doorknob
        elif (self.__current_scene == 5) and (self.__next_script == 3):
            self.__next_script = script_dark_corridor(self.__scenes[self.__current_scene], self.__wesker,
                                                      self.__screen, self.__clock)
            self.__wesker.change_x_velocity(0)
            self.__wesker.change_y_velocity(0)
            self.__wesker.change_y_position(ACTUAL_HEIGHT - self.__wesker.get_hitbox_rect().height)

        # Garden Shed script - Wesker leaves a note for Chris
        elif (self.__current_scene == 9) and (self.__next_script == 4):
            self.__next_script = script_garden_shed(self.__scenes[self.__current_scene], self.__wesker,
                                                    self.__screen, self.__clock)
            self.__wesker.change_x_velocity(0)
            self.__wesker.change_y_velocity(0)
            self.__wesker.change_y_position(ACTUAL_HEIGHT - self.__wesker.get_hitbox_rect().height)

        # Guardhouse Main Corridor script - Wesker meets Chris
        elif (self.__current_scene == 25) and (self.__next_script == 5) and (self.__wesker.get_hitbox_rect().x > 640):
            self.__next_script = script_gh_corr(self.__scenes[self.__current_scene], self.__wesker,
                                                self.__screen, self.__clock)

            self.__wesker.change_x_velocity(0)
            self.__wesker.change_y_velocity(0)
            self.__wesker.change_y_position(ACTUAL_HEIGHT - self.__wesker.get_hitbox_rect().height)

            self.__scenes[11].add_entity(Door(WIDTH // 2 - 200, 'empty_door',
                                              150, 270,
                                              11, 12, 'the tunnel behind the Waterfall',
                                              0, self.__font_special))

        # Guardhouse Gallery script - Wesker hears Rebecca, decides to go to Generator Room
        elif (self.__current_scene == 27) and (self.__next_script == 6):
            self.__next_script = script_gh_gallery(self.__scenes[self.__current_scene], self.__wesker,
                                                   self.__screen, self.__clock)

            self.__wesker.change_x_velocity(0)
            self.__wesker.change_y_velocity(0)
            self.__wesker.change_y_position(ACTUAL_HEIGHT - self.__wesker.get_hitbox_rect().height)

        # Generator Room script - Wesker hides from Chris, then follows him into Enrico Room
        elif (self.__current_scene == 15) and (self.__next_script == 7) and (self.__wesker.get_hitbox_rect().x > 400):
            self.__next_script = script_generator_room(self.__scenes[self.__current_scene], self.__wesker,
                                                       self.__screen, self.__clock)

            self.__wesker.change_x_velocity(0)
            self.__wesker.change_y_velocity(0)
            self.__wesker.change_y_position(ACTUAL_HEIGHT - self.__wesker.get_hitbox_rect().height)

        # Enrico Room script - Wesker shots Enrico and runs away
        elif (self.__current_scene == 16) and (self.__next_script == 8):
            self.__next_script = script_enrico_room(self.__scenes[self.__current_scene], self.__wesker,
                                                    self.__screen, self.__clock)

            self.__wesker.change_x_velocity(0)
            self.__wesker.change_y_velocity(0)
            self.__wesker.change_y_position(ACTUAL_HEIGHT - self.__wesker.get_hitbox_rect().height)

            self.__scenes[15].delete_last_entity()
            self.__current_scene = 15
            self.__wesker.change_x_position(WIDTH - 220)
            self.__scenes[18].add_entity(Enemy(WIDTH - 300, 6))
            self.__scenes[17].add_entity(Door(WIDTH // 2 - 75, 'empty_door',
                                              150, 270,
                                              17, 18, 'Altar', 40,
                                              self.__font_special))

        # Altar before fight script - Wesker finds Lisa, Chris enters the scene, the fight starts
        elif (self.__current_scene == 18) and (self.__next_script == 9):
            self.__next_script = script_altar(self.__scenes[self.__current_scene], self.__wesker,
                                              self.__screen, self.__clock)

            self.__wesker.change_x_velocity(0)
            self.__wesker.change_y_velocity(0)
            self.__wesker.change_y_position(ACTUAL_HEIGHT - self.__wesker.get_hitbox_rect().height)

        # Altar after fight script - Wesker lets Chris go forward
        elif (self.__current_scene == 18) and (self.__next_script == 10) and not self.__lisa:
            self.__next_script = script_altar_after_fight(self.__scenes[self.__current_scene], self.__wesker,
                                                          self.__screen, self.__clock)

            self.__wesker.change_x_velocity(0)
            self.__wesker.change_y_velocity(0)
            self.__wesker.change_y_position(ACTUAL_HEIGHT - self.__wesker.get_hitbox_rect().height)

        elif (self.__current_scene == 19) and (self.__next_script == 11):
            self.__next_script = script_main_lab(self.__scenes[self.__current_scene], self.__wesker,
                                                 self.__screen, self.__clock)

            self.__wesker.change_x_velocity(0)
            self.__wesker.change_y_velocity(0)
            self.__wesker.change_y_position(ACTUAL_HEIGHT - self.__wesker.get_hitbox_rect().height)

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

        # mansion - 0
        main_hall = [
            Door(WIDTH // 2 - 75,
                 'empty_door', 150, 270,
                 0, 1, 'Graveyard', WIDTH // 2,
                 self.__font_special),
            Door(200,
                 'empty_door', 150, 270,
                 0, 17, 'Stairway Passage', 150,
                 self.__font_special),
            Door(WIDTH - 400,
                 'empty_door', 150, 270,
                 0, 17, 'Stairway Passage', WIDTH - 520,
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
            Door(WIDTH // 2,
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
            Door(0,
                 'empty_door', 150, 270,
                 11, 20, 'Zigzag Passage', WIDTH - 220,
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

        # stairway_passage - 17
        stairway_passage = [
            Door(150,
                 'empty_door', 150, 270,
                 17, 0, 'Main Hall', 200,
                 self.__font_special),
            Door(WIDTH - 300,
                 'empty_door', 150, 270,
                 17, 0, 'Main Hall', WIDTH - 350,
                 self.__font_special),
        ]

        # altar - 18
        altar = [
            Door(40,
                 'empty_door', 150, 270,
                 18, 17, 'Main Hall', WIDTH // 2 - 75,
                 self.__font_special),
            Door(WIDTH - 150,
                 'empty_door', 150, 270,
                 18, 19, 'Main Lab', 0,
                 self.__font_special)
        ]

        # main_lab - 19
        main_lab = [
            Door(0,
                 'empty_door', 150, 270,
                 19, 18, 'Altar', WIDTH - 220,
                 self.__font_special)
        ]

        # zigzag_start - 20
        zigzag_start = [
            Door(WIDTH - 200,
                 'empty_door', 150, 270,
                 20, 11, 'Falls Area', 0,
                 self.__font_special),
            Door(0,
                 'empty_door', 150, 270,
                 20, 21, 'the next part of passage', WIDTH - 220,
                 self.__font_special)
        ]

        # zigzag_end - 21
        zigzag_end = [
            Door(WIDTH - 200,
                 'empty_door', 150, 270,
                 21, 20, 'the previous part of passage', 0,
                 self.__font_special),
            Door(300,
                 'empty_door', 150, 270,
                 21, 22, 'Guardhouse', WIDTH - 220,
                 self.__font_special)
        ]

        # gh_entr_0 - 22
        gh_entr_0 = [
            Door(WIDTH - 150,
                 'empty_door', 150, 270,
                 22, 21, 'Zigzag Passage', 300,
                 self.__font_special),
            Door(WIDTH // 2,
                 'empty_door', 150, 270,
                 22, 23, 'Corridor', WIDTH - 220,
                 self.__font_special)
        ]

        # gh_entr_1 - 23
        gh_entr_1 = [
            Door(WIDTH - 150,
                 'empty_door', 150, 270,
                 23, 22, 'Entrance', WIDTH // 2,
                 self.__font_special),
            Door(WIDTH - 500,
                 'empty_door', 150, 270,
                 23, 24, 'Break Room', WIDTH - 220,
                 self.__font_special),
            Door(350,
                 'empty_door', 150, 270,
                 23, 25, 'Main Corridor', 0,
                 self.__font_special)
        ]

        # break_room - 24
        break_room = [
            Door(WIDTH - 150,
                 'empty_door', 150, 270,
                 24, 23, 'Break Room', WIDTH - 500,
                 self.__font_special)
        ]

        # gh_corr_0 - 25 (Main Corridor)
        gh_corr_0 = [
            Door(100,
                 'empty_door', 150, 270,
                 25, 23, 'Corridor', 350,
                 self.__font_special),
            Door(WIDTH - 200,
                 'empty_door', 150, 270,
                 25, 26, 'the next part of Main Corridor', WIDTH - 220,
                 self.__font_special)
        ]

        # gh_corr_1 - 26 (Main Corridor)
        gh_corr_1 = [
            Door(WIDTH - 150,
                 'empty_door', 150, 270,
                 26, 25, 'the previous part of Main Corridor', WIDTH - 220,
                 self.__font_special),
            Door(WIDTH - 500,
                 'empty_door', 150, 270,
                 26, 27, 'Gallery', 0,
                 self.__font_special)
        ]

        # gh_gallery - 27
        gh_gallery = [
            Door(0,
                 'empty_door', 150, 270,
                 27, 26, 'Main Corridor', WIDTH - 500,
                 self.__font_special)
        ]

        self.__scenes = [Scene(0, 'main_hall', main_hall,
                               self.__font_special, 100, 100),
                         Scene(1, 'graveyard_top', graveyard_top,
                               self.__font_special, 490),
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
                               self.__font_special, 0, 490),
                         Scene(8, 'roofed_passage', roofed_passage,
                               self.__font_special, 200),
                         Scene(9, 'garden_shed', garden_shed,
                               self.__font_special, 0, 420),
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
                         Scene(17, 'stairway_passage', stairway_passage,
                               self.__font_special, 140, 140),
                         Scene(18, 'altar', altar,
                               self.__font_special, 40),
                         Scene(19, 'main_lab', main_lab,
                               self.__font_special, 0, 150),
                         Scene(20, 'zigzag_start', zigzag_start,
                               self.__font_special),
                         Scene(21, 'zigzag_end', zigzag_end,
                               self.__font_special, 300),
                         Scene(22, 'gh_entr_0', gh_entr_0,
                               self.__font_special, 50),
                         Scene(23, 'gh_entr_1', gh_entr_1,
                               self.__font_special, 300),
                         Scene(24, 'break_room', break_room,
                               self.__font_special, 120),
                         Scene(25, 'gh_corr_0', gh_corr_0,
                               self.__font_special),
                         Scene(26, 'gh_corr_1', gh_corr_1,
                               self.__font_special, 300),
                         Scene(27, 'gh_gallery', gh_gallery,
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
