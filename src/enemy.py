import pygame
import toolbox
import math
import random
from explosion import Explosion
from powerup import PowerUp

class Enemy(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, player):
        pygame.sprite.Sprite.__init__(self, self.container)
        self.screen = screen
        self.y = y
        self.x = x
        self.player = player
        image_number = random.randint(0, 4)
        if image_number == 0:
            self.image = pygame.image.load("../assets/Enemy_05.png")
        if image_number == 1:
            self.image = pygame.image.load("../assets/Enemy_052.png")
        if image_number == 2:
            self.image = pygame.image.load("../assets/Enemy_053.png")
        if image_number == 3:
            self.image = pygame.image.load("../assets/Enemy_054.png")
        if image_number == 4:
            self.image = pygame.image.load("../assets/Enemy_055.png")
        self.image_hurt = pygame.image.load("../assets/Enemy_05hurt.png")
        self.explosion_images = []
        self.explosion_images.append(pygame.image.load("../assets/MediumExplosion1.png"))
        self.explosion_images.append(pygame.image.load("../assets/MediumExplosion2.png"))
        self.explosion_images.append(pygame.image.load("../assets/MediumExplosion3.png"))                                 
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.angle = 0
        self.speed = 1.5
        self.health = 24
        self.hurt_timer = 0
        self.hurt_timer_max = 5
        self.damage = 0.7
        self.anger = 0
        self.anger_max = 15
        self.powerup_drop_chance = 33
        self.sfx_explode = pygame.mixer.Sound("../assets/sfx/explosion-small.wav")

    def update(self, projectiles, crates, explosions):
        self.angle = toolbox.angleBetweenPoints(self.x, self.y, self.player.x, self.player.y)

        angle_rads = math.radians(self.angle)
        self.x_move = math.cos(angle_rads) * self.speed
        self.y_move = -math.sin(angle_rads) * self.speed

        test_rect = self.rect
        new_x = self.x + self.x_move
        new_y = self.y + self.y_move

        test_rect.center = (new_x, self.y)
        for crate in crates:
            if test_rect.colliderect(crate.rect):
                new_x = self.x
                self.getAngry(crate)

        test_rect.center = (self.x, new_y)
        for crate in crates:
            if test_rect.colliderect(crate.rect):
                new_y = self.y
                self.getAngry(crate)
        
        self.x = new_x
        self.y = new_y
        self.rect.center = (self.x, self.y)

        for projectile in projectiles:
            if self.rect.colliderect(projectile.rect):
                self.getHit(projectile.damage)
                projectile.explode()

        for explosion in explosions:
            if explosion.damage and self.rect.colliderect(explosion.rect):
                self.getHit(explosion.damage)

        if self.hurt_timer <= 0:
            image_to_rotate = self.image
        else:
            image_to_rotate = self.image_hurt
            self.hurt_timer -= 1

        image_to_draw, image_rect = toolbox.getRotatedImage(image_to_rotate, self.rect, self.angle)
        
        self.screen.blit(image_to_draw, image_rect)

    def getHit(self, damage):
        if damage:
            self.hurt_timer = self.hurt_timer_max
            self.multiple = 5
        else:
            self.multiple = 2
        self.y -= self.y_move * self.multiple
        self.x -= self.x_move * self.multiple
        self.health -= damage
        if self.health <= 0:
            self.health = 999999
            self.sfx_explode.play()
            self.player.getPoints(50)
            Explosion(self.screen, self.x, self.y, self.explosion_images, 2, 0, False)
            if random.randint(0, 100) < self.powerup_drop_chance:
                PowerUp(self.screen, self.x, self.y)
            self.kill()

    def getAngry(self, crate):
        self.anger += 1
        if self.anger >= self.anger_max:
            crate.getHit(4)
            self.anger = 0
