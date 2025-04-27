import pygame

from game import Game


def main():

    game = Game()

    game.prepare_game()
    game.run()


if __name__ == '__main__':
    main()
