import pygame

from constants import WIDTH, ACTUAL_HEIGHT, FLOOR_HEIGHT, FPS
from scenes import Scene
from wesker import Wesker


def script_main_hall(scene: Scene, wesker: Wesker, screen: pygame.Surface, clock: pygame.time.Clock):
    font = pygame.font.Font('fonts/SpecialElite-Regular.ttf', 22)
    line_color = pygame.Color(250, 250, 250)
    lines = [
        'There are only three S.T.A.R.S. members left now.',  # 0
        'Jill, Chris, and myself.',  # 1
        'Jill: Is everyone alright?',  # 2
        'Chris: Barry? Where\'s Barry?',  # 3
        'Wesker: He\'s..',  # 4
        'Jill: No...',  # 5
        '*sound of a gunshot*',  # everyone is turning to the left - 6
        'Jill: What was that?',  # 7
        'Chris: I\'ll go and check it out.',  # 8
        'Wesker: Alright.',  # 9
        'Wesker: Jill and I will stay and secure this area.',  # Chris moves even more left - 10
        'Jill: Chris...',  # 11
        'Jill: Take care.',  # 12
        'Chris: Yeah.',  # 13
        # Chris disappears
        '...',  # 14
        'Wesker: Jill, come here.',  # move Wesker to the right entrance to the stairway passage - 15
        'Jill: Sure.',  # move Jill to the right entrance to the stairway passage - 16
        'Wesker: Look over there.',  # 17
        'Jill: There\'s something downstairs.',  # 18
        'Wesker: We should go and check it out.',  # 19
        # Jill and Wesker disappear
        '...',  # black screen here - 20
        # Wesker appears at the same place
        'Took care of Jill.',  # 21
        'Need to find Chris now.'  # 22
    ]
    next_line = 0

    line_surface = font.render(lines[next_line], 1, line_color)
    line_rect = line_surface.get_rect()
    line_rect.x = WIDTH // 2 - line_rect.width // 2
    line_rect.y = (ACTUAL_HEIGHT + FLOOR_HEIGHT // 2) - line_rect.height // 2

    floor_color = (10, 10, 10)
    floor_rect = pygame.Rect(0, ACTUAL_HEIGHT, WIDTH, FLOOR_HEIGHT)

    wesker.change_x_velocity(0)
    wesker.change_y_velocity(0)
    wesker.change_x_position(WIDTH // 2 + 100)
    wesker.change_y_position(ACTUAL_HEIGHT - wesker.get_hitbox_rect().height)
    wesker.change_state('wesker_idle_left')

    script_running = True
    while script_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0
            elif (event.type == pygame.KEYDOWN) and (event.key == pygame.K_RETURN):
                if next_line < len(lines) - 1:
                    next_line += 1
                    line_surface = font.render(lines[next_line], 1, line_color)
                    line_rect = line_surface.get_rect()
                    line_rect.x = WIDTH // 2 - line_rect.width // 2
                    line_rect.y = (ACTUAL_HEIGHT + FLOOR_HEIGHT // 2) - line_rect.height // 2

                    if next_line == 6:
                        ...
                    elif next_line == 10:
                        ...
                    elif next_line == 13:
                        ...
                    elif next_line == 15:
                        wesker.change_x_position(WIDTH - 300)
                    elif next_line == 16:
                        ...
                    elif next_line == 20:
                        wesker.change_x_position(1280)
                    elif next_line == 21:
                        wesker.change_x_position(WIDTH - 300)

                else:
                    return 2

        scene.draw_for_script(screen)
        wesker.draw_wesker(screen)
        pygame.draw.rect(screen, floor_color, floor_rect)

        if next_line == 20:
            pygame.draw.rect(screen, (0, 0, 0), (0, 0, 1280, 720))

        screen.blit(line_surface, line_rect)

        pygame.display.flip()
        clock.tick(FPS)


def script_east_wing_stairway(scene: Scene, wesker: Wesker, screen: pygame.Surface, clock: pygame.time.Clock):
    font = pygame.font.Font('fonts/SpecialElite-Regular.ttf', 22)
    line_color = pygame.Color(250, 250, 250)
    lines = [
        '...',  # 0
        'Chris was here.',  # 1
        'I\'ll leave a note for him in case he comes back.',  # 2
        '...',  # 3
        'The note says: \'\'I left some bullets in the room on the right...',  # 4
        '...I\'ll go ahead and look for a way out. -Wesker-\'\''  # 5
    ]
    next_line = 0

    line_surface = font.render(lines[next_line], 1, line_color)
    line_rect = line_surface.get_rect()
    line_rect.x = WIDTH // 2 - line_rect.width // 2
    line_rect.y = (ACTUAL_HEIGHT + FLOOR_HEIGHT // 2) - line_rect.height // 2

    floor_color = (10, 10, 10)
    floor_rect = pygame.Rect(0, ACTUAL_HEIGHT, WIDTH, FLOOR_HEIGHT)

    wesker.change_x_velocity(0)
    wesker.change_y_velocity(0)
    wesker.change_x_position(WIDTH - 220)
    wesker.change_y_position(ACTUAL_HEIGHT - wesker.get_hitbox_rect().height)
    wesker.change_state('wesker_idle_left')

    script_running = True
    while script_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0
            elif (event.type == pygame.KEYDOWN) and (event.key == pygame.K_RETURN):
                if next_line < len(lines) - 1:
                    next_line += 1
                    line_surface = font.render(lines[next_line], 1, line_color)
                    line_rect = line_surface.get_rect()
                    line_rect.x = WIDTH // 2 - line_rect.width // 2
                    line_rect.y = (ACTUAL_HEIGHT + FLOOR_HEIGHT // 2) - line_rect.height // 2

                    if next_line == 3:
                        wesker.change_x_position(WIDTH // 2 - 400)

                else:
                    return 3

        scene.draw_for_script(screen)
        wesker.draw_wesker(screen)
        pygame.draw.rect(screen, floor_color, floor_rect)

        if next_line == 3:
            pygame.draw.rect(screen, (0, 0, 0), (0, 0, 1280, 720))

        screen.blit(line_surface, line_rect)

        pygame.display.flip()
        clock.tick(FPS)


def script_dark_corridor(scene: Scene, wesker: Wesker, screen: pygame.Surface, clock: pygame.time.Clock):
    font = pygame.font.Font('fonts/SpecialElite-Regular.ttf', 22)
    line_color = pygame.Color(250, 250, 250)
    lines = [
        'The doorknob is ready to fall apart.',  # 0
        'Should probably repair it...',  # 1
        '...',  # 2
        'Now I need to move on.'  # 3
    ]
    next_line = 0

    line_surface = font.render(lines[next_line], 1, line_color)
    line_rect = line_surface.get_rect()
    line_rect.x = WIDTH // 2 - line_rect.width // 2
    line_rect.y = (ACTUAL_HEIGHT + FLOOR_HEIGHT // 2) - line_rect.height // 2

    floor_color = (10, 10, 10)
    floor_rect = pygame.Rect(0, ACTUAL_HEIGHT, WIDTH, FLOOR_HEIGHT)

    wesker.change_x_velocity(0)
    wesker.change_y_velocity(0)
    wesker.change_y_position(ACTUAL_HEIGHT - wesker.get_hitbox_rect().height)
    wesker.change_state('wesker_idle_right')

    script_running = True
    while script_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0
            elif (event.type == pygame.KEYDOWN) and (event.key == pygame.K_RETURN):
                if next_line < len(lines) - 1:
                    next_line += 1
                    line_surface = font.render(lines[next_line], 1, line_color)
                    line_rect = line_surface.get_rect()
                    line_rect.x = WIDTH // 2 - line_rect.width // 2
                    line_rect.y = (ACTUAL_HEIGHT + FLOOR_HEIGHT // 2) - line_rect.height // 2

                else:
                    return 4

        scene.draw_for_script(screen)
        wesker.draw_wesker(screen)
        pygame.draw.rect(screen, floor_color, floor_rect)

        if next_line == 2:
            pygame.draw.rect(screen, (0, 0, 0), (0, 0, 1280, 720))

        screen.blit(line_surface, line_rect)

        pygame.display.flip()
        clock.tick(FPS)


def script_garden_shed(scene: Scene, wesker: Wesker, screen: pygame.Surface, clock: pygame.time.Clock):
    font = pygame.font.Font('fonts/SpecialElite-Regular.ttf', 22)
    line_color = pygame.Color(250, 250, 250)
    lines = [
        'Hope Chris hasn\'t encountered Lisa yet.',  # 0
        'I need him to be alive to show him the Tyrant...',  # 1
        'I\'ll leave a note.',  # 2
        '...',  # 3
        'The note says: \'\'Use this to protect yourself from that monster in chains that can\'t be hurt by guns...',  # 4
        '...I also fixed the doorknob to make sure you can get away. -Wesker-\'\'',  # 5
    ]
    next_line = 0

    line_surface = font.render(lines[next_line], 1, line_color)
    line_rect = line_surface.get_rect()
    line_rect.x = WIDTH // 2 - line_rect.width // 2
    line_rect.y = (ACTUAL_HEIGHT + FLOOR_HEIGHT // 2) - line_rect.height // 2

    floor_color = (10, 10, 10)
    floor_rect = pygame.Rect(0, ACTUAL_HEIGHT, WIDTH, FLOOR_HEIGHT)

    wesker.change_x_velocity(0)
    wesker.change_y_velocity(0)
    wesker.change_y_position(ACTUAL_HEIGHT - wesker.get_hitbox_rect().height)
    wesker.change_state('wesker_idle_right')

    script_running = True
    while script_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0
            elif (event.type == pygame.KEYDOWN) and (event.key == pygame.K_RETURN):
                if next_line < len(lines) - 1:
                    next_line += 1
                    line_surface = font.render(lines[next_line], 1, line_color)
                    line_rect = line_surface.get_rect()
                    line_rect.x = WIDTH // 2 - line_rect.width // 2
                    line_rect.y = (ACTUAL_HEIGHT + FLOOR_HEIGHT // 2) - line_rect.height // 2

                else:
                    return 5

        scene.draw_for_script(screen)
        wesker.draw_wesker(screen)
        pygame.draw.rect(screen, floor_color, floor_rect)

        if next_line == 3:
            pygame.draw.rect(screen, (0, 0, 0), (0, 0, 1280, 720))

        screen.blit(line_surface, line_rect)

        pygame.display.flip()
        clock.tick(FPS)


def script_gh_corr(scene: Scene, wesker: Wesker, screen: pygame.Surface, clock: pygame.time.Clock):
    font = pygame.font.Font('fonts/SpecialElite-Regular.ttf', 22)
    line_color = pygame.Color(250, 250, 250)
    lines = [
        '...',  # Chris appears on the right side of the scene - 0
        'Chris: Wesker?',  # 1
        'Wesker: Chris! You\'re alive.',  # 2
        'Chris: My words exactly.',  # 3
        'Chris: Where\'s Jill?',  # 4 - Wesker moves a little to the right, Chris moves a little to the left
        'Chris: Thought you were with her?',  # 5 - Wesker moves even more to the right, Chris - to the left
        'Wesker: Yeah, I know.',  # 6 - Wesker and Chris turn to each other
        'Wesker: We got separated.',  # 7
        'Chris: I see.',  # 8
        'Chris: Anyway, we better find a way out of here before we turn into zombie food.',  # 9
        'Chris: Got any suggestions, Wesker?',  # 10
        'Wesker: We should get a better grip on the situation.',  # 11
        'Wesker: There must be areas still to be explored in that other mansion.',  # 12
        'Wesker: Chris, I want you to check them out one more time.',  # 13
        'Wesker: I\'ll continue my investigation here.',  # 14
        'Chris: Sure thing.',  # 15
        # Chris disappears
        '...',  # 16
    ]
    next_line = 0

    line_surface = font.render(lines[next_line], 1, line_color)
    line_rect = line_surface.get_rect()
    line_rect.x = WIDTH // 2 - line_rect.width // 2
    line_rect.y = (ACTUAL_HEIGHT + FLOOR_HEIGHT // 2) - line_rect.height // 2

    floor_color = (10, 10, 10)
    floor_rect = pygame.Rect(0, ACTUAL_HEIGHT, WIDTH, FLOOR_HEIGHT)

    wesker.change_x_velocity(0)
    wesker.change_y_velocity(0)
    wesker.change_x_position(WIDTH // 2)
    wesker.change_y_position(ACTUAL_HEIGHT - wesker.get_hitbox_rect().height)
    wesker.change_state('wesker_idle_right')

    script_running = True
    while script_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0
            elif (event.type == pygame.KEYDOWN) and (event.key == pygame.K_RETURN):
                if next_line < len(lines) - 1:
                    next_line += 1
                    line_surface = font.render(lines[next_line], 1, line_color)
                    line_rect = line_surface.get_rect()
                    line_rect.x = WIDTH // 2 - line_rect.width // 2
                    line_rect.y = (ACTUAL_HEIGHT + FLOOR_HEIGHT // 2) - line_rect.height // 2

                    if next_line == 4:
                        wesker.change_x_position(WIDTH // 2 + 100)
                        ...
                    elif next_line == 5:
                        wesker.change_x_position(WIDTH // 2 + 200)
                        ...
                    elif next_line == 6:
                        wesker.change_state('wesker_idle_left')
                        ...
                    elif next_line == 16:
                        ...

                else:
                    return 6

        scene.draw_for_script(screen)
        wesker.draw_wesker(screen)
        pygame.draw.rect(screen, floor_color, floor_rect)

        screen.blit(line_surface, line_rect)

        pygame.display.flip()
        clock.tick(FPS)


def script_gh_gallery(scene: Scene, wesker: Wesker, screen: pygame.Surface, clock: pygame.time.Clock):
    font = pygame.font.Font('fonts/SpecialElite-Regular.ttf', 22)
    line_color = pygame.Color(250, 250, 250)
    lines = [
        'It seems Chris got rid of Plant 42.',  # 0
        'Rebecca (from the medical room): Richard...',  # 1
        'Rebecca is alive.',  # 2
        'I can\'t get spotted by her.',  # 3
        'Better go and check the generator.'  # 4
    ]
    next_line = 0

    line_surface = font.render(lines[next_line], 1, line_color)
    line_rect = line_surface.get_rect()
    line_rect.x = WIDTH // 2 - line_rect.width // 2
    line_rect.y = (ACTUAL_HEIGHT + FLOOR_HEIGHT // 2) - line_rect.height // 2

    floor_color = (10, 10, 10)
    floor_rect = pygame.Rect(0, ACTUAL_HEIGHT, WIDTH, FLOOR_HEIGHT)

    wesker.change_x_velocity(0)
    wesker.change_y_velocity(0)
    wesker.change_y_position(ACTUAL_HEIGHT - wesker.get_hitbox_rect().height)
    wesker.change_state('wesker_idle_right')

    script_running = True
    while script_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0
            elif (event.type == pygame.KEYDOWN) and (event.key == pygame.K_RETURN):
                if next_line < len(lines) - 1:
                    next_line += 1
                    line_surface = font.render(lines[next_line], 1, line_color)
                    line_rect = line_surface.get_rect()
                    line_rect.x = WIDTH // 2 - line_rect.width // 2
                    line_rect.y = (ACTUAL_HEIGHT + FLOOR_HEIGHT // 2) - line_rect.height // 2

                else:
                    return 7

        scene.draw_for_script(screen)
        wesker.draw_wesker(screen)
        pygame.draw.rect(screen, floor_color, floor_rect)

        screen.blit(line_surface, line_rect)

        pygame.display.flip()
        clock.tick(FPS)


def script_generator_room(scene: Scene, wesker: Wesker, screen: pygame.Surface, clock: pygame.time.Clock):
    font = pygame.font.Font('fonts/SpecialElite-Regular.ttf', 22)
    line_color = pygame.Color(250, 250, 250)
    lines = [
        'Someone took the crank that I left here.',  # 0
        'But Chris hasn\'t been here yet.',  # 1
        'I need to be careful.',  # 2
        '...',  # 3 - Wesker hides, Chris appears
        '',  # 4 - Chris moves towards the Enrico Room
        '',  # 5 - Chris moves towards the Enrico Room
        '',  # 6 - Chris disappears
        'I need to follow him.',  # 7 - Wesker is not hiding anymore
    ]
    next_line = 0

    line_surface = font.render(lines[next_line], 1, line_color)
    line_rect = line_surface.get_rect()
    line_rect.x = WIDTH // 2 - line_rect.width // 2
    line_rect.y = (ACTUAL_HEIGHT + FLOOR_HEIGHT // 2) - line_rect.height // 2

    floor_color = (10, 10, 10)
    floor_rect = pygame.Rect(0, ACTUAL_HEIGHT, WIDTH, FLOOR_HEIGHT)

    wesker.change_x_velocity(0)
    wesker.change_y_velocity(0)
    wesker.change_x_position(400)
    wesker.change_y_position(ACTUAL_HEIGHT - wesker.get_hitbox_rect().height)
    wesker.change_state('wesker_idle_right')

    script_running = True
    while script_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0
            elif (event.type == pygame.KEYDOWN) and (event.key == pygame.K_RETURN):
                if next_line < len(lines) - 1:
                    next_line += 1
                    line_surface = font.render(lines[next_line], 1, line_color)
                    line_rect = line_surface.get_rect()
                    line_rect.x = WIDTH // 2 - line_rect.width // 2
                    line_rect.y = (ACTUAL_HEIGHT + FLOOR_HEIGHT // 2) - line_rect.height // 2

                    if next_line == 3:
                        wesker.change_x_position(350)
                        # wesker.change_state('wesker_hiding')
                    elif next_line == 4:
                        ...
                    elif next_line == 5:
                        ...
                    elif next_line == 7:
                        wesker.change_x_position(WIDTH // 2)
                        wesker.change_state('wesker_idle_right')

                else:
                    return 8

        scene.draw_for_script(screen)
        wesker.draw_wesker(screen)
        pygame.draw.rect(screen, floor_color, floor_rect)

        if next_line == 3:
            pygame.draw.rect(screen, (0, 0, 0), (0, 0, 1280, 720))

        screen.blit(line_surface, line_rect)

        pygame.display.flip()
        clock.tick(FPS)


def script_enrico_room(scene: Scene, wesker: Wesker, screen: pygame.Surface, clock: pygame.time.Clock):
    font = pygame.font.Font('fonts/SpecialElite-Regular.ttf', 22)
    line_color = pygame.Color(250, 250, 250)
    lines = [
        '...',  # 0 - moves Wesker closer
        'Chris: Enrico?!',  # 1 - move Wesker closer
        'Enrico: Don\'t come any closer, Chris.',  # 2 - move Wesker closer
        'Chris: What happened?',  # 3
        'Enrico: Double-crosser!',  # 4
        'Chris: Enrico, wait!',  # 5
        '',  # 6 - Wesker shots Enrico
        'Chris: Enrico!',  # 7
        'Enrico: Umbrella...',  # 8
        '',  # 9 - Enrico dies
        'Chris: A double-crosser?',  # 10
        '',  # 11 - Chris turns towards Wesker
        'I need to get out of here, quick.',  # 12
        '...'  # 13
    ]
    next_line = 0

    line_surface = font.render(lines[next_line], 1, line_color)
    line_rect = line_surface.get_rect()
    line_rect.x = WIDTH // 2 - line_rect.width // 2
    line_rect.y = (ACTUAL_HEIGHT + FLOOR_HEIGHT // 2) - line_rect.height // 2

    floor_color = (10, 10, 10)
    floor_rect = pygame.Rect(0, ACTUAL_HEIGHT, WIDTH, FLOOR_HEIGHT)

    wesker.change_x_velocity(0)
    wesker.change_y_velocity(0)
    wesker.change_y_position(ACTUAL_HEIGHT - wesker.get_hitbox_rect().height)
    wesker.change_state('wesker_idle_right')
    # wesker.change_state('wesker_coming')

    script_running = True
    while script_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0
            elif (event.type == pygame.KEYDOWN) and (event.key == pygame.K_RETURN):
                if next_line < len(lines) - 1:
                    next_line += 1
                    line_surface = font.render(lines[next_line], 1, line_color)
                    line_rect = line_surface.get_rect()
                    line_rect.x = WIDTH // 2 - line_rect.width // 2
                    line_rect.y = (ACTUAL_HEIGHT + FLOOR_HEIGHT // 2) - line_rect.height // 2

                    if next_line == 0:
                        wesker.change_x_position(200)
                    elif next_line == 1:
                        wesker.change_x_position(400)
                    elif next_line == 2:
                        wesker.change_x_position(600)
                    elif next_line == 4:
                        wesker.change_x_position(WIDTH // 2 + 50)
                    elif next_line == 5:
                        wesker.change_state('wesker_aiming_right')
                    elif next_line == 6:
                        wesker.change_state('wesker_firing_right')
                    elif next_line == 7:
                        wesker.change_x_position(400)
                        wesker.change_state('wesker_running_left_frame_0')
                    elif next_line == 8:
                        wesker.change_x_position(200)
                        wesker.change_state('wesker_running_left_frame_1')
                    elif next_line == 9:
                        ...
                        # wesker.change_state('wesker_coming')
                else:
                    return 9

        scene.draw_for_script(screen)
        wesker.draw_wesker(screen)
        pygame.draw.rect(screen, floor_color, floor_rect)

        if next_line == 13:
            pygame.draw.rect(screen, (0, 0, 0), (0, 0, 1280, 720))

        screen.blit(line_surface, line_rect)

        pygame.display.flip()
        clock.tick(FPS)


def script_altar(scene: Scene, wesker: Wesker, screen: pygame.Surface, clock: pygame.time.Clock):
    font = pygame.font.Font('fonts/SpecialElite-Regular.ttf', 22)
    line_color = pygame.Color(250, 250, 250)
    lines = [
        '...',  # 0
        'Lisa!',  # 1
        'Wesker: You\'re a bit of a mess up!',  # 2
        '...',  # 3 - Chris appears
        'Wesker: Chris! Take a piece of action!',  # 4
    ]
    next_line = 0

    line_surface = font.render(lines[next_line], 1, line_color)
    line_rect = line_surface.get_rect()
    line_rect.x = WIDTH // 2 - line_rect.width // 2
    line_rect.y = (ACTUAL_HEIGHT + FLOOR_HEIGHT // 2) - line_rect.height // 2

    floor_color = (10, 10, 10)
    floor_rect = pygame.Rect(0, ACTUAL_HEIGHT, WIDTH, FLOOR_HEIGHT)

    lisa_rect = pygame.Rect(WIDTH - 300, ACTUAL_HEIGHT - 200, 200, 200)
    lisa_img = image = pygame.transform.scale(
                pygame.image.load(
                    f'images/entity_img/enemy_img/lisa_trevor_1_0.png'
                ).convert_alpha(),
                (200, 200),
            )

    wesker.change_x_velocity(0)
    wesker.change_y_velocity(0)
    wesker.change_x_position(300)
    wesker.change_y_position(ACTUAL_HEIGHT - wesker.get_hitbox_rect().height)
    wesker.change_state('wesker_idle_right')

    script_running = True
    while script_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0
            elif (event.type == pygame.KEYDOWN) and (event.key == pygame.K_RETURN):
                if next_line < len(lines) - 1:
                    next_line += 1
                    line_surface = font.render(lines[next_line], 1, line_color)
                    line_rect = line_surface.get_rect()
                    line_rect.x = WIDTH // 2 - line_rect.width // 2
                    line_rect.y = (ACTUAL_HEIGHT + FLOOR_HEIGHT // 2) - line_rect.height // 2

                    if next_line == 1:
                        wesker.change_state('wesker_aiming_right')

                else:
                    return 10

        scene.draw_for_script(screen)
        wesker.draw_wesker(screen)
        screen.blit(lisa_img, lisa_rect)
        pygame.draw.rect(screen, floor_color, floor_rect)

        if next_line == 0:
            pygame.draw.rect(screen, (0, 0, 0), (0, 0, 1280, 720))

        screen.blit(line_surface, line_rect)

        pygame.display.flip()
        clock.tick(FPS)


def script_altar_after_fight(scene: Scene, wesker: Wesker, screen: pygame.Surface, clock: pygame.time.Clock):
    font = pygame.font.Font('fonts/SpecialElite-Regular.ttf', 22)
    line_color = pygame.Color(250, 250, 250)
    lines = [
        'Wesker: Chris, I\'ve got this place covered. Better just hurry on ahead.',  # 0
        'Chris: Got it!',  # 1
        '...',  # 2 - Chris disappears
        'I need to get to the lab before Chris.',  # 3
    ]
    next_line = 0

    line_surface = font.render(lines[next_line], 1, line_color)
    line_rect = line_surface.get_rect()
    line_rect.x = WIDTH // 2 - line_rect.width // 2
    line_rect.y = (ACTUAL_HEIGHT + FLOOR_HEIGHT // 2) - line_rect.height // 2

    floor_color = (10, 10, 10)
    floor_rect = pygame.Rect(0, ACTUAL_HEIGHT, WIDTH, FLOOR_HEIGHT)

    wesker.change_x_velocity(0)
    wesker.change_y_velocity(0)
    wesker.change_y_position(ACTUAL_HEIGHT - wesker.get_hitbox_rect().height)
    wesker.change_state('wesker_idle_right')

    script_running = True
    while script_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0
            elif (event.type == pygame.KEYDOWN) and (event.key == pygame.K_RETURN):
                if next_line < len(lines) - 1:
                    next_line += 1
                    line_surface = font.render(lines[next_line], 1, line_color)
                    line_rect = line_surface.get_rect()
                    line_rect.x = WIDTH // 2 - line_rect.width // 2
                    line_rect.y = (ACTUAL_HEIGHT + FLOOR_HEIGHT // 2) - line_rect.height // 2

                    if next_line == 1:
                        ...

                else:
                    return 11

        scene.draw_for_script(screen)
        wesker.draw_wesker(screen)
        pygame.draw.rect(screen, floor_color, floor_rect)

        if next_line == 2:
            pygame.draw.rect(screen, (0, 0, 0), (0, 0, 1280, 720))

        screen.blit(line_surface, line_rect)

        pygame.display.flip()
        clock.tick(FPS)


def script_main_lab(scene: Scene, wesker: Wesker, screen: pygame.Surface, clock: pygame.time.Clock):
    font = pygame.font.Font('fonts/SpecialElite-Regular.ttf', 22)
    line_color = pygame.Color(250, 250, 250)
    lines = [
        '...',  # 0 - black screen
        'I managed to sneak into the Main Lab unnoticed.',  # 1 - black screen
        'It\'s probably the best time to inject myself with the Prototype Virus Birkin gave me.',  # 2 - show the Main Lab
        '...',  # 3 - Wesker injects himself with the Prototype Virus
        '...',  # 4 - Wesker moves towards the control panel and looks at it
        '...',  # 5 - Chris and Rebecca enter the scene
        'Chris: Wesker.',  # 6
        'Wesker: So you\'ve come.',  # 7
        'Wesker: Chris, you make me proud',  # 8
        'Wesker: But of course, you are one of my men.',  # 9
        'Chris: Thanks.',  # 10
        '...',  # 11 - Wesker points the gun at Chris
        'Chris: Since when, Wesker?',  # 12
        'Wesker: I\'m afraid I don\'t know what you\'re talking about.',  # 13
        'Chris: Since when have they been slipping you a paycheck?!',  # 14
        'Wesker: I think you\'re a bit confused.',  # 15
        'Wesker: I\'ve always been with Umbrella.',  # 16
        'Wesker: And S.T.A.R.S. were Umbrella\'s--',  # 17
        'Wesker: No, rather, my little piggies.',  # 18
        'Wesker: The Tyrant Virus leaked polluting this whole place.',  # 19
        'Wesker: And unfortunately I had to give up my lovely members of S.T.A.R.S.',  # 20
        'Chris: You killed them with your own dirty hands!',  # 21
        'Chris: You son of a *****!',  # 22
        'Rebecca: No...',  # 23
        'Wesker: Oh yes, dear.',  # 24
        'Wesker: Just like this.',  # 25
        '...',  # 26 - Wesker shots Rebecca, she falls. Chris turns to Rebecca.
        'Chris: Rebecca!',  # 27
        'Wesker: Don\'t move!',  # 28
        'Chris: You...',  # 29
        'Wesker: I don\'t think you want to die just yet.',  # 30
        'Wesker: I have something that\'s of some interest to you.',  # 31
        # Wesker clicks something on the control panel. Fluid in Tyrant's capsule goes down
        '...',  # 32 - Chris moves closer to capsule
        # Wesker puts down the gun and turns to the Tyrant
        'Wesker: The ultimate life-form--',  # 33
        'Wesker: Tyrant!',  # 34
        'Chris: Wesker, you\'ve become senile.',  # 35
        'Wesker: Chris, you\'ll never understand.',  # 36 - Wesker goes to Tyrant's capsule and stands in front of it
        'Wesker: It\'s magnificent.',  # 37
        '...',  # 38 - Tyrant breaks the capsule and impales Wesker's chest with his claw
        'Chris: Wesker...',  # 39
        '...',  # 40 - Wesker POV being impaled
        '...',  # 41 - Wesker POV on the ground (Tyrant is now looking towards Chris)
        '...',  # 42 - black screen
        'The End?',  # 43
    ]
    next_line = 0

    line_surface = font.render(lines[next_line], 1, line_color)
    line_rect = line_surface.get_rect()
    line_rect.x = WIDTH // 2 - line_rect.width // 2
    line_rect.y = (ACTUAL_HEIGHT + FLOOR_HEIGHT // 2) - line_rect.height // 2

    floor_color = (10, 10, 10)
    floor_rect = pygame.Rect(0, ACTUAL_HEIGHT, WIDTH, FLOOR_HEIGHT)

    wesker.change_x_velocity(0)
    wesker.change_y_velocity(0)
    wesker.change_x_position(300)
    wesker.change_y_position(ACTUAL_HEIGHT - wesker.get_hitbox_rect().height)
    wesker.change_state('wesker_idle_right')

    script_running = True
    while script_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0
            elif (event.type == pygame.KEYDOWN) and (event.key == pygame.K_RETURN):
                if next_line < len(lines) - 1:
                    next_line += 1
                    line_surface = font.render(lines[next_line], 1, line_color)
                    line_rect = line_surface.get_rect()
                    line_rect.x = WIDTH // 2 - line_rect.width // 2
                    line_rect.y = (ACTUAL_HEIGHT + FLOOR_HEIGHT // 2) - line_rect.height // 2

                    if next_line == 3:
                        ...
                        # wesker.change_state('wesker_injecting')
                    elif next_line == 4:
                        wesker.change_x_position(WIDTH - 600)
                        # wesker.change_state('wesker_control')
                    elif next_line == 11:
                        ...
                        # wesker.change_state('wesker_control_aiming')
                    elif next_line == 26:
                        ...
                        # wesker.change_state('wesker_control_firing')
                    elif next_line == 27:
                        ...
                        # wesker.change_state('wesker_control_aiming')
                    elif next_line == 32:
                        wesker.change_x_position(WIDTH - 350)
                        # move Chris closer and lower the fluid level in capsule
                        # wesker.change_state('wesker_looking_up')
                    elif next_line == 38:
                        wesker.change_y_position(ACTUAL_HEIGHT - 400)
                        # wesker.change_state('wesker_impaled')

                else:
                    return 12

        scene.draw_for_script(screen)
        wesker.draw_wesker(screen)
        pygame.draw.rect(screen, floor_color, floor_rect)

        if (next_line == 0) or (next_line == 1) or (next_line == 42) or (next_line == 43):
            pygame.draw.rect(screen, (0, 0, 0), (0, 0, 1280, 720))
        elif next_line == 40:
            ...
            # screen.blit(impaled_img, impaled_rect)
        elif next_line == 41:
            ...
            # screen.blit(on_ground_img, on_ground_rect)

        screen.blit(line_surface, line_rect)

        pygame.display.flip()
        clock.tick(FPS)
