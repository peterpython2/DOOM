from sprite_system import *

# weapon class that builds off of the AnimatedSprite class
class Weapon(AnimatedSprite):
    def __init__(self, game, path='Resources/Sprites/Gun/9.png', scale=3, animation_time=90):
        super().__init__(game=game, path=path, scale=scale, animation_time=animation_time)
        self.images = deque(
            [pg.transform.smoothscale(img, (self.image.get_width() * scale, self.image.get_height() * scale))
             for img in self.images])
        # calculates positon of weapon 
        self.weapon_pos = (HALF_WIDTH - self.images[0].get_width() // 2, HEIGHT - self.images[0].get_height())
        self.reloading = False
        self.num_images = len(self.images)
        self.frame_counter = 0
        self.damage = 50

    def animate_shot(self):

        # check if reloading attribute is true
        if self.reloading:
            # set shot to false so player cannot shoot while reloading
            self.game.player.shot = False

            # rotates through image deque when animation_trigger is true, counts number of frames shown
            if self.animation_trigger:
                self.images.rotate(-1)
                self.image = self.images[0]
                self.frame_counter += 1

                # if the frame_counter is equal to the number of images animation if complete and self.reloading is...
                # ...false, also sets frame counter to zero so frame_counter is never greater than num_images
                if self.frame_counter == self.num_images:
                    self.reloading = False
                    self.frame_counter = 0
    def draw(self):

        # draws weapon onto screen

        self.game.screen.blit(self.images[0], self.weapon_pos)

    def update(self):

        # updates elements of the Weapon class

        self.check_animation_time()
        self.animate_shot()
