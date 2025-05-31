import pygame


from constants import WIDTH, HEIGHT, ACTUAL_HEIGHT, FLOOR_HEIGHT, ENEMY_TYPES, ITEM_TYPES, FPS
from wesker import Wesker
from hud import HUD


class Scene:
    def __init__(self, scene_id: int, background_image: str, entities: list, font: pygame.font.Font, music: str,
                 left_wall_width: int = 0, right_wall_width: int = 0, overlay_image: bool = False):
        self.__scene_id: int = scene_id
        self.__background_image: pygame.Surface = pygame.transform.scale(
            pygame.image.load(f'images/background_img/{background_image}.png').convert_alpha(),
            (WIDTH, ACTUAL_HEIGHT),
        )

        self.__overlay: bool = overlay_image
        if self.__overlay:
            self.__overlay_image: pygame.Surface = pygame.transform.scale(
                pygame.image.load(f'images/background_img/{background_image}_overlay.png').convert_alpha(),
                (WIDTH, ACTUAL_HEIGHT),
            )

        self.__left_wall_width: int = left_wall_width
        self.__right_wall_width: int = right_wall_width

        self.__background_rect: pygame.Rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
        self.__entities: list = entities

        self.__font: pygame.font.Font = font
        self.__music: str = music

    def get_left_wall(self):
        return self.__left_wall_width

    def get_right_wall(self):
        return self.__right_wall_width

    def add_entity(self, entity):
        self.__entities.append(entity)

    def delete_last_entity(self):
        self.__entities.pop()

    def get_entities(self):
        return self.__entities

    def get_music(self):
        return self.__music

    def check_scene_event(self, wesker: Wesker, hud: HUD, event_key):
        entity: Door | Enemy | EnvironmentItem | ItemBox | Kitty
        for entity in self.__entities:
            if entity.entity_type == 'door' and entity.scene_change_allowed() and event_key == pygame.K_f:
                wesker.change_x_position(entity.go_to_x_coords)
                return 1, entity.go_to_scene_id
            elif entity.entity_type == 'item' and entity.taking_allowed() and \
                    (hud.inventory_empty_slot() != 5) and event_key == pygame.K_t:
                entity.get_taken()
                hud.add_item(entity.get_item_type(), hud.inventory_empty_slot())
            elif entity.entity_type == 'kitty' and entity.kitty_power() and event_key == pygame.K_t:
                entity.kitty_change_state()
                wesker.kitty()
            elif entity.entity_type == 'item_box' and entity.box_active() and event_key == pygame.K_t:
                entity.get_opened()
                self.add_entity(Kitty(self.__font))
        return 0, 0

    def check_scene_logic(self, wesker: Wesker, hud: HUD):
        entity: Door | Enemy | EnvironmentItem
        for entity in self.__entities:
            entity.check_entity_logic(wesker, hud)
            if entity.entity_type == 'enemy' and entity.get_name() == 'lisa_trevor' and not entity.is_alive():
                hud.update_lisa_state(False)
        wesker.have_fired = False

    def draw(self, screen, wesker: Wesker):
        self.__draw_background(screen)
        self.__draw_entities(screen, wesker)

    def draw_overlay(self, screen: pygame.Surface):
        if self.__overlay:
            screen.blit(self.__overlay_image, self.__background_rect)

    def draw_for_script(self, screen: pygame.Surface):
        self.__draw_background(screen)

    def change_background_image(self, background_image: str):
        self.__background_image = pygame.transform.scale(
            pygame.image.load(f'images/background_img/{background_image}.png').convert_alpha(),
            (WIDTH, ACTUAL_HEIGHT),
        )

        if self.__overlay:
            self.__overlay_image = pygame.transform.scale(
                pygame.image.load(f'images/background_img/{background_image}_overlay.png').convert_alpha(),
                (WIDTH, ACTUAL_HEIGHT),
            )

    def __draw_background(self, screen: pygame.Surface):
        screen.blit(self.__background_image, self.__background_rect)

    def __draw_entities(self, screen: pygame.Surface, wesker: Wesker):
        entity: Door | Enemy | EnvironmentItem
        for entity in self.__entities:
            entity.draw_entity(screen, wesker)


class Enemy:
    def __init__(self, x: int, enemy_type: int, difficulty: int):
        self.entity_type: str = 'enemy'

        self.__name: str = ENEMY_TYPES[enemy_type][0]

        self.__health: int = ENEMY_TYPES[enemy_type][1] + difficulty
        self.__dmg: int = ENEMY_TYPES[enemy_type][2] + (difficulty * 5 if self.__name != 'adder' else 0)
        self.__velocity: int = ENEMY_TYPES[enemy_type][3]
        self.__is_poisonous: bool = ENEMY_TYPES[enemy_type][4]

        self.__width: int = ENEMY_TYPES[enemy_type][5]
        self.__height: int = ENEMY_TYPES[enemy_type][6]

        self.__x: int = x
        self.__y: int = ACTUAL_HEIGHT - self.__height

        self.__rect: pygame.Rect = pygame.Rect(self.__x, self.__y, self.__width, self.__height)

        self.__direction: int = 0  # 0 - right, 1 - left
        self.__last_frame: int = 0
        self.__last_frame_count: int = 0

        self.__alive: bool = True

    def get_x(self):
        return self.__rect.x

    def get_name(self):
        return self.__name

    def is_alive(self):
        return self.__alive

    def __get_damage(self):
        self.__health -= 1
        self.__last_frame = 2
        if not self.__health > 0:
            self.__alive = False
            self.__rect = pygame.Rect(self.__rect.x, ACTUAL_HEIGHT - 100, 250, 100)

    def __check_getting_damage(self, wesker: Wesker):
        if wesker.have_fired:
            shot_direction = wesker.get_last_direction()
            if (shot_direction and (wesker.get_hitbox_rect().x > self.__rect.x)) or \
                    (not shot_direction and (wesker.get_hitbox_rect().x < self.__rect.x)):
                self.__get_damage()

    def __check_enemy_movement(self, wesker: Wesker):
        if self.__alive:
            self.__direction = wesker.get_hitbox_rect().x < self.__rect.x
            if (pygame.time.get_ticks() - self.__last_frame_count) > 450:
                self.__last_frame_count = pygame.time.get_ticks()
                self.__last_frame = not self.__last_frame
            self.__rect.x += self.__velocity * ((-1) ** self.__direction)

    def __check_enemy_collision(self, wesker: Wesker, hud: HUD):
        if self.__alive and self.__rect.colliderect(wesker.get_hitbox_rect()):
            hud.get_damage(self.__dmg, self.__is_poisonous)

    def check_entity_logic(self, wesker: Wesker, hud: HUD):
        self.__check_getting_damage(wesker)
        self.__check_enemy_movement(wesker)
        self.__check_enemy_collision(wesker, hud)

    def __load_image(self):
        if self.__alive:
            image = pygame.transform.scale(
                pygame.image.load(
                    f'images/entity_img/enemy_img/{self.__name}_{int(self.__direction)}_{int(self.__last_frame)}.png'
                ).convert_alpha(),
                (self.__width, self.__height),
            )
        else:
            image = pygame.transform.scale(
                pygame.image.load(
                    f'images/entity_img/enemy_img/{self.__name}_dead_{int(self.__direction)}.png'
                ).convert_alpha(),
                (250, 100),
            )
        return image

    def draw_entity(self, screen: pygame.Surface, _):
        screen.blit(self.__load_image(), self.__rect)


class EnvironmentItem:
    def __init__(self, x: int, y: int, item_type: int, font: pygame.font.Font):
        self.entity_type: str = 'item'
        self.__item_type: int = item_type
        self.__item_name: str = ITEM_TYPES[item_type][0]

        self.__width: int = ITEM_TYPES[item_type][1]
        self.__height: int = ITEM_TYPES[item_type][2]

        self.__prompt_text: str = f'Take {ITEM_TYPES[item_type][3]}'
        self.__prompt_color: pygame.Color = pygame.Color(250, 250, 250)

        self.__x: int = x
        self.__y: int = y
        self.__rect: pygame.Rect = pygame.Rect(self.__x, self.__y, self.__width, self.__height)

        self.__font: pygame.font.Font = font
        self.__taken: bool = False
        self.__action: bool = False

    def check_entity_logic(self, wesker: Wesker, _):
        self.__check_item_collision(wesker)

    def __check_item_collision(self, wesker: Wesker):
        if self.__rect.colliderect(wesker.get_hitbox_rect()):
            self.__action = True
        else:
            self.__action = False

    def taking_allowed(self):
        return self.__action

    def get_taken(self):
        self.__taken = True
        self.__action = False

    def get_item_type(self):
        return self.__item_type

    def __show_prompt(self, screen: pygame.Surface, wesker: Wesker):
        button_x, button_y = wesker.get_hitbox_rect().x, wesker.get_hitbox_rect().y
        button_rect = pygame.Rect(button_x - 50, button_y - 50, 50, 50)
        button_image = pygame.transform.scale(
            pygame.image.load(f'images/entity_img/env_item_img/key_t.png').convert_alpha(),
            (40, 40),
        )

        prompt_surface = self.__font.render(self.__prompt_text, 1, self.__prompt_color)
        prompt_rect = prompt_surface.get_rect()
        prompt_rect.x = button_rect.x + 50
        prompt_rect.y = button_rect.y + 12

        screen.blit(button_image, button_rect)
        screen.blit(prompt_surface, prompt_rect)

    def __load_image(self):
        image = pygame.transform.scale(
            pygame.image.load(f'images/entity_img/env_item_img/{self.__item_name}.png').convert_alpha(),
            (self.__width, self.__height),
        )
        return image

    def draw_entity(self, screen: pygame.Surface, wesker: Wesker):
        if not self.__taken:
            screen.blit(self.__load_image(), self.__rect)
            if self.__action:
                self.__show_prompt(screen, wesker)


class Door:
    def __init__(self, x: int, image_source: str, image_width: int, image_height: int,
                 scene_id: int, go_to_scene_id: int, go_to_scene_name: str, go_to_x_coords: int,
                 font: pygame.font.Font):
        self.entity_type: str = 'door'

        self.__image_source: str = image_source
        self.__image_width: int = image_width
        self.__image_height: int = image_height

        self.__scene_id: int = scene_id
        self.go_to_scene_id: int = go_to_scene_id
        self.__go_to_scene_name: str = go_to_scene_name
        self.go_to_x_coords: int = go_to_x_coords

        self.__prompt_color: pygame.Color = pygame.Color(250, 250, 250)
        self.__prompt_text: str = f'Go to {self.__go_to_scene_name}'

        self.__x: int = x
        self.__y: int = ACTUAL_HEIGHT - self.__image_height
        self.__rect: pygame.Rect = pygame.Rect(self.__x, self.__y, self.__image_width, self.__image_height)

        self.__font: pygame.font.Font = font
        self.__action: bool = False

    def check_entity_logic(self, wesker: Wesker, _):
        self.__check_door_collision(wesker)

    def __check_door_collision(self, wesker: Wesker):
        if self.__rect.colliderect(wesker.get_hitbox_rect()):
            self.__action = True
        else:
            self.__action = False

    def scene_change_allowed(self):
        return self.__action

    def __show_prompt(self, screen: pygame.Surface):
        prompt_surface = self.__font.render(self.__prompt_text, 1, self.__prompt_color)
        prompt_rect: pygame.Rect = prompt_surface.get_rect()
        prompt_rect.x = WIDTH // 2 - prompt_rect.width // 2
        prompt_rect.y = (ACTUAL_HEIGHT + FLOOR_HEIGHT // 2) - prompt_rect.height // 2

        button_rect = pygame.Rect(prompt_rect.x - 60, ACTUAL_HEIGHT + 10, 50, 50)
        button_image = pygame.transform.scale(
            pygame.image.load(f'images/entity_img/door_img/key_f.png').convert_alpha(),
            (50, 50),
        )

        screen.blit(button_image, button_rect)
        screen.blit(prompt_surface, prompt_rect)

    def __load_image(self):
        image = pygame.transform.scale(
            pygame.image.load(f'images/entity_img/door_img/{self.__image_source}.png').convert_alpha(),
            (self.__image_width, self.__image_height),
        )
        return image

    def draw_entity(self, screen: pygame.Surface, _):
        screen.blit(self.__load_image(), self.__rect)
        if self.__action:
            self.__show_prompt(screen)


class ItemBox:
    def __init__(self, font: pygame.font.Font):
        self.entity_type: str = 'item_box'

        self.__prompt_color: pygame.Color = pygame.Color(250, 250, 250)
        self.__prompt_text: str = f'Open the Item Box'
        self.__opened: bool = False

        self.__box_size: int = 180

        self.__rect: pygame.Rect = pygame.Rect(620, ACTUAL_HEIGHT - self.__box_size, self.__box_size, self.__box_size)

        self.__font: pygame.font.Font = font
        self.__action: bool = False

    def box_active(self):
        return self.__action

    def get_opened(self):
        self.__opened = True
        self.__action = False

    def check_entity_logic(self, wesker: Wesker, _):
        self.__check_box_collision(wesker)

    def __check_box_collision(self, wesker: Wesker):
        if not self.__opened:
            if self.__rect.colliderect(wesker.get_hitbox_rect()):
                self.__action = True
            else:
                self.__action = False

    def __show_prompt(self, screen: pygame.Surface):
        prompt_surface = self.__font.render(self.__prompt_text, 1, self.__prompt_color)
        prompt_rect: pygame.Rect = prompt_surface.get_rect()
        prompt_rect.x = WIDTH // 2 - prompt_rect.width // 2
        prompt_rect.y = (ACTUAL_HEIGHT + FLOOR_HEIGHT // 2) - prompt_rect.height // 2

        button_rect = pygame.Rect(prompt_rect.x - 60, ACTUAL_HEIGHT + 15, 40, 40)
        button_image = pygame.transform.scale(
            pygame.image.load(f'images/entity_img/env_item_img/key_t.png').convert_alpha(),
            (40, 40),
        )

        screen.blit(button_image, button_rect)
        screen.blit(prompt_surface, prompt_rect)

    def draw_entity(self, screen: pygame.Surface, _):
        if self.__action and not self.__opened:
            self.__show_prompt(screen)


class Kitty:
    def __init__(self, font: pygame.font.Font):
        self.entity_type: str = 'kitty'

        self.__image_source: str = 'kitty'
        self.__image_width: int = 150
        self.__image_height: int = 150

        self.__prompt_color: pygame.Color = pygame.Color(30, 90, 220)
        self.__prompt_text: str = f'Accept Kitty\'s power!'
        self.__state: bool = False

        self.__rect: pygame.Rect = pygame.Rect(630, 350, self.__image_width, self.__image_height)

        self.__font: pygame.font.Font = font
        self.__action: bool = False

    def kitty_power(self):
        return self.__action

    def kitty_change_state(self):
        if not self.__state:
            self.__prompt_color = pygame.Color(160, 20, 20)
            self.__prompt_text = f'Return Kitty\'s power!'
            self.__state = True
        else:
            self.__prompt_color = pygame.Color(30, 90, 220)
            self.__prompt_text = f'Accept Kitty\'s power!'
            self.__state = False

    def check_entity_logic(self, wesker: Wesker, _):
        self.__check_kitty_collision(wesker)
        self.__check_kitty_position()

    def __check_kitty_collision(self, wesker: Wesker):
        if self.__rect.colliderect(wesker.get_hitbox_rect()):
            self.__action = True
        else:
            self.__action = False

    def __check_kitty_position(self):
        if pygame.time.get_ticks() // 1000 % 2:
            self.__rect.y = 330
        else:
            self.__rect.y = 350

    def __show_prompt(self, screen: pygame.Surface):
        prompt_surface = self.__font.render(self.__prompt_text, 1, self.__prompt_color)
        prompt_rect: pygame.Rect = prompt_surface.get_rect()
        prompt_rect.x = WIDTH // 2 - prompt_rect.width // 2
        prompt_rect.y = (ACTUAL_HEIGHT + FLOOR_HEIGHT // 2) - prompt_rect.height // 2

        button_rect = pygame.Rect(prompt_rect.x - 60, ACTUAL_HEIGHT + 15, 40, 40)
        button_image = pygame.transform.scale(
            pygame.image.load(f'images/entity_img/env_item_img/key_t.png').convert_alpha(),
            (40, 40),
        )

        screen.blit(button_image, button_rect)
        screen.blit(prompt_surface, prompt_rect)

    def __load_image(self):
        image = pygame.transform.scale(
            pygame.image.load(f'images/character_img/kitty.png').convert_alpha(),
            (self.__image_width, self.__image_height),
        )
        return image

    def draw_entity(self, screen: pygame.Surface, _):
        screen.blit(self.__load_image(), self.__rect)
        if self.__action:
            self.__show_prompt(screen)
