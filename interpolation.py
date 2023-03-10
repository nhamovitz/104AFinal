def neville(x, vec_x, vec_f, Q_table = None, i0 = -1, j0 = -1):
    n = 1  # x0, x1, ..., xn.

    if (Q_table == None):
        Q_table = np.zeros((n + 1, n + 1))

    for i in np.arange(0, n + 1):
        Q_table[i][0] = vec_f[i]
  
    for j in np.arange(1, n + 1):
        for i in np.arange(j, n + 1):
            # compute Q_{i,j}
            Q_table[i][j]  = 0.0
            Q_table[i][j] += (x - vec_x[i - j])*Q_table[i][j - 1]
            Q_table[i][j] -= (x - vec_x[i])*Q_table[i - 1][j - 1]
            Q_table[i][j] /= (vec_x[i] - vec_x[i - j])
                   
    return Q_table[n][n], Q_table

#Hermite interpolation
#we are interested in the values on the diagonal
def hermite(vec_x,vec_f, vec_fprime, Q_table = None, i0 = -1, j0 = -1):
    n = np.size(vec_x) - 1  # x0, x1, ..., xn.

    if (Q_table == None):
        Q_table = np.zeros((2*n + 2, 2*n + 2))

    z=np.zeros(2*n+2)
    for i in np.arange(0,n+1):
        z[2*i]=vec_x[i]
        z[2*i+1]=vec_x[i]
    
    for i in np.arange(0, n + 1):
        Q_table[2*i][0] = vec_f[i]
        Q_table[2*i+1][0]= vec_f[i]
        Q_table[2*i+1][1]=vec_fprime[i]
        
        if i !=0:
            Q_table[2*i][1]=(Q_table[2*i][0]-Q_table[2*i-1][0])/(z[2*i]-z[2*i-1])
    
    for j in np.arange(2, 2*n + 2):
        for i in np.arange(j, 2*n + 2):
            # compute Q_{i,j}
            Q_table[i][j]  = 0.0
            Q_table[i][j] += Q_table[i][j - 1]
            Q_table[i][j] -= Q_table[i - 1][j - 1]
            Q_table[i][j] /= (z[i] - z[i - j])
                   
    return Q_table

#natural cubic spline
#definitely could streamline this 
def ncubic(vec_x,a):
    n = np.size(vec_x) - 1  # x0, x1, ..., xn.
    result=np.zeros(4) #result lists a_i,b_i,c_i,d_i
    h=np.zeros(n)
    alpha=np.zeros(n)
    l=np.zeros(n+1)
    mu=np.zeros(n+1)
    z=np.zeros(n+1)
    c=np.zeros(n+1)
    b=np.zeros(n)
    d=np.zeros(n)
    
    for i in np.arange(0,n):
        h[i]=vec_x[i+1]-vec_x[i]
    
    for i in np.arange(1,n):
        alpha[i]=(3/h[i])*(a[i+1]-a[i])-(3/h[i-1])*(a[i]-a[i-1])
        
    l[0]=1
    mu[0]=0
    z[0]=0
    
    for i in np.arange(1,n):
        l[i]=2*(vec_x[i+1]-vec_x[i-1])-h[i-1]*mu[i-1]
        mu[i]=h[i]/l[i]
        z[i]=(alpha[i]-h[i-1]*z[i-1])/l[i]
    
    l[n]=1
    z[n]=0
    c[n]=0
    
    for i in np.arange(1,n+1):
        j=n-i
        if j<0:
            break
        c[j]=z[j]-mu[j]*c[j+1]
        b[j]=(a[j+1]-a[j])/(h[j])-h[j]*(c[j+1]+2*c[j])/3
        d[j]=(c[j+1]-c[j])/(3*h[j])
        
                   
    return a, b, c, d