from interpolation import natural_cubic_spline

def natural_cubic_spline1(n, x_vec, a_vec):
    h = [ x_vec[i+1] - x_vec[i] for i in range(n)]
    alpha = [0]
    for i in range(1,n):
        alpha.append((3/h[i])*(a_vec[i+1] - a_vec[i]) - (3/h[i-1])*(a_vec[i] - a_vec[i-1]))
    l, u, z = [1], [0], [0]
    for i in range(1,n):
        l.append(2*(x_vec[i+1] - x_vec[i-1]) - h[i-1]*u[i-1])
        u.append(h[i]/l[i])
        z.append((alpha[i] - (h[i-1]*z[i-1]))/l[i])
    l.append(1)
    z.append(0)
    c = [0 for _ in range(n+1)]
    b = [0 for _ in range(n+1)]
    d = [0 for _ in range(n+1)]
    for k in range(n):
        j = n - k - 1
        c[j] = z[j] - u[j]*c[j+1]
        b[j] = (a_vec[j+1] - a_vec[j])/h[j] - h[j]*(c[j+1] + 2*c[j])/3
        d[j] = (c[j+1] - c[j])/(3*h[j])
    return a_vec[0:n], b[0:n], c[0:n], d[0:n]

def spline_interpolation(x_vals, xi_vec, fi_vec):
    """
    Use spline interpolation to find the f_vector.
    x_vals: vector of points at which we would like to find f(x)
    xi_vec: x-coords of known datapoints
    fi_vec: f(x)-coords of known datapoints
    """
    # set up return vector
    f_vec = [ 10 for _ in x_vals]
    # find coefficients of spline
    a, b, c, d = natural_cubic_spline(xi_vec, fi_vec)
    # start iterating through x_vals at j = 0
    j = 0
    # iterate through every spline
    
    for i in range(len(xi_vec) - 1):
        xi = xi_vec[i]
        # take x_vals until not in range anymore (lower bound OK from previous iteration)
        while x_vals[j] < xi_vec[i+1]:
            x = x_vals[j]
            f_vec[j] = int(a[i] + b[i]*(x - xi) + c[i]*(x - xi)**2 + d[i]*(x-xi)**3)
            if f_vec[j] > 255:
                f_vec[j] = 255
            if f_vec[j] < 0:
                f_vec[j] = 0
                
            j += 1
    f_vec[-1] = fi_vec[-1]
    return f_vec

def linear_interpolation(x_vals, xi_vec, fi_vec):
    """
    x_vals: x values we want data at in the end
    """
    f_vec = [ 0 for _ in x_vals]
    # f(x) = (f(x_1) - f(x_0))/(x_1-x_0) * (x-x0) + f(x_0)
    j = 0
    for i in range(len(xi_vec) - 1):
        x0, x1 = xi_vec[i], xi_vec[i+1]
        while x_vals[j] < x1:
            f_vec[j] = fi_vec[i] + (x_vals[j]-x0)*(fi_vec[i+1] - fi_vec[i])/(x1-x0)
            if f_vec[j] > 255:
                f_vec[j] = 255
            if f_vec[j] < 0:
                f_vec[j] = 0
            j += 1
    f_vec[-1] = fi_vec[-1]
    return f_vec