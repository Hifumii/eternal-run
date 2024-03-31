import pygame


class AnimateSprite(pygame.sprite.Sprite):

    def __init__(self, name):
        super().__init__()

        self.sprite_sheet = pygame.image.load(f'../graphics/characters/{name}.png')
        self.animation_index = 0
        self.clock = 0
        self.status = 'idle_down'
        self.direction = 'down'
        self.images = {
            'idle_down': self.get_images(0, 1, False),
            'idle_up': self.get_images(16, 1, False),
            'idle_right': self.get_images(32, 1, False),
            'idle_left': self.get_images(32, 1, True),
            'moving_down': self.get_images(64, 2, True),
            'moving_up': self.get_images(96, 2, False),
            'moving_right': self.get_images(128, 2, False),
            'moving_left': self.get_images(128, 2, True),
        }
        self.speed = 2

    def animate(self):

        if self.clock >= 100:
            self.animation_index += 1  # passer à l'image suivante

            self.clock = 0

        if self.animation_index >= len(self.images[self.status]):
            self.animation_index = 0

        self.image = self.images[self.status][self.animation_index]
        self.image.set_colorkey(0, 0)
        self.clock += self.speed + 8

    def get_images(self, start_x, nb_image=1, flipped=False):
        images = []

        y = 0
        for i in range(nb_image):
            x = start_x + 16 * i
            image = self.get_image(x, y, flipped)
            images.append(image)

        return images

    def get_image(self, x, y, flipped=False):
        image = pygame.Surface([16, 16])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 16, 16))
        if flipped:
            image = pygame.transform.flip(image, True, False)
        return image
