import random


def generate_task():
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)

    rasu = random.choice(["+", "-", "*", "/"])

    if rasu == "-":
        num2 = random.randint(1, num1)
        answer = num1 - num2

    elif rasu == "+":
        answer = num1 + num2

    elif rasu == "*":
        answer = num1 * num2

    elif rasu == "/":
        num1 = num1 * num2
        answer = int(num1 / num2)

    task = f'{num1} {rasu} {num2}'

    return task, answer

def generate_eq():
    numa = random.randint(-5, 10)
    while numa == 0:
        numa = random.randint(-5, 10)
    if numa < 0:
        numfree = -1 * numa * random.randint(1, 5)
    else:
        numfree = numa * random.randint(1, 5)

    rasu = random.choice(["+", "-"])

    if rasu == "-":
        answer = int(numfree/numa)

    elif rasu == "+":
        answer = int(-1 * numfree/numa)

    if numa == 1:
        task = f'x {rasu} {numfree} = 0'
    elif numa == -1:
        task = f'-x {rasu} {numfree} = 0'
    else:
        task = f'{numa}x {rasu} {numfree} = 0'

    return task, answer


def generate_linsys(eqs: int = 2):
    x = random.randint(-25, 25)
    y = random.randint(-25, 25)
    repeat_factor = []
    task = ""

    def gen_eq():
        coefx = random.randint(-5, 5)
        coefy = random.randint(-5, 5)
        while coefx == 0:
            coefx = random.randint(-5, 5)
        while coefy == 0:
            coefy = random.randint(-5, 5)

        if coefx / coefy in repeat_factor:
            return gen_eq()
        else:
            repeat_factor.append(coefx / coefy)
            return coefx, coefy

    for i in range(eqs):

        coefx, coefy = gen_eq()

        if coefx == 1:
            xpart = f"x"
        elif coefx == -1:
            xpart = f"-x"
        else:
            xpart = f"{coefx}x"

        if coefy == 1:
            eq = f"{xpart} + y = {coefx * x + coefy * y}\n"
        elif coefy == -1:
            eq = f"{xpart} - y = {coefx * x + coefy * y}\n"
        elif coefy < -1:
            eq = f"{xpart} - {abs(coefy)}y = {coefx * x + coefy * y}\n"
        else:
            eq = f"{xpart} + {abs(coefy)}y = {coefx * x + coefy * y}\n"

        task = task + eq

    return task, x + y
