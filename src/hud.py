import pygame
import toolbox

class HUD():
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player
        self.state = "main menu"
        self.hud_font = pygame.font.SysFont("herculanumttf", 30)
        self.hud_font_small = pygame.font.SysFont("herculanumttf", 20)
        self.game_over_font = pygame.font.SysFont("herculanumttf", 80)
        self.score_text = self.hud_font.render("Score: " + str(self.player.score), True, (30, 30, 175))

        self.title_image = pygame.image.load("../assets/title.png")
        self.start_text = self.hud_font.render("Press any key to start", True, (60, 60, 60))

        self.game_over_text = self.game_over_font.render("Game Over", True, (255, 255, 255))
        self.reset_button = pygame.image.load("../assets/BtnReset.png")
        self.tutorial_text = self.hud_font_small.render("WASD to move - CLICK to shoot - SPACE for crate - M for explosive barrel", True, (255, 0, 0))
        
        self.crate_icon = pygame.image.load("../assets/Crate.png")
        self.explosive_crate_icon = pygame.image.load("../assets/ExplosiveBarrel.png")
        self.split_icon = pygame.image.load("../assets/iconSplit.png")
        self.burst_icon = pygame.image.load("../assets/iconBurst.png")
        self.normal_icon = pygame.image.load("../assets/BalloonSmall3.png")
        self.drop_icon = pygame.image.load("../assets/iconStream.png")

        self.crate_ammo_tile = AmmoTile(self.screen, self.crate_icon, self.hud_font)
        self.explosive_crate_ammo_tile = AmmoTile(self.screen, self.explosive_crate_icon, self.hud_font)
        self.balloon_ammo_tile = AmmoTile(self.screen, self.normal_icon, self.hud_font)

    def update(self):
        if self.state == "in game":
            self.score_text = self.hud_font.render("Score: " + str(self.player.score), True, (30, 30, 175))
            self.screen.blit(self.score_text, (30, 30))

            tile_x = 0
            self.crate_ammo_tile.update(tile_x, self.screen.get_height(), self.player.crate_ammo)
            tile_x += 72
            self.explosive_crate_ammo_tile.update(tile_x, self.screen.get_height(), self.player.explosive_crate_ammo)
            tile_x += 72
        
            if self.player.shot_type == "normal":
                self.balloon_ammo_tile = AmmoTile(self.screen, self.normal_icon, self.hud_font)
            if self.player.shot_type == "split":
                self.balloon_ammo_tile = AmmoTile(self.screen, self.split_icon, self.hud_font)
            if self.player.shot_type == "drops":
                self.balloon_ammo_tile = AmmoTile(self.screen, self.drop_icon, self.hud_font)
            if self.player.shot_type == "explosive":
                self.balloon_ammo_tile = AmmoTile(self.screen, self.burst_icon, self.hud_font)
            self.balloon_ammo_tile.update(tile_x, self.screen.get_height(), self.player.special_ammo)

        elif self.state == "main menu":
            title_x, title_y = toolbox.findMiddle(self.title_image, self.screen)
            self.screen.blit(self.title_image, (title_x, title_y - 50))
            text_x, text_y = toolbox.findMiddle(self.start_text, self.screen)
            self.screen.blit(self.start_text, (text_x, text_y + 100))
            tutorial_x, tutorial_y = toolbox.findMiddle(self.tutorial_text, self.screen)
            self.screen.blit(self.tutorial_text, (tutorial_x, tutorial_y + 250))

        elif self.state == "game over":
            text_x, text_y = toolbox.findMiddle(self.game_over_text, self.screen)
            self.screen.blit(self.game_over_text, (text_x, text_y - 110))
            self.score_text = self.hud_font.render("Final Score: " + str(self.player.score), True, (30, 30, 175))
            text_x, text_y = toolbox.findMiddle(self.score_text, self.screen)
            self.screen.blit(self.score_text, (text_x, text_y - 40))
            button_x, button_y = toolbox.findMiddle(self.reset_button, self.screen)
            button_rect = self.screen.blit(self.reset_button, (button_x, button_y + 65))
            
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_position = pygame.mouse.get_pos()
                    if button_rect.collidepoint(mouse_position):
                        self.state = "main menu"
        
class AmmoTile():
    def __init__(self, screen, icon, font):
        self.screen = screen
        self.icon = icon
        self.font = font
        self.bg_tile = pygame.image.load("../assets/hudTile.png")

    def update(self, x, y, ammo):
        tile_rect = self.bg_tile.get_rect()
        tile_rect.bottomleft = (x, y)
        self.screen.blit(self.bg_tile, tile_rect)
        
        icon_rect = self.icon.get_rect()
        icon_rect.center = tile_rect.center
        self.screen.blit(self.icon, icon_rect)

        ammo_text = self.font.render(str(ammo), True, (30, 175, 30))
        self.screen.blit(ammo_text, tile_rect.topleft)
