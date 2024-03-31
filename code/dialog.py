import pygame


class DialogBox:
    X_POSITION = 35
    Y_POSITION = 390
    MAX_WIDTH = 380

    def __init__(self):
        self.qcm = None
        self.box = pygame.image.load('../dialogs/dialog_box.png')
        self.box = pygame.transform.scale(self.box, (420, 80))
        self.texts = []
        self.text = ''
        self.text_index = 0
        self.letter_index = 0
        self.font = pygame.font.Font("../dialogs/dialog_font.ttf", 12)
        self.input_box = InputBox((480 - 300) / 2, self.Y_POSITION - 50, 300, 30, font=self.font,
                                  close_text_input=self.close_text_input)
        self.input_box_active = False
        self.reading = False
        self.main_dialog_index = 0

    def handle_input(self, events):
        if self.qcm is not None:
            self.qcm.handle_input(events)
        elif self.input_box_active:
            self.input_box.handle_event(events)
            self.input_box.update()

    def close_text_input(self, correct_answer: bool):
        self.input_box_active = False
        if correct_answer:
            self.main_dialog = self.texts
            self.texts = self.good_answer_dialog
            self.text_index = -1
        else:
            self.main_dialog = self.texts
            self.texts = self.bad_answer_dialog
            self.text_index = -1
        self.next_text()

    def end_qcm(self, correct_answer: bool):
        self.qcm = None
        if correct_answer:
            self.next_text()
        else:
            self.reading = False

    def execute(self, dialog: list):

        if self.reading:
            if self.qcm is None and self.input_box_active is False:
                self.next_text()

        else:
            self.reading = True
            self.text_index = 0
            self.texts = dialog
            self.text = self.texts[self.text_index]

    def render(self, screen):

        if self.reading:
            screen.blit(self.box, (self.X_POSITION, self.Y_POSITION))
            if self.qcm is not None:
                text = self.text
                text_image = Text(text, (self.X_POSITION + 50, self.Y_POSITION + 20))
                text_image.draw(screen)
                self.qcm.draw(screen)
            elif self.input_box_active:
                text = self.text
                text_image = Text(text, (self.X_POSITION + 50, self.Y_POSITION + 20))
                text_image.draw(screen)
                self.input_box.draw(screen)
            else:
                self.letter_index += 1

                if self.letter_index >= len(self.text):
                    self.letter_index = self.letter_index
                text = self.text[0:self.letter_index]
                text_image = Text(text, (self.X_POSITION + 50, self.Y_POSITION + 20))
                text_image.draw(screen)

    # def blit_text(surface, text, pos, font):
    # words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    #  space = font.size(' ')[0]  # The width of a space.
    # max_width, max_height = surface.get_size()
    # x, y = pos
    # for line in words:
    #   for word in line:
    #      word_surface = font.render(word)
    #     word_width, word_height = word_surface.get_size()
    #    if x + word_width >= max_width:
    #       x = pos[0]  # Reset the x.
    #      y += word_height  # Start on new row.
    # surface.blit(word_surface, (x, y))
    # x += word_width + space
    # x = pos[0]  # Reset the x.
    # y += word_height  # Start on new row.

    def next_text(self):
        self.text_index += 1
        self.letter_index = 0

        if self.text_index >= len(self.texts):
            # fermer le dialogue (donc creer statut ouvert ferme)
            if self.main_dialog_index == 0:
                self.reading = False
            else:
                self.texts = self.main_dialog
                self.text_index = self.main_dialog_index + 1
                self.main_dialog_index = 0
                self.text = self.texts[self.text_index]

        elif type(self.texts[self.text_index]) is list:
            # si le dialogue est une question

            correct_answer = self.texts[self.text_index][1]

            if type(correct_answer) is int:
                # on crée le qcm
                answers = self.texts[self.text_index][2:]
                self.qcm = MultipleChoices(answers=answers, correct_answer_index=correct_answer, end_qcm=self.end_qcm)

            elif type(correct_answer) is str:
                self.input_box_active = True
                self.input_box.change_answer(correct_answer)
                self.good_answer_dialog = self.texts[self.text_index][2]
                self.bad_answer_dialog = self.texts[self.text_index][3]
                self.main_dialog_index = self.text_index

            # on affiche la question
            self.text = self.texts[self.text_index][0]

        else:
            self.text = self.texts[self.text_index]


class Text:

    def __init__(self, text, pos):
        self.text_color = (0, 0, 0)

        lines = text.splitlines()

        self.font = pygame.font.Font("../dialogs/dialog_font.ttf", 12)
        self.text_image = pygame.surface.Surface((480, 480))
        self.text_image.fill((255, 0, 255))
        self.text_image.set_colorkey((255, 0, 255))
        y = pos[1]
        x = pos[0]
        for i, l in enumerate(lines):
            line_image = self.font.render(l, False, self.text_color)
            self.text_image.blit(line_image, (x, y + i * line_image.get_height()))

    def draw(self, screen):
        # text
        screen.blit(self.text_image, (0, 0))


class TextButton:

    def __init__(self, text, center, on_click=None, text_color=(0, 0, 0),
                 bg_color=(255, 255, 255), bg_hover_color=(166, 209, 224), outline_color=(61, 100, 151),
                 font=None, outlines=True, margin=10, line_spacing=1):

        self.on_click = on_click
        self.margin = margin
        self.line_spacing = line_spacing

        self.center_x = center[0]
        self.center_y = center[1]

        if font is None:
            font = pygame.font.SysFont(None, 12)
        self.font = font

        self.text = text

        self.text_color = text_color
        self.bg_normal_color = bg_color
        self.bg_hover_color = bg_hover_color
        self.bg_color = self.bg_normal_color
        self.outlines = outlines
        self.outline_color = outline_color

        self.normal_text_image = text_to_image(self.text, self.font, self.text_color, margin=self.margin,
                                               line_spacing=self.line_spacing)
        self.width = self.normal_text_image.get_width()
        self.height = self.normal_text_image.get_height()
        self.x = self.center_x - self.width / 2
        self.y = self.center_y - self.height / 2

        self.shrink = 0.9
        self.normal_rect = pygame.Rect((self.x, self.y), (self.width, self.height))
        self.shrunk_rect = self.normal_rect.scale_by(self.shrink)
        self.normal_outline_rect = pygame.Rect(self.normal_rect.x - 2, self.normal_rect.y - 2,
                                               self.normal_rect.width + 4, self.normal_rect.height + 4)
        self.shrunk_outline_rect = pygame.Rect(self.shrunk_rect.x - 2, self.shrunk_rect.y - 2,
                                               self.shrunk_rect.width + 4, self.shrunk_rect.height + 4)
        self.rect = self.normal_rect
        self.outline_rect = self.normal_outline_rect

        self.normal_text_rect = self.normal_text_image.get_rect(center=self.normal_rect.center)
        self.shrunk_text_image = pygame.transform.scale_by(self.normal_text_image, self.shrink)
        self.shrunk_text_rect = self.shrunk_text_image.get_rect(center=self.shrunk_rect.center)
        self.text_image = self.normal_text_image
        self.text_rect = self.normal_text_rect

        self.pressed = False

    def resize(self, width):
        self.width = width
        self.x = self.center_x - self.width / 2
        self.normal_rect = pygame.Rect((self.x, self.y), (self.width, self.height))
        self.shrunk_rect = self.normal_rect.scale_by(self.shrink)
        self.normal_outline_rect = pygame.Rect(self.normal_rect.x - 2, self.normal_rect.y - 2,
                                               self.normal_rect.width + 4, self.normal_rect.height + 4)
        self.shrunk_outline_rect = pygame.Rect(self.shrunk_rect.x - 2, self.shrunk_rect.y - 2,
                                               self.shrunk_rect.width + 4, self.shrunk_rect.height + 4)
        self.rect = self.normal_rect
        self.outline_rect = self.normal_outline_rect

        self.normal_text_rect = self.normal_text_image.get_rect(center=self.normal_rect.center)
        self.shrunk_text_image = pygame.transform.scale_by(self.normal_text_image, self.shrink)
        self.shrunk_text_rect = self.shrunk_text_image.get_rect(center=self.shrunk_rect.center)
        self.text_image = self.normal_text_image
        self.text_rect = self.normal_text_rect

    def move(self, x, y):
        self.x = x
        self.y = y

        self.normal_rect = pygame.Rect((self.x, self.y), (self.width, self.height))
        self.shrunk_rect = self.normal_rect.scale_by(self.shrink)
        self.normal_outline_rect = pygame.Rect(self.normal_rect.x - 2, self.normal_rect.y - 2,
                                               self.normal_rect.width + 4, self.normal_rect.height + 4)
        self.shrunk_outline_rect = pygame.Rect(self.shrunk_rect.x - 2, self.shrunk_rect.y - 2,
                                               self.shrunk_rect.width + 4, self.shrunk_rect.height + 4)
        self.rect = self.normal_rect
        self.outline_rect = self.normal_outline_rect

        self.normal_text_rect = self.normal_text_image.get_rect(center=self.normal_rect.center)
        self.shrunk_text_image = pygame.transform.scale_by(self.normal_text_image, self.shrink)
        self.shrunk_text_rect = self.shrunk_text_image.get_rect(center=self.shrunk_rect.center)
        self.text_image = self.normal_text_image
        self.text_rect = self.normal_text_rect

    def draw(self, screen):

        if self.outlines:
            # outlines
            pygame.draw.rect(screen, self.outline_color, self.outline_rect, 0)

        # button
        pygame.draw.rect(screen, self.bg_color, self.rect)

        # text
        screen.blit(self.text_image, self.text_rect)

    def on_hover(self):

        self.bg_color = self.bg_hover_color

    def unhover(self):

        self.bg_color = self.bg_normal_color

    def on_press(self):

        self.rect = self.shrunk_rect
        self.outline_rect = self.shrunk_outline_rect

        self.text_image = self.shrunk_text_image
        self.text_rect = self.shrunk_text_rect

        self.pressed = True

    def on_release(self):

        self.rect = self.normal_rect
        self.outline_rect = self.normal_outline_rect

        self.text_image = self.normal_text_image
        self.text_rect = self.normal_text_rect

        self.pressed = False


class MultipleChoices:

    def __init__(self, answers: list[str], correct_answer_index: int, end_qcm):
        self.end_qcm = end_qcm
        self.font = pygame.font.Font("../dialogs/dialog_font.ttf", 11)
        self.buttons = []
        biggest_width = 0
        btn_offset = 20
        total_height = btn_offset
        x = 480 / 2
        y = 480 / 2
        for answer in answers:
            btn = TextButton(text=answer,
                             center=(x, y),
                             font=self.font,
                             margin=5)
            biggest_width = max(biggest_width, btn.width)
            self.buttons.append(btn)
            total_height += btn.height + btn_offset

        y = 480 / 2 - total_height / 2 + btn_offset
        x = 480 / 2 - biggest_width / 2
        for i, btn in enumerate(self.buttons):
            btn.resize(width=biggest_width)
            btn.move(x, y)
            y += btn.height + btn_offset

        self.correct_answer_index = correct_answer_index
        self.btn_selected_index = 0
        self.buttons[self.btn_selected_index].on_hover()

    def handle_input(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    # Changer de niveau sélectionné avec le clavier (vers le bas)

                    self.buttons[self.btn_selected_index].unhover()
                    self.buttons[self.btn_selected_index].on_release()
                    self.btn_selected_index += 1
                    if self.btn_selected_index >= len(self.buttons):
                        self.btn_selected_index = 0
                    self.buttons[self.btn_selected_index].on_hover()

                elif event.key == pygame.K_UP or event.key == pygame.K_z:
                    # Changer de niveau sélectionné avec le clavier (vers le haut)

                    self.buttons[self.btn_selected_index].unhover()
                    self.buttons[self.btn_selected_index].on_release()
                    self.btn_selected_index -= 1
                    if self.btn_selected_index < 0:
                        self.btn_selected_index = len(self.buttons) - 1
                    self.buttons[self.btn_selected_index].on_hover()

                elif event.key == pygame.K_SPACE:

                    self.buttons[self.btn_selected_index].on_press()

            elif event.type == pygame.KEYUP:

                if event.key == pygame.K_SPACE:
                    if self.buttons[self.btn_selected_index].pressed:
                        # Tester la réponse sélectionnée
                        self.test_answer(self.btn_selected_index)
                    self.buttons[self.btn_selected_index].on_release()

    def test_answer(self, index):
        if index == self.correct_answer_index:
            self.end_qcm(True)
        else:
            self.end_qcm(False)

    def draw(self, screen):
        for btn in self.buttons:
            btn.draw(screen)


class Sign:

    def __init__(self, text):
        self.bg_color = (66, 66, 66)
        self.outline_color = (255, 255, 255)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.Font("../dialogs/dialog_font.ttf", 12)
        self.margin = 10
        self.line_spacing = 1

        self.width = 300
        self.height = 200
        self.x = 480 / 2 - self.width / 2
        self.y = 480 / 2 - self.height / 2
        self.rect = pygame.rect.Rect(self.x, self.y, self.width, self.height)

        self.text_image = text_to_image(text, self.font, self.text_color, self.margin, self.line_spacing)
        self.text_pos = (
            self.rect.centerx - self.text_image.get_width() / 2, self.rect.centery - self.text_image.get_height() / 2)

    def draw(self, screen):
        pygame.draw.rect(screen, self.bg_color, self.rect)
        pygame.draw.rect(screen, self.outline_color, self.rect, 1)
        screen.blit(self.text_image, self.text_pos)


def text_to_image(text, font, color=(0, 0, 0), margin=0, line_spacing=0):
    lines = text.splitlines()

    biggest_line = 0
    total_height = 2 * margin
    text_lines = []

    for line_text in lines:
        line = font.render(line_text, False, color)
        text_lines.append(line)
        biggest_line = max(biggest_line, line.get_width())
        total_height += (line.get_height() + line_spacing)

    text_width = biggest_line + 2 * margin
    text_height = total_height
    text_image = pygame.surface.Surface((text_width, text_height), pygame.SRCALPHA)

    line_pos = (margin, margin)
    for i, line in enumerate(text_lines):
        text_image.blit(line, line_pos)
        line_pos = (line_pos[0], line_pos[1] + line.get_height() + line_spacing)

    return text_image


class InputBox:

    def __init__(self, x, y, w, h, close_text_input, text='Écris ta réponse', font=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_active = (105, 105, 105)
        self.color_inactive = (0, 0, 0)
        self.color = self.color_inactive
        self.text = text
        if font is None:
            self.font = pygame.font.SysFont(None, 10)
        else:
            self.font = font
        self.txt_surface = self.font.render(self.text, True, self.color)
        self.active = False
        self.first_click = True
        self.correct_answer = None
        self.close_text_input = close_text_input

    def change_answer(self, answer):
        self.text = 'Écris ta réponse'
        self.correct_answer = answer

    def handle_event(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if self.rect.collidepoint(event.pos):
                    # Toggle the active variable.
                    if self.first_click:
                        self.text = ''
                        self.first_click = False
                    self.active = not self.active
                else:
                    self.active = False
                # Change the current color of the input box.
                self.color = self.color_active if self.active else self.color_inactive
                self.txt_surface = self.font.render(self.text, True, self.color)
            if event.type == pygame.KEYDOWN:
                if self.active:
                    if event.key == pygame.K_RETURN:
                        self.active = False
                        self.color = self.color_inactive
                        self.txt_surface = self.font.render(self.text, True, self.color)

                    elif event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                    else:
                        self.text += event.unicode
                    # Re-render the text.
                    self.txt_surface = self.font.render(self.text, True, self.color)
                else:
                    if event.key == pygame.K_RETURN:
                        self.test_answer(self.text)

    def test_answer(self, answer):
        if answer == self.correct_answer:
            self.close_text_input(True)
        else:
            self.close_text_input(False)

    def update(self):
        # Resize the box if the text is too long.
        self.old_width = self.rect.w
        width = max(self.rect.w, self.txt_surface.get_width() + 10)
        if self.old_width != width:
            self.rect.x = self.rect.centerx - width / 2
            self.rect.w = width

    def draw(self, screen):
        # Blit the white background
        pygame.draw.rect(screen, (255, 255, 255), self.rect)
        # Blit the text
        screen.blit(self.txt_surface, (self.rect.centerx - self.txt_surface.get_width() / 2, self.rect.y + 5))
        # Blit the outline rect
        pygame.draw.rect(screen, self.color, self.rect, 2)
