import numpy as np
from joblib import Parallel, delayed
from scipy.sparse import spdiags
from .Total_Anomaly import mbox,gbox  # Import the mbox function if needed
from scipy.sparse import diags

def a_integral(x, y, z):
    """
    Computes the integral for given coordinates (x, y, z) based on the provided formula.

    Parameters:
    -----------
    x, y, z : ndarray
        Arrays or scalars representing coordinates.

    Returns:
    --------
    f : ndarray
        The computed integral values.
    """
    Gamma = 6.674 * 0.001
    r = np.sqrt(x**2 + y**2 + z**2)
    # Handle cases where r might be zero to avoid division by zero
    with np.errstate(divide='ignore', invalid='ignore'):
        f = -Gamma * ((x * np.log(y + r)) + (y * np.log(x + r)) - (z * np.arctan(x * y / (z * r))))
    return f


def matrix_a_3d(cell_grid, data, d1, d2):
    """
    Computes the matrix A based on the given cell grid and data.

    Parameters:
    -----------
    cell_grid : ndarray
        Array of cell grid coordinates, each row contains [x_center, y_center, z_center, height].
    data : ndarray
        Array of observation coordinates, each row contains [x_obs, y_obs].
    d1, d2 : float
        Dimensions of the cell grid in x and y directions (in km).

    Returns:
    --------
    A : ndarray
        The computed matrix A.
    """
    num_data = len(data)
    num_cells = len(cell_grid)
    A = np.zeros((num_data, num_cells))

    for i in range(num_data):
        for j in range(num_cells):
            x2 = cell_grid[j, 0] + d1 / 2 - data[i, 0]
            x1 = cell_grid[j, 0] - d1 / 2 - data[i, 0]
            y2 = cell_grid[j, 1] + d2 / 2 - data[i, 1]
            y1 = cell_grid[j, 1] - d2 / 2 - data[i, 1]
            z2 = cell_grid[j, 2] + cell_grid[j, 3]
            z1 = cell_grid[j, 2] - cell_grid[j, 3]

            # Compute the matrix entry
            A[i, j] = (a_integral(x2, y2, z2) - a_integral(x2, y2, z1) -
                       a_integral(x2, y1, z2) + a_integral(x2, y1, z1) -
                       a_integral(x1, y2, z2) + a_integral(x1, y2, z1) +
                       a_integral(x1, y1, z2) - a_integral(x1, y1, z1))

    return A



def CallMatrix_mag(mi, md, fi, fd, azim, xm_min, ym_min, xobs, yobs, z0, dx, dy, dz, nx, ny, nz, eps, delta):
    m = nx * ny * nz

    i = np.arange(1, nx+1)
    x11 = xm_min + (i - 1.0) * dx
    x1 = np.tile(x11, ny * nz)
    x2 = x1 + dx

    y11 = np.zeros(nx * ny)
    for i in range(1, ny+1):
        temp = ym_min + (i - 1) * dy
        for j in range(1, nx+1):
            k = (i - 1) * nx + j - 1
            y11[k] = temp

    y1 = np.tile(y11, nz)
    y2 = y1 + dy
    z1 = np.zeros(m)
    for i in range(1, nz+1):
        temp = (i - 1) * dz
        for j in range(1, nx * ny + 1):
            k = (i - 1) * nx * ny + j - 1
            z1[k] = temp

    z2 = z1 + dz
    n = len(xobs)
    G = np.zeros((n, m))
    miu = 500 / (4 * np.pi)
    
    def compute_row(i):
        x0 = xobs[i]
        y0 = yobs[i]
        t1 = mbox(x0, y0, z0, x1, y1, z1, x2, y2, mi, md, fi, fd, miu, azim)
        t2 = mbox(x0, y0, z0, x1, y1, z2, x2, y2, mi, md, fi, fd, miu, azim)
        return t1 - t2

    # Parallel computation of G matrix rows
    results = Parallel(n_jobs=-1)(delayed(compute_row)(i) for i in range(n))

    # Populate G matrix with results and print progress at each 1% completion
    for i in range(n):
        G[i, :] = results[i]
        
        # Print progress every 1% of rows processed
        if (i + 1) % (n // 10) == 0:
            print(f"G matrix {((i + 1) / n) * 100:.0f}% completed")

    small_value = 1e-10
    q = np.zeros(m)
    
    for i in range(1, nz+1):
        wz = z0 + (i - 0.5) * dz
        wz = wz**3 + eps
        for j in range(nx * ny):
            k = (i - 1) * nx * ny + j
            q[k] = wz

    Q = spdiags(q, 0, m, m)

    cov = np.ones(n) * delta
    D = spdiags(cov, 0, n, n)

    return G, Q, D, x1, y1, z1


def CallMatrix_grav(xm_min, ym_min, xobs, yobs, z0, dx, dy, dz, nx, ny, nz, eps, delta):
    """
    Computes the matrices G, Q, and D for a geophysical inversion problem.

    Parameters:
    -----------
    xm_min, ym_min : float
        Minimum x and y coordinates of the model space.
    xobs, yobs : ndarray
        Arrays of observation point coordinates.
    z0 : float
        Reference depth for the depth-weighting matrix.
    dx, dy, dz : float
        Grid cell dimensions in x, y, and z directions (in km).
    nx, ny, nz : int
        Number of grid cells in x, y, and z directions.
    eps : float
        A small constant to prevent division by zero.
    delta : float
        Standard deviation for the data covariance matrix.

    Returns:
    --------
    G : ndarray
        The system matrix for the inversion.
    Q : scipy.sparse.csr_matrix
        The depth-weighting matrix.
    D : scipy.sparse.csr_matrix
        The data covariance matrix.
    x1, y1, z1 : ndarray
        Coordinates of the model cell corners.
    """
    # Number of model cells
    m = nx * ny * nz

    # x1 and x2 are the x-coordinates of one specific model cell.
    i = np.arange(nx)
    x11 = xm_min + i * dx
    x1 = np.tile(x11, ny * nz)
    x2 = x1 + dx

    # y1 and y2 are the y-coordinates of one specific model cell.
    y11 = np.zeros(nx * ny)
    for i in range(ny):
        temp = ym_min + i * dy
        y11[i * nx:(i + 1) * nx] = temp
    y1 = np.tile(y11, nz)
    y2 = y1 + dy

    # z1 and z2 are the z-coordinates of one specific model cell.
    z1 = np.zeros(m)
    for i in range(nz):
        temp = i * dz
        z1[i * nx * ny:(i + 1) * nx * ny] = temp
    z2 = z1 + dz

    # Cell grid coordinates
    cell_grid = np.column_stack([x1 + dx / 2, y1 + dy / 2, z1 + dz / 2, dz / 2 * np.ones(m)])

    # Calculation of the A matrix (G)
    G = matrix_a_3d(cell_grid, np.column_stack([xobs, yobs]), dx, dy)

    # Compute the depth-weighting matrix (Q)
    wz = np.zeros(nz * nx * ny)
    for i in range(nz):
        depth = z0 + (i + 0.5) * dz
        wz[i * nx * ny:(i + 1) * nx * ny] = depth ** 3
    wz = wz + eps
    q = wz
    Q = diags(q, 0, (m, m), format='csr')

    # Compute the data covariance matrix (D)
    n = len(xobs)
    cov = np.full(n, delta)
    D = diags(cov, 0, (n, n), format='csr')

    return G, Q, D, x1, y1, z1