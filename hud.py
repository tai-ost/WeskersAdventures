import pygame

from constants import (ITEM_WIDTH, ITEM_HEIGHT,
                       INVENTORY_SLOT_WIDTH, INVENTORY_SLOT_HEIGHT,
                       DEFAULT_AMMO_LOADED, DEFAULT_AMMO_STORED)


class Item:
    def __init__(self, name, image_source, action):
        self.__name = name
        self.__image_source = image_source
        self.__action = action
        ...

    def action(self):
        return self.__action

    def load_image(self):
        image = pygame.transform.scale(
            pygame.image.load(f'images/item_img/{self.__image_source}.png').convert_alpha(),
            (ITEM_WIDTH, ITEM_HEIGHT),
        )
        return image


class HUD:
    def __init__(self, font: pygame.font.Font):
        self.__hidden = False

        self.__font: pygame.font.Font = font

        self.__health_points = 100
        self.__health_state = 'fine'
        self.__poisoned = False

        self.__ammo_stored = DEFAULT_AMMO_STORED
        self.__ammo_loaded = DEFAULT_AMMO_LOADED
        self.__inventory = list()
        self.__current_slot = 0

        self.__ammo_text_color = pygame.Color(0, 0, 0)
        self.__health_rect = pygame.Rect(0, 0, 160, 80)
        ...

    def hide_or_show(self):
        self.__hidden = not self.__hidden

    def add_item(self, item: Item):
        ...

    def use_item(self):
        action = self.__inventory[self.__current_slot].action()
        if action == 1:
            ...

    def check_health(self):
        if self.__poisoned:
            self.__health_points -= 0.1
            self.__health_state = 'poisoned'
        elif self.__health_points > 66:
            self.__health_state = 'fine'
        elif self.__health_points > 33:
            self.__health_state = 'caution'
        else:
            self.__health_state = 'danger'

    def update_ammo(self, ammo):
        self.__ammo_loaded = ammo

    def get_ammo_stored(self):
        return self.__ammo_stored

    def reload(self):
        needed_ammo = DEFAULT_AMMO_LOADED - self.__ammo_loaded
        if self.__ammo_stored < needed_ammo:
            remaining_ammo = self.__ammo_stored
            self.__ammo_stored = 0
            return remaining_ammo
        self.__ammo_stored -= needed_ammo
        return needed_ammo

    def __load_inventory_slot_image(self, slot_number):
        ...

    def __load_health_state_image(self):
        image = pygame.transform.scale(
            pygame.image.load(f'images/hud_img/{self.__health_state}.png').convert_alpha(),
            (160, 80),
        )
        return image

    def __show_ammo(self, screen):
        ammo_surface = self.__font.render(f'Ammo: {self.__ammo_loaded}/{self.__ammo_stored}',
                                          1, self.__ammo_text_color)
        ammo_rect = ammo_surface.get_rect()
        ammo_rect.x = 10
        ammo_rect.y = 10
        screen.blit(ammo_surface, ammo_rect)

    def draw_hud(self, screen):
        if not self.__hidden:
            # screen.blit(self.__load_health_state_image(), self.__health_rect)
            self.__show_ammo(screen)
