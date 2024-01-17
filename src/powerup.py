import pygame
import random
import toolbox

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, screen, x, y):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.screen = screen
        self.x = x
        self.y = y
        self.pick_power = random.randint(0, 6)
        if self.pick_power == 0: #Crate ammo increase with red background
            self.image = pygame.image.load("../assets/powerupCrate.png")
            self.background_image = pygame.image.load("../assets/powerupBackgroundRed.png")
            self.power_type = "crate ammo"

        if self.pick_power == 1: #ExplosiveBarrel ammo increase with orange background
            self.image = pygame.image.load("../assets/powerupExplosiveBarrel.png")                       
            self.background_image = pygame.image.load("../assets/powerupBackgroundOrange.png")
            self.power_type = "explosive barrel ammo"

        if self.pick_power == 2: #Split shot with a blue background
            self.image = pygame.image.load("../assets/powerupSplit.png")                       
            self.background_image = pygame.image.load("../assets/powerupBackgroundBlue.png")
            self.power_type = "split shot"

        if self.pick_power == 3: #Water drops with green background
            self.image = pygame.image.load("../assets/powerupDrop.png")                       
            self.background_image = pygame.image.load("../assets/powerupBackgroundGreen.png")
            self.power_type = "water drop"

        if self.pick_power == 4: #Explode balloons with purple background
            self.image = pygame.image.load("../assets/SplashSmall1.png")                       
            self.background_image = pygame.image.load("../assets/powerupBackgroundPurple.png")
            self.power_type = "explosive balloon"

        if self.pick_power == 5: #More health with yellow background
            self.power_type = "health bonus"
            self.image = pygame.image.load("../assets/Heart.png")                       
            self.background_image = pygame.image.load("../assets/powerupBackgroundYellow.png")

        if self.pick_power == 6: #Black background with extra speed and ninja
            self.power_type = "stealth"
            self.image = pygame.image.load("../assets/balloonWhite.png")                       
            self.background_image = pygame.image.load("../assets/powerupBackgroundBlack.png")

        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.background_angle = 0
        self.spin_speed = 6
        self.despawn_timer = 150
        self.sfx_pickup = pygame.mixer.Sound("../assets/sfx/powerup.wav")

    def update(self, player):
        self.background_angle += self.spin_speed
        bg_image_to_draw, bg_rect = toolbox.getRotatedImage(self.background_image, self.rect, self.background_angle)
            
        if self.rect.colliderect(player.rect):
            self.sfx_pickup.play()
            player.powerup(self.power_type)
            self.kill()

        self.despawn_timer -= 1
        if self.despawn_timer <= 0:
            self.kill()

        if self.despawn_timer % 10 > 5 or self.despawn_timer > 45:
            self.screen.blit(bg_image_to_draw, bg_rect)
            self.screen.blit(self.image, self.rect)
            
