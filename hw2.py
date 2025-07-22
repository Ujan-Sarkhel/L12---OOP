import pygame
import random

pygame.init()


WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sprite Collision Game with Sound")

background_img = pygame.image.load("istockphoto-2172528373-612x612.jpg") 
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))


WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)


clock = pygame.time.Clock()
FPS = 60


score = 0
font = pygame.font.SysFont(None, 36)


collision_sound = pygame.mixer.Sound("fast-collision-reverb-14611.mp3")  
pygame.mixer.music.load("noncopyright-music-pianos-295174.mp3")
pygame.mixer.music.play(-1)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: self.rect.x -= 5
        if keys[pygame.K_RIGHT]: self.rect.x += 5
        if keys[pygame.K_UP]: self.rect.y -= 5
        if keys[pygame.K_DOWN]: self.rect.y += 5
        self.rect.clamp_ip(screen.get_rect())

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect(
            center=(random.randint(0, WIDTH), random.randint(0, HEIGHT))
        )


player = Player()
enemies = pygame.sprite.Group()
for _ in range(7):
    enemies.add(Enemy())
all_sprites = pygame.sprite.Group(player, *enemies)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.update()

    
    collisions = pygame.sprite.spritecollide(player, enemies, dokill=True)
    if collisions:
        collision_sound.play()  
        score += len(collisions)
        for _ in range(len(collisions)):
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)


    screen.blit(background_img, (0, 0))
    all_sprites.draw(screen)
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
