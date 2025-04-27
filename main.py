import pygame

from constants import WIDTH, HEIGHT, FPS
from game import Game


def main():

    game = Game(WIDTH, HEIGHT, FPS)

    game.prepare_game()
    game.run()


if __name__ == '__main__':
    main()
