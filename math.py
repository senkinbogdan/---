from flask import Flask, render_template, request
import random

app = Flask (__name__)

def generate_question():
    operation = random. choice(['*', '-', '*', '/'])
    num1 = random. randint(1, 10)
    num2 = random. randint(1,10)

    if operation == '/':
        num1 = num1 * num2
    return num1, num2, operation

@ app. route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_answer = request. form.get('answer')
        correct_answer = float (request. form. get( 'correct_answer'))
        result = "Правильно, молодец!!" if float(user_answer) == correct_answer else "Неправильно. Попробуй решить другой пример."

        num1, num2, operation = generate_question()
        correct_answer = eval(f" {num1} {operation} {num2}")
    else:
        num1, num2, operation = generate_question()
        correct_answer = eval(f"{num1} {operation} {num2}")
        result = None

    return render_template ('math_1.html', num1=num1, num2=num2, operation=operation, result=result, correct_answer=correct_answer)

if __name__ == '__main__':
    app.run(debug=True)