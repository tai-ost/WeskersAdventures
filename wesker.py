import pygame

from constants import WIDTH, HEIGHT, FPS, ACTUAL_HEIGHT, GRAVITY_ACCELERATION


class Wesker:
    def __init__(self):
        self.__hitbox_width = 100
        self.__hitbox_height = 250

        self.__image_width = 220
        self.__image_height = 250

        self.__x_coord = WIDTH // 2 - self.__image_width // 2
        self.__y_coord = ACTUAL_HEIGHT - self.__image_height

        self.__rect = pygame.Rect(self.__x_coord, self.__y_coord, self.__image_width, self.__image_height)
        self.__hitbox_rect = pygame.Rect(self.__rect.x, self.__rect.y, self.__hitbox_width, self.__hitbox_height)

        # Словарь с возможными состояниями и соответствующими им названиями изображений
        self.__possible_states = {
            0: 'wesker_idle_right',
            1: 'wesker_idle_left',
            2: 'wesker_running_right_frame_0',
            3: 'wesker_running_right_frame_1',
            4: 'wesker_running_left_frame_0',
            5: 'wesker_running_left_frame_1',
            6: 'wesker_jumping_right',
            7: 'wesker_jumping_left',
            8: 'wesker_falling_right',
            9: 'wesker_falling_left',
            10: 'wesker_aiming_right',
            11: 'wesker_aiming_left',
            12: 'wesker_firing_right',
            13: 'wesker_firing_left'
        }

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
            pygame.K_d: False
        }

        self.__last_direction = False  # Флаг для определения idle состояния по окончании движения

        self.__ammo = 30

        self.__aiming = False
        self.__firing = False
        self.__firing_delay = 0
        self.__have_fired = False

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
                self.__firing = True
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:
                self.__aiming = False

    def shot_fired(self):
        return self.__have_fired, self.__last_direction

    def check_wesker_logic(self):
        self.__check_wall_collision()

    def __check_wall_collision(self):
        if self.__rect.x < 0:
            self.__rect.x = 0
            self.__x_velocity = 0
        elif self.__rect.x > WIDTH - self.__rect.width:
            self.__rect.x = WIDTH - self.__rect.width
            self.__x_velocity = 0
        if self.__rect.y < 0:
            self.__rect.y = 0
            self.__y_velocity = 0
        elif self.__rect.y > ACTUAL_HEIGHT - self.__rect.height:
            self.__rect.y = ACTUAL_HEIGHT - self.__rect.height
            self.__y_velocity = 0

    def move(self):
        # Меняем скорость в зависимости от направления ускорения по оси X
        self.__x_velocity += self.__acceleration * (self.__direction[pygame.K_d] - self.__direction[pygame.K_a]) \
                             * (not self.__aiming)

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
            self.__y_velocity += self.__acceleration * (self.__direction[pygame.K_s] - self.__direction[pygame.K_w])
        self.__y_velocity += self.__gravity_acceleration
        if self.__y_velocity > self.__max_y_velocity:
            self.__y_velocity = self.__max_y_velocity
        elif self.__y_velocity < -self.__max_y_velocity:
            self.__y_velocity = -self.__max_y_velocity

        # Свободное перемещение по воздуху (смешнявка)
        # self.__y_velocity += self.__acceleration * (self.__direction[pygame.K_s] - self.__direction[pygame.K_w])
        # if not (self.__direction[pygame.K_w] or self.__direction[pygame.K_s]):
        #     self.__y_velocity += self.__gravity_acceleration
        # elif self.__y_velocity > self.__max_y_velocity:
        #     self.__y_velocity = self.__max_y_velocity
        # elif self.__y_velocity < -self.__max_y_velocity:
        #     self.__y_velocity = -self.__max_y_velocity

        # Меняем позицию
        self.__rect.x += self.__x_velocity
        self.__rect.y += self.__y_velocity

    def __load_wesker_image(self, image_path):
        image = pygame.transform.scale(
            pygame.image.load(f'images/wesker_img/{image_path}.png').convert_alpha(),
            (self.__image_width, self.__image_height),
        )
        return image

    def __check_wesker_state(self):
        if self.__aiming and (self.__rect.y >= (ACTUAL_HEIGHT - self.__rect.height)):
            self.__x_velocity = 0
            if self.__firing and (self.__firing_delay == 0) and (self.__ammo > 0):
                self.__firing_delay = FPS // 2
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
        if self.__firing_delay > 0:
            self.__firing_delay -= 1

    def change_x_position(self, new_x):
        self.__rect.x = new_x

    def get_rect(self):  # ;)
        return self.__rect

    def draw_wesker(self, screen):
        self.__check_wesker_state()
        screen.blit(self.__load_wesker_image(self.__state), self.__rect)
