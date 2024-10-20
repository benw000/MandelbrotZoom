import argparse
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def mandlebrot_f(c: complex, z: complex) -> complex:
    '''
    Mandlebrot generator function f_c(z)=z^2 + c
    '''
    return z*z + c

def recursion(c: complex, N: int, recursion_func = mandlebrot_f) -> complex:
    '''
    Packaging function to recursively call recursion_func N times.
    recursion_func must accept z and c as arguments.
    Returns the final z value
    '''
    if N <= 0:
        raise ValueError("Please supply a number of iterations over 0.")
    
    z: complex = 0+0j
    # Call recursion func N times on z=0+0i input
    for iter_num in range(N):
        z = recursion_func(c=c,z=z)
    return z

def get_colour(c: complex, N: int = 10, recursion_func = mandlebrot_f) -> float:
    '''
    Function taking point c in complex plane, and calling it's recursive function f_c N times.
    Determines colour based on absolute value of final point.
    '''
    # Check c isn't outside r=2 disc - we know these diverge
    abs_c = abs(c)
    if abs_c >= 2:
        return 0

    # Call recursive function N times
    final_z = recursion(c,N,recursion_func)

    # Find its absolute value
    try:
        abs_z = abs(final_z)
    except:
        return 0
    if np.isnan(abs_z):
        return 0
    
    # Return piecewise colour function of absolute value
    cut_off = 2
    if abs_z <= cut_off:
        return 1
    else:
        scale = 0.01
        return np.exp(-scale*(abs_z-cut_off))

def step_pixel_to_complex_coords(u: int,v: int, res_x:int=500, res_y:int=500,
                                  focus: complex = 0+0j,
                                  step: int = 0) -> complex:
    '''
    Function to convert pixel coordinates in a certain resolution pixel frame into complex coords.
    res_x and res_y must be even
    '''
    # Calculate width w of a pixel in complex coord frame
    # Our image should at minimum view [2,2]^2 
    w = 2 * (2/(min(res_x,res_y))) * 2/(2*(step+1))
    
    # Calculate top left x and y complex points
    top_left_x, top_left_y = focus.real + -w*(res_x/2)+w/2 , focus.imag + w*(res_y/2)-w/2

    # Calculate complex points
    x,y = top_left_x + u*w, top_left_y - v*w

    return complex(x,y)

def step_get_image_vals(step: int = 0, res_x:int=500, res_y:int=500, focus: complex = 0+0j,
                        N: int = 10, recursion_func = mandlebrot_f) -> np.ndarray:
    '''
    Gets a matrix of res_x by res_y values for a particular step, and queries the colour for each with get_colour.
    '''
    image_matrix = np.zeros([res_x, res_y])

    for u in range(res_x):
        for v in range(res_y):
            c = step_pixel_to_complex_coords(u=u, v=v, res_x=res_x, res_y=res_y, 
                                             focus=focus,step=step)
            image_matrix[u,v] = get_colour(c=c, N=N, recursion_func=recursion_func)

    return image_matrix

def zoom_in_step(step: int, ax, focus: complex,
            res_x: int, res_y: int, num_frames: int, recentering_steps: int = 5, N: int = 10):
    ''' 
    Zoom in function, renders the Nth step
    Phase 1: Recentering
        Move from origin to supplied focus point in recentering_steps many steps, while zooming in
    Phase 2: Normal zooming
        Just zoom in for the remaining steps
    '''
    if res_x % 2 == 1 or res_y % 2 ==1 or res_x <= 2 or res_y <= 2:
        raise ValueError("Please input positive, even resolutions for x and y.")
    if step < 0:
        raise ValueError("Can't have negative step")
    
    print(f"Step {round(step+1)}/{num_frames}", end='\r', flush=True)

    if step <= recentering_steps: # Phase 1
        current_focus = focus * step/recentering_steps
        image_matrix = step_get_image_vals(res_x=res_x, res_y=res_y, N=N,
                                            focus=current_focus, step=step)
    else: # Phase 2
        image_matrix = step_get_image_vals(res_x=res_x, res_y=res_y, N=N,
                                            focus=focus, step=step)
    
    ax = ax[0]
    ax.clear()
    ax.set_axis_off()
    cmap = plt.cm.afmhot_r
    ax.matshow(image_matrix.transpose(), vmin=0, vmax=1, cmap=cmap)
    
def render_zoom_in(focus: complex,
                    res_x: int = 400, res_y: int = 400, N: int = 50,
                    num_frames: int = 20, interval_between_frames: int = 200,
                    centering_frames: int = 5,
                    save_as_mp4: bool = True, user_mp4_path: str = None):
    ''' 
    Render mandelbrot zoom.

    focus - complex number that we zoom in on
    res_x, res_y - even integers for x and y resolution, default 400,400
    num_frames - number of frames, each frame zooms in
    interval_between_frames - interval in milliseconds between frames
    centering_frames - number of initial frames used to center on our focus
    save_as_mp4 - bool, whether to save as mp4
    user_mp4_path - path to save the mp4
    '''

    print(f"Runtime approximately {round(num_frames*(res_x*res_y)/80000)} seconds")
    print("-")

    fig, ax = plt.subplots(figsize=[15,15])
    _ = ax.scatter([], [])

    ani = FuncAnimation(fig, zoom_in_step, frames=num_frames, \
                            fargs=([ax],focus,res_x,res_y,num_frames, centering_frames, N,),
                              interval=interval_between_frames)

    save_as_mp4 = True
    if save_as_mp4:
        mp4_path = f"renders/Mandlebrot_{res_x}_by_{res_y}_with_{num_frames}_steps.mp4"
        if user_mp4_path:
            mp4_path = "renders/" + user_mp4_path
            if not mp4_path.lower().endswith('.mp4'):
                mp4_path += '.mp4'
        fps = 1/(interval_between_frames*(10**(-3))) # period -> frequency
        ani.save(mp4_path, writer='ffmpeg', fps=fps)
        print("\n")
        print(f"Saved simulation as mp4 at {mp4_path}.")
    
def main(args):
    # Unpack user arguments
    focus_x = args.focus_real
    focus_y = args.focus_imag
    focus = complex(focus_x, focus_y)
    res_x = args.res_x
    res_y = args.res_y
    num_frames = args.num_frames
    N = args.search_depth
    save_as_mp4 = args.save_mp4
    user_mp4_path = args.mp4_name

    # Call main command with user
    render_zoom_in(focus=focus, res_x=res_x, res_y=res_y,
                   N=N, num_frames=num_frames,
                    save_as_mp4=save_as_mp4, user_mp4_path=user_mp4_path)

if __name__ == "__main__":
    # Create the argument parser
    parser = argparse.ArgumentParser(description="Mandelbrot zoom options.")
    
    # Add arguments
    parser.add_argument('--focus_real', type=float, help='Real part of the focus point.')
    parser.add_argument('--focus_imag', type=float, help='Imaginary part of the focus point.')
    parser.add_argument('--res_x', type=int, help='Horizontal x resolution, default 400.', default=400)
    parser.add_argument('--res_y', type=int, help='Vertical y resolution, default 400.', default=400)
    parser.add_argument('--num_frames', type=int, help='Number of frames, default 20.', default=20)
    parser.add_argument('--search_depth', type=int, help='Search depth for each colour calculation. Default 20, up to 50 for better quality.', default=20)
    parser.add_argument('--save_mp4', type=bool, help='Whether to save as mp4 into renders folder. Default True.', default=True)
    parser.add_argument('--mp4_name', type=str, help='Optional mp4 file name. (automatically put into renders folder) - NOTE THIS OVERWRITES OTHERS. default None.', default=None)

    # Parse the arguments
    args = parser.parse_args()
    
    # Call the main function with parsed arguments
    main(args)