from PyQt5.QtWidgets import QListWidgetItem

class Task(QListWidgetItem):
    def __init__(self, id, title, completed):
        super().__init__(title)
        self.id = id
        self.completed = completed
