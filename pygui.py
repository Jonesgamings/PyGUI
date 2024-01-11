import pygame

pygame.init()
pygame.font.init()

class Element:

    def __init__(self, window, position, dimensions, colour, active_colour, border_size, border_colour, draggable) -> None:
        self.window = window
        self.x, self.y = position
        self.width, self.height = dimensions
        self.hitbox = pygame.Rect(self.x - self.width / 2, self.y - self.height / 2, self.width, self.height)

        self.colour = colour
        self.rest_colour = colour
        self.active_colour = active_colour

        self.border_size = border_size
        self.border_colour = border_colour

        self.draggable = draggable
        self.selected = False

        self.window.add_element(self)

    def check_event(self, event):
        mousex, mousey = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.hitbox.collidepoint(mousex, mousey):
                self.selected = True

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.selected = False

    def draw(self, screen):
        pass

class Label(Element):

    def __init__(self, window, position, dimensions, text = None, text_size = 0, text_colour = (0, 0, 0), bold = False, italic = None, font = None, colour = (250, 250, 250), border_colour = (200, 200, 200), border_size = 2) -> None:
        super().__init__(window, position, dimensions, colour, colour, border_size, border_colour, False)
        self.text = text
        self.text_size = text_size
        self.text_colour = text_colour
        self.bold = bold
        self.italic = italic
        self.font = font

        self.pygame_font = pygame.font.SysFont(self.font, self.text_size, self.bold, self.italic)
        if self.text: self.text_height = self.pygame_font.size(self.text)[1]

    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, self.hitbox)
        pygame.draw.rect(screen, self.border_colour, self.hitbox, self.border_size)
        if not self.text: return
        for line, text in enumerate(self.text.split("\n")):
            screen.blit(self.pygame_font.render(text, True, self.text_colour), (self.hitbox.left + 5, self.hitbox.top + 5 + self.text_height * line))

class Button(Label):

    def __init__(self, window, position, dimensions, text = None, text_size = 0, function = None, function_args = [], function_kargs = {}, text_colour=(0, 0, 0), bold=False, italic=None, font=None, colour=(250, 250, 250), border_colour=(200, 200, 200), border_size=2, active_colour = (150, 150, 150), on_hover = False) -> None:
        super().__init__(window, position, dimensions, text, text_size, text_colour, bold, italic, font, colour, border_colour, border_size)
        self.function = function
        self.active_colour = active_colour
        self.on_hover = on_hover
        self.function_args = function_args
        self.function_kargs = function_kargs
        self.hovering = False
        self.selected = False

    def check_event(self, event):
        mousex, mousey = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.hitbox.collidepoint(mousex, mousey):
                if self.function: self.function(*self.function_args, **self.function_kargs)
                self.selected = True

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.selected = False

        if self.hitbox.collidepoint(mousex, mousey):
            self.hovering = True

        else:
            self.hovering = False

    def draw(self, screen):
        if not self.on_hover:
            if self.selected: self.colour = self.active_colour
            if not self.selected: self.colour = self.rest_colour
        else:
            if self.hovering: self.colour = self.active_colour
            if not self.hovering: self.colour = self.rest_colour
        return super().draw(screen)
    
class Entry(Element):

    def __init__(self, window, position, dimensions, colour, active_colour, border_size, border_colour, default_text = None, text_size = 0, text_colour = (255, 255, 255), ) -> None:
        super().__init__(window, position, dimensions, colour, active_colour, border_size, border_colour, False)

class SelectionBox(Element):

    def __init__(self, window, position, dimensions, colour, active_colour, border_size, border_colour, draggable) -> None:
        super().__init__(window, position, dimensions, colour, active_colour, border_size, border_colour, draggable)

class Window:

    def __init__(self, width = 0, height = 0, fullscreen = False, colour = (200, 200, 200)) -> None:
        self.window = pygame.display.set_mode((width, height), pygame.FULLSCREEN if fullscreen else None)
        self.width, self.height = self.window.get_size()
        self.fullscreen = fullscreen
        self.colour = colour

        self.running = True
        self.keybinds = {}
        self.elements = []

        self.initialise()

    def close(self):
        self.running = False

    def add_element(self, element):
        self.elements.append(element)

    def initialise(self):
        if self.fullscreen: self.keybinds[pygame.K_ESCAPE] = [self.close]
        self.keybinds[pygame.QUIT] = [self.close]

    def do_keypress(self, key):
        if key in self.keybinds:
            functions = self.keybinds[key]
            for function in functions:
                function()

    def send_event(self, event):
        for element in self.elements:
            element.check_event(event)

    def draw_elements(self):
        for element in self.elements:
            element.draw(self.window)

    def mainloop(self):
        while self.running:

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    self.do_keypress(event.key)

                self.send_event(event)

            self.window.fill(self.colour)
            self.draw_elements()
            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    def test(a, b):
        print(a, b)

    window = Window(fullscreen=True)
    l = Label(window, (200, 200), (200, 45), "HI\n121134134", 32)
    b = Button(window, (300, 300), (50, 50), border_colour=(100, 100, 100), on_hover=True, function=test, function_kargs={"a":"2", "b":"1"})
    window.mainloop()