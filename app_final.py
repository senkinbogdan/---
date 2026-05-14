from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import random
from passlib.hash import sha256_crypt

app = Flask(__name__)
app.secret_key = 'cd6DiJZnwzNaSq9xq3MKqwbMXQoYcFtL'

def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE NOT NULL,
                  password TEXT NOT NULL,
                  class_name INTEGER NOT NULL CHECK (class_name IN (1, 2, 3, 4)))''')
    conn.commit()
    conn.close()

def generate_task():
    operation = random.choice(['+', '-', '*', '/'])
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)

    if operation == '/':
        num1 = num1 * num2
    return num1, num2, operation

@app.route('/', methods=['GET', 'POST'])
def home():
    if 'username' not in session:
        return redirect(url_for('login'))

    num1, num2, operation, correct_answer, result = None, None, None, None, None

    if request.method == 'POST':
        try:
            user_answer = float(request.form.get('answer', 0))
            correct_answer = float(request.form.get('correct_answer', 0))

            if abs(user_answer - correct_answer) < 1e-9:
                result = "Правильно, молодец!"
            else:
                result = "Неправильно. Попробуй решить другой пример."
        except (ValueError, TypeError):
            result = "Ошибка: введите числовой ответ"

        num1, num2, operation = generate_task()
        correct_answer = eval(f"{num1} {operation} {num2}")
    else:
        num1, num2, operation = generate_task()
        correct_answer = eval(f"{num1} {operation} {num2}")

    return render_template('home.html',
                         username=session['username'],
                         class_name=session.get('class_name'),
                         num1=num1,
                         num2=num2,
                         operation=operation,
                         result=result,
                         correct_answer=correct_answer)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = c.fetchone()
        conn.close()

        if user and sha256_crypt.verify(password, user[2]):
            session['username'] = username
            session['class_name'] = user[3]
            flash('Вы успешно вошли в систему!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Неверное имя пользователя или пароль', 'error')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        class_name = request.form['class_name']

        if class_name not in ['1', '2', '3', '4']:
            flash('Выберите корректный класс обучения (1, 2, 3 или 4)', 'error')
            return render_template('register_1.html')

        hashed_password = sha256_crypt.hash(password)

        try:
            conn = sqlite3.connect('users.db')
            c = conn.cursor()
            c.execute("INSERT INTO users (username, password, class_name) VALUES (?, ?, ?)",
                     (username, hashed_password, class_name))
            conn.commit()
            conn.close()
            flash('Регистрация прошла успешно! Теперь вы можете войти.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Пользователь с таким именем уже существует', 'error')

    return render_template('register_1.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('class_name', None)
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('login'))


if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='localhost', port=8000)