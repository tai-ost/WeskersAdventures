import pygame


from constants import WIDTH, HEIGHT, ACTUAL_HEIGHT, FLOOR_HEIGHT, DOOR_TYPES, ENEMY_TYPES, ITEM_TYPES, FPS
from wesker import Wesker
from hud import HUD


class Scene:
    def __init__(self, scene_id, background_image, entities, font):
        self.__scene_id = scene_id
        self.__background_image = pygame.transform.scale(
            pygame.image.load(f'images/background_img/{background_image}.png').convert_alpha(),
            (WIDTH, ACTUAL_HEIGHT),
        )
        self.__background_rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
        self.__entities = entities

        self.__font = font

    def get_entities(self):
        return self.__entities

    def check_scene_event(self, wesker: Wesker, hud: HUD, event_key):
        entity: Door | Enemy | EnvironmentItem
        for entity in self.__entities:
            if entity.entity_type == 'door' and entity.scene_change_allowed() and event_key == pygame.K_f:
                wesker.change_x_position(entity.get_x_position())
                return 1, entity.go_to_scene
            elif entity.entity_type == 'item' and entity.taking_allowed() and \
                    (hud.inventory_empty_slot() != 5) and event_key == pygame.K_t:
                entity.get_taken()
                hud.add_item(entity.get_item_type(), hud.inventory_empty_slot())
        return 0, 0

    def check_scene_logic(self, wesker: Wesker, hud: HUD):
        entity: Door | Enemy | EnvironmentItem
        for entity in self.__entities:
            entity.check_entity_logic(wesker, hud)

        wesker.have_fired = False

    def draw(self, screen, wesker: Wesker):
        self.__draw_background(screen)
        self.__draw_entities(screen, wesker)

    def __draw_background(self, screen):
        screen.blit(self.__background_image, self.__background_rect)

    def __draw_entities(self, screen, wesker: Wesker):
        entity: Door | Enemy | EnvironmentItem
        for entity in self.__entities:
            entity.draw_entity(screen, wesker)


class Enemy:
    def __init__(self, x, enemy_type):
        self.entity_type = 'enemy'

        self.__name = ENEMY_TYPES[enemy_type][0]

        self.__health = ENEMY_TYPES[enemy_type][1]
        self.__dmg = ENEMY_TYPES[enemy_type][2]
        self.__velocity = ENEMY_TYPES[enemy_type][3]
        self.__is_poisonous = ENEMY_TYPES[enemy_type][4]

        self.__width = ENEMY_TYPES[enemy_type][5]
        self.__height = ENEMY_TYPES[enemy_type][6]

        self.__x = x
        self.__y = ACTUAL_HEIGHT - self.__height

        self.__rect = pygame.Rect(self.__x, self.__y, self.__width, self.__height)

        self.__direction = 0  # 0 - right, 1 - left
        self.__last_frame = 0
        self.__last_frame_count = 0

        self.__alive = True

    def get_x(self):
        return self.__rect.x

    def __get_damage(self):
        self.__health -= 1
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
            self.__last_frame_count += 1
            if self.__last_frame_count > (FPS // 2):
                self.__last_frame_count = 0
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

    def draw_entity(self, screen, _):
        screen.blit(self.__load_image(), self.__rect)


class EnvironmentItem:
    def __init__(self, x, y, item_type, font: pygame.font.Font):
        self.entity_type: str = 'item'
        self.__item_type = item_type
        self.__item_name: str = ITEM_TYPES[item_type][0]

        self.__width: int = ITEM_TYPES[item_type][1]
        self.__height: int = ITEM_TYPES[item_type][2]

        self.__prompt_text: str = f'Take {ITEM_TYPES[item_type][3]}'
        self.__prompt_color: pygame.Color = pygame.Color(250, 250, 250)

        self.__x: int = x
        self.__y: int = y
        self.__rect: pygame.Rect = pygame.Rect(self.__x, self.__y, self.__width, self.__height)

        self.__font: pygame.font.Font = font
        self.__taken = False
        self.__action = False

    def check_entity_logic(self, wesker: Wesker, hud: HUD):
        self.__check_item_collision(wesker)
        ...

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

    def __show_prompt(self, screen, wesker: Wesker):
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

    def draw_entity(self, screen, wesker: Wesker):
        if not self.__taken:
            screen.blit(self.__load_image(), self.__rect)
            if self.__action:
                self.__show_prompt(screen, wesker)


class Door:
    def __init__(self, x, image_source, image_width, image_height, scene_id, go_to_scene, door_type, font):
        self.entity_type = 'door'

        self.__image_source = image_source
        self.__image_width = image_width
        self.__image_height = image_height

        self.__prompt_color = pygame.Color(250, 250, 250)
        self.__prompt_text = DOOR_TYPES[door_type]

        self.__x = x
        self.__y = ACTUAL_HEIGHT - self.__image_height
        self.__rect = pygame.Rect(self.__x, self.__y, self.__image_width, self.__image_height)

        self.__scene_id = scene_id
        self.go_to_scene = go_to_scene

        self.__font = font
        self.__action = False

    def check_entity_logic(self, wesker: Wesker, _):
        self.__check_door_collision(wesker)

    def __check_door_collision(self, wesker: Wesker):
        if self.__rect.colliderect(wesker.get_hitbox_rect()):
            self.__action = True
        else:
            self.__action = False

    def get_x_position(self):
        return self.__rect.x

    def scene_change_allowed(self):
        return self.__action

    def __show_prompt(self, screen):
        button_rect = pygame.Rect(WIDTH // 2 - 200, ACTUAL_HEIGHT + 10, 50, 50)
        button_image = pygame.transform.scale(
            pygame.image.load(f'images/entity_img/door_img/key_f.png').convert_alpha(),
            (50, 50),
        )

        prompt_surface = self.__font.render(self.__prompt_text, 1, self.__prompt_color)
        prompt_rect = prompt_surface.get_rect()
        prompt_rect.x = button_rect.x + 70
        prompt_rect.y = button_rect.y + 15

        screen.blit(button_image, button_rect)
        screen.blit(prompt_surface, prompt_rect)

    def __load_image(self):
        image = pygame.transform.scale(
            pygame.image.load(f'images/entity_img/door_img/{self.__image_source}.png').convert_alpha(),
            (self.__image_width, self.__image_height),
        )
        return image

    def draw_entity(self, screen, _):
        screen.blit(self.__load_image(), self.__rect)
        if self.__action:
            self.__show_prompt(screen)
