from manim import *
import numpy as np

def get_complex_graph(axes, func, delta_x=0.01):
    # f: real -> complex

    x_min, x_max = axes.x_range[:2]
    xs = np.arange(x_min, x_max, delta_x)
    zs = func(xs)
    points = np.array([
        (x, z.real, z.imag)
        for x, z in zip(xs, zs)
    ])

    curve = VMobject()
    curve.set_points_smoothly([axes.c2p(x, y, z) for x,y,z in points])
    
    return curve

def get_complex_vector(axes, z, x, color=YELLOW):
    z_vect = Vector()

    z_vect.put_start_and_end_on(
        axes.c2p(x, 0, 0),
        axes.c2p(x, z.real, z.imag)
    )
    z_vect.rotate(90 * DEGREES, axis=z_vect.get_vector())
    z_vect.set_color(color)

    return z_vect

class SchrodingerPlay(ThreeDScene):
    def construct(self):
        # Axes
        z_max = 3
        axes = ThreeDAxes(
            x_range=(0,20),
            z_range=(-z_max,z_max),
            y_range=(-z_max,z_max),
            x_length=10,
            y_length=6,
            z_length=6,
            tips=False
        )
        self.add(axes)
        self.set_camera_orientation(
            phi=74 * DEGREES, # + Down - Up
            theta=-17 * DEGREES, # + Right - Left
            gamma=0 * DEGREES,
            frame_center=(-1.4, -0.21, 0.58),
            focal_distance=6.58
        )
        self.set_camera_orientation(zoom=1)

        # Add complex planes
        planes = VGroup()
        for x in range(1,10):
            sheet = ComplexPlane(
                x_range=[-z_max, z_max, 0.25], 
                y_range=[-z_max, z_max, 0.25],
                background_line_style=dict(stroke_color=BLUE, stroke_width=1, stroke_opacity=1),
                faded_line_style=dict(stroke_color=BLUE, stroke_width=1, stroke_opacity=0.4),
                y_length=6,
                x_length=6
            )

            margin = SurroundingRectangle(sheet, buff=0, color=BLUE, stroke_width=3)
            plane = VGroup(sheet, margin)
            plane.rotate(90 * DEGREES, RIGHT)
            plane.rotate(90 * DEGREES, OUT)
            planes.add(plane)
            plane.move_to(axes.c2p(x, 0, 0))

        plane_index = 6
        plane = planes[plane_index][0]
        plane_and_margin = planes[plane_index]
        self.add(plane_and_margin)

        # Show graph of one solution
        A = 1
        k = 0.5
        w = 1

        t_tracker = ValueTracker(0)
        get_t = t_tracker.get_value

        def plane_wave(x):
            t = get_t()
            return A * np.exp(1j * (k * x - w * t))

        graph = always_redraw(lambda: get_complex_graph(axes, plane_wave))
        self.add(graph)

        self.play(t_tracker.animate.set_value(3), run_time=3, rate_func=linear)

        # Add solution arrow on one plane
        x = axes.x_axis.p2n(plane.get_center())
        z_vect = get_complex_vector(axes, plane_wave(x), x)
        z_dot = Dot3D(color=YELLOW)
        z_dot.move_to(z_vect.get_end())

        self.add(z_vect)
        self.add(z_dot)

        # Add Laplacian and difference vector
        def laplacian(x):
            return -1 * (k**2) * plane_wave(x)
        
        def ddt_psi(x):
            return -1j * laplacian(x)
        
        l_vect = get_complex_vector(axes, laplacian(x), x, color=BLUE) #l_vector for laplacian_vector
        dt_vect = get_complex_vector(axes, ddt_psi(x), x, color=TEAL)

        self.move_camera(
            phi=90 * DEGREES,
            theta=-17 * DEGREES,
            frame_center=(-1.4, -0.21, 0.58),
            zoom=1.8,
            run_time=3
        )
        self.play(GrowArrow(l_vect))
        self.wait()
        self.play(TransformFromCopy(l_vect, dt_vect))
        self.wait()
        self.play(dt_vect.animate.shift(z_vect.get_vector()))
        self.wait()

        self.add(dt_vect)