from sprite_system import *
from random import random



class NPC(AnimatedSprite):
    def __init__(self, game, path='Resources/Sprites/NPC/0.png', pos=(10.5, 1),
                 scale=0.6, shift=0.1, animation_time=180):
        super().__init__(game, path, pos, scale, shift, animation_time)

        # gets image files from specified path

        self.attack_images = self.get_images(self.path + '/attack')
        self.death_images = self.get_images(self.path + '/death')
        self.idle_images = self.get_images(self.path + '/idle')
        self.pain_images = self.get_images(self.path + '/pain')
        self.walk_images = self.get_images(self.path + '/walk')

        # sets initial variables for NPC

        self.size = 20
        self.alive = True
        self.pain = False
        self.ray_cast_value = False
        self.frame_counter = 0
        self.player_search_trigger = False

    def update(self):

        # updates elements of the NPC class

        self.check_animation_time()
        self.get_sprite()
        self.run_logic()


    def check_wall(self, x, y):

        # check if the position is a wall
        return (x, y) not in self.game.map.world_map

    def check_wall_collision(self, dx, dy):

        # checks if the npc is colliding with a wall

        if self.check_wall(int(self.x + dx * self.size), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * self.size)):
            self.y += dy

    def movement(self):

        # gets position on the path to the player
        next_pos = self.game.pathfinding.get_path(self.map_pos, self.game.player.map_pos)
        next_x, next_y = next_pos

        # move towards the next position if it is not occupied by another NPC
        if next_pos not in self.game.object_handler.npc_positions:
            angle = math.atan2(next_y + 0.5 - self.y, next_x + 0.5 - self.x)
            dx = math.cos(angle) * self.speed
            dy = math.sin(angle) * self.speed
            self.check_wall_collision(dx, dy)

    def attack(self):

        # checks if animation trigger it true
        if self.animation_trigger:

            # if random number is less than accuracy player takes damage
            if random() < self.accuracy:
                self.game.player.get_damage(self.attack_damage)

    def animate_death(self):

        # check if the npc is alive, if animation trigger is true and frame counter < number of death images than ...
        # ... it will rotate through images until all have been shown
        if not self.alive:
            if self.animation_trigger and self.frame_counter < len(self.death_images) - 1:
                self.death_images.rotate(-1)
                self.image = self.death_images[0]
                self.frame_counter += 1

    def animate_pain(self):

        # animates pain attribute
        self.animate(self.pain_images)

        # if animation trigger is true set pain to false
        if self.animation_trigger:
            self.pain = False

    def check_hit_in_npc(self):

        # checks if ray_cast_value and shot attrubute are true
        if self.ray_cast_value and self.game.player.shot:

            # check if position of npc screen position is within range of player screen position
            if HALF_WIDTH - self.sprite_half_width < self.screen_x < HALF_WIDTH + self.sprite_half_width:

                # sets player shot to false, set pain to true, subtract weapon damage from health, check health
                self.game.player.shot = False
                self.pain = True
                self.health -= self.game.weapon.damage
                self.check_health()

    def check_health(self):
        # check if npc health less than 1, if yes set alive attribute to false
        if self.health < 1:
            self.alive = False


    def run_logic(self):

        # checks if npc is alive, if yes set ray_cast_value = ray_cast_npc and check if npc has been hit
        if self.alive:
            self.ray_cast_value = self.ray_cast_player_npc()
            self.check_hit_in_npc()

            # checks if pain if true, if yes runs pain animation
            if self.pain:
                self.animate_pain()

            # if npc sees the player, set player_search_trigger = True
            elif self.ray_cast_value:
                self.player_search_trigger = True

                # if distance between npc and player is less that attack distance run attack animation and ...
                # ...attack function
                if self.dist < self.attack_dist:
                    self.animate(self.attack_images)
                    self.attack()
                # if distance is more run walk animations and run movement function
                else:
                    self.animate(self.walk_images)
                    self.movement()
            # check if player_search_trigger is true, if yes run walk animation and movement function
            elif self.player_search_trigger:
                self.animate(self.walk_images)
                self.movement()
            # if npc does not see player and player search trigger is not true, run idle animation
            else:
                self.animate(self.idle_images)
        # if npc is dead run death animation
        else:
            self.animate_death()

    # property method to return the map position of npc as a tuple
    @property
    def map_pos(self):
        return int(self.x), int(self.y)

    def ray_cast_player_npc(self):

        # check if player and npc are on the same place on the map
        if self.game.player.map_pos == self.map_pos:
            return True

        # initializes variables for distances of walls and player in the horizontal and vertical directions
        wall_dist_v, wall_dist_h = 0, 0
        player_dist_v, player_dist_h = 0, 0

        # gets players position
        ox, oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos

        # get angle of ray
        ray_angle = self.theta

        sin_a = math.sin(ray_angle)
        cos_a = math.cos(ray_angle)

        # check horizontal distances
        y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)

        depth_hor = (y_hor - oy) / sin_a
        x_hor = ox + depth_hor * cos_a

        delta_depth = dy / sin_a
        dx = delta_depth * cos_a

        for i in range(MAX_DEPTH):
            tile_hor = int(x_hor), int(y_hor)
            # check if the current tile is npc position
            if tile_hor == self.map_pos:
                player_dist_h = depth_hor
                break
            # check if current tile is a wall
            if tile_hor in self.game.map.world_map:
                wall_dist_h = depth_hor
                break
            x_hor += dx
            y_hor += dy
            depth_hor += delta_depth

        # check vertical distances
        x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)

        depth_vert = (x_vert - ox) / cos_a
        y_vert = oy + depth_vert * sin_a

        delta_depth = dx / cos_a
        dy = delta_depth * sin_a

        for i in range(MAX_DEPTH):
            # check if the current tile is the npc position
            tile_vert = int(x_vert), int(y_vert)
            if tile_vert == self.map_pos:
                player_dist_v = depth_vert
                break
            # check if current tile is the wall
            if tile_vert in self.game.map.world_map:
                wall_dist_v = depth_vert
                break
            x_vert += dx
            y_vert += dy
            depth_vert += delta_depth

        player_dist = max(player_dist_v, player_dist_h)
        wall_dist = max(wall_dist_v, wall_dist_h)

        if 0 < player_dist < wall_dist or not wall_dist:
            return True
        return False

    def draw_ray_cast(self):

        # used for top-down map view, not needed for final reasult
        pg.draw.circle(self.game.screen, 'red', (100 * self.x, 100 * self.y), 15)
        if self.ray_cast_player_npc():
            pg.draw.line(self.game.screen, 'orange', (100 * self.game.player.x, 100 * self.game.player.y),
                         (100 * self.x, 100 * self.y), 2)


# class for the npc used, defines initial variables as well as base image
class CacoDemonNPC(NPC):
    def __init__(self, game, path='Resources/Sprites/NPC/0.png', pos=(10.5, 6.5),
                 scale=0.7, shift=0.001, animation_time=250):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.attack_dist = 1.0
        self.health = 150
        self.attack_damage = 25
        self.speed = 0.05
        self.accuracy = 0.5


