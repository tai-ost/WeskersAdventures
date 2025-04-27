import pygame

from constants import ITEM_WIDTH, ITEM_HEIGHT


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
    def __init__(self, ammo):
        self.__hidden = False

        self.__health = 100
        self.__poisoned = False

        self.__ammo = ammo
        self.__inventory = list()
        self.__current_slot = 0
        ...

    def add_item(self, item: Item):
        ...

    def use_item(self):
        action = self.__inventory[self.__current_slot].action()
        if action == 1:
            ...

    def check_health(self):
        ...

    def update_ammo(self, ammo):
        self.__ammo = ammo

    def get_ammo(self):
        return self.__ammo
