from PyQt5.QtWidgets import QListWidgetItem, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLineEdit, QListWidget, QMessageBox, QHBoxLayout, QLabel, QCheckBox
from database import Database

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.database = Database()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Task Manager")
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Enter a new task...")
        layout.addWidget(self.task_input)

        self.add_button = QPushButton("Add Task")
        self.add_button.clicked.connect(self.add_task)
        layout.addWidget(self.add_button)

        self.tasks_list = QListWidget()
        layout.addWidget(self.tasks_list)
        self.load_tasks()

    def add_task(self):
        task_title = self.task_input.text()
        if task_title:
            self.database.add_task(task_title)
            self.task_input.clear()
            self.load_tasks()

    def load_tasks(self):
        self.tasks_list.clear()
        tasks = self.database.get_tasks()
        for task_id, title, completed in tasks:
            self.add_task_to_list(task_id, title, completed)

    def add_task_to_list(self, task_id, title, completed):
        container = QWidget()
        container_layout = QHBoxLayout()

        checkbox = QCheckBox()
        checkbox.setChecked(completed)
        checkbox.stateChanged.connect(lambda state, id=task_id: self.mark_completed(id, state))
        container_layout.addWidget(checkbox)

        label = QLabel(title)
        container_layout.addWidget(label)

        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(lambda _, id=task_id: self.delete_task(id))
        container_layout.addWidget(delete_button)

        container.setLayout(container_layout)
        list_item = QListWidgetItem(self.tasks_list)
        list_item.setSizeHint(container.sizeHint())
        self.tasks_list.addItem(list_item)
        self.tasks_list.setItemWidget(list_item, container)

    def delete_task(self, task_id):
        self.database.delete_task(task_id)
        self.load_tasks()

    def mark_completed(self, task_id, state):
        self.database.mark_completed(task_id, state == 2)  # 2 is the state for 'checked'
