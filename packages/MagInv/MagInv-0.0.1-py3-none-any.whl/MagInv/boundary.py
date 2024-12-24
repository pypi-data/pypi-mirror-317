import numpy as np
from scipy.spatial import ConvexHull
from scipy.interpolate import griddata
from matplotlib.path import Path
import matplotlib.pyplot as plt

def make_boundary(xobs, yobs, d_obs, X, Y):
    """
    Processes the convex hull for a set of points, interpolates data on a grid, and determines points inside the polygon.

    Parameters:
    -----------
    xobs : ndarray
        1D array of x-coordinates of the observed data points.
    
    yobs : ndarray
        1D array of y-coordinates of the observed data points.
    
    d_obs : ndarray
        1D array of observed values at the corresponding (xobs, yobs) points.
    
    X : ndarray
        2D array representing the x-coordinates of the grid.
    
    Y : ndarray
        2D array representing the y-coordinates of the grid.

    Returns:
    --------
    kkkk : ndarray
        Array of indices that define the convex hull, with the first index repeated at the end for closed polygon plotting.
    
    Vq : ndarray
        2D array of interpolated values at the grid points (X, Y).
    
    in_polygon : ndarray
        2D boolean array indicating whether the grid points (X, Y) lie inside the convex hull polygon.
    """
    # Compute convex hull
    hull = ConvexHull(np.column_stack([xobs, yobs]))
    kkkk = hull.vertices
    kkkk = np.append(kkkk, kkkk[0])  # Close the hull by appending the first vertex at the end

    # Plot convex hull for visualization (optional)
    plt.plot(xobs[kkkk], yobs[kkkk], 'black')

    # Interpolate the observed data onto the grid using linear interpolation
    Vq = griddata((xobs, yobs), d_obs, (X, Y), method='linear')

    # Create a polygon path using the convex hull vertices
    polygon = Path(np.column_stack([xobs[kkkk], yobs[kkkk]]))
    
    # Flatten X and Y and stack them as points
    points = np.column_stack([X.ravel(), Y.ravel()])
    
    # Check which points are inside the convex hull polygon
    in_polygon = polygon.contains_points(points)
    in_polygon = in_polygon.reshape(X.shape)  # Reshape the result to match the shape of the grid

    return kkkk, Vq, in_polygon
