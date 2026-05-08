from manim import *
import numpy as np

# CODE DIVIDED IN TWO PARTS
# First part: this first part was done when I knew nothing about fractals (in fact, I didn't even know what even was the Mandelbrot's Set I was trying to represent)
# Orbit for a particular c (c=-0.74364388 + 0.1318259j, z0=0+0j))

# z_n = z_n-1^2 + c
def mandelbrot_set_1(iterations, c=-0.74364388 + 0.1318259j, z0=0+0j):
    z = [z0]
    for n in range(iterations):
        z.append(z[n]**2+c)
    return z

# Mandelbrot set (Seahorse Valley for c arround -0.75+0.1j)
class MandelbrotSet_1(Scene):

    def construct(self):

        axes = Axes(
            x_range=[-2, 0.5, 0.5], 
            y_range=[-1.2, 1.2, 0.5], 
            x_length=7,
            y_length=7
        )

        points = mandelbrot_set_1(1000)
        colors = color_gradient([YELLOW, RED], len(points))

        # Different options to show the Mandelbrot set
        set = []
        rectangles = VGroup()
        
        for point, color in zip(points, colors):
            rectangle = Rectangle(width=.2, height=.2,fill_color=LIGHT_BROWN, fill_opacity=1, color=LIGHT_BROWN)
            position = axes.c2p(np.real(point), np.imag(point))

            set.append([np.real(point)*7, np.imag(point)*7, 0])

            rectangle.move_to(position)
            rectangles.add(rectangle)

        curve = VMobject(color=BLUE).set_points_as_corners([axes.c2p(x, y, z) for x, y, z in set])
        curve.set_stroke(width=2)

        self.add(rectangles)
        self.add(axes)



# Second part: now I have a solid (although very basic) idea on what fractals, specially Mandelbrot like, are, as well as what does the Mandelbrot really means
# Mandelbrot Set (scapetime fractal)


def iterations_orbit_for_c(c, iterations):

    z = [0+0j]
    i = 0
    for n in range(iterations):
        # Mandelbrot complex iterated function
        z_n = z[n]**2 + c
        z.append(z_n)
        if np.abs(z_n) >= 2:
            break
        else:
            i += 1
    
    return i

def mandelbrot_set(from_left_c, to_right_c, box_size, iterations):

    # All the data in the form of [c, i]
    data = []

    # Define each point in the complex plane
    for real_dx in range(int((np.real(to_right_c) - np.real(from_left_c))/box_size)):
        c_real = np.real(from_left_c) + box_size*real_dx
        for imag_dy in range(int((np.imag(to_right_c) - np.imag(from_left_c))/box_size)):
            c_imag = np.imag(from_left_c) + box_size*imag_dy
            
            c = c_real + c_imag*1j

            # Calculate the iterations until |z|>2
            i = iterations_orbit_for_c(c, iterations)

            data.append([c, i])

    return data # return a list with [c, i] where c is the point in the complex plane and i is the number of iterations until it scapes (|z|>2)

class MandelbrotSet(MovingCameraScene):

    def construct(self):

        # Parameters
        from_left_c = -0.8 - 0.2j
        to_right_c = -0.7 + 0.2j
        box_size = 0.001
        iterations = 50

        # All the information in the form of [[c1, i1], [c2, i2],..., [cn, in]]
        data = mandelbrot_set(from_left_c, to_right_c, box_size, iterations)

        # Scene
        axes = Axes(
            x_range=[np.real(from_left_c), np.real(to_right_c), box_size],
            y_range=[np.imag(from_left_c), np.imag(to_right_c), box_size], 
            x_length=np.real(to_right_c) - np.real(from_left_c),
            y_length=np.imag(to_right_c) - np.imag(from_left_c)
        )

        colors = color_gradient([YELLOW, GREEN, ORANGE, RED, BLUE, PURPLE, DARK_GRAY, BLACK], iterations)

        set = VGroup()
        for value in data:
            square = Square(side_length=box_size, color=colors[value[1]-1])
            square.move_to(axes.c2p(np.real(value[0]), np.imag(value[0])))

            set.add(square)

        self.add(set)
        if axes.width >= axes.height:
            self.camera.frame.set(width=axes.width)
        else:
            self.camera.frame.set(height=axes.height)