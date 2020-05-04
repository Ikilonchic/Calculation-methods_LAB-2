if __name__ != '__main__':
    exit()

from Rectangle import Rectangle
from Trapezoid import Trapezoid
from Simpson import Simpson
from prettytable import PrettyTable
from integral import interval, find_best, draw_function, stop_therads
from threading import Thread

acc = '{:.7f}'.format
threads = list()
try:
    while True:
        formula = input('Введите формулу: ')  #my variant: (3 * (x) + 4) / (2 * (x) + 7)
        if formula == 'exit':
            exit()
        a = float(input('Введите "a": '))
        b = float(input('Введите "b": '))
        n = int(input('Введите "n": '))
        rct = Rectangle(formula)
        trp = Trapezoid(formula)
        sim = Simpson(formula)
        h = (b - a) / n; print(f'h is {h}')

        Names = ['Левые прям.', 'Правые прям.', 'Средние прям.', 'Трапезоид', 'Симпсон']

        Integrals = [
            rct.integral_left,
            rct.integral_right,
            rct.integral_middle,
            trp.get_integral_value,
            sim.get_integral_value
        ]

        Runge = [
            rct.runge_left,
            rct.runge_right,
            rct.runge_middle,
            trp.runge,
            sim.runge
        ]

        Methods = {
            'Левые прям.' : rct.integral_left,
            'Правые прям.' : rct.integral_right,
            'Средние прям.' : rct.integral_middle,
            'Трапезоид' : trp.get_integral_value,
            'Симпсон' : sim.get_integral_value
        }

        Errors = {
            'Левые прям.' : rct.runge_left,
            'Правые прям.' : rct.runge_right,
            'Средние прям.' : rct.runge_middle,
            'Трапезоид' : trp.runge,
            'Симпсон' : sim.runge
        }

        tbl = PrettyTable()
        tbl.add_column('', ['Интегральное значение с h', 'Интегральное значение с h/2', 'Погрешность'])
        for name, val, err in zip(Names, Integrals, Runge):
            tbl.add_column(name, (acc(val(a, b, h)), acc(val(a, b, h / 2)), acc(err(a, b, h))))
        print(tbl)

        draw_function(rct._formula, a, b)

        print('Высчитывается лучшее "n" для всех методов. Это может занять некоторое время. Ждите...')
        
        results = {
            'Левые прям.': find_best(rct, a, b, 'l'),
            'Правые прям.': find_best(rct, a, b, 'r'),
            'Средние прям.': find_best(rct, a, b, 'm'),
            'Трапезоид': find_best(trp, a, b),
            'Симпсон': find_best(sim, a, b),
        }

        for name, n in zip(results.keys(), results.values()):
            print(f'{name} лучшее "n": {n}')
            print(f'\tЗначение: {acc(Methods[name](a, b, (b - a) / n))}, погрешность: {acc(Errors[name](a, b, (b - a) / n))}')

except:
    print('Неизвестная ошибка!')