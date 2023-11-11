import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('tasks.db')
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                               id INTEGER PRIMARY KEY,
                               title TEXT,
                               completed BOOLEAN)''')
        self.conn.commit()

    def add_task(self, title):
        self.cursor.execute('INSERT INTO tasks (title, completed) VALUES (?, ?)', (title, False))
        self.conn.commit()

    def get_tasks(self):
        self.cursor.execute('SELECT id, title, completed FROM tasks')
        return self.cursor.fetchall()

    def update_task(self, task_id, title):
        self.cursor.execute('UPDATE tasks SET title = ? WHERE id = ?', (title, task_id))
        self.conn.commit()

    def delete_task(self, task_id):
        self.cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        self.conn.commit()

    def mark_completed(self, task_id, completed):
        self.cursor.execute('UPDATE tasks SET completed = ? WHERE id = ?', (completed, task_id))
        self.conn.commit()
