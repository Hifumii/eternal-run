import pygame
from dialog import TextButton


class StartMenu:

    def __init__(self, start_game):
        self.start_game = start_game

        self.title_image = pygame.image.load('../graphics/title_screen/eternal_run_title.png').convert_alpha()
        self.title_image.set_colorkey((0, 255, 0))
        self.title_image = pygame.transform.scale_by(self.title_image, 0.5)
        self.title_x = 480 / 2 - self.title_image.get_width() / 2
        self.title_y = 480 / 2 - self.title_image.get_height() / 2

        btn_up = pygame.image.load('../graphics/title_screen/btn_up.png').convert_alpha()
        btn_up = pygame.transform.scale_by(btn_up, 4)
        btn_down = pygame.image.load('../graphics/title_screen/btn_down.png').convert_alpha()
        btn_down = pygame.transform.scale_by(btn_down, 4)
        btn_pos = (480 / 2 - btn_up.get_width() / 2, self.title_y + self.title_image.get_height())
        self.play_button = ImageButton(btn_pos, btn_up, btn_down, on_click=self.start_game)

    def draw(self, screen):
        screen.blit(self.title_image, (self.title_x, self.title_y))
        self.play_button.draw(screen)

    def update(self):
        self.play_button.check_click()


class ImageButton:

    def __init__(self, pos, released_image, pressed_image, on_click=None):
        self.on_click = on_click

        self.x = pos[0]
        self.y = pos[1]

        self.released_image = released_image
        self.pressed_image = pressed_image
        self.image = released_image

        self.width = released_image.get_width()
        self.height = released_image.get_height()

        self.rect = pygame.Rect((self.x, self.y), (self.width, self.height))

        self.pressed = False

    def draw(self, screen):
        # button
        screen.blit(self.image, (self.x, self.y))

    def on_press(self):
        self.image = self.pressed_image
        self.pressed = True

    def on_release(self):
        self.image = self.released_image
        self.pressed = False

    def check_click(self):

        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                if not self.pressed:
                    self.on_press()
                    self.pressed = True
            else:
                if self.pressed:
                    self.on_release()
                    if self.on_click is not None:
                        self.on_click()
                    self.pressed = False
        else:
            if self.pressed:
                self.pressed = False
                self.on_release()
