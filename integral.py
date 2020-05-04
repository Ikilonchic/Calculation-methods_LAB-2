import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import numpy as np

stop_therads = False

def interval(start, finish = None, step = 1):
    if finish is None:
        finish = start
        start = 0
    if start < finish:
        if step <= 0:
            return
        while start < finish:
            #dot.append(round(start, 4))
            yield start
            start += step
            
    else:
        if step >= 0:
            return
        while start > finish:
            #dot.append(round(start, 4))
            yield start
            start += step


def draw_function(func: 'function', begin: float, end: float, step = 0.01) -> None:
    xs = [x for x in interval(begin - 1, end + 1, step)]
    ys = [func(x) for x in xs]

    fig, ax = plt.subplots()
    ax.plot(xs, ys, 'r', linewidth=2)
    #ax.set_xlim(bottom=0)
    #ax.set_ylim(bottom=0)

    ix = [x for x in np.arange(begin, end + step, step)]
    iy = [func(x) for x in ix]
    
    verts = [(begin, 0), *zip(ix, iy), (end, 0)]
    poly = Polygon(verts, facecolor='0.9', edgecolor='0.5')
    ax.add_patch(poly)

    fig.text(0.9, 0.05, '$x$')
    fig.text(0.1, 0.9, '$y$')

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')

    ax.set_xticks((begin, end))
    ax.set_xticklabels((f'${begin}$', f'${end}$'))
   
    plt.show()


def find_best(obj, a, b, *args, e = 10**-4):
    n = 2; error = 0; good = 0
    simpson_check = obj.__class__.__name__ == 'Simpson'
    
    while True:
        h = (b - a) / n
        error = obj.runge(a, b, h, *args)
        if abs(error) < e:
            break
        n *= 2

    prev_n = 2; prev_error = error; check = False
    
    while True:
        save = n; h = (b - a) / n
        error = obj.runge(a, b, h, *args)
        if abs(error) <= e:
            n -= round(abs(prev_n - n) / 2 + 0.1)
            n -= 1 if simpson_check and n % 2 != 0 else 0
        else:
            n += round(abs(prev_n - n) / 2 + 0.1)
            n += 1 if simpson_check and n % 2 != 0 else 0
        if abs(n - prev_n) == 0 or n == 0:
            if not check:
                check = True; prev_error = error; prev_n = save
                continue
            good = n if abs(error) < abs(prev_error) else prev_n
            break
        prev_error = error; prev_n = save

    if abs(obj.runge(a, b, (b - a) / good, *args)) < e:
        return good
    else:
        return good + 1
