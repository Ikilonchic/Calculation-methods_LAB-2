from math import *
from functools import lru_cache
from integral import *

class Rectangle:
    def __init__(self, formula: str):
        self._formula = None

        try:
            eval(formula.replace('x', '1'), {'__builtins__':{}, 'sqrt': sqrt, 'pow': pow})
        except ZeroDivisionError:
            pass
        except Exception as what:
            print(f"Формула некорректна. Проверте синтаксис.")
            print(what)
        else:
            def temp(x):
                try:
                    return eval(formula.replace('x', str(x)), {'__builtins__':{}, 'sqrt': sqrt, 'pow': pow})
                except ZeroDivisionError:
                    pass
            
            self._formula = temp

    @lru_cache
    def get_integral_value(self, a, b, h, param = 'l'):
        if param == 'l':
            return h * sum([self._formula(x) for x in interval(a, b, h)])
        elif param == 'm':
            return h * sum([self._formula((x + x + h) / 2) for x in interval(a, b, h)])
        elif param == 'r':
            return h * sum([self._formula(x) for x in interval(a + h, b + h, h)])
        else:
            raise RuntimeError('Parameter error: param shall be either "l", or "m", or "r".')
        
    def integral_left(self, a, b, h):
        return self.get_integral_value(a, b, h, 'l')

    def integral_middle(self, a, b, h):
        return self.get_integral_value(a, b, h, 'm')

    def integral_right(self, a, b, h):
        return self.get_integral_value(a, b, h, 'r')

    @lru_cache
    def runge(self, a, b, h, param = 'l'):
        by_h = self.get_integral_value(a, b, h, param)
        by_h_2 = self.get_integral_value(a, b, h / 2, param)
        res = (by_h_2 - by_h) / (3 if param == 'm' else 1)
        return res

    def runge_left(self, a, b, h):
        return self.runge(a, b, h, 'l')

    def runge_middle(self, a, b, h):
        return self.runge(a, b, h, 'm')

    def runge_right(self, a, b, h):
        return self.runge(a, b, h, 'r')


if __name__ == '__main__':
    tmp = Rectangle('(x)**2')
    print(tmp.get_integral_value(1, 4, 0.0001, 'l'))
    print(tmp.get_integral_value(1, 4, 0.0001, 'm'))
    print(tmp.get_integral_value(1, 4, 0.0001, 'r'))
    print(tmp.runge(1, 4, 0.0001, 'l'))
    print(tmp.runge(1, 4, 0.0001, 'm'))
    print(tmp.runge(1, 4, 0.0001, 'r'))
