import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import plotly.graph_objects as go
import plotly.io as pio  # Use plotly.io for show()
import ipywidgets as widgets
from ipywidgets import interact
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

# pyo.init_notebook_mode(connected=False)  # Initialize Plotly offline mode

def pseudo(xd, psd, ro, loglind):
    """
    Generates a filled contour plot based on input data and interpolates the values on a grid.
    
    Parameters:
    -----------
    xd : ndarray
        1D or 2D array representing the x-coordinates of the data points.
    
    psd : ndarray
        1D or 2D array representing the y-coordinates (pseudo-depth) of the data points.
    
    ro : ndarray
        1D or 2D array representing the z-values (e.g., resistivity or other data) at the corresponding (xd, psd) points.
    
    loglind : bool
        A flag indicating whether to apply a logarithmic transformation to the z-values:
        - If True, applies `log10` to the interpolated z-values.
        - If False, no transformation is applied.

    Returns:
    --------
    None. This function directly plots the filled contour plot using `matplotlib`.

    Notes:
    ------
    - The function uses linear interpolation to generate a smooth grid of z-values for the contour plot.
    - If `loglind` is True, values are transformed to `log10` scale before plotting.
    """
    # Create grid for interpolation
    unique_xd = np.unique(xd)
    unique_psd = np.unique(psd)
    xc, yc = np.meshgrid(unique_xd, unique_psd)
    # Assuming xd and psd are pandas Series, convert them to NumPy arrays
    xd = xd.flatten()  # Convert to NumPy array and then flatten
    psd = psd.flatten()  # Convert to NumPy array and then flatten

    # Now apply griddata
    zT = griddata((xd, psd), ro, (xc, yc), method='linear')



    # Apply logarithmic scale if needed
    if loglind:
        zT = np.log10(zT)

    # Plot filled contour
    plt.contourf(unique_xd, unique_psd, zT, levels=50, linestyles='none')
    
    


def plot_3d_scatter_at_depth(X, Y, Z, VV, depth_index, depth_approx=0.5):
    """
    Creates a 3D scatter plot of data at a specific depth index.

    Parameters:
    -----------
    X : ndarray
        3D array representing the x-coordinates.
    
    Y : ndarray
        3D array representing the y-coordinates.
    
    Z : ndarray
        3D array representing the z-coordinates.
    
    VV : ndarray
        3D array of values to be visualized.
    
    depth_index : int
        Index of the depth slice to visualize (0-based).
    
    depth_approx : float, optional
        Tolerance for depth matching. Default is 0.5.

    Returns:
    --------
    None. This function directly shows the 3D scatter plot using Plotly.
    """
    # Flatten the arrays
    x_flat = X.ravel()
    y_flat = Y.ravel()
    z_flat = Z.ravel()
    vv_flat = VV.ravel()

    # Create a mask for the specific depth
    depth_mean = Z[:, :, depth_index].mean()
    depth_mask = np.isclose(z_flat, depth_mean, atol=depth_approx)
    mask = depth_mask & ~np.isnan(vv_flat)

    # Create the 3D scatter plot
    fig = go.Figure(data=[go.Scatter3d(
        x=x_flat[mask],
        y=y_flat[mask],
        z=z_flat[mask],
        mode='markers',
        marker=dict(
            size=5,
            color=vv_flat[mask],  # Color by VV value
            colorscale='Jet',
            colorbar=dict(title='VV value')
        )
    )])

    # Update layout with larger figure size
    fig.update_layout(
        title=f'Data at Depth = {depth_mean:.2f}',
        scene=dict(
            xaxis_title='X position (m)',
            yaxis_title='Y position (m)',
            zaxis_title='Z position (m)'
        ),
        width=1000,  # Increase the width
        height=500   # Increase the height
    )

    # Show the plot
    fig.show()





# def plot_multiple_contours(X, Y, Z, VV, depth_indices=None, colorscale='Jet', climit=None):
#     """
#     Plot multiple 2D contour plots and surfaces at different depths using the provided X, Y, Z, and VV data.

#     Parameters:
#     - X: 3D numpy array of X coordinates.
#     - Y: 3D numpy array of Y coordinates.
#     - Z: 3D numpy array of Z coordinates (depths).
#     - VV: 3D numpy array of VV values.
#     - depth_indices: List or array of indices representing the depths to plot.
#     - colorscale: The colorscale for both contour and surface plots.
#     - climit: Tuple (vmin, vmax) to set color scale limits. If None, it will use the min and max of the data.
    
#     Returns:
#     - A Plotly figure object.
#     """
#     # Create a figure
#     fig = go.Figure()

#     # Set color scale limits based on the climit parameter or the entire VV data
#     if climit:
#         vmin, vmax = climit
#     else:
#         vmin, vmax = VV.min(), VV.max()

#     # Loop over depth indices to plot contours and surfaces at different Z-levels
#     for depth_index in depth_indices:
#         # Extract the Z plane (depth) and the corresponding VV values
#         z_value = Z[:, :, depth_index].mean()  # The Z value for this contour level
#         vv_at_depth = VV[:, :, depth_index]  # The VV values at this depth

#         # Create a contour plot at the specified depth
#         fig.add_trace(
#             go.Contour(
#                 x=X[:, :, depth_index].flatten(),  # X-axis (flattened for contour plot)
#                 y=Y[:, :, depth_index].flatten(),  # Y-axis (flattened for contour plot)
#                 z=vv_at_depth,  # VV values for the contour
#                 colorscale=colorscale,
#                 colorbar=dict(
#                     title='VV Value',
#                 ),
#                 line_width=2,
#                 showscale=False,  # Hide color scale for each contour plot
#                 name=f'Depth = {z_value:.2f}',  # Label the contour with its depth
#                 zhoverformat=".2f",
#                 hoverinfo='x+y+z'
#             )
#         )

#         # Add the surface plot for each depth
#         fig.add_trace(
#             go.Surface(
#                 x=X[:, :, depth_index],  # X coordinates
#                 y=Y[:, :, depth_index],  # Y coordinates
#                 z=np.full_like(X[:, :, depth_index], z_value),  # Set all Z coordinates to the depth
#                 surfacecolor=vv_at_depth,  # Color the surface using VV data
#                 colorscale=colorscale,
#                 colorbar=dict(
#                     title="Magnetic Susceptibility",
#                     titleside="right",  # Position the title to the right of the colorba
#                 ),
#                 showscale=True,  # Ensure the colorbar is visible
#                 opacity=1,  # Set opacity so contours are visible
#             )
#         )


#     # Update layout for better visualization
#     fig.update_layout(
#         title='Multiple 2D Contour Plots at Different Depths',
#         scene=dict(
#             yaxis_title='Easting (m)',
#             xaxis_title='Northing (m)',
#             zaxis_title='Depth (m)',
#             zaxis=dict(autorange='reversed'),  # Reverse Z-axis if needed
#             camera=dict(eye=dict(x=1.5, y=1.5, z=1.5))  # Set the camera for 3D view
#         ),
#         width=1000,
#         height=700
#     )


#     # Show the plot
#     return fig
def plot_multiple_contours(X, Y, Z, VV, depth_indices=None, colorscale='Jet', climit=None):
    """
    Plot multiple 2D contour plots and surfaces at different depths using the provided X, Y, Z, and VV data.

    Parameters:
    - X: 3D numpy array of X coordinates.
    - Y: 3D numpy array of Y coordinates.
    - Z: 3D numpy array of Z coordinates (depths).
    - VV: 3D numpy array of VV values.
    - depth_indices: List or array of indices representing the depths to plot.
    - colorscale: The colorscale for both contour and surface plots.
    - climit: Tuple (vmin, vmax) to set color scale limits. If None, it will use the min and max of the data.
    
    Returns:
    - A Plotly figure object.
    """
    # Create a figure
    fig = go.Figure()

    # Set color scale limits based on the climit parameter or the entire VV data
    if climit:
        vmin, vmax = climit
    else:
        vmin, vmax = VV.min(), VV.max()

    # Loop over depth indices to plot contours and surfaces at different Z-levels
    for depth_index in depth_indices:
        # Extract the Z plane (depth) and the corresponding VV values
        z_value = Z[:, :, depth_index].mean()  # The Z value for this contour level
        vv_at_depth = VV[:, :, depth_index]  # The VV values at this depth

        # Create a contour plot at the specified depth
        fig.add_trace(
            go.Contour(
                x=X[:, :, depth_index].flatten(),  # X-axis (flattened for contour plot)
                y=Y[:, :, depth_index].flatten(),  # Y-axis (flattened for contour plot)
                z=vv_at_depth,  # VV values for the contour
                colorscale=colorscale,
                colorbar=dict(
                    title='VV Value',
                    tickvals=[vmin, vmax],  # Optionally specify tick values for color bar
                    ticktext=[f'{vmin:.2f}', f'{vmax:.2f}'],
                    titleside="right"  # Position the title to the right of the colorbar
                ),
                line_width=2,
                showscale=False,  # Hide color scale for each contour plot
                name=f'Depth = {z_value:.2f}',  # Label the contour with its depth
                zhoverformat=".2f",
                hoverinfo='x+y+z'
            )
        )

        # Add the surface plot for each depth
        fig.add_trace(
            go.Surface(
                x=X[:, :, depth_index],  # X coordinates
                y=Y[:, :, depth_index],  # Y coordinates
                z=np.full_like(X[:, :, depth_index], z_value),  # Set all Z coordinates to the depth
                surfacecolor=vv_at_depth,  # Color the surface using VV data
                colorscale=colorscale,
                colorbar=dict(
                    title="Magnetic Susceptibility",
                    titleside="right",  # Position the title to the right of the colorbar
                    tickvals=[vmin, vmax],  # Optionally specify tick values for color bar
                    ticktext=[f'{vmin:.2f}', f'{vmax:.2f}'],
                ),
                showscale=False,  # Hide color scale for each surface plot
                opacity=1,  # Set opacity so contours are visible
            )
        )

    # Update layout for better visualization
    fig.update_layout(
        title='Multiple 2D Contour Plots at Different Depths',
        scene=dict(
            yaxis_title='Easting (m)',
            xaxis_title='Northing (m)',
            zaxis_title='Depth (m)',
            zaxis=dict(autorange='reversed'),  # Reverse Z-axis if needed
            yaxis=dict(autorange='reversed'),  # Reverse Y-axis to invert it
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.5))  # Set the camera for 3D view
        ),
        width=1000,
        height=700
    )

    # Show the plot
    return fig




def plot_multiple_contours_mpl(X, Y, Z, VV, depth_indices=None, colorscale='jet', climit=None):
    """
    Plot multiple 2D contour plots and surfaces at different depths using Matplotlib.

    Parameters:
    - X: 3D numpy array of X coordinates.
    - Y: 3D numpy array of Y coordinates.
    - Z: 3D numpy array of Z coordinates (depths).
    - VV: 3D numpy array of VV values.
    - depth_indices: List or array of indices representing the depths to plot.
    - colorscale: The colorscale for both contour and surface plots.
    - climit: Tuple (vmin, vmax) to set color scale limits. If None, it will use the min and max of the data.
    
    Returns:
    - A static Matplotlib figure object with all depth plots.
    """
    # Set color scale limits based on the climit parameter or the entire VV data
    if climit:
        vmin, vmax = climit
    else:
        vmin, vmax = VV.min(), VV.max()
    
    # Create the figure and axis
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Loop over depth indices to plot contours and surfaces
    for depth_index in depth_indices:
        # Extract the Z plane (depth) and the corresponding VV values
        z_value = Z[:, :, depth_index].mean()
        vv_at_depth = VV[:, :, depth_index]

        # Plot surface for the depth
        ax.plot_surface(X[:, :, depth_index], Y[:, :, depth_index], np.full_like(X[:, :, depth_index], z_value),
                        facecolors=cm.get_cmap(colorscale)((vv_at_depth - vmin) / (vmax - vmin)), 
                        rstride=1, cstride=1, alpha=0.8)

        # Add contour plot for the depth
        ax.contour(X[:, :, depth_index], Y[:, :, depth_index], vv_at_depth, cmap=colorscale, offset=z_value)

    # Customize the colorbar
    m = cm.ScalarMappable(cmap=colorscale)
    m.set_array(VV)
    m.set_clim(vmin, vmax)
    fig.colorbar(m, ax=ax, label='VV Value')

    # Set axis labels and title
    ax.set_xlabel('X position (m)')
    ax.set_ylabel('Y position (m)')
    ax.set_zlabel('Z position (m)')
    ax.set_title('Multiple Contours and Surfaces at Different Depths')

    plt.show()

# Example usage:
# Assuming X, Y, Z, and VV are pre-defined 3D arrays and depth_indices is a list of indices
# depth_indices = np.arange(0, Z.shape[2], 1)  # Example depth indices

# Call the function
# plot_multiple_contours_mpl(X, Y, Z, VV, depth_indices=depth_indices)





def interactive_contour_plot(X, Y, VV, Z_vals, z_idx_default=5, vmin=None, vmax=None):
    """
    Displays an interactive 2D contour plot for a selected depth index with a slider.

    Parameters:
    -----------
    X, Y : ndarray
        3D arrays representing the X and Y coordinates of the grid at different depths.
    VV : ndarray
        3D array representing the VV values at corresponding X, Y, Z coordinates.
    Z_vals : ndarray
        1D array representing the depth values (Z-axis) corresponding to the Z index.
    z_idx_default : int, optional
        Default index for the Z-axis slider (default is 5).
    vmin : float, optional
        Minimum value for color scale (default is -0.0025).
    vmax : float, optional
        Maximum value for color scale (default is 0.0125).
    """
    
    def plot_contour(z_idx):
        plt.figure()
        contour = plt.contourf(X[:, :, z_idx], Y[:, :, z_idx], VV[:, :, z_idx], cmap='jet', vmin=vmin, vmax=vmax)
        plt.title(f'Contour at Z = {Z_vals[z_idx]:.2f}')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.colorbar(label='VV')
        plt.show()

    # Create the interactive slider for Z index
    z_slider = widgets.IntSlider(value=z_idx_default, min=0, max=X.shape[2]-1, step=1, description='z_idx')

    # Use ipywidgets interact to create interactive contour plot
    interact(plot_contour, z_idx=z_slider)

