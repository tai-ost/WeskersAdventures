import pygame


from constants import WIDTH, HEIGHT, ACTUAL_HEIGHT, FLOOR_HEIGHT, DOOR_TYPES, ENEMY_TYPES
from wesker import Wesker


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

    def check_scene_event(self, wesker: Wesker):
        entity: Door
        for entity in self.__entities:
            if entity.entity_type == 'door' and entity.scene_change_allowed():
                wesker.change_x_position(entity.get_x_position())
                return 1, entity.go_to_scene
        return 0, 0

    def check_scene_logic(self, wesker: Wesker):
        entity: Door
        for entity in self.__entities:
            entity.check_entity_logic(wesker)

    def draw(self, screen):
        self.__draw_background(screen)
        self.__draw_entities(screen)

    def __draw_background(self, screen):
        screen.blit(self.__background_image, self.__background_rect)

    def __draw_entities(self, screen):
        entity: Door
        for entity in self.__entities:
            entity.draw_entity(screen)


class Enemy:
    def __init__(self, x, y, enemy_type):
        self.__x = x
        self.__y = y

        self.__name = ENEMY_TYPES[enemy_type][0]

        self.__health = ENEMY_TYPES[enemy_type][1]
        self.__dmg = ENEMY_TYPES[enemy_type][2]
        self.__speed = ENEMY_TYPES[enemy_type][3]
        self.__is_poisonous = ENEMY_TYPES[enemy_type][4]

        self.__width = ENEMY_TYPES[enemy_type][5]
        self.__height = ENEMY_TYPES[enemy_type][6]
        self.__rect = pygame.Rect(self.__x, self.__y, self.__width, self.__height)

        self.__alive = True

    def __get_damage(self):
        self.__health -= 1
        self.__alive = self.__health > 0

    def __check_enemy_collision(self, wesker: Wesker):
        ...

    def check_entity_logic(self, wesker: Wesker):
        ...

    def draw_entity(self, screen):
        ...


class Door:
    def __init__(self, x, image_source, image_width, image_height, scene_id, go_to_scene, font, door_type):
        self.entity_type = 'door'
        self.__image_source = image_source
        self.__image_width = image_width
        self.__image_height = image_height

        self.__prompt_color = pygame.Color(250, 250, 250)
        self.__prompt_text = DOOR_TYPES[door_type]

        self.__x_coord = x
        self.__y_coord = ACTUAL_HEIGHT - self.__image_height
        self.__rect = pygame.Rect(self.__x_coord, self.__y_coord, self.__image_width, self.__image_height)

        self.__scene_id = scene_id
        self.go_to_scene = go_to_scene

        self.__font = font
        self.__action = False

    def check_entity_logic(self, wesker: Wesker):
        self.__check_door_collision(wesker)

    def __check_door_collision(self, wesker: Wesker):
        if self.__rect.colliderect(wesker.get_hitbox_rect()):
            self.__action = True
        else:
            self.__action = False
        ...

    def get_x_position(self):
        return self.__rect.x

    def scene_change_allowed(self):
        return self.__action

    def __show_prompt(self, screen):
        button_rect = pygame.Rect(WIDTH // 2 - 200, ACTUAL_HEIGHT + 10, 50, 50)
        button_image = pygame.transform.scale(
            pygame.image.load(f'images/entity_img/key_f.png').convert_alpha(),
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
            pygame.image.load(f'images/entity_img/{self.__image_source}.png').convert_alpha(),
            (self.__image_width, self.__image_height),
        )
        return image

    def draw_entity(self, screen):
        screen.blit(self.__load_image(), self.__rect)
        if self.__action:
            self.__show_prompt(screen)
