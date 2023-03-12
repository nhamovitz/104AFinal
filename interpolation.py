
# from Nathaniel, HW3
def map_zip(points, f):
    return zip(points, map(f, points))

from functools import partial

def lagrange1(points):
    ps = list(list(points).copy())
    Ls = []

    for (x_k, _) in ps.copy():
        def L(t, ps = ps.copy(), x_k = x_k):
            ret = 1
            for (x_i, _) in ps:
                x_i = x_i
                if x_i != x_k:
                    ret *= ((t - x_i) / (x_k - x_i))
            return ret
        Ls.append(L)
    
    def P(x):
        ret = 0
        for (k, (_, val_k)) in enumerate(ps.copy()):
            val_k = val_k
            ret += (val_k * Ls[k](x))
        return ret

    return P

def lagrange2(points):
    def L(t, k, x_k):
        ret = 1
        for (i, (x_i, _)) in points:
            if i != k:
                ret *= ((t - x_i) / (x_k - x_i))
        return ret

    def P(x):
        ret = 0
        for (k, (x_k, val_k)) in enumerate(points):
            ret += (val_k * L(x, k, x_k))
        return ret

    return P

def rianna_mod(x, f, points = []):
    def L(x, k, points = []):
        ret = 1
        for i in range(len(points)):
            if i != k:
                ret *= (x - points[i]) / (points[k] - points[i])
        return ret
    
    def P(x, f, points = []):
        ret = 0
        for k in range(len(points)):
            ret += f(points[k]) * L(x, k, points)
        return ret

    return P(x, f, points)

# from Nathaniel, HW4
def neville(points):
    n = len(points) - 1
    Qs = [[(lambda x, i=i: points[i][1])] for i in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, i + 1):
            def Q(x, i = i, j = j):
                num1 = (x - points[i - j][0])*Qs[i][j - 1](x)
                num2 = (x - points[i][0]) * Qs[i - 1][j - 1](x)
                denom = points[i][0] - points[i - j][0]
                return (num1 - num2) / denom
            Qs[i].append(Q)
    return Qs

def best_neville(points):
    Qs = neville(points)
    return Qs[-1][-1]

def best_neville_at(points, x):
    Qs = neville(points)
    return Qs[-1][-1](x)

def apply_total(Qs, x):
    ret = []
    for row in Qs:
        ret_row = []
        for Q in row:
            val = None
            if Q is not None:
                val = Q(x)
            ret_row.append(val)
        ret.append(ret_row)
    return ret

def newton_divided_difference(points = None, *, xs = None, ys = None):
    if points is not None:
        n = len(points)

        points = zip(*points)
        xs = list(next(points))
        ys = list(next(points))
        try:
            next(points)
        except StopIteration:
            pass
        else:
            raise Exception("smth fucky")
    else:
        assert len(xs) == len(ys)
        n = len(xs)



    F = np.zeros((n, n))

    F[:, 0] = ys
    # print(F)

    for i in range(1, n):
        for j in range(1, i + 1):
            F[i, j] = (F[i, j - 1] - F[i - 1, j - 1])/(xs[i] - xs[i - j])

    # print(F)

    def P(x, n = n - 1, F = F, xs = xs):
        n = n + 1
        ret = F[0, 0]
        for i in range(1, n):
            par_sum = F[i, i]
            for j in range(0, i):
                par_sum *= (x - xs[j])
            ret += par_sum
        # return (F.diagonal(), ret)
        return ret

    return {"P": P, "coeffs": F.diagonal()}


# from Nathaniel, HW5
## Sec 3.4
def hermite(xs, f_xs, f_primes):
    assert len(xs) == len(f_xs)

    n = len(xs) - 1
    zs = np.zeros(2*(n + 1))

    for i in range(n + 1):
        zs[2*i] = xs[i]
        zs[2*i + 1] = xs[i]

    Q = np.zeros((2*(n + 1), 2*(n + 1)))

    for i in range(n + 1):
        Q[2*i, 0] = f_xs[i]
        Q[2*i + 1, 0] = f_xs[i]
        Q[2*i + 1, 1] = f_primes[i]

        if i != 0:
            Q[2*i, 1] = (Q[2*i, 0] - Q[2*i - 1, 0]) / (zs[2*i] - zs[2*i - 1])

    for i in range(2, 2*n + 1 + 1):
        for j in range(2, i + 1):
            Q[i, j] = (Q[i, j - 1] - Q[i - 1, j - 1]) / (zs[i] - zs[i - j])

    # return Q, #Q.diagonal()
    return Q.diagonal(), zs, n

## Sec 3.5
def natural_cubic_spline(xs, f_xs):
    assert len(xs) == len(f_xs)
    a = f_xs

    n = len(xs) - 1

    h = []
    for i in range(n-1 + 1):
        h.append(xs[i + 1] - xs[i])
    
    alpha = [None]
    for i in range(1, n-1 + 1):
        alpha.append(
            (3 / h[i])*(f_xs[i + 1] - f_xs[i]) - \
                (3 / h[i - 1]) * (f_xs[i] - f_xs[i - 1])
        )

    l = [1]
    mu = [0]
    z = [0]
    for i in range(1, n-1 + 1):
        l.append(2 * (xs[i + 1] - xs[i - 1]) - h[i - 1] * mu[i - 1])
        mu.append(h[i] / l[i])
        z.append(
            (alpha[i] - h[i - 1] * z[i - 1]) / l[i]
        )
    l.append(1)
    z.append(0)

    c = np.zeros(n + 1)
    b = np.zeros(n + 1)
    d = np.zeros(n + 1)

    c[n] = 0
    for j in range(n - 1, 0 - 1, -1):
        c[j] = (z[j] - mu[j]*c[j + 1])
        b[j] = (f_xs[j + 1] - f_xs[j]) / h[j] - h[j] * (c[j + 1] + 2*c[j]) / 3
        d[j] = (c[j + 1] - c[j]) / (3 * h[j])

    ret = np.zeros((4, n-1 + 1))
    # print(n, list(map(len, (f_xs, b, c, d))))
    # print( f_xs, b, c, d)
    ret[0, :] = a[0:-1]
    ret[1, :] = b[0:-1]
    ret[2, :] = c[0:-1]
    ret[3, :] = d[0:-1]

    ret = ret.transpose()

    tex = ""
    for j in range(n-1 + 1):
        tex += f"$S_{j} = {a[j]} + {b[j]}(x - {xs[j]}) + {c[j]}(x - {xs[j]})^2 + {d[j]}(x - {xs[j]})^3$"
        if j != n-1:
            tex += "; "
    display(Latex(tex))

    # table = table_writer(ret, [f"$S_{j}$" for j in range(n-1 + 1)], ["$a_j$", "$b_j$", "$c_j$", "$d_j$"])
    # print(table)

    print(tex)
    return ret

## Sec 3.6
def natural_cubic_spline(xs, f_xs):
    assert len(xs) == len(f_xs)
    a = f_xs

    n = len(xs) - 1

    h = []
    for i in range(n-1 + 1):
        h.append(xs[i + 1] - xs[i])
    
    alpha = [None]
    for i in range(1, n-1 + 1):
        alpha.append(
            (3 / h[i])*(f_xs[i + 1] - f_xs[i]) - \
                (3 / h[i - 1]) * (f_xs[i] - f_xs[i - 1])
        )

    l = [1]
    mu = [0]
    z = [0]
    for i in range(1, n-1 + 1):
        l.append(2 * (xs[i + 1] - xs[i - 1]) - h[i - 1] * mu[i - 1])
        mu.append(h[i] / l[i])
        z.append(
            (alpha[i] - h[i - 1] * z[i - 1]) / l[i]
        )
    l.append(1)
    z.append(0)

    c = np.zeros(n + 1)
    b = np.zeros(n + 1)
    d = np.zeros(n + 1)

    c[n] = 0
    for j in range(n - 1, 0 - 1, -1):
        c[j] = (z[j] - mu[j]*c[j + 1])
        b[j] = (f_xs[j + 1] - f_xs[j]) / h[j] - h[j] * (c[j + 1] + 2*c[j]) / 3
        d[j] = (c[j + 1] - c[j]) / (3 * h[j])

    ret = np.zeros((4, n-1 + 1))
    # print(n, list(map(len, (f_xs, b, c, d))))
    # print( f_xs, b, c, d)
    ret[0, :] = a[0:-1]
    ret[1, :] = b[0:-1]
    ret[2, :] = c[0:-1]
    ret[3, :] = d[0:-1]

    ret = ret.transpose()

    tex = ""
    for j in range(n-1 + 1):
        tex += f"$S_{j} = {a[j]} + {b[j]}(x - {xs[j]}) + {c[j]}(x - {xs[j]})^2 + {d[j]}(x - {xs[j]})^3$"
        if j != n-1:
            tex += "; "
    display(Latex(tex))

    # table = table_writer(ret, [f"$S_{j}$" for j in range(n-1 + 1)], ["$a_j$", "$b_j$", "$c_j$", "$d_j$"])
    # print(table)

    print(tex)
    return ret

