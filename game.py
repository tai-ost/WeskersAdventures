import pygame

from constants import WIDTH, HEIGHT, FPS, ACTUAL_HEIGHT, FLOOR_HEIGHT
from wesker import Wesker
from hud import HUD
from scenes import Scene, Door, Enemy, EnvironmentItem, ItemBox
from scripts import (script_main_hall, script_gh_corr, script_gh_gallery,
                     script_enrico_room, script_altar, script_main_lab,
                     script_east_wing_stairway, script_dark_corridor, script_garden_shed,
                     script_generator_room, script_altar_after_fight, script_end_screen, script_death)


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

        self.__icon = pygame.image.load('images/icon.png')
        pygame.display.set_icon(self.__icon)

        self.__width: int = WIDTH
        self.__height: int = HEIGHT
        self.__screensize: tuple = (self.__width, self.__height)
        self.__screen: pygame.Surface = pygame.display.set_mode(self.__screensize)

        self.__fps: int = FPS
        self.__clock: pygame.time.Clock = pygame.time.Clock()
        self.__seven_minutes: bool = True  # ... is all he can spare to play with you ;)

        self.__current_scene: int = start_scene
        self.__previous_scene: int = start_scene

        self.__current_music: str = 'mansion_theme'
        pygame.mixer.music.load(f'music/{self.__current_music}.wav')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.pause()
        self.__music_paused: bool = True

        self.__alpha_level: int = 0

        # Sounds
        self.__sound_gunshot: pygame.mixer.Sound = pygame.mixer.Sound('sounds/sound_gunshot.mp3')
        self.__sound_gunshot.set_volume(0.3)

        self.__sound_reload: pygame.mixer.Sound = pygame.mixer.Sound('sounds/sound_reload.mp3')

        self.__sound_wesker_fires: pygame.mixer.Sound = pygame.mixer.Sound('sounds/sound_wesker_fires.mp3')

        # Wesker
        self.__wesker: Wesker = Wesker(self.__sound_reload, self.__sound_wesker_fires)

        self.__sound_wesker_fires.set_volume(0.2)

        self.__lisa: bool = True
        self.__chris_moved: bool = False
        self.__altar_start: int = 0

        self.__next_script: int = 1

        self.__difficulty: None | int = None

        self.__menu: Menu
        self.__hud: HUD
        self.__font_re: pygame.font.Font
        self.__font_re_item: pygame.font.Font
        self.__font_special: pygame.font.Font
        self.__scenes: list

    def __del__(self):
        pygame.quit()

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
        if not self.__music_paused:
            pygame.mixer.music.pause()
            self.__music_paused = True

        event: pygame.event.Event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False
            elif event.type == pygame.MOUSEMOTION:
                self.__menu.check_button_hover(event.pos)
                self.__menu.check_volume_pointer(event.pos)
            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):
                self.__running = not self.__menu.check_exit_button_pressed()
                self.__menu.change_volume_pointer_state(True)
                if self.__menu.check_play_button_pressed():
                    if self.__difficulty is None:
                        self.__difficulty = 1
                        self.__menu.set_difficulty(self.__difficulty)
                        self.__prepare_scenes()
                    self.__in_menu = False
                    self.__in_menu_time = pygame.time.get_ticks() - self.__menu.get_start_time_in_menu()
                if self.__difficulty is None:
                    if self.__menu.check_dif_hard_button_pressed():
                        self.__difficulty = 2
                        self.__menu.set_difficulty(self.__difficulty)
                        self.__prepare_scenes()
                    if self.__menu.check_dif_normal_button_pressed():
                        self.__difficulty = 1
                        self.__menu.set_difficulty(self.__difficulty)
                        self.__prepare_scenes()
                    if self.__menu.check_dif_easy_button_pressed():
                        self.__difficulty = 0
                        self.__menu.set_difficulty(self.__difficulty)
                        self.__prepare_scenes()
            elif (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):
                self.__menu.change_volume_pointer_state(False)

    def __check_time(self):
        self.__time_passed = pygame.time.get_ticks() - self.__start_time - self.__in_menu_time
        self.__seven_minutes = self.__time_passed < 420_000

    def __check_events(self):
        if self.__music_paused:
            pygame.mixer.music.unpause()
            self.__music_paused = False

        self.__hud.update_ammo(self.__wesker.get_ammo())

        event: pygame.event.Event
        for event in pygame.event.get():
            if (event.type == pygame.QUIT) or (self.__next_script == 0):
                self.__running = False
            elif self.__hud.get_health_points() <= 0:
                self.__alpha_level = 255
                self.__next_script = script_death(self.__scenes[self.__current_scene], self.__screen,
                                                  self.__font_special, self.__clock)
            elif (event.type == pygame.KEYDOWN) and (event.key == pygame.K_ESCAPE):
                self.__in_menu = True
                self.__menu.change_volume_pointer_state(False)
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
                    self.__change_current_music(self.__scenes[action].get_music())
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

    def __check_logic(self):
        self.__wesker.check_wesker_logic(self.__scenes[self.__current_scene])
        self.__scenes[self.__current_scene].check_scene_logic(self.__wesker, self.__hud)
        self.__hud.check_health()
        self.__hud.update_time(self.__time_passed)
        self.__lisa = self.__hud.check_lisa_state()
        self.__check_altar()
        self.__check_scripts()

    def __check_altar(self):
        if self.__altar_start and not self.__chris_moved:
            if self.__time_passed - self.__altar_start > 15000:
                self.__scenes[18].change_background_image('altar_2')
                self.__chris_moved = True

    def __check_scripts(self):
        # Entry script
        if (self.__current_scene == 0) and (self.__next_script == 1):
            self.__next_script = script_main_hall(self.__scenes[self.__current_scene], self.__wesker,
                                                  self.__screen, self.__clock, self.__sound_gunshot)
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
            self.__scenes[20].add_entity(Enemy(WIDTH - 300, 2, self.__difficulty))
            if self.__difficulty > 0:
                self.__scenes[11].add_entity(Enemy(WIDTH // 2, 1, self.__difficulty))

        # Guardhouse Gallery script - Wesker hears Rebecca, decides to go to Generator Room
        elif (self.__current_scene == 27) and (self.__next_script == 6):
            self.__next_script = script_gh_gallery(self.__scenes[self.__current_scene], self.__wesker,
                                                   self.__screen, self.__clock)

            self.__wesker.change_x_velocity(0)
            self.__wesker.change_y_velocity(0)
            self.__wesker.change_y_position(ACTUAL_HEIGHT - self.__wesker.get_hitbox_rect().height)

        # Generator Room script - Wesker hides from Chris, then follows him into Enrico Room
        elif (self.__current_scene == 15) and (self.__next_script == 7) and (self.__wesker.get_hitbox_rect().x > 200):
            self.__next_script = script_generator_room(self.__scenes[self.__current_scene], self.__wesker,
                                                       self.__screen, self.__clock)

            self.__wesker.change_x_velocity(0)
            self.__wesker.change_y_velocity(0)
            self.__wesker.change_y_position(ACTUAL_HEIGHT - self.__wesker.get_hitbox_rect().height)

        # Enrico Room script - Wesker shots Enrico and runs away
        elif (self.__current_scene == 16) and (self.__next_script == 8):
            self.__next_script = script_enrico_room(self.__scenes[self.__current_scene], self.__wesker,
                                                    self.__screen, self.__clock, self.__sound_wesker_fires)

            self.__wesker.change_x_velocity(0)
            self.__wesker.change_y_velocity(0)
            self.__wesker.change_y_position(ACTUAL_HEIGHT - self.__wesker.get_hitbox_rect().height)

            self.__scenes[15].delete_last_entity()
            self.__current_scene = 15
            self.__wesker.change_x_position(WIDTH - 220)
            self.__scenes[17].add_entity(Door(WIDTH // 2 - 75, 'empty_door',
                                              150, 270,
                                              17, 18, 'Altar', 40,
                                              self.__font_special))
            self.__scenes[5].add_entity(Enemy(WIDTH // 2, 3, self.__difficulty))
            self.__scenes[6].add_entity(Enemy(200, 3, self.__difficulty))
            self.__scenes[3].add_entity(Enemy(200, 3, self.__difficulty))

        # Altar before fight script - Wesker finds Lisa, Chris enters the scene, the fight starts
        elif (self.__current_scene == 18) and (self.__next_script == 9):
            self.__next_script = script_altar(self.__scenes[self.__current_scene], self.__wesker,
                                              self.__screen, self.__clock)

            self.__wesker.change_x_velocity(0)
            self.__wesker.change_y_velocity(0)
            self.__wesker.change_y_position(ACTUAL_HEIGHT - self.__wesker.get_hitbox_rect().height)
            self.__altar_start = pygame.time.get_ticks()
            self.__scenes[18].change_background_image('altar_1')

        # Altar after fight script - Wesker lets Chris go forward
        elif (self.__current_scene == 18) and (self.__next_script == 10) and not self.__lisa:
            self.__scenes[18].change_background_image('altar_3')
            self.__chris_moved = True

            self.__next_script = script_altar_after_fight(self.__scenes[self.__current_scene], self.__wesker,
                                                          self.__screen, self.__clock)

            self.__wesker.change_x_velocity(0)
            self.__wesker.change_y_velocity(0)
            self.__wesker.change_y_position(ACTUAL_HEIGHT - self.__wesker.get_hitbox_rect().height)

            self.__scenes[18].add_entity(Door(40, 'empty_door', 150, 270,
                                              18, 17, 'Main Hall', WIDTH // 2 - 75,
                                              self.__font_special))
            self.__scenes[18].add_entity(Door(WIDTH - 150, 'empty_door', 150, 270,
                                              18, 19, 'Main Lab', 0,
                                              self.__font_special))

        # Main Lab script
        elif (self.__current_scene == 19) and (self.__next_script == 11):
            self.__next_script = script_main_lab(self.__scenes[self.__current_scene], self.__wesker,
                                                 self.__screen, self.__clock, self.__sound_wesker_fires)

            self.__scenes[self.__current_scene].change_background_image('black_screen')

            self.__wesker.change_x_velocity(0)
            self.__wesker.change_y_velocity(0)
            self.__wesker.change_y_position(ACTUAL_HEIGHT - self.__wesker.get_hitbox_rect().height)

        # End screen script
        elif self.__next_script == 12:
            self.__alpha_level = 255
            self.__next_script = script_end_screen(self.__screen, self.__time_passed, self.__seven_minutes,
                                                   self.__font_special_caption, self.__clock)

    def __move(self):
        self.__wesker.move()

    def __draw(self):
        self.__draw_scene()
        self.__draw_characters()
        self.__draw_overlay()
        self.__draw_hud()
        self.__draw_darkness()

        pygame.display.flip()

    def __draw_scene(self):
        self.__draw_floor()
        self.__scenes[self.__current_scene].draw(self.__screen, self.__wesker)

    def __draw_floor(self):
        floor_color = (0, 0, 0)
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

    def __draw_overlay(self):
        self.__scenes[self.__current_scene].draw_overlay(self.__screen)

    def __draw_hud(self):
        self.__hud.draw_hud(self.__screen)

    def __change_current_music(self, new_music):
        if new_music != self.__current_music:
            self.__current_music = new_music
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            pygame.mixer.music.load(f'music/{self.__current_music}.wav')
            pygame.mixer.music.play(-1)

    def __change_current_scene(self, next_scene):
        self.__previous_scene = self.__current_scene
        self.__current_scene = next_scene

    def prepare_game(self):
        self.__prepare_font()
        self.__prepare_menu()
        self.__prepare_hud()

    def __prepare_font(self):
        self.__font_special = pygame.font.Font('fonts/SpecialElite-Regular.ttf', 22)
        self.__font_special_menu = pygame.font.Font('fonts/SpecialElite-Regular.ttf', 40)
        self.__font_special_caption = pygame.font.Font('fonts/SpecialElite-Regular.ttf', 50)
        self.__font_controls = pygame.font.Font('fonts/SpecialElite-Regular.ttf', 20)

    def __prepare_menu(self):
        self.__menu = Menu(self.__font_special_menu, self.__font_special_caption, self.__font_controls)
        self.__menu.update_start_time(self.__time_passed)

    def __prepare_hud(self):
        self.__hud = HUD(self.__font_special)

    def __prepare_scenes(self):
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
            Door(300,
                 'empty_door', 150, 270,
                 2, 3, 'Large Gallery', 0,
                 self.__font_special),
            EnvironmentItem(20, ACTUAL_HEIGHT - 100, 2, self.__font_special),
            Enemy(300, 0, self.__difficulty)
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
                 self.__font_special),
            EnvironmentItem(WIDTH // 2 + 50, ACTUAL_HEIGHT - 105, 5, self.__font_special),
            Enemy(WIDTH - 150, 0, self.__difficulty)
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
                 self.__font_special),
            EnvironmentItem(WIDTH // 4, ACTUAL_HEIGHT - 155, 6, self.__font_special),
            ItemBox(self.__font_special)
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
                 self.__font_special),
            Enemy(300, 1, self.__difficulty)
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
                 self.__font_special),
            EnvironmentItem(WIDTH // 2 - 300, ACTUAL_HEIGHT - 80, 1, self.__font_special),
            EnvironmentItem(WIDTH // 2 + 58, ACTUAL_HEIGHT - 163, 6, self.__font_special),
            EnvironmentItem(80, ACTUAL_HEIGHT - 214, 5, self.__font_special)
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
                 self.__font_special),
            EnvironmentItem(WIDTH - 100, ACTUAL_HEIGHT - 100, 3, self.__font_special)
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
                 self.__font_special),
            EnvironmentItem(100, ACTUAL_HEIGHT - 100, 4, self.__font_special),
            Enemy(150, 1, self.__difficulty)
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
                 self.__font_special),
            Enemy(200, 3, self.__difficulty)
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
                 self.__font_special),
            Enemy(WIDTH - 300, 3, self.__difficulty)
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
                 self.__font_special)
        ]

        # altar - 18
        altar = [
            Enemy(WIDTH - 300, 4, self.__difficulty)
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
                 self.__font_special),
            Enemy(400, 2, self.__difficulty)
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
                 self.__font_special),
            Enemy(WIDTH // 2, 2, self.__difficulty)
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
                 self.__font_special),
            EnvironmentItem(150, ACTUAL_HEIGHT - 100 - 82, 4, self.__font_special)
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
                 self.__font_special),
            Enemy(300, 0, self.__difficulty)
        ]

        # break_room - 24
        break_room = [
            Door(WIDTH - 150,
                 'empty_door', 150, 270,
                 24, 23, 'Break Room', WIDTH - 500,
                 self.__font_special),
            EnvironmentItem(WIDTH // 2 + 100, ACTUAL_HEIGHT - 178, 6, self.__font_special),
            EnvironmentItem(WIDTH // 2 - 180, ACTUAL_HEIGHT - 140, 5, self.__font_special),
            EnvironmentItem(150, ACTUAL_HEIGHT - 80, 1, self.__font_special)
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
                               self.__font_special, 'mansion_theme', 100, 100),
                         Scene(1, 'graveyard_top', graveyard_top,
                               self.__font_special, 'mansion_theme', 490, overlay_image=True),
                         Scene(2, 'graveyard_bottom', graveyard_bottom,
                               self.__font_special, 'mansion_theme'),
                         Scene(3, 'large_gallery_front', large_gallery_front,
                               self.__font_special, 'mansion_theme'),
                         Scene(4, 'large_gallery_back', large_gallery_back,
                               self.__font_special, 'mansion_theme', overlay_image=True),
                         Scene(5, 'dark_corridor', dark_corridor,
                               self.__font_special, 'mansion_theme', 50),
                         Scene(6, 'east_wing_stairway', east_wing_stairway,
                               self.__font_special, 'mansion_theme', overlay_image=True),
                         Scene(7, 'east_wing_storeroom', east_wing_storeroom,
                               self.__font_special, 'save_theme', 0, 490, overlay_image=True),
                         Scene(8, 'roofed_passage', roofed_passage,
                               self.__font_special, 'mansion_theme', 200, overlay_image=True),
                         Scene(9, 'garden_shed', garden_shed,
                               self.__font_special, 'garden_theme', 0, 420),
                         Scene(10, 'main_garden', main_garden,
                               self.__font_special, 'garden_theme', overlay_image=True),
                         Scene(11, 'falls_area', falls_area,
                               self.__font_special, 'garden_theme', 0, 100, overlay_image=True),
                         Scene(12, 'fall_tunnel', fall_tunnel,
                               self.__font_special, 'tunnel_theme'),
                         Scene(13, 'mining_area', mining_area,
                               self.__font_special, 'tunnel_theme'),
                         Scene(14, 'forked_passage', forked_passage,
                               self.__font_special, 'tunnel_theme'),
                         Scene(15, 'generator_room', generator_room,
                               self.__font_special, 'tunnel_theme'),
                         Scene(16, 'enrico_room', enrico_room,
                               self.__font_special, 'tunnel_theme'),
                         Scene(17, 'stairway_passage', stairway_passage,
                               self.__font_special, 'mansion_theme', 140, 140),
                         Scene(18, 'altar_0', altar,
                               self.__font_special, 'altar_theme', 40, 30, overlay_image=True),
                         Scene(19, 'main_lab_fine', main_lab,
                               self.__font_special, 'lab_theme', 0, 150, overlay_image=True),
                         Scene(20, 'zigzag_start', zigzag_start,
                               self.__font_special, 'garden_theme'),
                         Scene(21, 'zigzag_end', zigzag_end,
                               self.__font_special, 'garden_theme', 300),
                         Scene(22, 'gh_entr_0', gh_entr_0,
                               self.__font_special, 'gh_theme'),
                         Scene(23, 'gh_entr_1', gh_entr_1,
                               self.__font_special, 'gh_theme'),
                         Scene(24, 'break_room', break_room,
                               self.__font_special, 'save_theme', 120),
                         Scene(25, 'gh_corr_0', gh_corr_0,
                               self.__font_special, 'gh_theme'),
                         Scene(26, 'gh_corr_1', gh_corr_1,
                               self.__font_special, 'gh_theme'),
                         Scene(27, 'gh_gallery', gh_gallery,
                               self.__font_special, 'gh_theme'),
                         ]

        if self.__difficulty < 2:
            self.__scenes[27].add_entity(EnvironmentItem(WIDTH // 2 + 110, ACTUAL_HEIGHT - 187, 1,
                                                         self.__font_special))
        if self.__difficulty == 0:
            self.__scenes[22].add_entity(EnvironmentItem(WIDTH // 2 - 190, ACTUAL_HEIGHT - 100, 2,
                                                         self.__font_special))
            self.__scenes[24].add_entity(EnvironmentItem(WIDTH - 200, ACTUAL_HEIGHT - 100, 3,
                                                         self.__font_special))


class Menu:
    def __init__(self, font_buttons: pygame.font.Font, font_caption: pygame.font.Font, font_controls: pygame.font.Font):
        self.__background_rect: pygame.Rect = pygame.Rect(0, 0, WIDTH, HEIGHT)

        self.__start_time_in_menu: int = 0

        self.__font_buttons: pygame.font.Font = font_buttons
        self.__font_caption: pygame.font.Font = font_caption
        self.__font_controls: pygame.font.Font = font_controls

        # Caption
        self.__caption_color: pygame.Color = pygame.Color(250, 250, 250)
        self.__caption_text: pygame.Surface = self.__font_caption.render('Wesker\'s Adventures',
                                                                         1, self.__caption_color)
        self.__caption_rect: pygame.Rect = self.__caption_text.get_rect()
        self.__caption_rect.x = WIDTH // 2 - self.__caption_rect.width // 2
        self.__caption_rect.y = HEIGHT // 4

        # Buttons
        self.__button_color_idle: pygame.Color = pygame.Color(150, 150, 150)
        self.__button_color_hover: pygame.Color = pygame.Color(230, 230, 230)

        self.__play_button_state: bool = False
        self.__play_button_surface: pygame.Surface = self.__font_buttons.render('Play',
                                                                                1, self.__button_color_idle)
        self.__play_button_rect: pygame.Rect = self.__play_button_surface.get_rect()
        self.__play_button_rect.x = WIDTH // 2 - self.__play_button_rect.width // 2
        self.__play_button_rect.y = HEIGHT // 2 - self.__play_button_rect.height // 2

        self.__exit_button_state: bool = False
        self.__exit_button_surface: pygame.Surface = self.__font_buttons.render('Exit',
                                                                                1, self.__button_color_idle)
        self.__exit_button_rect: pygame.Rect = self.__exit_button_surface.get_rect()
        self.__exit_button_rect.x = WIDTH // 2 - self.__exit_button_rect.width // 2
        self.__exit_button_rect.y = self.__play_button_rect.y + 50

        # Volume
        self.__volume: float = 0.5
        pygame.mixer.music.set_volume(self.__volume)

        self.__slider_rect: pygame.Rect = pygame.Rect(150, HEIGHT // 2, 200, 20)
        self.__slider_color = pygame.Color(80, 80, 80)
        self.__pointer_rect: pygame.Rect = pygame.Rect(int(self.__volume * 100 * 2) + self.__slider_rect.x - 5,
                                                       HEIGHT // 2 - 5, 10, 30)
        self.__pointer_color = pygame.Color(120, 120, 120)
        self.__pointer_state = False

        self.__volume_text_surface: pygame.Surface = self.__font_controls.render(
            f'Volume: {int(self.__volume * 100)}%', 1, self.__button_color_idle)
        self.__volume_text_rect: pygame.Rect = self.__volume_text_surface.get_rect()
        self.__volume_text_rect.x = (self.__slider_rect.x + self.__slider_rect.width // 2 -
                                     self.__volume_text_rect.width // 2)
        self.__volume_text_rect.y = self.__slider_rect.y + self.__slider_rect.height + 15

        # Difficulty
        self.__difficulty: None | int = None

        self.__dif_surface: pygame.Surface = self.__font_controls.render('Difficulty:',
                                                                         1, self.__button_color_idle)
        self.__dif_rect: pygame.Rect = self.__dif_surface.get_rect()
        self.__dif_rect.x = WIDTH - 350
        self.__dif_rect.y = HEIGHT // 2 - 40

        self.__hard_button_state = False
        self.__hard_button_surface: pygame.Surface = self.__font_controls.render('Hard',
                                                                                 1, self.__button_color_idle)
        self.__hard_button_rect: pygame.Rect = self.__hard_button_surface.get_rect()
        self.__hard_button_rect.x = self.__dif_rect.x
        self.__hard_button_rect.y = self.__dif_rect.y + 30

        self.__normal_button_state = False
        self.__normal_button_surface: pygame.Surface = self.__font_controls.render('Normal',
                                                                                   1, self.__button_color_idle)
        self.__normal_button_rect: pygame.Rect = self.__normal_button_surface.get_rect()
        self.__normal_button_rect.x = self.__dif_rect.x
        self.__normal_button_rect.y = self.__hard_button_rect.y + 30

        self.__easy_button_state = False
        self.__easy_button_surface: pygame.Surface = self.__font_controls.render('Easy',
                                                                                 1, self.__button_color_idle)
        self.__easy_button_rect: pygame.Rect = self.__easy_button_surface.get_rect()
        self.__easy_button_rect.x = self.__dif_rect.x
        self.__easy_button_rect.y = self.__normal_button_rect.y + 30

        self.__dif_set_surface: pygame.Surface = self.__font_controls.render('Normal',
                                                                             1, self.__button_color_idle)
        self.__dif_set_rect: pygame.Rect = pygame.Rect(1, 1, 1, 1)

        # Controls
        self.__wasd_image: pygame.Surface = pygame.transform.scale(
            pygame.image.load(f'images/hud_img/other/wasd.png').convert_alpha(),
            (140, 90),
        )
        self.__wasd_rect: pygame.Rect = pygame.Rect(WIDTH // 4 - 70, HEIGHT - 200, 140, 90)
        self.__wasd_text_surface: pygame.Surface = self.__font_controls.render('Movement',
                                                                               1, self.__button_color_idle)
        self.__wasd_text_rect: pygame.Rect = self.__wasd_text_surface.get_rect()
        self.__wasd_text_rect.x = self.__wasd_rect.x + self.__wasd_rect.width // 2 - self.__wasd_text_rect.width // 2
        self.__wasd_text_rect.y = self.__wasd_rect.y + self.__wasd_rect.height + 10

        self.__c_image: pygame.Surface = pygame.transform.scale(
            pygame.image.load(f'images/hud_img/other/c.png').convert_alpha(),
            (40, 40),
        )
        self.__c_rect: pygame.Rect = pygame.Rect(WIDTH // 2 - 20, HEIGHT - 200, 40, 40)
        self.__c_text_surface: pygame.Surface = self.__font_controls.render('Combine herbs',
                                                                            1, self.__button_color_idle)
        self.__c_text_rect: pygame.Rect = self.__c_text_surface.get_rect()
        self.__c_text_rect.x = self.__c_rect.x + self.__c_rect.width // 2 - self.__c_text_rect.width // 2
        self.__c_text_rect.y = self.__c_rect.y + self.__c_rect.height + 10

        self.__u_image: pygame.Surface = pygame.transform.scale(
            pygame.image.load(f'images/hud_img/other/u.png').convert_alpha(),
            (40, 40),
        )
        self.__u_rect: pygame.Rect = pygame.Rect(WIDTH // 2 - 100, self.__c_text_rect.y + 30, 40, 40)
        self.__u_text_surface: pygame.Surface = self.__font_controls.render('Use the item',
                                                                            1, self.__button_color_idle)
        self.__u_text_rect: pygame.Rect = self.__u_text_surface.get_rect()
        self.__u_text_rect.x = self.__u_rect.x + self.__u_rect.width // 2 - self.__u_text_rect.width // 2
        self.__u_text_rect.y = self.__u_rect.y + self.__u_rect.height + 10

        self.__h_image: pygame.Surface = pygame.transform.scale(
            pygame.image.load(f'images/hud_img/other/h.png').convert_alpha(),
            (40, 40),
        )
        self.__h_rect: pygame.Rect = pygame.Rect(WIDTH // 2 + 60, self.__c_text_rect.y + 30, 40, 40)
        self.__h_text_surface: pygame.Surface = self.__font_controls.render('Hide\\show HUD',
                                                                            1, self.__button_color_idle)
        self.__h_text_rect: pygame.Rect = self.__h_text_surface.get_rect()
        self.__h_text_rect.x = self.__h_rect.x + self.__h_rect.width // 2 - self.__h_text_rect.width // 2
        self.__h_text_rect.y = self.__h_rect.y + self.__h_rect.height + 10

        self.__rmb_image: pygame.Surface = pygame.transform.scale(
            pygame.image.load(f'images/hud_img/other/rmb.png').convert_alpha(),
            (60, 80),
        )
        self.__rmb_rect: pygame.Rect = pygame.Rect(WIDTH - WIDTH // 4 - 100, HEIGHT - 200, 60, 80)
        self.__rmb_text_surface: pygame.Surface = self.__font_controls.render('Aim',
                                                                              1, self.__button_color_idle)
        self.__rmb_text_rect: pygame.Rect = self.__rmb_text_surface.get_rect()
        self.__rmb_text_rect.x = self.__rmb_rect.x + self.__rmb_rect.width // 2 - self.__rmb_text_rect.width // 2
        self.__rmb_text_rect.y = self.__rmb_rect.y + self.__rmb_rect.height + 10

        self.__lmb_image: pygame.Surface = pygame.transform.scale(
            pygame.image.load(f'images/hud_img/other/lmb.png').convert_alpha(),
            (60, 80),
        )
        self.__lmb_rect: pygame.Rect = pygame.Rect(self.__rmb_rect.x + self.__rmb_rect.width + 20, self.__rmb_rect.y,
                                                   60, 80)
        self.__lmb_text_surface: pygame.Surface = self.__font_controls.render('Fire',
                                                                              1, self.__button_color_idle)
        self.__lmb_text_rect: pygame.Rect = self.__lmb_text_surface.get_rect()
        self.__lmb_text_rect.x = self.__lmb_rect.x + self.__lmb_rect.width // 2 - self.__lmb_text_rect.width // 2
        self.__lmb_text_rect.y = self.__lmb_rect.y + self.__lmb_rect.height + 10

        self.__r_image: pygame.Surface = pygame.transform.scale(
            pygame.image.load(f'images/hud_img/other/r.png').convert_alpha(),
            (40, 40),
        )
        self.__r_rect: pygame.Rect = pygame.Rect(self.__lmb_rect.x + self.__lmb_rect.width + 40, self.__rmb_rect.y + 20,
                                                 40, 40)
        self.__r_text_surface: pygame.Surface = self.__font_controls.render('Reload',
                                                                            1, self.__button_color_idle)
        self.__r_text_rect: pygame.Rect = self.__r_text_surface.get_rect()
        self.__r_text_rect.x = self.__r_rect.x + self.__r_rect.width // 2 - self.__r_text_rect.width // 2
        self.__r_text_rect.y = self.__r_rect.y + self.__r_rect.height + 10

        self.__esc_image: pygame.Surface = pygame.transform.scale(
            pygame.image.load(f'images/hud_img/other/esc.png').convert_alpha(),
            (50, 40),
        )
        self.__esc_rect: pygame.Rect = pygame.Rect(WIDTH - 300, 20, 50, 40)
        self.__esc_text_surface: pygame.Surface = self.__font_controls.render('Return to menu (Pause)',
                                                                              1, self.__button_color_idle)
        self.__esc_text_rect: pygame.Rect = self.__esc_text_surface.get_rect()
        self.__esc_text_rect.x = self.__esc_rect.x + self.__esc_rect.width + 10
        self.__esc_text_rect.y = self.__esc_rect.y + self.__esc_rect.height // 2 - self.__esc_text_rect.height // 2 + 2

    def change_volume_pointer_state(self, state):
        self.__pointer_state = state

    def check_volume_pointer(self, mouse_pos):
        if self.__pointer_state:
            mouse_x, mouse_y = mouse_pos
            if (self.__pointer_rect.y < mouse_y < self.__pointer_rect.y + self.__pointer_rect.height) and \
                    (150 < mouse_x < 350):
                self.__pointer_rect.x = mouse_x
                self.__volume = ((self.__pointer_rect.x - 150) // 2) * 0.01

            if self.__pointer_rect.x < 150:
                self.__pointer_rect.x = 150
            if self.__pointer_rect.x > 350:
                self.__pointer_rect.x = 350

            pygame.mixer.music.set_volume(self.__volume)
            self.__volume_text_surface = self.__font_controls.render(f'Volume: {int(self.__volume * 100)}%',
                                                                     1, self.__button_color_idle)

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

        if self.__difficulty is None:
            if self.__hard_button_rect.collidepoint(mouse_pos):
                self.__hard_button_surface = self.__font_controls.render('Hard', 1, self.__button_color_hover)
                self.__hard_button_state = True
            else:
                self.__hard_button_surface = self.__font_controls.render('Hard', 1, self.__button_color_idle)
                self.__hard_button_state = False

            if self.__normal_button_rect.collidepoint(mouse_pos):
                self.__normal_button_surface = self.__font_controls.render('Normal', 1, self.__button_color_hover)
                self.__normal_button_state = True
            else:
                self.__normal_button_surface = self.__font_controls.render('Normal', 1, self.__button_color_idle)
                self.__normal_button_state = False

            if self.__easy_button_rect.collidepoint(mouse_pos):
                self.__easy_button_surface = self.__font_controls.render('Easy', 1, self.__button_color_hover)
                self.__easy_button_state = True
            else:
                self.__easy_button_surface = self.__font_controls.render('Easy', 1, self.__button_color_idle)
                self.__easy_button_state = False

    def check_play_button_pressed(self):
        return self.__play_button_state

    def check_exit_button_pressed(self):
        return self.__exit_button_state

    def check_dif_hard_button_pressed(self):
        return self.__hard_button_state

    def check_dif_normal_button_pressed(self):
        return self.__normal_button_state

    def check_dif_easy_button_pressed(self):
        return self.__easy_button_state

    def set_difficulty(self, difficulty: int):
        self.__difficulty = difficulty

        self.__hard_button_state = False
        self.__normal_button_state = False
        self.__easy_button_state = False

        self.__dif_rect.y += 55
        self.__dif_set_rect.x = self.__dif_rect.x + self.__dif_rect.width + 5
        self.__dif_set_rect.y = self.__dif_rect.y
        if difficulty == 0:
            self.__dif_set_surface = self.__font_controls.render('Easy', 1, self.__button_color_idle)
            self.__dif_set_rect.width = self.__easy_button_surface.get_rect().width
            self.__dif_set_rect.height = self.__easy_button_surface.get_rect().height
        elif difficulty == 1:
            self.__dif_set_rect.width = self.__normal_button_surface.get_rect().width
            self.__dif_set_rect.height = self.__normal_button_surface.get_rect().height
        elif difficulty == 2:
            self.__dif_set_surface = self.__font_controls.render('Hard', 1, self.__button_color_idle)
            self.__dif_set_rect.width = self.__hard_button_surface.get_rect().width
            self.__dif_set_rect.height = self.__hard_button_surface.get_rect().height

    def update_start_time(self, time: int):
        self.__start_time_in_menu = time

    def get_start_time_in_menu(self):
        return self.__start_time_in_menu

    def __draw_background(self, screen: pygame.Surface):
        pygame.draw.rect(screen, (50, 50, 50), self.__background_rect)

    def __show_caption(self, screen: pygame.Surface):
        screen.blit(self.__caption_text, self.__caption_rect)

    def __show_controls(self, screen: pygame.Surface):
        screen.blit(self.__wasd_image, self.__wasd_rect)
        screen.blit(self.__c_image, self.__c_rect)
        screen.blit(self.__u_image, self.__u_rect)
        screen.blit(self.__h_image, self.__h_rect)
        screen.blit(self.__rmb_image, self.__rmb_rect)
        screen.blit(self.__lmb_image, self.__lmb_rect)
        screen.blit(self.__r_image, self.__r_rect)
        screen.blit(self.__esc_image, self.__esc_rect)

        screen.blit(self.__wasd_text_surface, self.__wasd_text_rect)
        screen.blit(self.__c_text_surface, self.__c_text_rect)
        screen.blit(self.__u_text_surface, self.__u_text_rect)
        screen.blit(self.__h_text_surface, self.__h_text_rect)
        screen.blit(self.__rmb_text_surface, self.__rmb_text_rect)
        screen.blit(self.__lmb_text_surface, self.__lmb_text_rect)
        screen.blit(self.__r_text_surface, self.__r_text_rect)
        screen.blit(self.__esc_text_surface, self.__esc_text_rect)

    def __show_buttons(self, screen: pygame.Surface):
        screen.blit(self.__play_button_surface, self.__play_button_rect)
        screen.blit(self.__exit_button_surface, self.__exit_button_rect)

    def __show_difficulty(self, screen: pygame.Surface):
        screen.blit(self.__dif_surface, self.__dif_rect)
        if self.__difficulty is None:
            screen.blit(self.__hard_button_surface, self.__hard_button_rect)
            screen.blit(self.__normal_button_surface, self.__normal_button_rect)
            screen.blit(self.__easy_button_surface, self.__easy_button_rect)
        else:
            screen.blit(self.__dif_set_surface, self.__dif_set_rect)

    def __show_volume_slider(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self.__slider_color, self.__slider_rect)
        pygame.draw.rect(screen, self.__pointer_color, self.__pointer_rect)
        screen.blit(self.__volume_text_surface, self.__volume_text_rect)

    def draw_menu(self, screen: pygame.Surface):
        self.__draw_background(screen)
        self.__show_controls(screen)
        self.__show_caption(screen)
        self.__show_buttons(screen)
        self.__show_difficulty(screen)
        self.__show_volume_slider(screen)

        pygame.display.flip()
