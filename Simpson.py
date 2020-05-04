from functools import lru_cache
from integral import *

class Simpson:
    def __init__(self, formula: str):
        self._formula = None

        try:
            eval(formula.replace('x', '1'))
        except ZeroDivisionError:
            pass
        except Exception as what:
            print(f"Формула некорректна. Проверте синтаксис.")
            print(what)
        else:
            def temp(x):
                try:
                    return eval(formula.replace('x', str(x)))
                except ZeroDivisionError:
                    pass
            
            self._formula = temp

    @lru_cache
    def get_integral_value(self, a: 'any number', b: 'any number', h: 'any number'):
        if round((b - a) / h) % 2 != 0:
            raise RuntimeError(f'{round((b - a) / h)} is not even!')
        res = h / 3
        frst = 4 * sum([self._formula(x) for i, x in enumerate(interval(a + h, b, h)) if (i + 1) % 2 != 0])
        scnd = 2 * sum([self._formula(x) for i, x in enumerate(interval(a + 2 * h, b - h, h)) if i % 2 == 0])
        res *= (self._formula(a) + self._formula(b) + frst + scnd)
        return res

    @lru_cache
    def runge(self, a, b, h):
        by_h = self.get_integral_value(a, b, h)
        by_h_2 = self.get_integral_value(a, b, h / 2)
        res = (by_h_2 - by_h) / 15
        return res


if __name__ == '__main__':
    tmp = Simpson('x**2')
    print(tmp.get_integral_value(1, 4, 0.001))
    print(tmp.runge(1, 4, 0.001))