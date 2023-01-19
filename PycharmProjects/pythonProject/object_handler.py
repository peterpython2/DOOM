from npc import *
from sprite_system import *
class ObjectHandler:
    def __init__(self, game):
        self.game = game
        self.sprite_list = []
        self.npc_list = []
        self.npc_sprite_path = 'Resources/Sprites/NPC/'
        self.static_sprite_path = 'Resources/Sprites/Objects/'
        self.animated_sprite_path = 'Resources/Sprites/Light/'
        add_sprite = self.add_sprite
        add_npc = self.add_npc
        #Sprite Map

        add_sprite(SpriteSystem(game))
        add_sprite(SpriteSystem(game, pos=(8, 3)))
        add_sprite(AnimatedSprite(game))

        #NPC Map

        add_npc(NPC(game))

    def update(self):
        [sprite.update() for sprite in self.sprite_list]
        [npc.update() for npc in self.npc_list]

    def add_npc(self, npc):
        self.npc_list.append(npc)


    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)



