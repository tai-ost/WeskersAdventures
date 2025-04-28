import pygame

from constants import (ITEM_WIDTH, ITEM_HEIGHT,
                       INVENTORY_SLOT_WIDTH, INVENTORY_SLOT_HEIGHT,
                       DEFAULT_AMMO_LOADED, DEFAULT_AMMO_STORED)


class Item:
    def __init__(self, name, image_source=None, action=None):
        self.__name = name
        self.__active = False

        self.__image_source = image_source
        self.__action = action
        ...

    def get_name(self):
        return self.__name

    def change_to_active(self):
        self.__active = True

    def change_to_passive(self):
        self.__active = False

    def get_state(self):
        return self.__active

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
        self.__poisoned_last_tick = 0
        self.__poisoned_current_tick = 0

        self.__ammo_stored = DEFAULT_AMMO_STORED
        self.__ammo_loaded = DEFAULT_AMMO_LOADED

        self.__inventory_keys = {
            pygame.K_1: 0,
            pygame.K_2: 1,
            pygame.K_3: 2,
            pygame.K_4: 3
        }
        self.__inventory: list[Item] = [
            Item(None),
            Item(None),
            Item(None),
            Item(None)
        ]
        self.__current_slot = 0
        self.__slot = 'inventory_slot'

        self.__ammo_text_color = pygame.Color(150, 150, 150)
        self.__health_rect = pygame.Rect(0, 0, 160, 80)
        self.__ammo_box_rect = pygame.Rect(0, self.__health_rect.height, 160, 40)
        ...

    def hide_or_show(self):
        self.__hidden = not self.__hidden

    def add_item(self, item: Item):
        ...

    def use_item(self):
        action = self.__inventory[self.__current_slot].action()
        if action == 1:
            ...

    def get_inventory_keys(self):
        return self.__inventory_keys.keys()

    def inventory_passive(self):
        for i in range(4):
            self.__inventory[i].change_to_passive()

    def activate_inventory_slot(self, key):
        slot_number = self.__inventory_keys[key]
        self.inventory_passive()
        self.__inventory[slot_number].change_to_active()

    def got_poisoned(self):
        self.__poisoned = not self.__poisoned  # Заглушка пока нет врагов с отравлением
        self.__poisoned_last_tick = self.__poisoned_current_tick = pygame.time.get_ticks()

    def check_health(self):
        if self.__poisoned:
            self.__poisoned_current_tick = pygame.time.get_ticks()
            if (self.__poisoned_current_tick - self.__poisoned_last_tick) > 1000:
                self.__poisoned_last_tick = self.__poisoned_current_tick
                self.__health_points -= 5
        if self.__health_points > 75:
            self.__health_state = 'fine'
        elif self.__health_points > 50:
            self.__health_state = 'caution_yellow'
        elif self.__health_points > 25:
            self.__health_state = 'caution_orange'
        else:
            self.__health_state = 'danger'

    def update_ammo(self, ammo):
        self.__ammo_loaded = ammo

    def get_ammo_stored(self):
        return self.__ammo_stored

    def get_health_points(self):
        return self.__health_points

    def reload(self):
        needed_ammo = DEFAULT_AMMO_LOADED - self.__ammo_loaded
        if self.__ammo_stored < needed_ammo:
            remaining_ammo = self.__ammo_stored
            self.__ammo_stored = 0
            return remaining_ammo
        self.__ammo_stored -= needed_ammo
        return needed_ammo

    def __load_inventory_slot_image(self, slot_number):
        if self.__inventory[slot_number].get_name():
            ...
        else:
            slot_state = '_active' if self.__inventory[slot_number].get_state() else ''
            image = pygame.transform.scale(
                pygame.image.load(f'images/hud_img/{self.__slot + slot_state}.png').convert_alpha(),
                (INVENTORY_SLOT_WIDTH, INVENTORY_SLOT_HEIGHT),
            )
            return image

    def __show_inventory(self, screen):
        for slot_number in range(4):
            slot_rect = pygame.Rect(self.__health_rect.width + INVENTORY_SLOT_WIDTH * slot_number, 0,
                                    INVENTORY_SLOT_WIDTH, INVENTORY_SLOT_HEIGHT)
            screen.blit(self.__load_inventory_slot_image(slot_number), slot_rect)

    def __load_health_state_image(self):
        poison = 'poison_' if self.__poisoned else ''
        image = pygame.transform.scale(
            pygame.image.load(f'images/hud_img/{poison + self.__health_state}.png').convert_alpha(),
            (160, 80),
        )
        return image

    def __show_ammo(self, screen):
        ammo_surface = self.__font.render(f'Ammo: {self.__ammo_loaded}/{self.__ammo_stored}',
                                          1, self.__ammo_text_color)
        ammo_rect = ammo_surface.get_rect()
        ammo_rect.x = self.__ammo_box_rect.x + 12
        ammo_rect.y = self.__ammo_box_rect.y + 10

        ammo_box_image = pygame.transform.scale(
                pygame.image.load(f'images/hud_img/ammo_box.png').convert_alpha(),
                (self.__ammo_box_rect.width, self.__ammo_box_rect.height),
            )
        screen.blit(ammo_box_image, self.__ammo_box_rect)
        screen.blit(ammo_surface, ammo_rect)

    def draw_hud(self, screen):
        if not self.__hidden:
            screen.blit(self.__load_health_state_image(), self.__health_rect)
            self.__show_ammo(screen)
            self.__show_inventory(screen)
