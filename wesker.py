import pygame

from constants import WIDTH, FPS, ACTUAL_HEIGHT, GRAVITY_ACCELERATION, DEFAULT_AMMO_LOADED


class Wesker:
    def __init__(self):
        self.__hitbox_width = 100
        self.__hitbox_height = 250

        self.__image_width = 220
        self.__image_height = 250

        self.__x_coord = WIDTH // 2 - self.__image_width // 2
        self.__y_coord = ACTUAL_HEIGHT - self.__image_height

        self.__rect = pygame.Rect(self.__x_coord, self.__y_coord, self.__image_width, self.__image_height)
        self.__hitbox_rect = pygame.Rect(self.__rect.x + 50, self.__rect.y, self.__hitbox_width, self.__hitbox_height)

        # Кортеж с возможными состояниями и соответствующими им названиями изображений
        self.__possible_states = (
            'wesker_idle_right',                # 0
            'wesker_idle_left',                 # 1
            'wesker_running_right_frame_0',     # 2
            'wesker_running_right_frame_1',     # 3
            'wesker_running_left_frame_0',      # 4
            'wesker_running_left_frame_1',      # 5
            'wesker_jumping_right',             # 6
            'wesker_jumping_left',              # 7
            'wesker_falling_right',             # 8
            'wesker_falling_left',              # 9
            'wesker_aiming_right',              # 10
            'wesker_aiming_left',               # 11
            'wesker_firing_right',              # 12
            'wesker_firing_left',               # 13
            'wesker_reloading_frame_0',         # 14
            'wesker_reloading_frame_1'          # 15
        )

        self.__state = self.__possible_states[0]  # Текущее состояние
        self.__last_running_frame = False  # Последний использованный кадр при движении (0 или 1)
        self.__last_running_frame_count = 0  # Счетчик для изменения изображения

        self.__x_velocity = self.__y_velocity = 0
        self.__max_x_velocity = 10
        self.__max_y_velocity = 20

        self.__acceleration = 0.5
        self.__deceleration = 0.35
        self.__gravity_acceleration = GRAVITY_ACCELERATION / FPS

        # Словарь с флагами для направлений движения
        self.__direction = {
            pygame.K_w: False,
            pygame.K_s: False,
            pygame.K_a: False,
            pygame.K_d: False,
            pygame.K_SPACE: False
        }

        # Флаг для определения idle/aiming состояния по окончании движения, False = right, True = Left
        self.__last_direction = False

        self.__ammo = DEFAULT_AMMO_LOADED

        self.__reloading = False
        self.__reloading_start_time = 0
        self.__reloading_end_time = 0

        self.__aiming = False
        self.__firing = False
        self.__firing_delay = 0
        self.have_fired = False

        self.__kitty = False

    def get_movement_keys(self):
        return self.__direction.keys()

    def check_movement_event(self, event):
        if event.type == pygame.KEYDOWN:
            self.__direction[event.key] = True
        else:
            self.__direction[event.key] = False

    def check_aiming_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:  # Проверка на нажатие ПКМ
                self.__aiming = True
            elif event.button == 1:
                if self.__aiming:
                    self.__firing = True
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:
                self.__aiming = False
                self.__firing = False

    def get_ammo(self):
        return self.__ammo

    def reload(self, new_ammo):
        self.__reloading = True
        self.__reloading_start_time = self.__reloading_end_time = pygame.time.get_ticks()
        self.__ammo += new_ammo

    def get_last_direction(self):
        return self.__last_direction

    def check_wesker_logic(self, scene):
        self.__check_wall_collision(scene)
        self.__check_wesker_state()

    def __check_wall_collision(self, scene):
        if self.__rect.x < scene.get_left_wall():
            self.__rect.x = scene.get_left_wall()
            self.__x_velocity = 0
        elif self.__rect.x > WIDTH - self.__rect.width - scene.get_right_wall():
            self.__rect.x = WIDTH - self.__rect.width - scene.get_right_wall()
            self.__x_velocity = 0
        if self.__rect.y < 0:
            self.__rect.y = 0
            self.__y_velocity = 0
        elif self.__rect.y > ACTUAL_HEIGHT - self.__rect.height:
            self.__rect.y = ACTUAL_HEIGHT - self.__rect.height
            self.__y_velocity = 0
        self.__update_hitbox_rect()

    def move(self):
        # Меняем скорость в зависимости от направления ускорения по оси X
        self.__x_velocity += self.__acceleration * (self.__direction[pygame.K_d] - self.__direction[pygame.K_a]) \
                             * (not self.__aiming) * (not self.__firing) * (not self.__reloading)

        # Проверяем крайние случаи
        if not (self.__direction[pygame.K_a] or self.__direction[pygame.K_d]):
            if abs(self.__x_velocity) < self.__deceleration:
                self.__x_velocity = 0
            elif self.__x_velocity > 0:
                self.__x_velocity -= self.__deceleration
            else:
                self.__x_velocity += self.__deceleration
        elif self.__x_velocity > self.__max_x_velocity:
            self.__x_velocity = self.__max_x_velocity
        elif self.__x_velocity < -self.__max_x_velocity:
            self.__x_velocity = -self.__max_x_velocity

        # Прыжок
        if self.__rect.y >= (ACTUAL_HEIGHT - self.__image_height - 15):
            self.__y_velocity += self.__acceleration * (self.__direction[pygame.K_s] -
                                                        (self.__direction[pygame.K_w] or
                                                         self.__direction[pygame.K_SPACE]))
        self.__y_velocity += self.__gravity_acceleration
        if self.__y_velocity > self.__max_y_velocity:
            self.__y_velocity = self.__max_y_velocity
        elif self.__y_velocity < -self.__max_y_velocity:
            self.__y_velocity = -self.__max_y_velocity

        # Свободное перемещение по воздуху (смешнявка)
        # self.__y_velocity += self.__acceleration * (self.__direction[pygame.K_s] -
        #                                             (self.__direction[pygame.K_w] or
        #                                              self.__direction[pygame.K_SPACE]))
        # if not (self.__direction[pygame.K_w] or self.__direction[pygame.K_s]):
        #     self.__y_velocity += self.__gravity_acceleration
        # elif self.__y_velocity > self.__max_y_velocity:
        #     self.__y_velocity = self.__max_y_velocity
        # elif self.__y_velocity < -self.__max_y_velocity:
        #     self.__y_velocity = -self.__max_y_velocity

        # Меняем позицию
        self.__rect.x += self.__x_velocity
        self.__rect.y += self.__y_velocity
        self.__update_hitbox_rect()

    def __load_wesker_image(self, image_path):
        kitty = '_kitty' if self.__kitty else ''
        image = pygame.transform.scale(
            pygame.image.load(f'images/wesker_img/{image_path + kitty}.png').convert_alpha(),
            (self.__image_width, self.__image_height),
        )
        return image

    def __check_wesker_state(self):
        # Перезарядка
        if self.__reloading:
            self.__x_velocity = self.__y_velocity = 0
            reloading_duration = self.__reloading_end_time - self.__reloading_start_time
            self.__state = self.__possible_states[14 + (reloading_duration > 500)]
            self.__reloading_end_time = pygame.time.get_ticks()
            if reloading_duration >= 1000:
                self.__reloading = False
        # Прицеливание / выстрел
        elif self.__aiming and (self.__rect.y >= (ACTUAL_HEIGHT - self.__rect.height)):
            self.__x_velocity = self.__y_velocity = 0
            if self.__firing and (self.__firing_delay == 0) and (self.__ammo > 0):
                self.__firing_delay = pygame.time.get_ticks() + 500
                self.have_fired = True
                if not self.__kitty:
                    self.__ammo = max(0, self.__ammo - 1)
                self.__state = self.__possible_states[12 + self.__last_direction]
            else:
                self.__state = self.__possible_states[10 + self.__last_direction]
            self.__firing = False
        # Неподвижность
        elif self.__x_velocity == 0:
            self.__state = self.__possible_states[0 + self.__last_direction]
        # Прыжок
        elif (self.__y_velocity < 0) and (self.__rect.y < (ACTUAL_HEIGHT - self.__rect.height)):
            self.__state = self.__possible_states[6 + (self.__x_velocity < 0)]
        # Падение
        elif (self.__y_velocity > 0) and (self.__rect.y < (ACTUAL_HEIGHT - self.__rect.height)):
            self.__state = self.__possible_states[8 + (self.__x_velocity < 0)]
        # Движение влево
        elif self.__direction[pygame.K_a]:
            self.__last_direction = True  # Меняем флаг, чтобы получить idle_left
            self.__x_velocity += 0.45 * self.__last_running_frame  # Прерывистое движение (можно убрать для плавности)
            self.__state = self.__possible_states[4 + self.__last_running_frame]
            self.__last_running_frame_count += 1
            if self.__last_running_frame_count > (FPS // 3):
                self.__last_running_frame_count = 0
                self.__last_running_frame = not self.__last_running_frame
        # Движение вправо
        elif self.__direction[pygame.K_d]:
            self.__last_direction = False  # Меняем флаг, чтобы получить idle_right
            self.__x_velocity -= 0.45 * self.__last_running_frame  # Прерывистое движение (можно убрать для плавности)
            self.__state = self.__possible_states[2 + self.__last_running_frame]
            self.__last_running_frame_count += 1
            if self.__last_running_frame_count > (FPS // 3):
                self.__last_running_frame_count = 0
                self.__last_running_frame = not self.__last_running_frame

        # Отсчитываем задержку перед следующей возможностью выстрелить
        if self.__firing_delay and (pygame.time.get_ticks() > self.__firing_delay):
            self.__firing_delay = 0

    def change_x_position(self, new_x):
        self.__rect.x = new_x
        self.__update_hitbox_rect()

    def change_x_velocity(self, new_v):
        self.__x_velocity = new_v

    def change_y_position(self, new_y):
        self.__rect.y = new_y
        self.__update_hitbox_rect()

    def change_y_velocity(self, new_v):
        self.__y_velocity = new_v

    def change_state(self, state):
        self.__state = state

    def kitty(self):
        self.__kitty = not self.__kitty

    def get_hitbox_rect(self):
        return self.__hitbox_rect

    def __update_hitbox_rect(self):
        self.__hitbox_rect.x = self.__rect.x + 50
        self.__hitbox_rect.y = self.__rect.y

    def draw_wesker(self, screen):
        screen.blit(self.__load_wesker_image(self.__state), self.__rect)
