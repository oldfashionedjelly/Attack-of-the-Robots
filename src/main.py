import pygame
import random
from player import Player
from projectile import WaterBalloon
from enemy import Enemy
from crate import Crate
from crate import ExplosiveCrate
from explosion import Explosion
from powerup import PowerUp
from hud import HUD

# Start the game
pygame.init()
pygame.mixer.pre_init(buffer=1024)
game_width = 1000
game_height = 650
screen = pygame.display.set_mode((game_width, game_height))
clock = pygame.time.Clock()
running = True

game_started = False

background_pic = pygame.image.load("../assets/BG_Grass.png")

player_group = pygame.sprite.Group()
Player.containers = player_group
bob_the_player = Player(screen, game_width / 2, game_height / 2)

projectile_group = pygame.sprite.Group()
WaterBalloon.containers = projectile_group

enemies_group = pygame.sprite.Group()
Enemy.container = enemies_group
enemy_spawn_timer_max = 80
enemy_spawn_timer = 0
enemy_spawn_speedup_timer_max = 300
enemy_spawn_speedup_timer = enemy_spawn_speedup_timer_max

crate_group = pygame.sprite.Group()
Crate.container = crate_group

explosionsGroup = pygame.sprite.Group()
Explosion.containers = explosionsGroup

powerupsGroup = pygame.sprite.Group()
PowerUp.containers = powerupsGroup

hud = HUD(screen, bob_the_player)

def startGame():
    global game_started
    global hud
    global bob_the_player
    global enemy_spawn_timer_max
    global enemy_spawn_timer
    global enemy_spawn_speedup_timer
    game_started = True
    hud.state = "in game"
    bob_the_player.__init__(screen, game_width / 2, game_height / 2)
    enemy_spawn_timer_max = 80
    enemy_spawn_timer = 0
    enemy_spawn_speedup_timer = enemy_spawn_speedup_timer_max
    for counter in range(0, 5):
        x = random.randint(0, game_width)
        y = random.randint(0, game_height)
        ExplosiveCrate(screen, x, y, bob_the_player)
        x = random.randint(0, game_width)
        y = random.randint(0, game_height)
        Crate(screen, x, y, bob_the_player)
    
# ***************** Loop Land Below *****************
# Everything under 'while running' will be repeated over and over again
while running:
    # Makes the game stop if the player clicks the X or presses esc
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
            
    screen.blit(background_pic, (0, 0))
    if not game_started:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                startGame()
                break

    if game_started:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            bob_the_player.move(2, 0, crate_group)
            
        if keys[pygame.K_a]:
            bob_the_player.move(-2, 0, crate_group)
            
        if keys[pygame.K_w]:
            bob_the_player.move(0, -2, crate_group)
            
        if keys[pygame.K_s]:
            bob_the_player.move(0, 2, crate_group)

        if pygame.mouse.get_pressed()[0]:
            bob_the_player.shoot()

        if keys[pygame.K_SPACE]:
            bob_the_player.placeCrate()

        if keys[pygame.K_m]:
            bob_the_player.placeExplosiveCrate()

        enemy_spawn_speedup_timer -= 1
        if enemy_spawn_speedup_timer <= 0:
            if enemy_spawn_timer > 20:
                enemy_spawn_timer_max -= 7
            enemy_spawn_speedup_timer = enemy_spawn_speedup_timer_max
            
        enemy_spawn_timer -= 1
        if enemy_spawn_timer <= 0:
            new_enemy = Enemy(screen, 0, 0, bob_the_player)
            side_to_spawn = random.randint(0, 3)
            
            if side_to_spawn == 0:
                new_enemy.y = -new_enemy.image.get_height()
                new_enemy.x = random.randint(0, game_width)
                
            elif side_to_spawn == 1:
                new_enemy.y = new_enemy.image.get_height() + game_height
                new_enemy.x = random.randint(0, game_width)

            elif side_to_spawn == 2: 
                new_enemy.x = -new_enemy.image.get_width()
                new_enemy.y = random.randint(0, game_height)

            elif side_to_spawn == 3:
                new_enemy.x = new_enemy.image.get_width() + game_width
                new_enemy.y = random.randint(0, game_height)
                
            enemy_spawn_timer = enemy_spawn_timer_max

        for power in powerupsGroup:
            power.update(bob_the_player)

        for projectile in projectile_group:
            projectile.update()

        for enemy in enemies_group:
            enemy.update(projectile_group, crate_group, explosionsGroup)

        for crate in crate_group:
            crate.update(projectile_group, explosionsGroup)

        for explosion in explosionsGroup:
            explosion.update()

        bob_the_player.update(enemies_group, explosionsGroup)

        if not bob_the_player.alive:
            if hud.state == "in game":
                hud.state = "game over"
            elif hud.state == "main menu":
                game_started = False
                player_group.empty()
                projectile_group.empty()
                enemies_group.empty()
                explosionsGroup.empty()
                crate_group.empty()
                powerupsGroup.empty()
            
    hud.update()

    # Tell pygame to update the screen
    pygame.display.flip()
    clock.tick(40)
    pygame.display.set_caption("ATTACK OF THE ROBOTS fps: " + str(clock.get_fps()))
