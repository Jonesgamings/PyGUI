import pygame

pygame.font.init()
pygame.display.init()

class Element:

    def __init__(self, window, position, dimensions, colour, active_colour, border_size, border_colour) -> None:
        self.window = window
        self.x, self.y = position
        self.width, self.height = dimensions
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

        self.colour = colour
        self.rest_colour = colour
        self.active_colour = active_colour

        self.border_size = border_size
        self.border_colour = border_colour

        self.selected = False
        self.visible = True

        self.window.add_element(self)

    def get_position(self):
        return (self.x + self.window.get_position()[0], self.y + self.window.get_position()[1])

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def set_visibility(self, visible):
        self.visible = visible

    def toggle_visibility(self):
        self.visible = not self.visible

    def check_event(self, event):
        pass

    def draw(self, screen):
        pass
    
class Label(Element):

    def __init__(self, window, position, dimensions, text = "", text_size = 0, text_colour = (0, 0, 0), bold = False, italic = None, font = None, colour = (250, 250, 250), border_colour = (200, 200, 200), border_size = 2) -> None:
        super().__init__(window, position, dimensions, colour, colour, border_size, border_colour)
        self.text = text
        self.text_size = text_size
        self.text_colour = text_colour
        self.bold = bold
        self.italic = italic
        self.font = font

        self.pygame_font = pygame.font.SysFont(self.font, self.text_size, self.bold, self.italic)
        self.text_height = self.pygame_font.size(self.text)[1]

    def draw(self, screen):
        if not self.visible: return
        window_pos = self.window.get_position()
        draw_rect = (self.hitbox.x + window_pos[0], self.hitbox.y + window_pos[1], self.hitbox.width, self.hitbox.height)
        pygame.draw.rect(screen, self.colour, draw_rect)
        pygame.draw.rect(screen, self.border_colour, draw_rect, self.border_size)
        if not self.text: return
        for line, text in enumerate(self.text.split("\n")):
            screen.blit(self.pygame_font.render(text, True, self.text_colour), (self.hitbox.left + 5, self.hitbox.top + 5 + self.text_height * line))

class Button(Label):

    def __init__(self, window, position, dimensions, text = "", text_size = 32, function = None, function_args = [], function_kargs = {}, text_colour=(0, 0, 0), bold=False, italic=None, font=None, colour=(250, 250, 250), border_colour=(200, 200, 200), border_size=2, active_colour = (150, 150, 150), on_hover = False) -> None:
        super().__init__(window, position, dimensions, text, text_size, text_colour, bold, italic, font, colour, border_colour, border_size)
        self.function = function
        self.active_colour = active_colour
        self.on_hover = on_hover
        self.function_args = function_args
        self.function_kargs = function_kargs
        self.hovering = False
        self.selected = False

    def check_event(self, event):
        if not self.visible: return
        mousex, mousey = pygame.mouse.get_pos()
        window_pos = self.window.get_position()
        mousex -= window_pos[0]
        mousey -= window_pos[1]
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
        if not self.visible: return

        if not self.on_hover:
            if self.selected: self.colour = self.active_colour
            if not self.selected: self.colour = self.rest_colour
        else:
            if self.hovering: self.colour = self.active_colour
            if not self.hovering: self.colour = self.rest_colour

        super().draw(screen)
    
class Entry(Element):

    def __init__(self, window, position, dimensions, colour=(250, 250, 250), border_size = 2, border_colour=(200, 200, 200), default_text = None, text_size = 32, text_colour = (0, 0, 0), bold = False, italic = False, font = None, hidden = None, lines = 1, input_character = "|", restricted = True, tab_length = 4) -> None:
        super().__init__(window, position, dimensions, colour, None, border_size, border_colour)
        self.default_text = default_text
        self.text_size = text_size
        self.text_colour = text_colour
        self.bold = bold
        self.italic = italic
        self.font = font
        self.hidden = hidden
        self.lines = lines
        self.input_character = input_character
        self.restricted = restricted
        self.tab_length = tab_length

        self.starting_width = self.width

        self.default_text_colour = (200, 200, 200)

        self.text = ["" for _ in range(self.lines)]
        self.raw_text = ""
        self.current_line = 0
        self.current_pos = 0

        self.pygame_font = pygame.font.SysFont(self.font, self.text_size, self.bold, self.italic)
        self.text_height = self.pygame_font.size(self.text[0])[1]

    def get(self, line=None):
        if line:
            return self.text[line]
        
        else:
            return "\n".join(self.text)
        
    def add_char_line(self, key):
        if key in [pygame.K_ESCAPE]: return
        if self.hidden: text = "".join(self.hidden for _ in range(len(self.text[self.current_line])))
        else: text = self.text[self.current_line]

        if self.pygame_font.size(text + key + self.input_character)[0] > self.width:
            if self.restricted:
                self.current_line += 1
                if self.current_line == self.lines: 
                    self.current_line = self.lines - 1
                    self.current_pos = len(self.text[self.current_line])

                else:
                    self.add_char_line(key)

            else:
                self.width += self.pygame_font.size(self.hidden if self.hidden else key)[0]
                self.hitbox.width = self.width

                self.text[self.current_line] = self.text[self.current_line][:self.current_pos] + key + self.text[self.current_line][self.current_pos:]
                self.raw_text = self.raw_text[:self.current_pos] + key + self.raw_text[self.current_pos:]
                self.current_pos += 1

        else:
            self.text[self.current_line] = self.text[self.current_line][:self.current_pos] + key + self.text[self.current_line][self.current_pos:]
            self.raw_text = self.raw_text[:self.current_pos] + key + self.raw_text[self.current_pos:]
            self.current_pos += 1

    def check_event(self, event):
        if not self.visible: return
        mousex, mousey = pygame.mouse.get_pos()
        window_pos = self.window.get_position()
        mousex -= window_pos[0]
        mousey -= window_pos[1]
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.hitbox.collidepoint(mousex, mousey):
                self.selected = not self.selected

            else:
                self.selected = False
            
        if self.selected:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.current_line += 1
                    if self.current_line == self.lines: 
                        self.current_line = self.lines - 1
                        
                    else:
                        self.current_pos = len(self.text[self.current_line])

                elif event.key == pygame.K_BACKSPACE:
                    if self.current_pos == 0:
                        self.current_line -= 1
                        if self.current_line < 0: 
                            self.current_line = 0

                        else:
                            self.current_pos = len(self.text[self.current_line])

                    else:
                        removed_char = self.text[self.current_line][self.current_pos-1]
                        self.text[self.current_line] = self.text[self.current_line][:self.current_pos - 1] + self.text[self.current_line][self.current_pos:]
                        self.raw_text = self.raw_text[:self.current_pos - 1] + self.raw_text[self.current_pos:]
                        self.current_pos -= 1

                        if not self.restricted and self.width > self.starting_width:
                            self.width -= self.pygame_font.size(self.hidden if self.hidden else removed_char)[0]
                            self.hitbox.width = self.width

                elif event.key == pygame.K_UP:
                    self.current_line -= 1
                    if self.current_line < 0: 
                        self.current_line = 0
                    
                    self.current_pos = len(self.text[self.current_line]) if self.current_pos > len(self.text[self.current_line]) else self.current_pos

                elif event.key == pygame.K_DOWN:
                    self.current_line += 1
                    if self.current_line == self.lines: 
                        self.current_line = self.lines - 1

                    self.current_pos = len(self.text[self.current_line]) if self.current_pos > len(self.text[self.current_line]) else self.current_pos

                elif event.key == pygame.K_RIGHT:
                    self.current_pos += 1
                    if self.current_pos > len(self.text[self.current_line]):
                        self.current_line += 1
                        if self.current_line == self.lines:
                            self.current_line = self.lines - 1
                            self.current_pos -= 1

                        else: 
                            self.current_pos = 0

                elif event.key == pygame.K_LEFT:
                    self.current_pos -= 1
                    if self.current_pos < 0:
                        self.current_line -= 1
                        if self.current_line < 0:
                            self.current_line = 0
                            self.current_pos += 1
                        else: 
                            self.current_pos = len(self.text[self.current_line])

                elif event.key == pygame.K_TAB:
                    for _ in range(self.tab_length):
                        self.add_char_line(" ")

                else:
                    key = event.unicode
                    if key == None or key == "": return
                    self.add_char_line(key)

    def draw_text(self, screen):
        window_pos = self.window.get_position()
        if len(self.raw_text) == 0 and self.default_text and not self.selected:
            screen.blit(self.pygame_font.render(self.default_text, True, self.default_text_colour), (self.hitbox.left + 5 + window_pos[0], self.hitbox.top + 5 + window_pos[1]))

        else:
            for line, text in enumerate(self.text):

                if self.hidden: text = "".join(self.hidden for _ in range(len(text)))

                if self.current_line == line and self.selected:
                    text = text[:self.current_pos] + self.input_character + text[self.current_pos:]

                screen.blit(self.pygame_font.render(text, True, self.text_colour), (self.hitbox.left + 5 + window_pos[0], self.hitbox.top + 5 + window_pos[1] + self.text_height * line))


    def draw(self, screen):
        if not self.visible: return
        window_pos = self.window.get_position()
        draw_rect = (self.hitbox.x + window_pos[0], self.hitbox.y + window_pos[1], self.hitbox.width, self.hitbox.height)
        pygame.draw.rect(screen, self.colour, draw_rect)
        pygame.draw.rect(screen, self.border_colour, draw_rect, self.border_size)
        self.draw_text(screen)

class ProgressBar(Element):

    def __init__(self, window, position, dimensions, max_value, colour=(250, 250, 250), border_size = 2, border_colour=(100, 100, 100), min_value = 0, starting_value = None, bar_colour = (0, 255, 0), interactable = False, vertical = False, reversed_dir = False) -> None:
        super().__init__(window, position, dimensions, colour, None, border_size, border_colour)
        self.min_value = min_value
        self.max_value = max_value
        self.current_value = starting_value
        self.bar_colour = bar_colour
        self.interactable = interactable
        self.vertical = vertical
        self.reversed_dir = reversed_dir
        if self.current_value == None: self.current_value = self.min_value
        if self.current_value > self.max_value: self.current_value = self.max_value
        if self.current_value < self.min_value: self.current_value = self.min_value
        if self.vertical: self.bar_rect = pygame.Rect(self.x + self.border_size, self.y + self.border_size, self.width - 2*self.border_size, 0)
        else: self.bar_rect = pygame.Rect(self.x + self.border_size, self.y + self.border_size, 0, self.height - 2*self.border_size)

    def set_value(self, value):
        if value < self.min_value: value = self.min_value
        if value > self.max_value: value = self.max_value
        self.current_value = value

    def set_percentage(self, percentage):
        if percentage < 0: percentage = 0
        if percentage > 1: percentage = 1
        self.current_value = ((self.max_value - self.min_value) * percentage) + self.min_value

    def get_percentage(self):
        return (self.current_value - self.min_value) / (self.max_value - self.min_value)

    def get(self):
        return (self.current_value, self.get_percentage())

    def check_event(self, event):
        if not self.visible: return
        if self.interactable:
            mousex, mousey = pygame.mouse.get_pos()
            window_pos = self.window.get_position()
            mousex -= window_pos[0]
            mousey -= window_pos[1]
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.hitbox.collidepoint(mousex, mousey):
                    self.selected = True

            if event.type == pygame.MOUSEBUTTONUP and self.selected:
                self.selected = False

            if self.selected:
                if self.vertical:
                    if self.reversed_dir: self.set_percentage(1-(mousey - self.x) / self.height)
                    else: self.set_percentage((mousey - self.x) / self.height)

                else:
                    if self.reversed_dir: self.set_percentage(1-(mousex - self.x) / self.width)
                    else: self.set_percentage((mousex - self.x) / self.width)

        if self.vertical:
            self.bar_rect.height = ((self.current_value - self.min_value) / (self.max_value - self.min_value)) * (self.height - 2*self.border_size)
            if self.reversed_dir: self.bar_rect.y = self.height - self.bar_rect.height + self.y - self.border_size

        else: 
            self.bar_rect.width = ((self.current_value - self.min_value) / (self.max_value - self.min_value)) * (self.width - 2*self.border_size)
            if self.reversed_dir: self.bar_rect.x = self.width - self.bar_rect.width + self.x - self.border_size
    
    def draw(self, screen):
        if not self.visible: return
        window_pos = self.window.get_position()
        draw_rect = (self.hitbox.x + window_pos[0], self.hitbox.y + window_pos[1], self.hitbox.width, self.hitbox.height)
        draw_bar_rect = (self.bar_rect.x + window_pos[0], self.bar_rect.y + window_pos[1], self.bar_rect.width, self.bar_rect.height)
        pygame.draw.rect(screen, self.colour, draw_rect)
        pygame.draw.rect(screen, self.border_colour, draw_rect, self.border_size)
        pygame.draw.rect(screen, self.bar_colour, draw_bar_rect)

class ScrollBar(Element):

    def __init__(self, window, position, dimensions, colour=(250, 250, 250), border_size = 2, border_colour=(100, 100, 100), scroll_height = 50, scroll_width = 20, scroll_colour = (100, 100, 100), scroll_border_size = 1, scroll_border_colour = (50, 50, 50), scrollable = True, scroll_speed = 0.01, scrollable_window = False) -> None:
        super().__init__(window, position, dimensions, colour, None, border_size, border_colour)
        self.scroll_height = scroll_height
        self.scroll_width = scroll_width
        self.scroll_colour = scroll_colour
        self.scroll_border_size = scroll_border_size
        self.scroll_border_colour = scroll_border_colour

        self.scroll_x = self.x
        self.scroll_y = self.y

        self.clamp_top = self.y
        self.clamp_bottom = self.height - self.scroll_height

        self.clamp_left = self.x
        self.clamp_right = self.width - self.scroll_width

        self.scroll_rect = pygame.Rect(self.x, self.y, self.scroll_width, self.scroll_height)
        self.scrollable = scrollable
        self.scrollable_window = scrollable_window
        self.scroll_speed = scroll_speed

    def draw(self, screen):
        if not self.visible: return
        window_pos = self.window.get_position()
        draw_rect = (self.hitbox.x + window_pos[0], self.hitbox.y + window_pos[1], self.hitbox.width, self.hitbox.height)
        draw_scroll_rect = (self.scroll_rect.x + window_pos[0], self.scroll_rect.y + window_pos[1], self.scroll_rect.width, self.scroll_rect.height)
        pygame.draw.rect(screen, self.colour, draw_rect)
        pygame.draw.rect(screen, self.border_colour, draw_rect, self.border_size)
        pygame.draw.rect(screen, self.scroll_colour, draw_scroll_rect)
        pygame.draw.rect(screen, self.scroll_border_colour, draw_scroll_rect, self.scroll_border_size)

    def get_y(self):
        return ((self.scroll_y - self.clamp_top) / (self.clamp_bottom - self.clamp_top)) if (self.clamp_bottom - self.clamp_top) > 0 else 0
    
    def get_x(self):
        return ((self.scroll_x - self.clamp_left) / (self.clamp_right - self.clamp_left)) if (self.clamp_right - self.clamp_left) > 0 else 0
    
    def get(self):
        return (self.get_x(), self.get_y())
    
    def check_scroll(self):
        if self.scroll_y >= self.clamp_bottom:
            self.scroll_y = self.clamp_bottom

        elif self.scroll_y <= self.clamp_top:
            self.scroll_y = self.clamp_top

        if self.scroll_x >= self.clamp_right:
            self.scroll_x = self.clamp_right

        elif self.scroll_x <= self.clamp_left:
            self.scroll_x = self.clamp_left
    
    def check_event(self, event):
        if not self.visible: return
        mousex, mousey = pygame.mouse.get_pos()
        window_pos = self.window.get_position()
        mousex -= window_pos[0]
        mousey -= window_pos[1]
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.scroll_rect.collidepoint(mousex, mousey):
            self.selected = True
            
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.selected:
            self.selected = False

        if self.scrollable:
            if event.type == pygame.MOUSEWHEEL and (self.hitbox.collidepoint(mousex, mousey) or self.scrollable_window):
                self.scroll_y -= self.scroll_speed * (self.clamp_bottom - self.clamp_top) * event.y
                self.scroll_x += self.scroll_speed * (self.clamp_right - self.clamp_left) * event.y
                
                self.check_scroll()

                self.scroll_rect.y = self.scroll_y
                self.scroll_rect.x = self.scroll_x

        if self.selected:
            self.scroll_y = mousey - self.scroll_height / 2
            self.scroll_x = mousex - self.scroll_width / 2

            self.check_scroll()

            self.scroll_rect.y = self.scroll_y
            self.scroll_rect.x = self.scroll_x

class Frame(Element):

    def __init__(self, window, position, dimensions, colour=(250, 250, 250), border_size = 2, border_colour=(100, 100, 100), draggable = False) -> None:
        super().__init__(window, position, dimensions, colour, None, border_size, border_colour)
        self.draggable = draggable
        self.elements = []

    def add_element(self, element):
        self.elements.append(element)

    def check_event(self, event):
        if not self.visible: return
        mousex, mousey = pygame.mouse.get_pos()
        window_pos = self.window.get_position()
        mousex -= window_pos[0]
        mousey -= window_pos[1]
        isTouchingElement = False
        if not self.selected:
            for element in self.elements:
                if element.visible:
                    element.check_event(event)
                    if element.hitbox.collidepoint(mousex - self.x, mousey - self.y):
                        isTouchingElement = True
        
        if self.draggable and not isTouchingElement:
            if event.type == pygame.MOUSEBUTTONDOWN and self.hitbox.collidepoint(mousex, mousey):
                self.selected = True
                self.offset_x = mousex - self.x
                self.offset_y = mousey - self.y

            if event.type == pygame.MOUSEBUTTONUP and self.selected:
                self.selected = False

            if self.selected:
                self.x = mousex - self.offset_x
                self.y = mousey - self.offset_y

            if self.x > self.window.width - self.width:
                self.x = self.window.width - self.width

            if self.x < 0:
                self.x = 0

            if self.y > self.window.height - self.height:
                self.y = self.window.height - self.height

            if self.y < 0:
                self.y = 0

            self.hitbox.x = self.x
            self.hitbox.y = self.y

    def draw(self, screen):
        if not self.visible: return
        window_pos = self.window.get_position()
        draw_rect = (self.hitbox.x + window_pos[0], self.hitbox.y + window_pos[1], self.hitbox.width, self.hitbox.height)
        pygame.draw.rect(screen, self.colour, draw_rect)
        pygame.draw.rect(screen, self.border_colour, draw_rect, self.border_size)
        for element in self.elements:
            if element.visible:
                element.draw(screen)

class DropDown(Element):

    def __init__(self, window, position, dimensions, colour, active_colour, border_size, border_colour) -> None:
        super().__init__(window, position, dimensions, colour, active_colour, border_size, border_colour)

    def check_event(self, event):
        if not self.visible: return

    def draw(self, screen):
        if not self.visible: return

class SelectionBox(Element):

    def __init__(self, window, position, dimensions, colour, active_colour, border_size, border_colour) -> None:
        super().__init__(window, position, dimensions, colour, active_colour, border_size, border_colour)

    def check_event(self, event):
        if not self.visible: return

    def draw(self, screen):
        if not self.visible: return

class Window:

    def __init__(self, width = 0, height = 0, fullscreen = False, colour = (200, 200, 200), fps = 60) -> None:
        self.window = pygame.display.set_mode((width, height), pygame.FULLSCREEN if fullscreen else pygame.SHOWN)
        self.width, self.height = self.window.get_size()
        self.x = 0
        self.y = 0
        self.fullscreen = fullscreen
        self.colour = colour

        self.running = True
        self.keybinds = {}
        self.elements = []

        self.fps = fps
        self.clock = pygame.time.Clock()

        self.initialise()

    def get_position(self):
        return (self.x, self.y)

    def close(self):
        self.running = False

    def add_element(self, element):
        self.elements.append(element)

    def initialise(self):
        if self.fullscreen: self.keybinds[pygame.K_ESCAPE] = [self.close]

    def do_keypress(self, key):
        if key in self.keybinds:
            functions = self.keybinds[key]
            for function in functions:
                function()

    def send_event(self, event):
        for element in self.elements:
            if element.visible:
                element.check_event(event)

    def draw_elements(self):
        for element in self.elements:
            if element.visible:
                element.draw(self.window)

    def mainloop(self):
        while self.running:
            

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    self.do_keypress(event.key)
            
                if event.type == pygame.QUIT:
                    self.close()

                self.send_event(event)

            self.window.fill(self.colour)
            self.draw_elements()
            pygame.display.flip()

            self.clock.tick(self.fps)

        pygame.quit()

def main():
    def test(e):
        print(e.get())

    window = Window(fullscreen=True)
    s = ScrollBar(window, (0, 0), (50, window.height), scroll_height=50, scroll_width=50, scrollable_window=False)
    f = Frame(window, (600, 600), (400, 400), draggable=True)
    f2 = Frame(f, (0, 0), (300, 300), draggable=True)
    #p = ProgressBar(f2, (0,0), (300, 50), 100, interactable=False, reversed_dir=False, starting_value=30)
    b = Button(window, (300, 300), (50, 50), border_colour=(100, 100, 100), on_hover=True, function=test, function_args=[s])
    e = Entry(f2, (0, 0), (100, 40))
    window.mainloop()

if __name__ == "__main__":
    main()