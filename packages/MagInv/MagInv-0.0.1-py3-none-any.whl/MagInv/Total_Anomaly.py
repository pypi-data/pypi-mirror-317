import numpy as np

def dircos(incl, decl, azim):
    """
    Compute direction cosines from inclination and declination.
    """
    d2rad = np.pi / 180.0 
    xincl = incl * d2rad
    xdecl = decl * d2rad
    xazim = azim * d2rad
    
    a = np.cos(xincl) * np.cos(xdecl - xazim)
    b = np.cos(xincl) * np.sin(xdecl - xazim)
    c = np.sin(xincl)
    
    return a, b, c

def mbox(x0, y0, z0, x1, y1, z1, x2, y2, mi, md, fi, fd, m, theta):
    """
    Computes the total-field anomaly of an infinitely extended rectangular prism.
    """
    cm = 1e-7  
    t2nt = 1e9 
    
    ma, mb, mc = dircos(mi, md, theta)
    fa, fb, fc = dircos(fi, fd, theta)
    
    fm1 = ma * fb + mb * fa
    fm2 = ma * fc + mc * fa
    fm3 = mb * fc + mc * fb
    fm4 = ma * fa
    fm5 = mb * fb
    fm6 = mc * fc
    
    alpha = np.array([[x1 - x0], [x2 - x0]])
    beta = np.array([[y1 - y0], [y2 - y0]])
    h = z1 - z0
    t = 0.0
    hsq = h ** 2
    
    for i in range(2):
        alphasq = alpha[i, :] ** 2
        for j in range(2):
            sign = 1.0
            if i != j:
                sign = -1.0
            
            r0sq = alphasq + beta[j, :] ** 2 + hsq
            r0 = np.sqrt(r0sq)
            r0h = r0 * h
            alphabeta = alpha[i, :] * beta[j, :]
            
            arg1 = (r0 - alpha[i, :]) / (r0 + alpha[i, :])
            arg2 = (r0 - beta[j, :]) / (r0 + beta[j, :])
            arg3 = alphasq + r0h + hsq
            arg4 = r0sq + r0h - alphasq
            
            tlog = fm3 * np.log(arg1) / 2.0 + fm2 * np.log(arg2) / 2.0 - fm1 * np.log(r0 + h)
            tatan = -fm4 * np.arctan2(alphabeta, arg3) - fm5 * np.arctan2(alphabeta, arg4) + fm6 * np.arctan2(alphabeta, r0h)
            
            t += sign * (tlog + tatan)
    
    t = t * m * cm * t2nt
    return t


def gbox(x0, y0, z0, x1, y1, z1, x2, y2, z2, rho):
    """
    Computes the vertical attraction of a rectangular prism.
    The sides of the prism are parallel to the x, y, and z axes, with the z-axis being vertical down.

    Parameters:
    -----------
    x0, y0, z0 : float
        Coordinates of the observation point (in km).
    x1, y1, z1 : float
        Coordinates of the first corner of the prism (in km).
    x2, y2, z2 : float
        Coordinates of the second corner of the prism (in km).
    rho : float
        Density of the prism (in kg/m^3).

    Returns:
    --------
    g : float
        The vertical attraction of gravity in mGal.
    """
    # Constants
    isign = np.array([-1, 1])
    gamma = 6.670e-11  # Gravitational constant (m^3/kg/s^2)
    twopi = 6.2831853  # 2 * pi
    si2mg = 1.e5  # SI to mGal conversion factor
    km2m = 1.e3  # km to meters conversion factor

    # Differences between observation point and prism coordinates
    x = [x0 - x1, x0 - x2]
    y = [y0 - y1, y0 - y2]
    z = [z0 - z1, z0 - z2]

    total_sum = 0.0  # Initialize the sum

    # Triple nested loop to iterate over the corners of the prism
    for i in range(2):
        for j in range(2):
            for k in range(2):
                rijk = np.sqrt(x[i]**2 + y[j]**2 + z[k]**2)
                ijk = isign[i] * isign[j] * isign[k]

                # Compute arg1
                arg1 = np.arctan2((x[i] * y[j]), (z[k] * rijk))
                if arg1 < 0:
                    arg1 += twopi

                # Compute arg2 and arg3
                arg2 = rijk + y[j]
                arg3 = rijk + x[i]

                if arg2 < 0 or arg3 < 0:
                    raise ValueError("Bad field point")

                arg2 = np.log(arg2)
                arg3 = np.log(arg3)

                # Update the sum
                total_sum += ijk * (z[k] * arg1 - x[i] * arg2 - y[j] * arg3)

    # Calculate the vertical attraction of gravity
    g = rho * gamma * total_sum * si2mg * km2m

    return g



