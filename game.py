import os
import random
import pygame

class Settings:
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600
    FPS = 60
    FILE_PATH = os.path.dirname(os.path.abspath(__file__))
    IMAGE_PATH = os.path.join(FILE_PATH, "images")
    OBSTACLE_COUNT = 5

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((0, 128, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

class MovingObject(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)
        self.speedx = random.randint(2, 5)
        self.speedy = random.randint(2, 5)

    def update(self):
        self.rect = self.rect.move(self.speedx, self.speedy)
        if self.rect.left < 0 or self.rect.right > Settings.WINDOW_WIDTH:
            self.speedx *= -1
        if self.rect.top < 0 or self.rect.bottom > Settings.WINDOW_HEIGHT:
            self.speedy *= -1

def create_random_obstacles(obstacle_group):
    obstacle_list = []
    for _ in range(Settings.OBSTACLE_COUNT):
        valid_position = False
        while not valid_position:
            width = random.randint(60, 120)
            height = random.randint(40, 80)
            x = random.randint(0, Settings.WINDOW_WIDTH - width)
            y = random.randint(0, Settings.WINDOW_HEIGHT - height)

            new_obstacle_rect = pygame.Rect(x, y, width, height)

            if not any(obstacle.rect.colliderect(new_obstacle_rect) for obstacle in obstacle_list):
                valid_position = True
                obstacle = Obstacle(x, y, width, height)
                obstacle_list.append(obstacle)
                obstacle_group.add(obstacle)

def main():
    os.environ["SDL_VIDEO_WINDOW_POS"] = "50, 50"
    pygame.init()

    screen = pygame.display.set_mode((Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT))
    pygame.display.set_caption("Bewegliche Objekte und Hindernisse")
    clock = pygame.time.Clock()

    all_sprites = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    moving_objects = pygame.sprite.Group()

    create_random_obstacles(obstacles)
    all_sprites.add(obstacles)

    running = True
    spawn_timer = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        spawn_timer += 1
        if spawn_timer > 100:
            moving_object = MovingObject()
            all_sprites.add(moving_object)
            moving_objects.add(moving_object)
            spawn_timer = 0


        moving_objects.update()


        for obj in moving_objects:
            if pygame.sprite.spritecollideany(obj, obstacles):
                obj.kill() 


        screen.fill((0, 0, 0))


        all_sprites.draw(screen)

        pygame.display.flip()
        clock.tick(Settings.FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
