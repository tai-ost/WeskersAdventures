import pygame

from constants import (ITEM_WIDTH, ITEM_HEIGHT, ITEM_TYPES,
                       INVENTORY_SLOT_WIDTH, INVENTORY_SLOT_HEIGHT,
                       DEFAULT_AMMO_LOADED, DEFAULT_AMMO_STORED)


class Item:
    def __init__(self, name, action=None):
        self.__name = name
        self.__active = False

        self.__action = action

        self.combining = False
        ...

    def get_name(self):
        return self.__name

    def configure_item(self, item_type: int):
        self.__name = ITEM_TYPES[item_type][0]
        self.__action = item_type

    def set_to_default(self):
        self.__name = None
        self.__active = False

        self.__action = None

    def change_to_active(self):
        self.__active = True

    def change_to_passive(self):
        self.__active = False

    def get_state(self):
        return self.__active

    def action(self):
        return self.__action


class HUD:
    def __init__(self, font: pygame.font.Font):
        self.__hidden = False

        self.__font: pygame.font.Font = font

        self.__health_points = 100
        self.__health_state = 'fine'

        self.__grace = False
        self.__grace_period = 0

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
        self.__current_slot = 4
        self.__slot = 'inventory_slot'
        self.__combine_item_slots = list()
        self.__combine_frame_color = pygame.Color(150, 30, 30)

        self.__ammo_text_color = pygame.Color(150, 150, 150)
        self.__health_rect = pygame.Rect(0, 0, 160, 80)
        self.__ammo_box_rect = pygame.Rect(0, self.__health_rect.height, 160, 40)

        self.__defensive_item_count = 8
        self.__defensive_item_count_color = pygame.Color(150, 150, 150)
        self.__defensive_item_box_rect = pygame.Rect(480, 0, 80, 80)

        self.__item_name_color = pygame.Color(200, 200, 200)
        ...

    def hide_or_show(self):
        self.__hidden = not self.__hidden

    def inventory_empty_slot(self):
        for i in range(4):
            if not self.__inventory[i].get_name():
                return i
        return 5

    def add_item(self, item_type: int, slot: int):
        self.__inventory[slot].configure_item(item_type)

    def use_item(self):
        if self.__current_slot != 4:
            action = self.__inventory[self.__current_slot].action()
            # First Aid Spray and Mixed Herbs (G + R)
            if action == 1 or action == 8:
                self.__health_points = 100
            # Green Herb
            elif action == 2:
                self.__health_points = min(100, self.__health_points + 25)
            # Red Herb
            elif action == 3:
                pass
            # Blue Herb
            elif action == 4:
                self.__poisoned = False
            # Dagger
            elif action == 5:
                self.__defensive_item_count += 1
            # Handgun Ammo
            elif action == 6:
                self.__ammo_stored += 15
            # Mixed Herbs (G + B)
            elif action == 7:
                self.__poisoned = False
                self.__health_points = min(100, self.__health_points + 25)
            # Mixed Herbs (G + G)
            elif action == 9:
                self.__health_points = min(100, self.__health_points + 50)
            # Mixed Herbs (G + R + B)
            elif action == 10:
                self.__poisoned = False
                self.__health_points = 100

            self.__inventory[self.__current_slot].set_to_default()

    def get_inventory_keys(self):
        return self.__inventory_keys.keys()

    def inventory_passive(self):
        for i in range(4):
            self.__inventory[i].change_to_passive()
        self.__current_slot = 4

    def activate_inventory_slot(self, key):
        slot_number = self.__inventory_keys[key]
        self.inventory_passive()
        self.__inventory[slot_number].change_to_active()
        self.__current_slot = self.__inventory_keys[key]

    def combine_herbs(self):
        if (self.__inventory[self.__current_slot] != 4) and \
                (self.__inventory[self.__current_slot].action() in (2, 3, 4, 7, 8)):
            self.__inventory[self.__current_slot].combining = not self.__inventory[self.__current_slot].combining
            if self.__inventory[self.__current_slot].combining:
                if not self.__combine_item_slots or \
                        (self.__combine_item_slots and self.__combine_item_slots[0] != self.__current_slot):
                    self.__combine_item_slots.append(self.__current_slot)
            if len(self.__combine_item_slots) == 2:
                if self.__inventory[self.__combine_item_slots[0]].action() == 2:

                    if self.__inventory[self.__combine_item_slots[1]].action() == 3:
                        self.__inventory[self.__combine_item_slots[0]].configure_item(7)
                        self.__inventory[self.__combine_item_slots[1]].set_to_default()

                    elif self.__inventory[self.__combine_item_slots[1]].action() == 4:
                        self.__inventory[self.__combine_item_slots[0]].configure_item(8)
                        self.__inventory[self.__combine_item_slots[1]].set_to_default()

                    elif self.__inventory[self.__combine_item_slots[1]].action() == 2:
                        self.__inventory[self.__combine_item_slots[0]].configure_item(9)
                        self.__inventory[self.__combine_item_slots[1]].set_to_default()

                elif self.__inventory[self.__combine_item_slots[0]].action() == 3:

                    if self.__inventory[self.__combine_item_slots[1]].action() == 2:
                        self.__inventory[self.__combine_item_slots[0]].configure_item(7)
                        self.__inventory[self.__combine_item_slots[1]].set_to_default()

                    elif self.__inventory[self.__combine_item_slots[1]].action() == 8:
                        self.__inventory[self.__combine_item_slots[0]].configure_item(10)
                        self.__inventory[self.__combine_item_slots[1]].set_to_default()

                elif self.__inventory[self.__combine_item_slots[0]].action() == 4:

                    if self.__inventory[self.__combine_item_slots[1]].action() == 2:
                        self.__inventory[self.__combine_item_slots[0]].configure_item(8)
                        self.__inventory[self.__combine_item_slots[1]].set_to_default()

                    elif self.__inventory[self.__combine_item_slots[1]].action() == 7:
                        self.__inventory[self.__combine_item_slots[0]].configure_item(10)
                        self.__inventory[self.__combine_item_slots[1]].set_to_default()

                elif self.__inventory[self.__combine_item_slots[0]].action() == 7:

                    if self.__inventory[self.__combine_item_slots[1]].action() == 4:
                        self.__inventory[self.__combine_item_slots[0]].configure_item(10)
                        self.__inventory[self.__combine_item_slots[1]].set_to_default()

                elif self.__inventory[self.__combine_item_slots[0]].action() == 8:

                    if self.__inventory[self.__combine_item_slots[1]].action() == 3:
                        self.__inventory[self.__combine_item_slots[0]].configure_item(10)
                        self.__inventory[self.__combine_item_slots[1]].set_to_default()

                self.__inventory[self.__combine_item_slots[0]].combining = False
                self.__inventory[self.__combine_item_slots[1]].combining = False
                self.__combine_item_slots = list()

    def get_damage(self, dmg, is_poisonous):
        if not self.__grace_period:
            if not self.__defensive_item_count:
                self.__health_points -= dmg
                self.__poisoned = is_poisonous
            else:
                self.__defensive_item_count = max(0, self.__defensive_item_count - 1)
            self.__grace_period = pygame.time.get_ticks() + 1000

    def got_poisoned(self):
        self.__poisoned = not self.__poisoned
        self.__poisoned_last_tick = self.__poisoned_current_tick = pygame.time.get_ticks()

    def check_health(self):
        if self.__poisoned:
            self.__poisoned_current_tick = pygame.time.get_ticks()
            if (self.__poisoned_current_tick - self.__poisoned_last_tick) > 1000:
                self.__poisoned_last_tick = self.__poisoned_current_tick
                self.__health_points -= 1
        if self.__health_points > 75:
            self.__health_state = 'fine'
        elif self.__health_points > 50:
            self.__health_state = 'caution_yellow'
        elif self.__health_points > 25:
            self.__health_state = 'caution_orange'
        else:
            self.__health_state = 'danger'

        if self.__grace_period and (pygame.time.get_ticks() > self.__grace_period):
            self.__grace_period = 0

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

    def __load_health_state_image(self):
        poison = 'poison_' if self.__poisoned else ''
        image = pygame.transform.scale(
            pygame.image.load(f'images/hud_img/health_states/{poison + self.__health_state}.png').convert_alpha(),
            (160, 80),
        )
        return image

    def __show_health(self, screen):
        screen.blit(self.__load_health_state_image(), self.__health_rect)

    def __load_inventory_slot_image(self, slot_number: int):
        slot_state = '_active' if self.__inventory[slot_number].get_state() else ''
        slot_image = pygame.transform.scale(
            pygame.image.load(f'images/hud_img/other/{self.__slot + slot_state}.png').convert_alpha(),
            (INVENTORY_SLOT_WIDTH, INVENTORY_SLOT_HEIGHT),
        )
        return slot_image

    def __load_inventory_item_image(self, slot_number: int):
        item_name = self.__inventory[slot_number].get_name()
        if item_name:
            item_image = pygame.transform.scale(
                pygame.image.load(
                    f'images/hud_img/item_img/inventory_{item_name}.png'
                ).convert_alpha(),
                (ITEM_WIDTH, ITEM_HEIGHT),
            )
        else:
            item_image = pygame.transform.scale(
                pygame.image.load(
                    f'images/hud_img/item_img/nothing_img.png'
                ).convert_alpha(),
                (ITEM_WIDTH, ITEM_HEIGHT),
            )
        return item_image

    def __show_item_name(self, screen):
        name_surface = self.__font.render(f'{ITEM_TYPES[self.__inventory[self.__current_slot].action()][3]}',
                                          1, self.__item_name_color)
        name_rect = name_surface.get_rect()
        name_rect.x = self.__ammo_box_rect.x + self.__ammo_box_rect.width + 5
        name_rect.y = self.__ammo_box_rect.y + 12

        screen.blit(name_surface, name_rect)

    def __show_inventory(self, screen):
        for slot_number in range(4):
            slot_rect = pygame.Rect(self.__health_rect.width + INVENTORY_SLOT_WIDTH * slot_number, 0,
                                    INVENTORY_SLOT_WIDTH, INVENTORY_SLOT_HEIGHT)
            item_rect = pygame.Rect(self.__health_rect.width + INVENTORY_SLOT_WIDTH * slot_number + 13, 13,
                                    ITEM_WIDTH, ITEM_HEIGHT)
            screen.blit(self.__load_inventory_slot_image(slot_number), slot_rect)
            screen.blit(self.__load_inventory_item_image(slot_number), item_rect)
            if self.__inventory[slot_number].combining:
                pygame.draw.rect(screen, self.__combine_frame_color,
                                 (self.__health_rect.width + INVENTORY_SLOT_WIDTH * slot_number + 13, 13,
                                  54, 54),
                                 2)

    def __show_ammo(self, screen):
        ammo_surface = self.__font.render(f'Ammo: {self.__ammo_loaded}/{self.__ammo_stored}',
                                          1, self.__ammo_text_color)
        ammo_rect = ammo_surface.get_rect()
        ammo_rect.x = self.__ammo_box_rect.x + 12
        ammo_rect.y = self.__ammo_box_rect.y + 10

        ammo_box_image = pygame.transform.scale(
                pygame.image.load(f'images/hud_img/other/ammo_box.png').convert_alpha(),
                (self.__ammo_box_rect.width, self.__ammo_box_rect.height),
            )
        screen.blit(ammo_box_image, self.__ammo_box_rect)
        screen.blit(ammo_surface, ammo_rect)

    def __show_defensive_item(self, screen):
        defensive_item_surface = self.__font.render(f'x{self.__defensive_item_count}',
                                                    1, self.__defensive_item_count_color)
        defensive_item_rect = defensive_item_surface.get_rect()
        defensive_item_rect.x = self.__defensive_item_box_rect.x + 25
        defensive_item_rect.y = self.__defensive_item_box_rect.y + 45

        defensive_item_box_image = pygame.transform.scale(
            pygame.image.load(f'images/hud_img/other/defensive_item_box.png').convert_alpha(),
            (self.__defensive_item_box_rect.width, self.__defensive_item_box_rect.height),
        )
        screen.blit(defensive_item_box_image, self.__defensive_item_box_rect)
        screen.blit(defensive_item_surface, defensive_item_rect)

    def draw_hud(self, screen):
        if not self.__hidden:
            self.__show_health(screen)
            self.__show_ammo(screen)
            self.__show_inventory(screen)
            if self.__defensive_item_count:
                self.__show_defensive_item(screen)
            if (self.__current_slot != 4) and (self.__inventory[self.__current_slot].action()):
                self.__show_item_name(screen)
