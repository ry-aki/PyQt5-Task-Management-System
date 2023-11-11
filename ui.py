from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QLineEdit, QListWidget, QListWidgetItem, QHBoxLayout, QLabel, QCheckBox
from PyQt5.QtCore import Qt
from database import Database

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.database = Database()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Task Manager")
        self.setGeometry(300, 300, 600, 400)  # Adjust window size as needed

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Input for new tasks
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Enter a new task...")
        layout.addWidget(self.task_input)

        # Button to add new tasks
        self.add_button = QPushButton("Add Task")
        self.add_button.clicked.connect(self.add_task)
        layout.addWidget(self.add_button)

        # List for active tasks
        self.active_tasks_list = QListWidget()
        layout.addWidget(self.active_tasks_list)

        # Separator label
        separator = QLabel("Completed Tasks")
        layout.addWidget(separator)

        # List for completed tasks
        self.completed_tasks_list = QListWidget()
        layout.addWidget(self.completed_tasks_list)

        self.load_tasks()

    def add_task(self):
        task_title = self.task_input.text()
        if task_title:
            self.database.add_task(task_title)
            self.task_input.clear()
            self.load_tasks()

    def load_tasks(self):
        self.active_tasks_list.clear()
        self.completed_tasks_list.clear()
        tasks = self.database.get_tasks()
        for task_id, title, completed in tasks:
            if completed:
                self.add_task_to_list(task_id, title, completed, self.completed_tasks_list)
            else:
                self.add_task_to_list(task_id, title, completed, self.active_tasks_list)

    def add_task_to_list(self, task_id, title, completed, list_widget):
        container = QWidget()
        container_layout = QHBoxLayout()

        checkbox = QCheckBox()
        checkbox.setChecked(completed)
        checkbox.stateChanged.connect(lambda state, id=task_id: self.mark_completed(id, state, list_widget))
        container_layout.addWidget(checkbox)

        label = QLabel(title)
        container_layout.addWidget(label)

        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(lambda _, id=task_id: self.delete_task(id))
        container_layout.addWidget(delete_button)

        container.setLayout(container_layout)
        list_item = QListWidgetItem(list_widget)
        list_item.setSizeHint(container.sizeHint())
        list_widget.addItem(list_item)
        list_widget.setItemWidget(list_item, container)

    def delete_task(self, task_id):
        self.database.delete_task(task_id)
        self.load_tasks()

    def mark_completed(self, task_id, state, list_widget):
        completed = state == 2  # 2 is the state for 'checked'
        self.database.mark_completed(task_id, completed)
        self.load_tasks()
