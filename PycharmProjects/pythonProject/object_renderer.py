import pygame as pg

import timer
from settings import *
from timer import *

class ObjectRenderer(Timer):
    def __init__(self, game, ):
        # initialize variables
        self.game = game
        self.screen = game.screen
        self.wall_textures = self.load_wall_textures()
        self.pain_screen = self.get_texture('Resources/Sprites/pain_screen.png', RES)
        self.victory_image = self.get_texture('Resources/victory.png', RES)
        self.defeat_image = self.get_texture('Resources/defeat.png', RES)

    def draw(self):
        # draw background and game objects
        self.draw_background()
        self.render_game_objects()

    def game_over(self):
        # draw game over screen
        self.screen.blit(self.defeat_image, (0, 0))
        self.timer.Timer.save_time()
        self.timer.Timer.print_results()


    def victory(self):
        # draw game over screen
        self.screen.blit(self.victory_image, (0, 0))

    def player_damage(self):
        # draw pain screen when player takes damage
        self.screen.blit(self.pain_screen, (0, 0))

    def draw_background(self):
        # draws the background
        pg.draw.rect(self.screen, FLOOR_COLOR, (0, HALF_HEIGHT, WIDTH, HEIGHT))
        pg.draw.rect(self.screen, CEILING_COLOR, (0, 0, WIDTH, HALF_HEIGHT))

    def render_game_objects(self):
        # sort and render game objects
        list_objects = sorted(self.game.raycasting.object_to_render, key=lambda t: t[0], reverse=True)
        for depth, image, pos in list_objects:
            self.screen.blit(image, pos)

    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        # load and return a texture
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)

    def load_wall_textures(self):
        # load and return wall textures
        return {
            1: self.get_texture('Resources/Textures/tex-1.png'),
            2: self.get_texture('Resources/Textures/tex-2.png'),

        }
