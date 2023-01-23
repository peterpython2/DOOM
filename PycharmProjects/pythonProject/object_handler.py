
from npc import *
from random import choices, randrange


class ObjectHandler:
    def __init__(self, game):

        self.game = game
        self.sprite_list = []
        self.npc_list = []
        self.npc_sprite_path = 'Resources/Sprites/NPC/'
        self.static_sprite_path = 'Resources/Sprites/Objects/'
        self.anim_sprite_path = 'Resources/Sprites/Light/'
        add_sprite = self.add_sprite
        add_npc = self.add_npc
        self.npc_positions = {}

        # spawn npcs
        self.enemies = 6  # npc count
        self.npc_types = [CacoDemonNPC] # type of npc
        self.weights = [20]
        self.restricted_area = {(i, j) for i in range(10) for j in range(10)}
        self.spawn_npc()

        # sprite map
        add_sprite(AnimatedSprite(game))

    def draw(self):
        # draw background and game objects
        self.draw_background()
        self.render_game_objects()
        pass

    def spawn_npc(self):
        # spawns npcs
        for i in range(self.enemies):
                npc = choices(self.npc_types, self.weights)[0]
                pos = x, y = randrange(self.game.map.cols), randrange(self.game.map.rows)
                while (pos in self.game.map.world_map) or (pos in self.restricted_area):
                    pos = x, y = randrange(self.game.map.cols), randrange(self.game.map.rows)
                self.add_npc(npc(self.game, pos=(x + 0.5, y + 0.5)))

    def check_win(self):
        # check if all npcs have been defeated
        if not len(self.npc_positions):
            self.game.object_renderer.victory()
            pg.display.flip()
            pg.time.delay(1500)
            self.game.new_game()

    def update(self):
        # update positions of npcs and sprites
        self.npc_positions = {npc.map_pos for npc in self.npc_list if npc.alive}
        [sprite.update() for sprite in self.sprite_list]
        [npc.update() for npc in self.npc_list]
        self.check_win()

    def add_npc(self, npc):
        # add an npc to the npc list
        self.npc_list.append(npc)

    def add_sprite(self, sprite):
        # add a sprite to the sprite list
        self.sprite_list.append(sprite)



