from functools import lru_cache
from integral import *

class Trapezoid:
    def __init__(self, formula: str):
        self._formula = None

        try:
            eval(formula.replace('x', '1'), {'__builtins__':{}})
        except ZeroDivisionError:
            pass
        except Exception as what:
            print(f"Формула некорректна. Проверте синтаксис.")
            print(what)
        else:
            def temp(x):
                try:
                    return eval(formula.replace('x', str(x)), {'__builtins__':{}})
                except ZeroDivisionError:
                    pass
            
            self._formula = temp

    @lru_cache
    def get_integral_value(self, a, b, h):
        res = (h * (self._formula(a) + self._formula(b)) / 2) + h * sum([self._formula(x) for x in interval(a + h, b, h)])
        return res

    @lru_cache
    def runge(self, a, b, h):
        by_h = self.get_integral_value(a, b, h)
        by_h_2 = self.get_integral_value(a, b, h / 2)
        res = (by_h_2 - by_h) / 3
        return res


if __name__ == '__main__':
    tmp = Trapezoid('(x)**2')
    print(tmp.get_integral_value(1, 4, 0.001))
    print(tmp.runge(1, 4, 0.001))