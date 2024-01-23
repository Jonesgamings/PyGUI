import pygame
from pygui import *

# ... (the UI system code goes here, omitting the Window class and main function for brevity)

class LoginPage:
    def __init__(self):
        pygame.init()

        # Create the window
        self.window = Window(width=400, height=300, fullscreen=False, colour=(255, 255, 255), fps=60)

        # Create UI elements
        self.username_entry = Entry(self.window, position=(150, 100), dimensions=(200, 30), default_text="Username")
        self.password_entry = Entry(self.window, position=(150, 150), dimensions=(200, 30), default_text="Password", hidden="*")
        self.login_button = Button(self.window, position=(200, 200), dimensions=(100, 40), text="Login", function=self.try_login)

        # Add UI elements to the window
        self.window.add_element(self.username_entry)
        self.window.add_element(self.password_entry)
        self.window.add_element(self.login_button)

    def try_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        print(f"Attempting login with username: {username} and password: {password}")

    def run(self):
        # Run the main loop
        self.window.mainloop()

# Run the login page
if __name__ == "__main__":
    login_page = LoginPage()
    login_page.run()