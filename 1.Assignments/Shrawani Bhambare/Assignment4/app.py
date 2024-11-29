from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     description TEXT NOT NULL,
                     status INTEGER NOT NULL CHECK (status IN (0, 1))
                 )''')
    conn.commit()
    conn.close()

# Initialize the database
init_db()

# CRUD Routes
@app.route('/')
def home():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('SELECT * FROM tasks')
    tasks = c.fetchall()
    conn.close()
    return render_template('home.html', tasks=tasks)

@app.route('/create', methods=['GET', 'POST'])
def create_task():
    if request.method == 'POST':
        description = request.form['description']
        status = 0  # Default status as incomplete
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute('INSERT INTO tasks (description, status) VALUES (?, ?)', (description, status))
        conn.commit()
        conn.close()
        return redirect(url_for('home'))
    return render_template('create.html')

@app.route('/update/<int:task_id>', methods=['GET', 'POST'])
def update_task(task_id):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    if request.method == 'POST':
        description = request.form['description']
        status = request.form['status']
        c.execute('UPDATE tasks SET description = ?, status = ? WHERE id = ?', (description, status, task_id))
        conn.commit()
        conn.close()
        return redirect(url_for('home'))
    c.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
    task = c.fetchone()
    conn.close()
    return render_template('update.html', task=task)

@app.route('/delete/<int:task_id>', methods=['GET', 'POST'])
def delete_task(task_id):
    if request.method == 'POST':
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        conn.commit()
        conn.close()
        return redirect(url_for('home'))
    return render_template('delete.html', task_id=task_id)

if __name__ == '__main__':
    app.run(debug=True)
