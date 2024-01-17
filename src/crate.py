import pygame
from explosion import Explosion

class Crate(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, player):
        pygame.sprite.Sprite.__init__(self, self.container)
        self.screen = screen
        self.x = x
        self.y = y
        self.player = player
        self.image = pygame.image.load("../assets/Crate.png")
        self.image_hurt = pygame.image.load("../assets/Crate_hurt.png")
        self.explosion_images = []
        self.explosion_images.append(pygame.image.load("../assets/CrateRubble.png"))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.health = 50
        self.hurt_timer = 0
        self.hurt_timer_max = 5
        self.just_placed = True
        self.sfx_break = pygame.mixer.Sound("../assets/sfx/break.wav")

    def update(self, projectiles, explosions):
        if not self.rect.colliderect(self.player.rect):
            self.just_placed = False
        
        for projectile in projectiles:
            if self.rect.colliderect(projectile.rect):
                self.getHit(projectile.damage)
                projectile.kill()

        for explosion in explosions:
            if explosion.damage and self.rect.colliderect(explosion.rect):
                self.getHit(explosion.damage)
                
        if self.hurt_timer > 0:
            self.hurt_timer -= 1
            image_to_draw = self.image_hurt
        else:image_to_draw = self.image

        self.screen.blit(image_to_draw, self.rect)

    def getHit(self, damage):
        self.health -= damage
        self.hurt_timer = self.hurt_timer_max
        if self.health <= 0:
            self.sfx_break.play()
            Explosion(self.screen, self.x, self.y, self.explosion_images, 5, 0, False)
            self.health = 999999
            self.kill()

class ExplosiveCrate(Crate):
    def __init__(self, screen, x, y, player):
        Crate.__init__(self, screen, x, y, player)
        self.health = 30
        self.image = pygame.image.load("../assets/ExplosiveBarrel.png")
        self.image_hurt = pygame.image.load("../assets/ExplosiveBarrel_hurt.png")
        self.explosion_images = []
        self.explosion_images.append(pygame.image.load("../assets/LargeExplosion1.png"))
        self.explosion_images.append(pygame.image.load("../assets/LargeExplosion2.png"))
        self.explosion_images.append(pygame.image.load("../assets/LargeExplosion3.png"))
        self.sfx_explode = pygame.mixer.Sound("../assets/sfx/explosion-big.wav")
        
    def getHit(self, damage):
        self.health -= damage
        self.hurt_timer = self.hurt_timer_max
        if self.health <= 0:
            self.sfx_explode.play()
            Explosion(self.screen, self.x, self.y, self.explosion_images, 3, 4, True)
            self.health = 999999
            self.kill()

