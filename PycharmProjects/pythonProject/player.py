from settings import *
import pygame as pg
import math


# class Player defines methods of control for the player in the game and ways the player interacts with other game elements

class Player:
    def __init__(self, game):

        # sets initial variables of player such as location, health, angle, ect.
        self.game = game
        self.x, self.y = PLAYER_POS
        self.angle = PLAYER_ANGLE
        self.shot = False
        self.health = PLAYER_MAX_HEALTH
        self.rel = 0
        self.health_recovery_delay = 600
        self.time_prev = pg.time.get_ticks()
        self.complete = True

    def single_fire_event(self, event):

        # when right mouse button is clicked shot occurs and reloading animation is set into action
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1 and not self.shot and not self.game.weapon.reloading:
                self.shot = True
                self.game.weapon.reloading = True

    def recover_health(self):

        # increases players health by one if players health is less than maximum and after the recovery delay passes
        if self.check_health_recovery_delay() and self.health < PLAYER_MAX_HEALTH:
            self.health += 1

    def check_health_recovery_delay(self):

        # checks if delay is passed by comparing current time with the previous time health was recovered
        time_now = pg.time.get_ticks()
        if time_now - self.time_prev > self.health_recovery_delay:
            self.time_prev = time_now
            return True

    def check_game_over(self):

        # checks if health is less than 0, if so calls game_over
        if self.health < 1:
            complete = False
            self.game.object_renderer.game_over()
            pg.display.flip()
            pg.time.delay(1500)
            self.game.new_game()

    def get_damage(self, damage):

        # decreases players health by set amount when attacked
        self.health -= damage
        self.game.object_renderer.player_damage()
        self.check_game_over()

    def movement(self):

        # calculates sin and cosine of angle
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)

        # initialize dx and dy
        dx, dy = 0, 0

        # calculates speed based on delta time (time passed since the last frame) and speed constant
        speed = PLAYER_SPEED * self.game.delta_time
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a

        keys = pg.key.get_pressed()

        # if w is pressed, move player in direction of angle
        if keys[pg.K_w]:
            dx += speed_cos
            dy += speed_sin

        # if s is pressed, move player in opposite direction of angle
        if keys[pg.K_s]:
            dx += -speed_cos
            dy += -speed_sin

        # if a key is pressed, move player left of angle
        if keys[pg.K_a]:
            dx += speed_sin
            dy += -speed_cos

        # if d key is pressed, move player right of angle
        if keys[pg.K_d]:
            dx += -speed_sin
            dy += speed_cos

        self.check_wall_collision(dx, dy)

        self.angle %= math.tau

    def check_wall(self, x, y):

        # check if current position is on  the map
        return (x, y) not in self.game.map.world_map

    def check_wall_collision(self, dx, dy):

        # scales movement by player size and delta time (time that has passed since last frame)
        scale = PLAYER_SIZE_SCALE / self.game.delta_time

        # check for collisions with walls on x and y-axis
        if self.check_wall(int(self.x + dx * scale), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * scale)):
            self.y += dy

    def draw(self):

        # draws player in overhead view mini map, not relevant to final code
        pg.draw.line(self.game.screen, 'yellow', (self.x * 100, self.y * 100),
                     (self.x * 100 + WIDTH * math.cos(self.angle),
                      self.y * 100 + WIDTH * math.sin(self.angle)), 2)
        pg.draw.circle(self.game.screen, 'green', (self.x * 100, self.y * 100), 15)

    def mouse_control(self):

        # initializes mx and my with mouse position
        mx, my = pg.mouse.get_pos()

        # makes sure the mouse does not leave the game window
        if mx < MOUSE_BORDER_LEFT or mx > MOUSE_BORDER_RIGHT:
            pg.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
        if my < MOUSE_BORDER_UP or my > MOUSE_BORDER_DOWN:
            pg.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])

        # gets relative movement of mouse on the x-axis
        self.rel = pg.mouse.get_rel()[0]

        # limits range of relative movement of the mouse
        self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))

        # increases player angle by amount proportional to mouse movement using set sensitivity and delta time
        self.angle += self.rel * MOUSE_SENSITIVITY * self.game.delta_time

    def update(self):

        # updates elements of the Player class
        self.movement()
        self.mouse_control()
        self.recover_health()

    @property
    # returns player coordinates
    def pos(self):
        return self.x, self.y

    @property
    # returns which tile of the map player is on
    def map_pos(self):
        return int(self.x), int(self.y)
