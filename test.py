import pygame
from pygui import *

# ... (the UI system code goes here, omitting the Window class and main function for brevity)

class ToDoList:
    def __init__(self):
        pygame.init()

        # Create the window
        self.window = Window(width=400, height=400, fullscreen=False, colour=(255, 255, 255), fps=60)

        # Create UI elements
        self.task_entry = Entry(self.window, position=(50, 50), dimensions=(250, 30), default_text="Enter task")
        self.add_button = Button(self.window, position=(310, 50), dimensions=(70, 30), text="Add", function=self.add_task)
        self.task_list = Label(self.window, position=(50, 100), dimensions=(300, 200), text="", text_size=16, text_colour=(0, 0, 0))
        self.clear_button = Button(self.window, position=(50, 320), dimensions=(100, 30), text="Clear Completed", function=self.clear_completed)

        # Task list data
        self.tasks = []

    def add_task(self):
        new_task = self.task_entry.get()
        if new_task:
            self.tasks.append(new_task)
            self.update_task_list()

    def clear_completed(self):
        self.tasks = [task for task in self.tasks if not task.startswith("[Done]")]
        self.update_task_list()

    def update_task_list(self):
        task_text = "\n".join(f"[Done] {task}" if task.startswith("[Done]") else task for task in self.tasks)
        self.task_list.text = task_text
        self.task_entry.set_visibility(True)
        self.task_entry.hide()
        self.task_entry.show()

    def run(self):
        # Run the main loop
        self.window.mainloop()

# Run the to-do list
if __name__ == "__main__":
    todo_list = ToDoList()
    todo_list.run()
