# Mandelbrot Zoom

Small project to visualise and zoom into the mandelbrot set.

---


![seahorse](https://github.com/benw000/MandelbrotZoom/blob/main/demo_vids/seahorse.gif)

Run this: \
 ```python mandelbrot_render.py --focus_real -0.75 --focus_imag 0.1 --mp4_name seahorse ```

---

### Mandlebrot set definition:

The subset of complex numbers $c$ in the complex plane, such that the function:
$$
f_{c}(z) = z^2 + c
$$
does not diverge to infinity, when $f$ is iterated, from initial condition $z$.

ie, the sequence $ (f_c(0), \ f_c(f_c(0)), \ f_c^3(0), \ ... )$ remains bounded in absolute value.


Find out more about this incredible set: 
https://en.wikipedia.org/wiki/Mandelbrot_set 

---

#### Method:
We check for diverging by recursively calling the function $N$ times for each point $c$, and if the final value has a complex magnitude larger than $r=2$ we claim it diverges. \
This final magnitude is passed through an exponential decay function then a colour map to get a plotting colour. For magnitudes less than $2$, we assume it doesn't diverge, and colour it black. \
Then for each pixel in our frame, we recursively apply the function a search depth $N$ many times, and plot this colour. \
We zoom in on a specific complex point that the user can define, by changing the frame window's focus point towards the specified point, then zooming in by dividing the width scale. (This is done with basic affine transformations, detailed inside the **step_pixel_to_complex_coords()** function).

#### Disclaimers:
- This code is not quick! I'm sure there are efficiencies to be made, but I mainly wanted to see basic results. For a 400x400 resolution video with 20 frames, search depth of 20, it may take around 20 seconds to compute and render. For better search depths like 50, this goes up to about a minute.
- This code hasn't been rigorously tested either.
- There are alternative, maybe smarter ways of computing the assigned colour, such as the one in the Wiki page, but I tried to do this without referencing anything.
- The smaller the scale gets, the less detailed it gets, as my current method requires more search depth. I'm not sure if this is a fundamental problem, or a problem in my code.
- If you are reading this and know some more about better methods, please reach out to me via [LinkedIn](www.linkedin.com/in/ben-winstanley-ml-engineer)! I'm very much a beginner when it comes to this field, and I'd love to know more :))


---

### Files:

- mandelbrot_render.py: \
    Main python script containing code needed to produce render. Zooms in on a specific complex number focus point. \
    Type ``` python mandelbrot_render.py -h ``` for help on input arguments.
- mandlebrot.ipynb: \
    The jupyter notebook I developed this script in. Generalised by the main .py script. (I'm aware the file name is spelt wrong, but I couldn't change this without losing git history).
- .gitignore: \
    git file to tell git to ignore renders folder, the default location for saved mp4s.
- renders:
    folder containing selected renders.
    
---