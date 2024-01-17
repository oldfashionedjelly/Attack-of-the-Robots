import pygame
import toolbox
import projectile
from crate import Crate
from crate import ExplosiveCrate

class Player(pygame.sprite.Sprite):
    
    def __init__(self, screen, x, y):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.screen = screen
        self.x = x
        self.y = y
        self.pic = pygame.image.load("../assets/Player_02.png")
        self.pic_hurt = pygame.image.load("../assets/Player_02hurt.png")
        self.robot_pic = pygame.image.load("../assets/Player_robot.png")
        self.rect = self.pic.get_rect()
        self.rect.center = (self.x, self.y)
        self.speed = 8
        self.angle = 0
        self.shoot_cooldown = 0
        self.shoot_cooldown_max = 5
        self.health_max = 30
        self.health = self.health_max
        self.health_bar_width = self.pic.get_width()
        self.health_bar_height = 8
        self.health_bar_green = pygame.Rect(0, 0, self.health_bar_width, self.health_bar_height)
        self.health_bar_red = pygame.Rect(0, 0, self.health_bar_width, self.health_bar_height)
        self.alive = True
        self.hurt_timer = 0
        self.hurt_timer_max = 5
        self.crate_ammo = 8
        self.crate_cooldown = 0
        self.crate_cooldown_max = 10
        self.explosive_crate_ammo = 6
        self.shot_type = "normal"
        self.special_ammo = 0
        self.score = 0
        self.sfx_shot = pygame.mixer.Sound("../assets/sfx/shot.wav")
        self.sfx_place = pygame.mixer.Sound("../assets/sfx/bump.wav")
        self.sfx_defeat = pygame.mixer.Sound("../assets/sfx/electrocute.wav")
        self.power_timer_max = 200
        self.power_timer = self.power_timer_max
        self.stealth = False

    def update(self, enemies, explosions):
        if self.stealth:
            self.power_timer -= 1
            if self.power_timer <= 0:
                self.pic = pygame.image.load("../assets/Player_02.png")
                self.pic_hurt = pygame.image.load("../assets/Player_02hurt.png")
                self.speed = 8
                self.shoot_cooldown_max = 5
                self.stealth = False
                self.power_timer = self.power_timer_max
        
        self.rect.center = (self.x, self.y)

        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                self.getHit(enemy.damage)
                enemy.getHit(0)

        for explosion in explosions:
            if explosion.damage_player and self.rect.colliderect(explosion.rect):
                self.getHit(explosion.damage)

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        if self.crate_cooldown > 0:
            self.crate_cooldown -= 1

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.screen.get_width():
            self.rect.right = self.screen.get_width()
        if self.rect.bottom > self.screen.get_height():
            self.rect.bottom = self.screen.get_height()
        if self.rect.top < 0:
            self.rect.top = 0

        self.x = self.rect.centerx
        self.y = self.rect.centery
        
        if self.alive:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.angle = toolbox.angleBetweenPoints(self.x, self.y, mouse_x, mouse_y)
        if self.alive:
            if self.hurt_timer > 0:
                image_to_rotate = self.pic_hurt
                self.hurt_timer -= 1
            else:
                image_to_rotate = self.pic
        else:
            image_to_rotate = self.robot_pic

        image_to_draw, image_rect = toolbox.getRotatedImage(image_to_rotate, self.rect, self.angle)

        self.screen.blit(image_to_draw, image_rect)

        self.health_bar_red.x = self.rect.x
        self.health_bar_red.bottom = self.rect.y - 5
        pygame.draw.rect(self.screen, (255, 0, 0), self.health_bar_red)
        self.health_bar_green.topleft = self.health_bar_red.topleft
        health_percentage = self.health / self.health_max
        self.health_bar_green.width = self.health_bar_width * health_percentage
        if self.alive:
            pygame.draw.rect(self.screen, (0, 255, 0), self.health_bar_green)

    def move(self, x_movement, y_movement, crates):
        if self.alive:
            test_rect = self.rect
            test_rect.x += self.speed * x_movement
            test_rect.y += self.speed * y_movement
            collision = False
            for crate in crates:
                if not crate.just_placed:
                    if test_rect.colliderect(crate.rect):
                        collision = True
            if not collision:
                self.x += self.speed * x_movement
                self.y += self.speed * y_movement

    def shoot(self):
        if self.shoot_cooldown <= 0 and self.alive:
            self.sfx_shot.play()
            if self.shot_type == "normal":
                projectile.WaterBalloon(self.screen, self.x, self.y, self.angle)
            elif self.shot_type == "split":
                projectile.SplitBalloon(self.screen, self.x, self.y, self.angle - 15)
                projectile.SplitBalloon(self.screen, self.x, self.y, self.angle)
                projectile.SplitBalloon(self.screen, self.x, self.y, self.angle + 15)
                self.special_ammo -= 1
                if not self.special_ammo:
                    self.powerup("normal")
            elif self.shot_type == "drops":
                projectile.WaterDrop(self.screen, self.x, self.y, self.angle)
                self.special_ammo -= 1
                if not self.special_ammo:
                    self.powerup("normal")
            elif self.shot_type == "explosive":
                projectile.ExplosiveBalloon(self.screen, self.x, self.y, self.angle)
                self.special_ammo -= 1
                if not self.special_ammo:
                    self.powerup("normal")
            self.shoot_cooldown = self.shoot_cooldown_max
                
    def getHit(self, damage):
        if self.alive:
            self.hurt_timer = self.hurt_timer_max
            self.health -= damage
            if self.health <= 0:
                self.sfx_defeat.play()
                self.health = 0
                self.alive = False

    def placeCrate(self):
        if self.alive and self.crate_ammo > 0 and self.crate_cooldown <= 0:
            self.sfx_place.play()
            Crate(self.screen, self.x, self.y, self)
            self.crate_ammo -= 1
            self.crate_cooldown = self.crate_cooldown_max

    def placeExplosiveCrate(self):
        if self.alive and self.explosive_crate_ammo > 0 and self.crate_cooldown <= 0:
            self.sfx_place.play()
            ExplosiveCrate(self.screen, self.x, self.y, self)
            self.explosive_crate_ammo -= 1
            self.crate_cooldown = self.crate_cooldown_max

    def powerup(self, power_type):
        if power_type == "crate ammo":
            self.crate_ammo += 6
            self.getPoints(10)

        if power_type == "explosive barrel ammo":
            self.explosive_crate_ammo += 5
            self.getPoints(10)

        if power_type == "split shot":
            self.shot_type = "split"
            self.special_ammo = 15
            self.shoot_cooldown_max = 15
            self.getPoints(20)

        if power_type == "normal":
            self.shot_type = "normal"
            self.shoot_cooldown_max = 5

        if power_type == "water drop":
            self.shoot_cooldown_max = 3
            self.shot_type = "drops"
            self.special_ammo = 100
            self.getPoints(10)
            
        if power_type == "explosive balloon":
            self.shoot_cooldown_max = 15
            self.shot_type = "explosive"
            self.special_ammo = 10
            self.getPoints(20)

        if power_type == "health bonus":
            if self.health < 20:
                self.health += 10
            else:
                self.health = self.health_max

        if power_type == "stealth":
            self.pic = pygame.image.load("../assets/Player_03.png")
            self.pic_hurt = pygame.image.load("../assets/Player_03hurt.png")
            self.speed = 15
            self.shoot_cooldown_max = 3
            self.getPoints(30)
            self.stealth = True

    def getPoints(self, score):
        if self.alive:
            self.score += score
